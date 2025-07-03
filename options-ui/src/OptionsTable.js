import React from "react";
import classNames from "classnames";
import "./OptionsTable.css";

// Helper: render fields for one side
const buildCells = (obj, groupKey, fields, visibleColumns, getValue) =>
    fields.map(f => {
        const id = `${groupKey}::${f.value}`;
        let val = getValue(obj, f.value);

        // Format (e.g. for price, OI, etc.)
        if (val && !isNaN(+val) && f.value !== "expiry") {
            val = (+val).toLocaleString(undefined, { maximumFractionDigits: 4 });
        }
        return visibleColumns.includes(id) &&
            <div key={id} className={classNames("cell", groupKey, f.value)}>{val}</div>;
    });

export default function OptionsTable({
    optionsData, visibleColumns, expiry, underlying, FIELD_GROUPS, getValue
}) {
    // Group by strike and filter by expiry/underlying
    const filteredStrikes = Object.keys(optionsData).filter(key => {
        const ref = optionsData[key];
        const sample = ref.call || ref.put;
        return (!expiry || (sample && sample.symbol && sample.symbol.includes(expiry)))
            && (!underlying || (sample && sample.symbol && sample.symbol.includes(underlying)));
    }).sort((a, b) => {
        // Sort by strike
        const as = a.split("-")[2], bs = b.split("-")[2];
        return +as - +bs;
    });

    return (
        <div className="options-table">
            <div className="options-row table-header">
                {FIELD_GROUPS[0].fields.map(f =>
                    visibleColumns.includes(`call::${f.value}`) &&
                    <div key={`call::${f.value}`} className="cell call">{f.label}</div>
                )}
                {FIELD_GROUPS[1].fields.map(f =>
                    visibleColumns.includes(`center::${f.value}`) &&
                    <div key={`center::${f.value}`} className="cell strike">{f.label}</div>
                )}
                {FIELD_GROUPS[2].fields.map(f =>
                    visibleColumns.includes(`put::${f.value}`) &&
                    <div key={`put::${f.value}`} className="cell put">{f.label}</div>
                )}
            </div>
            {filteredStrikes.map(key => {
                const ref = optionsData[key];
                return (
                    <div className="options-row" key={key}>
                        {buildCells(ref.call || {}, "call", FIELD_GROUPS[0].fields, visibleColumns, getValue)}
                        {buildCells(ref.call || ref.put || {}, "center", FIELD_GROUPS[1].fields, visibleColumns, getValue)}
                        {buildCells(ref.put || {}, "put", FIELD_GROUPS[2].fields, visibleColumns, getValue)}
                    </div>
                );
            })}
        </div>
    );
}