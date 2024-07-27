
<script>
  import { page } from '$app/stores';
  import "../app.css";
 import "tailwindcss/tailwind.css";
</script>

<nav class="navbar bg-[#7D8ABC] rounded-lg shadow-lg p-4 w-full">
  <div class="container text-white w-full px-8 flex justify-between items-center">
    <a href="/" class="text-xl font-semibold">Water Quality Analysis</a>
    <ul class="grid grid-flow-col gap-4 font-medium px-1">
      <li><a href="/" class:active={$page.url.pathname === "/"}>Home</a></li>
      <li><a href="/analysis" class:active={$page.url.pathname === "/analysis"}>Analysis</a></li>
      <li><a href="/visualize" class:active={$page.url.pathname === "/visualize"}>Visualize</a></li>
    </ul>
  </div>
</nav>

<main class="container bg-[#77E4C8] min-h-[80vh] mx-auto my-8 p-4 bg-base-200 rounded-lg shadow-md dark:text-white">
  <slot />
</main>

