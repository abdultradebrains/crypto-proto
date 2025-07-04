import * as server from '../entries/pages/sverdle/_page.server.ts.js';

export const index = 4;
let component_cache;
export const component = async () => component_cache ??= (await import('../entries/pages/sverdle/_page.svelte.js')).default;
export { server };
export const server_id = "src/routes/sverdle/+page.server.ts";
export const imports = ["_app/immutable/nodes/4.ChrozJXM.js","_app/immutable/chunks/CWj6FrbW.js","_app/immutable/chunks/AWGgylXS.js","_app/immutable/chunks/9ZkQc-hj.js","_app/immutable/chunks/BywFvj-s.js","_app/immutable/chunks/C7FwJ61l.js","_app/immutable/chunks/DE6qcIQU.js","_app/immutable/chunks/CFr9uBtg.js","_app/immutable/chunks/BFkOmnuw.js"];
export const stylesheets = ["_app/immutable/assets/4.yeGN9jlM.css"];
export const fonts = [];
