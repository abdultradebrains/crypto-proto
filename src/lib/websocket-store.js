// File: src/lib/websocket-store.js
// Description: Handles WebSocket connection and manages the central data store for options contracts.

import { writable } from 'svelte/store';

// The key will be the contract symbol, e.g., 'C-BTC-100000-040725'.
export const optionsData = writable({});

/**
 * Connects to a WebSocket server and updates the store with incoming data.
 * @param {string} url - The URL of the WebSocket server.
 * @param {object} subscriptionMessage - The message to send upon connection.
 */
export function connectWebSocket(url, subscriptionMessage) {
    const socket = new WebSocket(url);

    socket.onopen = () => {
        console.log('WebSocket connection established.');
        // Send the subscription message when the connection is open
        if (subscriptionMessage) {
            socket.send(JSON.stringify(subscriptionMessage));
            console.log('Subscription message sent.');
        }
    };

    socket.onmessage = (event) => {
        try {
            const data = JSON.parse(event.data);
            // The v2/ticker channel sends data without a top-level symbol,
            // so we check for contract_type to identify the relevant messages.
            if (data && data.symbol && data.type === 'v2/ticker') {
                optionsData.update(currentData => {
                    return {
                        ...currentData,
                        [data.symbol]: data
                    };
                });
            }
        } catch (error) {
            console.error('Error parsing incoming WebSocket data:', error);
        }
    };

    socket.onerror = (error) => {
        console.error('WebSocket error:', error);
    };

    socket.onclose = () => {
        console.log('WebSocket connection closed.');
    };
}