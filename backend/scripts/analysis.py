def identify_pollution_sources(df, safe_limits, correlation_matrix):
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
                pollution_sources.append({
                    'parameter': param,
                    'source': potential_sources.get(param, 'Unknown'),
                    'correlations': [col for col in correlation_matrix.index if abs(correlation_matrix.at[param, col]) > 0.7],
                    'locations': exceeding[['Name of Monitoring Location', 'State Name', 'Type Water Body', param]].to_dict(orient='records')
                })

    return pollution_sources


