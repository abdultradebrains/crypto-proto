<!-- File: src/lib/components/OptionsTable.svelte -->
<!-- Description: Renders the main options chain table for calls and puts. -->

<script context="module" lang="ts">
	export interface OptionContract {
		strike: number | string;
		call?: Record<string, any>;
		put?: Record<string, any>;
		[key: string]: any;
	}
</script>

<script lang="ts">
	export let contracts: OptionContract[] = [];

	const FIELD_GROUPS = [
		// Your FIELD_GROUPS configuration here...
		{
			key: 'call',
			label: 'Calls',
			fields: [
				{ label: 'Delta', value: 'greeks.delta' },
				{ label: 'Theta', value: 'greeks.theta' },
				{ label: 'Spot', value: 'greeks.spot' },
				{ label: 'Bid', value: 'quotes.best_bid' },
				{ label: 'Bid Size', value: 'quotes.bid_size' },
				{ label: 'Ask', value: 'quotes.best_ask' },
				{ label: 'Ask Size', value: 'quotes.ask_size' },
				{ label: 'Mark', value: 'mark_price' },
				{ label: 'Mark Chg 24h', value: 'mark_change_24h' },
				{ label: 'OI', value: 'oi' }
			]
		},
		{
			key: 'center',
			label: 'Central',
			fields: [{ label: 'Strike', value: 'strike_price' }]
		},
		{
			key: 'put',
			label: 'Puts',
			fields: [
				{ label: 'OI', value: 'oi' },
				{ label: 'Bid Size', value: 'quotes.bid_size' },
				{ label: 'Bid', value: 'quotes.best_bid' },
				{ label: 'Ask', value: 'quotes.best_ask' },
				{ label: 'Ask Size', value: 'quotes.ask_size' },
				{ label: 'Mark', value: 'mark_price' },
				{ label: 'Delta', value: 'greeks.delta' },
				{ label: 'Theta', value: 'greeks.theta' }
			]
		}
	];

	/**
	 * Safely gets a nested value from an object using a string path.
	 * @param {object} obj The object to access.
	 * @param {string} path The path to the value (e.g., 'greeks.delta').
	 * @returns {*} The value, or '-' if not found.
	 */
	function getNestedValue(obj: any, path: string) {
		if (!obj || !path) return '-';
		const value = path
			.split('.')
			.reduce((o, p) => (o && o[p] !== undefined ? o[p] : undefined), obj);
		if (value === undefined || value === null) return '-';

		// Basic formatting for numbers
		if (!isNaN(parseFloat(value))) {
			return parseFloat(value).toLocaleString('en-US', {
				minimumFractionDigits: 2,
				maximumFractionDigits: 4
			});
		}

		return value;
	}
</script>

<div class="options-table-wrapper">
	<table class="options-table">
		<thead>
			<tr>
				{#each FIELD_GROUPS as group}
					{#each group.fields as field}
						<th class:strike-header={group.key === 'center'}>{field.label}</th>
					{/each}
				{/each}
			</tr>
		</thead>
		<tbody>
			{#each contracts as row (row.strike)}
				<tr>
					{#each FIELD_GROUPS as group}
						{#each group.fields as field}
							{@const contract = group.key === 'put' ? row.put : row.call}
							<td
								class:strike-price={field.value === 'strike_price'}
								class:bid={field.label.includes('Bid')}
								class:ask={field.label.includes('Ask')}
							>
								{getNestedValue(contract, field.value)}
							</td>
						{/each}
					{/each}
				</tr>
			{/each}
		</tbody>
	</table>
</div>

<style>
	.options-table-wrapper {
		overflow-x: auto;
		background-color: #1e2a38;
		width: 100%;
	}
	.options-table {
		width: 100%;
		border-collapse: collapse;
		color: #ecf0f1;
		font-size: 0.9em;
		white-space: nowrap;
	}
	th,
	td {
		padding: 0.75rem;
		text-align: right;
		border-bottom: 1px solid #34495e;
	}
	th {
		background-color: #2c3e50;
		font-weight: normal;
		color: #95a5a6;
		position: sticky;
		top: 0;
		z-index: 2;
	}
	/* .strike-header,
	.strike-price {
		text-align: center;
		font-weight: bold;
		background-color: #19222c;
		border-left: 1px solid #34495e;
		border-right: 1px solid #34495e;
		position: sticky;
		left: 50%;
		transform: translateX(-50%);
		z-index: 1;
	} */
	.strike-price {
		color: #f1c40f;
	}
	.bid {
		color: #2ecc71;
	}
	.ask {
		color: #e74c3c;
	}
	tbody tr:hover {
		background-color: #34495e;
	}
</style>
