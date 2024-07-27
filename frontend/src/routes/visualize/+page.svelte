<script>
  import { analysisStore } from '../../stores.ts';

  let dataLoaded = false;
  let imageUrls = [];

  // Subscribe to the analysis store and handle data
  analysisStore.subscribe(data => {
    if (data && data.image_url) {
      // Remove 'frontend/static/' from the image_url
      imageUrls = [data.image_url.replace('frontend/static/', '')];
      if (data.boxplot_urls) {
        imageUrls = imageUrls.concat(data.boxplot_urls.map(url => url.replace('frontend/static/', '')));
      }
      if (data.barplot_urls) {
        imageUrls = imageUrls.concat(data.barplot_urls.map(url => url.replace('frontend/static/', '')));
      }
      dataLoaded = true;
    } else {
      dataLoaded = false;
    }
  });
</script>

<style>
  .image-container {
    max-width: 100%;
    overflow: hidden;
    border-radius: 0.5rem;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    margin-bottom: 1rem;
  }
</style>

{#if dataLoaded}
  <div class="container mx-auto px-4 py-8">
    <h1 class="text-4xl font-extrabold text-center my-8 text-primary">Visualization</h1>

    <div class="flex flex-wrap justify-center">
      {#each imageUrls as url}
        <div class="image-container">
          <img src={url} alt="Analysis Visualization" class="w-full h-auto" />
        </div>
      {/each}
    </div>
  </div>
{:else}
  <div class="flex items-center justify-center h-screen bg-gray-100">
    <div class="text-center">
      <h1 class="text-4xl font-extrabold text-primary mb-4">Upload a CSV file to perform analysis</h1>
      <p class="text-lg text-gray-600">Once a file is uploaded, you'll be able to view the analysis results here.</p>
    </div>
  </div>
{/if}