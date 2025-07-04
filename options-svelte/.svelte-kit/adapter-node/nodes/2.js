import * as universal from '../entries/pages/_page.ts.js';

export const index = 2;
let component_cache;
export const component = async () => component_cache ??= (await import('../entries/pages/_page.svelte.js')).default;
export { universal };
export const universal_id = "src/routes/+page.ts";
export const imports = ["_app/immutable/nodes/2.D3r5117z.js","_app/immutable/chunks/CWj6FrbW.js","_app/immutable/chunks/CQABdrtb.js","_app/immutable/chunks/AWGgylXS.js","_app/immutable/chunks/9ZkQc-hj.js","_app/immutable/chunks/C_4fyel-.js","_app/immutable/chunks/CFr9uBtg.js","_app/immutable/chunks/C7FwJ61l.js"];
export const stylesheets = ["_app/immutable/assets/2.DHFZGk4D.css"];
export const fonts = [];
