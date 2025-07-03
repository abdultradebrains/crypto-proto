import React, { useEffect, useRef, useState } from "react";
import OptionsTable from "./OptionsTable";
import "./App.css";

// Define all possible fields from your JSON sample
const FIELD_GROUPS = [
  {
    key: "call",
    label: "Calls",
    fields: [
      { label: "Delta", value: "greeks.delta" },
      { label: "Gamma", value: "greeks.gamma" },
      { label: "Vega", value: "greeks.vega" },
      { label: "Theta", value: "greeks.theta" },
      { label: "Rho", value: "greeks.rho" },
      { label: "Spot", value: "greeks.spot" },
      { label: "Bid", value: "quotes.best_bid" },
      { label: "Bid Size", value: "quotes.bid_size" },
      { label: "Ask", value: "quotes.best_ask" },
      { label: "Ask Size", value: "quotes.ask_size" },
      { label: "Mark", value: "mark_price" },
      { label: "Mark IV", value: "quotes.mark_iv" },
      { label: "Mark Chg 24h", value: "mark_change_24h" },
      { label: "OI", value: "oi" }
    ]
  },
  {
    key: "center",
    label: "Central",
    fields: [
      { label: "Strike", value: "strike_price" },
      { label: "Expiry", value: "expiry" }
    ]
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
      { label: "Mark IV", value: "quotes.mark_iv" },
      { label: "Delta", value: "greeks.delta" },
      { label: "Gamma", value: "greeks.gamma" },
      { label: "Vega", value: "greeks.vega" },
      { label: "Theta", value: "greeks.theta" },
      { label: "Rho", value: "greeks.rho" }
    ]
  }
];

// Helper safely gets nested value from the object, or empty
const getValue = (obj, path) => (
  path.split(".").reduce((o, k) => (o && o[k] !== undefined ? o[k] : ""), obj)
);

export default function App() {
  const [optionsData, setOptionsData] = useState({});
  const [expiries, setExpiries] = useState([]);
  const [underlyings, setUnderlyings] = useState([]);
  const [selectedExpiry, setSelectedExpiry] = useState("");
  const [selectedUnderlying, setSelectedUnderlying] = useState("");
  // Unique column id is always `${grp.key}::${field.value}`
  const allColumns = FIELD_GROUPS.flatMap(
    grp => grp.fields.map(f => ({ ...f, group: grp.key, id: `${grp.key}::${f.value}` }))
  );
  const [visibleColumns, setVisibleColumns] = useState(
    allColumns.map(c => c.id)
  );
  const ws = useRef(null);
  useEffect(() => {
    setUnderlyings(['BTC', 'ETH']);
    ws.current = new window.WebSocket("wss://socket.delta.exchange");
    ws.current.onopen = () => {
      const subscription_msg = {
        type: "subscribe",
        payload: {
          channels: [
            {
              name: "v2/ticker",
              symbols: ["call_options", "put_options"]
            }
          ]
        }
      };
      ws.current.send(JSON.stringify(subscription_msg));
    };
    ws.current.onmessage = (event) => {
      // try {
      const msg = JSON.parse(event.data);
      const update = msg;
      console.log("Received update:", update);
      // Get {call|put}, underlying, expiry, strike for keying
      const symbol = update.symbol || "";
      const parts = symbol.split("-");
      if (parts.length < 4) return;
      const optType = parts[0] === "C" ? "call" : "put";
      const expiry = parts[3];
      const strike = update.strike_price;
      const key = symbol;

      setOptionsData(prev => {
        const next = { ...prev };
        if (!next[key]) next[key] = {};
        next[key][optType] = update;
        return next;
      });
      if (!expiries.includes(expiry))
        setExpiries(exs => [...exs, expiry]);
      console.log(expiries, 'list of expieres')

      // } catch (e) { console.error("Error parsing message:", e, event.data); }
    };
    return () => ws.current && ws.current.close();
    // eslint-disable-next-line
  }, []);

  const handleColumnToggle = id =>
    setVisibleColumns(cols =>
      cols.includes(id) ? cols.filter(c => c !== id) : [...cols, id]
    );

  return (
    <div className="App">
      <header>
        <div className="filter-tabs">
          {underlyings.map(u => (
            <button key={u}
              className={u === selectedUnderlying ? "active" : ""}
              onClick={() => setSelectedUnderlying(u)}>
              {u}
            </button>
          ))}
        </div>
        <div className="filter-tabs">
          {/* {expiries.map(e => (
            <button key={e}
              className={e === selectedExpiry ? "active" : ""}
              onClick={() => setSelectedExpiry(e)}>
              {e}
            </button>
          ))} */}
        </div>
        <div style={{ marginBottom: 8 }}>
          <strong>Columns:</strong>
          {allColumns.map(f =>
            <label key={f.id} style={{ margin: "0 1em" }}>
              <input
                type="checkbox"
                checked={visibleColumns.includes(f.id)}
                onChange={() => handleColumnToggle(f.id)}
              />
              {f.label}
            </label>
          )}
        </div>
      </header>
      <OptionsTable
        optionsData={optionsData}
        visibleColumns={visibleColumns}
        expiry={selectedExpiry}
        underlying={selectedUnderlying}
        FIELD_GROUPS={FIELD_GROUPS}
        getValue={getValue}
      />
    </div>
  );
}