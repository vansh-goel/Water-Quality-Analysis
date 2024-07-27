from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import os
import uuid

app = Flask(__name__)
CORS(app)

parameters = ['Temperature', 'Dissolved Oxygen (mg/L)', 'pH', 'Conductivity (?mhos/cm)',
              'BOD (mg/L)', 'Nitrate N + Nitrite N(mg/L)', 'Fecal Coliform (MPN/100ml)',
              'Total Coliform (MPN/100ml)']

def to_numeric_safe(s):
    return pd.to_numeric(s, errors='coerce')

def analyze_data(file):
    df = pd.read_csv(file, encoding='latin-1')

    for param in parameters:
        min_col = next((col for col in df.columns if col.startswith(param) and 'Min' in col), None)
        max_col = next((col for col in df.columns if col.startswith(param) and 'Max' in col), None)
        if min_col and max_col:
            df[min_col] = to_numeric_safe(df[min_col])
            df[max_col] = to_numeric_safe(df[max_col])

    overview = {}
    for param in parameters:
        min_col = next((col for col in df.columns if col.startswith(param) and 'Min' in col), None)
        max_col = next((col for col in df.columns if col.startswith(param) and 'Max' in col), None)
        avg_col = f"Avg_{param.split()[0]}"

        if min_col and max_col:
            df[avg_col] = (df[min_col] + df[max_col]) / 2
            overview[param] = df[avg_col].describe().to_dict()
        else:
            overview[param] = "Columns not found"

    correlation_columns = [f"Avg_{param.split()[0]}" for param in parameters if f"Avg_{param.split()[0]}" in df.columns]
    correlation_matrix = df[correlation_columns].corr().to_dict()

    def identify_pollution_sources(df, safe_limits, correlation_matrix, threshold=0.7):
        high_correlation_pairs = []
        for i in range(len(correlation_matrix.columns)):
            for j in range(i+1, len(correlation_matrix.columns)):
                if abs(correlation_matrix.iloc[i, j]) > threshold:
                    high_correlation_pairs.append((correlation_matrix.columns[i], correlation_matrix.columns[j]))

        potential_sources = {
            'Avg_Temperature': 'thermal pollution from industrial discharges, removal of riparian vegetation',
            'Avg_pH': 'industrial discharge, agricultural runoff, mining activities, atmospheric deposition',
            'Avg_Dissolved': 'organic matter decomposition, sewage discharge, industrial effluents',
            'Avg_DO': 'organic matter decomposition, sewage discharge, industrial effluents',
            'Avg_Conductivity': 'mining activities, industrial discharges, urban runoff, agricultural runoff',
            'Avg_BOD': 'organic pollutants from sewage, agricultural runoff, industrial discharges, urban runoff',
            'Avg_Nitrate': 'agricultural runoff, industrial waste, sewage discharge, urban runoff, atmospheric deposition',
            'Avg_Nitrite': 'agricultural runoff, industrial waste, sewage discharge, urban runoff, atmospheric deposition',
            'Avg_Ammonia': 'sewage discharge, agricultural runoff, industrial waste',
            'Avg_Phosphate': 'agricultural runoff, sewage discharge, industrial discharges, urban runoff',
            'Avg_Fecal': 'sewage contamination, animal waste, stormwater runoff',
            'Avg_Total': 'sewage contamination, animal waste, stormwater runoff',
            'Avg_Metals': 'industrial discharges, mining activities, urban runoff',
            'Avg_Turbidity': 'soil erosion, urban runoff, industrial discharges, construction activities',
            'Avg_Hardness': 'mining activities, industrial discharges, natural geological formations',
            'Avg_Chloride': 'road salt application, sewage discharge, industrial discharges',
            'Avg_Sulfate': 'industrial discharges, mining activities, atmospheric deposition',
            'Avg_Alkalinity': 'natural geological formations, industrial discharges',
            'Avg_Chemical Oxygen Demand (COD)': 'industrial discharges, sewage discharge, urban runoff'
        }

        pollution_sources = []
        for param, (lower, upper) in safe_limits.items():
            if param in df.columns:
                exceeding = df[(df[param] < lower) | (df[param] > upper)]
                if not exceeding.empty:
                    source = potential_sources.get(param, "Unknown sources")
                    correlated_params = [col1 if col2 == param else col2 for col1, col2 in high_correlation_pairs if col1 == param or col2 == param]
                    pollution_sources.append({
                        "parameter": param,
                        "source": source,
                        "locations": exceeding[['Name of Monitoring Location', 'State Name', 'Type Water Body', param]].to_dict(orient='records'),
                        "correlations": correlated_params
                    })

        return pollution_sources

    safe_limits = {
        'Avg_pH': (6.5, 8.5),
        'Avg_Dissolved': (5, float('inf')),
        'Avg_BOD': (0, 30),
        'Avg_Nitrate': (0, 10),
        'Avg_Fecal': (0, 500),
        'Avg_Total': (0, 5000)
    }

    pollution_sources = identify_pollution_sources(df, safe_limits, df[correlation_columns].corr())

    return overview, correlation_matrix, pollution_sources, df

