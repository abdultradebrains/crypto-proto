<!-- File: src/lib/components/FilterControls.svelte -->
<script>
	import { createEventDispatcher } from 'svelte';

	/** @type {string[]} */
	export let availableAssets = [];
	/**
	 * @type {any[]}
	 */
	export let availableExpiries = [];
	export let selectedAsset;
	export let selectedExpiry;

	const dispatch = createEventDispatcher();

	/**
	 * @param {string} asset
	 */
	function selectAsset(asset) {
		dispatch('selectAsset', asset);
	}

	/**
	 * @param {any} expiry
	 */
	function selectExpiry(expiry) {
		dispatch('selectExpiry', expiry);
	}
</script>

<div class="filter-container">
	<div class="asset-filters">
		{#each availableAssets as asset}
			<button class:active={selectedAsset === asset} on:click={() => selectAsset(asset)}>
				{asset}
			</button>
		{/each}
	</div>
	<div class="expiry-filters">
		{#each availableExpiries as expiry}
			<button class:active={selectedExpiry === expiry} on:click={() => selectExpiry(expiry)}>
				{expiry}
			</button>
		{/each}
	</div>
</div>

<style>
	.filter-container {
		display: flex;
		flex-direction: column;
		gap: 0.5rem;
		margin-bottom: 1rem;
	}
	.asset-filters,
	.expiry-filters {
		display: flex;
		gap: 0.5rem;
	}
	button {
		background-color: #2c3e50;
		color: #bdc3c7;
		border: 1px solid #34495e;
		padding: 0.5rem 1rem;
		border-radius: 4px;
		cursor: pointer;
		transition:
			background-color 0.2s,
			color 0.2s;
	}
	button:hover {
		background-color: #34495e;
	}
	button.active {
		background-color: #f39c12;
		color: #1c1c1c;
		border-color: #f39c12;
	}
</style>
