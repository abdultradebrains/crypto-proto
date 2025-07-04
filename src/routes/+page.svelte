<!-- File: src/routes/+page.svelte -->
<!-- Description: The main page that orchestrates all components and data flow. -->

<script>
	import { onMount } from 'svelte';
	import { optionsData, connectWebSocket } from '$lib/websocket-store.js';
	import FilterControls from '$lib/components/FilterControls.svelte';
	import OptionsTable from '$lib/components/OptionsTable.svelte';

	onMount(() => {
		// Define the subscription message for the delta.exchange API
		const subscription_msg = {
			type: 'subscribe',
			payload: {
				channels: [
					{
						name: 'v2/ticker',
						symbols: ['call_options', 'put_options']
					}
				]
			}
		};
		// Connect to the live WebSocket endpoint
		connectWebSocket('wss://socket.delta.exchange', subscription_msg);
	});

	// Component State
	let selectedAsset = 'BTC';
	let availableAssets = ['BTC', 'ETH']; // You can expand this as needed
	let selectedExpiry = '04 Jul 25'; // Initial default selection

	// --- Reactive Data Processing ---

	// 1. Get all contracts as an array from the store
	$: allContracts = Object.values($optionsData);

	// 2. Derive available expiry dates from the data
	$: availableExpiries = [
		...new Set(
			allContracts
				.filter((c) => c.underlying_asset_symbol === selectedAsset)
				.map((c) => {
					const [, , , expiryStr] = c.symbol.split('-');
					const day = expiryStr.slice(0, 2);
					// Convert month number to short name
					const month = new Date(`2000-${expiryStr.slice(2, 4)}-01`).toLocaleString('en-US', {
						month: 'short'
					});
					const year = expiryStr.slice(4, 6);
					return `${day} ${month} ${year}`;
				})
		)
	].sort((a, b) => new Date(a).getTime() - new Date(b).getTime());

	// 3. Filter contracts based on selected asset and expiry
	$: filteredContracts = allContracts.filter((contract) => {
		if (!contract.symbol) return false;
		const [, asset, , expiryStr] = contract.symbol.split('-');
		const day = expiryStr.slice(0, 2);
		const month = new Date(`2000-${expiryStr.slice(2, 4)}-01`).toLocaleString('en-US', {
			month: 'short'
		});
		const year = expiryStr.slice(4, 6);
		const formattedExpiry = `${day} ${month} ${year}`;

		return asset === selectedAsset && selectedExpiry === formattedExpiry;
	});

	// 4. Group filtered contracts by strike price for the table
	$: groupedByStrike = filteredContracts.reduce((acc, contract) => {
		const strike = contract.strike_price;
		if (!acc[strike]) {
			acc[strike] = { strike: parseFloat(strike) };
		}
		// Differentiate between calls and puts based on the symbol
		if (contract.symbol.startsWith('C-')) {
			acc[strike].call = contract;
		} else if (contract.symbol.startsWith('P-')) {
			acc[strike].put = contract;
		}
		return acc;
	}, {});

	$: tableData = Object.values(groupedByStrike).sort((a, b) => a.strike - b.strike);
</script>

<main>
	<header>
		<h1>Options Chain</h1>
	</header>

	<FilterControls
		{availableAssets}
		{availableExpiries}
		{selectedAsset}
		{selectedExpiry}
		on:selectAsset={(e) => {
			selectedAsset = e.detail;
			// Reset expiry when asset changes
			if (availableExpiries.length > 0) {
				selectedExpiry = availableExpiries[0];
			}
		}}
		on:selectExpiry={(e) => (selectedExpiry = e.detail)}
	/>

	<OptionsTable contracts={tableData} />
</main>

<style>
	:global(body) {
		background-color: #1c1c1c;
		color: #f0f0f0;
		font-family:
			-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
	}

	main {
		max-width: 100%;
		margin: 0 auto;
		padding: 1rem;
	}

	header h1 {
		font-size: 1.5rem;
		color: #f39c12;
		margin-bottom: 1rem;
	}
</style>
