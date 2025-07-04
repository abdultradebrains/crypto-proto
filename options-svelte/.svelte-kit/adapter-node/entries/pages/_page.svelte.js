import { G as fallback, I as ensure_array_like, J as attr_class, E as escape_html, K as bind_props, B as pop, z as push, M as store_get, N as unsubscribe_stores } from "../../chunks/index3.js";
import { w as writable } from "../../chunks/index2.js";
const optionsData = writable({});
function FilterControls($$payload, $$props) {
  push();
  let availableAssets = fallback($$props["availableAssets"], () => [], true);
  let availableExpiries = fallback($$props["availableExpiries"], () => [], true);
  let selectedAsset = $$props["selectedAsset"];
  let selectedExpiry = $$props["selectedExpiry"];
  const each_array = ensure_array_like(availableAssets);
  const each_array_1 = ensure_array_like(availableExpiries);
  $$payload.out += `<div class="filter-container svelte-mgkby8"><div class="asset-filters svelte-mgkby8"><!--[-->`;
  for (let $$index = 0, $$length = each_array.length; $$index < $$length; $$index++) {
    let asset = each_array[$$index];
    $$payload.out += `<button${attr_class("svelte-mgkby8", void 0, { "active": selectedAsset === asset })}>${escape_html(asset)}</button>`;
  }
  $$payload.out += `<!--]--></div> <div class="expiry-filters svelte-mgkby8"><!--[-->`;
  for (let $$index_1 = 0, $$length = each_array_1.length; $$index_1 < $$length; $$index_1++) {
    let expiry = each_array_1[$$index_1];
    $$payload.out += `<button${attr_class("svelte-mgkby8", void 0, { "active": selectedExpiry === expiry })}>${escape_html(expiry)}</button>`;
  }
  $$payload.out += `<!--]--></div></div>`;
  bind_props($$props, {
    availableAssets,
    availableExpiries,
    selectedAsset,
    selectedExpiry
  });
  pop();
}
function OptionsTable($$payload, $$props) {
  push();
  let contracts = fallback($$props["contracts"], () => [], true);
  const FIELD_GROUPS = [
    // Your FIELD_GROUPS configuration here...
    {
      key: "call",
      label: "Calls",
      fields: [
        { label: "Delta", value: "greeks.delta" },
        { label: "Theta", value: "greeks.theta" },
        { label: "Spot", value: "greeks.spot" },
        { label: "Bid", value: "quotes.best_bid" },
        { label: "Bid Size", value: "quotes.bid_size" },
        { label: "Ask", value: "quotes.best_ask" },
        { label: "Ask Size", value: "quotes.ask_size" },
        { label: "Mark", value: "mark_price" },
        { label: "Mark Chg 24h", value: "mark_change_24h" },
        { label: "OI", value: "oi" }
      ]
    },
    {
      key: "center",
      label: "Central",
      fields: [{ label: "Strike", value: "strike_price" }]
    },
    {
      key: "put",
      label: "Puts",
      fields: [
        { label: "OI", value: "oi" },
        { label: "Bid Size", value: "quotes.bid_size" },
        { label: "Bid", value: "quotes.best_bid" },
        { label: "Ask", value: "quotes.best_ask" },
        { label: "Ask Size", value: "quotes.ask_size" },
        { label: "Mark", value: "mark_price" },
        { label: "Delta", value: "greeks.delta" },
        { label: "Theta", value: "greeks.theta" }
      ]
    }
  ];
  function getNestedValue(obj, path) {
    if (!obj || !path) return "-";
    const value = path.split(".").reduce((o, p) => o && o[p] !== void 0 ? o[p] : void 0, obj);
    if (value === void 0 || value === null) return "-";
    if (!isNaN(parseFloat(value))) {
      return parseFloat(value).toLocaleString("en-US", { minimumFractionDigits: 2, maximumFractionDigits: 4 });
    }
    return value;
  }
  const each_array = ensure_array_like(FIELD_GROUPS);
  const each_array_2 = ensure_array_like(contracts);
  $$payload.out += `<div class="options-table-wrapper svelte-6v4bw5"><table class="options-table svelte-6v4bw5"><thead><tr><!--[-->`;
  for (let $$index_1 = 0, $$length = each_array.length; $$index_1 < $$length; $$index_1++) {
    let group = each_array[$$index_1];
    const each_array_1 = ensure_array_like(group.fields);
    $$payload.out += `<!--[-->`;
    for (let $$index = 0, $$length2 = each_array_1.length; $$index < $$length2; $$index++) {
      let field = each_array_1[$$index];
      $$payload.out += `<th${attr_class("svelte-6v4bw5", void 0, { "strike-header": group.key === "center" })}>${escape_html(field.label)}</th>`;
    }
    $$payload.out += `<!--]-->`;
  }
  $$payload.out += `<!--]--></tr></thead><tbody class="svelte-6v4bw5"><!--[-->`;
  for (let $$index_4 = 0, $$length = each_array_2.length; $$index_4 < $$length; $$index_4++) {
    let row = each_array_2[$$index_4];
    const each_array_3 = ensure_array_like(FIELD_GROUPS);
    $$payload.out += `<tr class="svelte-6v4bw5"><!--[-->`;
    for (let $$index_3 = 0, $$length2 = each_array_3.length; $$index_3 < $$length2; $$index_3++) {
      let group = each_array_3[$$index_3];
      const each_array_4 = ensure_array_like(group.fields);
      $$payload.out += `<!--[-->`;
      for (let $$index_2 = 0, $$length3 = each_array_4.length; $$index_2 < $$length3; $$index_2++) {
        let field = each_array_4[$$index_2];
        const contract = group.key === "put" ? row.put : row.call;
        $$payload.out += `<td${attr_class("svelte-6v4bw5", void 0, {
          "strike-price": field.value === "strike_price",
          "bid": field.label.includes("Bid"),
          "ask": field.label.includes("Ask")
        })}>${escape_html(getNestedValue(contract, field.value))}</td>`;
      }
      $$payload.out += `<!--]-->`;
    }
    $$payload.out += `<!--]--></tr>`;
  }
  $$payload.out += `<!--]--></tbody></table></div>`;
  bind_props($$props, { contracts });
  pop();
}
function _page($$payload, $$props) {
  push();
  var $$store_subs;
  let allContracts, availableExpiries, filteredContracts, groupedByStrike, tableData;
  let selectedAsset = "BTC";
  let availableAssets = ["BTC", "ETH"];
  let selectedExpiry = "04 Jul 25";
  allContracts = Object.values(store_get($$store_subs ??= {}, "$optionsData", optionsData));
  availableExpiries = [
    ...new Set(allContracts.filter((c) => c.underlying_asset_symbol === selectedAsset).map((c) => {
      const [, , , expiryStr] = c.symbol.split("-");
      const day = expiryStr.slice(0, 2);
      const month = (/* @__PURE__ */ new Date(`2000-${expiryStr.slice(2, 4)}-01`)).toLocaleString("en-US", { month: "short" });
      const year = expiryStr.slice(4, 6);
      return `${day} ${month} ${year}`;
    }))
  ].sort((a, b) => new Date(a).getTime() - new Date(b).getTime());
  filteredContracts = allContracts.filter((contract) => {
    if (!contract.symbol) return false;
    const [, asset, , expiryStr] = contract.symbol.split("-");
    const day = expiryStr.slice(0, 2);
    const month = (/* @__PURE__ */ new Date(`2000-${expiryStr.slice(2, 4)}-01`)).toLocaleString("en-US", { month: "short" });
    const year = expiryStr.slice(4, 6);
    const formattedExpiry = `${day} ${month} ${year}`;
    return asset === selectedAsset && selectedExpiry === formattedExpiry;
  });
  groupedByStrike = filteredContracts.reduce(
    (acc, contract) => {
      const strike = contract.strike_price;
      if (!acc[strike]) {
        acc[strike] = { strike: parseFloat(strike) };
      }
      if (contract.symbol.startsWith("C-")) {
        acc[strike].call = contract;
      } else if (contract.symbol.startsWith("P-")) {
        acc[strike].put = contract;
      }
      return acc;
    },
    {}
  );
  tableData = Object.values(groupedByStrike).sort((a, b) => a.strike - b.strike);
  $$payload.out += `<main class="svelte-11tqb00"><header class="svelte-11tqb00"><h1 class="svelte-11tqb00">Options Chain</h1></header> `;
  FilterControls($$payload, {
    availableAssets,
    availableExpiries,
    selectedAsset,
    selectedExpiry
  });
  $$payload.out += `<!----> `;
  OptionsTable($$payload, {
    contracts: (
      // Reset expiry when asset changes
      tableData
    )
  });
  $$payload.out += `<!----></main>`;
  if ($$store_subs) unsubscribe_stores($$store_subs);
  pop();
}
export {
  _page as default
};