def save_plot_as_image(df, filename, plot_type, **kwargs):
    plt.figure(figsize=(10, 6))
    if plot_type == 'heatmap':
        sns.heatmap(df.corr(), annot=True, cmap='coolwarm', vmin=-1, vmax=1)
        plt.title('Correlation Matrix')
    elif plot_type == 'boxplot':
        sns.boxplot(x=kwargs['x'], y=kwargs['y'], data=df)
        plt.title(kwargs['title'])
        plt.xticks(rotation=45)
    elif plot_type == 'barplot':
        df.groupby(kwargs['x'])[kwargs['y']].mean().sort_values().plot(kind='bar')
        plt.title(kwargs['title'])
        plt.xticks(rotation=90)
    plt.savefig(filename)
    plt.close()

@app.route('/analyze', methods=['POST'])
def analyze():
    try:
        file = request.files['file']
        overview, correlation_matrix, pollution_sources, df = analyze_data(file)
        
        # Save the correlation matrix plot as an image
        image_filename = f"frontend/static/{uuid.uuid4()}.png"
        save_plot_as_image(pd.DataFrame(correlation_matrix), image_filename, 'heatmap')
        
        # Save boxplot images
        boxplot_filenames = []
        for param in parameters[:4]:  # Limiting to 4 for readability
            avg_col = f"Avg_{param.split()[0]}"
            if avg_col in df.columns:
                boxplot_filename = f"frontend/static/{uuid.uuid4()}.png"
                save_plot_as_image(df, boxplot_filename, 'boxplot', x='Type Water Body', y=avg_col, title=f'{param} by Water Body Type')
                boxplot_filenames.append(boxplot_filename)
        
        # Save barplot images
        barplot_filenames = []
        for param in parameters[:4]:  # Limiting to 4 for readability
            avg_col = f"Avg_{param.split()[0]}"
            if avg_col in df.columns:
                barplot_filename = f"frontend/static/{uuid.uuid4()}.png"
                save_plot_as_image(df, barplot_filename, 'barplot', x='State Name', y=avg_col, title=f'Average {param} by State')
                barplot_filenames.append(barplot_filename)
        
        return jsonify({
            "overview": overview,
            "correlation_matrix": correlation_matrix,
            "pollution_sources": pollution_sources,
            "image_url": f"frontend/static/{os.path.basename(image_filename)}",
            "boxplot_urls": [f"frontend/static/{os.path.basename(filename)}" for filename in boxplot_filenames],
            "barplot_urls": [f"frontend/static/{os.path.basename(filename)}" for filename in barplot_filenames]
        })
    except Exception as e:
        print(f"Error occurred: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    if not os.path.exists('frontend/static'):
        os.makedirs('frontend/static')
    app.run(debug=True)