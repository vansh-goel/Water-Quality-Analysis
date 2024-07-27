<script>
  import { analysisStore } from '../../stores.ts';
  import { Bar } from 'svelte-chartjs';
  import { onMount } from 'svelte';

  let pollutionSources = [];
  let correlationMatrix = {};
  let showMore = {};
  let dataLoaded = false;
  let overview = {};

  analysisStore.subscribe(data => {
    if (data) {
      pollutionSources = data.pollution_sources;
      correlationMatrix = data.correlation_matrix;
      overview = data.overview;
      showMore = pollutionSources.reduce((acc, source) => {
        acc[source.parameter] = false;
        return acc;
      }, {});
      dataLoaded = true;
    } else {
      dataLoaded = false;
    }
  });

  function toggleShowMore(parameter) {
    showMore[parameter] = !showMore[parameter];
  }

  function toTitleCase(str) {
    return str.replace(/\w\S*/g, (txt) => txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase());
  }

  let chartData = {
    labels: [],
    datasets: []
  };

  onMount(() => {
    if (dataLoaded) {
      chartData.labels = Object.keys(overview);
      chartData.datasets = [{
        label: 'Average Values',
        data: Object.values(overview).map(o => o.mean),
        backgroundColor: 'rgba(75, 192, 192, 0.2)',
        borderColor: 'rgba(75, 192, 192, 1)',
        borderWidth: 1
      }];
    }
  });
</script>

{#if dataLoaded}
  <h1 class="text-4xl font-extrabold text-center my-8 text-primary">Analysis Results</h1>

  <div class="my-8">
    <Bar {chartData} options={{ responsive: true, maintainAspectRatio: false }} />
  </div>

  <h2 class="text-3xl font-semibold my-4 text-secondary">Potential Pollution Sources</h2>
  {#each pollutionSources as source}
    <div class="card shadow-xl my-6 bg-base-100">
      <div class="card-body">
        <h3 class="card-title text-xl font-bold text-accent">{toTitleCase(source.parameter)}</h3>
        <p class="text-base-content">Source: <span class="font-semibold">{source.source}</span></p>
        <p class="text-base-content">Correlations: {source.correlations.join(', ')}</p>
        <h4 class="text-lg font-semibold mt-4 text-info">Affected Locations:</h4>
        <ul class="list-disc list-inside ml-4 {showMore[source.parameter] ? 'max-h-80' : 'max-h-40'} overflow-y-auto">
          {#each source.locations.slice(0, showMore[source.parameter] ? source.locations.length : 15) as location}
            <li class="text-base-content">{location['Name of Monitoring Location']} ({location['State Name']}, {location['Type Water Body']}): {location[source.parameter].toFixed(2)}</li>
          {/each}
        </ul>
        {#if source.locations.length > 15}
          <button class="btn btn-link text-info mt-2" on:click={() => toggleShowMore(source.parameter)}>
            {showMore[source.parameter] ? 'Show Less' : 'Show More'}
          </button>
        {/if}
      </div>
    </div>
  {/each}
{:else}
  <div class="flex items-center justify-center h-screen">
    <div class="text-center">
      <h1 class="text-4xl font-extrabold text-primary">Upload a CSV file to perform analysis</h1>
    </div>
  </div>
{/if}