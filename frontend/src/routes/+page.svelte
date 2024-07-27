<script>
  import { goto } from '$app/navigation';
  import { analysisStore } from '../stores';

  let file = null;

  async function handleSubmit() {
    if (!file) {
      alert("Please select a file");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await fetch("http://localhost:5000/analyze", {
        method: "POST",
        body: formData,
      });

      if (response.ok) {
        const data = await response.json();
        analysisStore.set(data);
        goto("/analysis");
      } else {
        alert("Error analyzing file: " + response.statusText);
      }
    } catch (error) {
      console.error("Error:", error);
      alert("Error analyzing file");
    }
  }
</script>

<div class="w-full py-8 h-full flex-col gap-4 items-between">
<h1 class="text-6xl pb-4 font-bold">Water Quality Analysis</h1>
<form on:submit|preventDefault={handleSubmit}>
  <input type="file" class="file-input file-input-bordered w-full max-w-xs" accept=".csv" on:change="{e => file = e.target.files[0]}" />
  <button class="btn btn-primary" type="submit">Upload and Analyze</button>
</form>
</div>

<style>
  form {
    display: flex;
    flex-direction: column;
    align-items: center;
    margin-top: 20px;
  }

  input[type="file"] {
    margin-bottom: 10px;
  }

  button {
    padding: 10px 20px;
    font-size: 16px;
  }

  h1 {
    text-align: center;
  }
</style>

