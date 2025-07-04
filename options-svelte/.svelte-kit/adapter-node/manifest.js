export const manifest = (() => {
function __memo(fn) {
	let value;
	return () => value ??= (value = fn());
}

return {
	appDir: "_app",
	appPath: "_app",
	assets: new Set(["favicon.svg","robots.txt"]),
	mimeTypes: {".svg":"image/svg+xml",".txt":"text/plain"},
	_: {
		client: {start:"_app/immutable/entry/start.DcLD--W9.js",app:"_app/immutable/entry/app.BDgCAO1X.js",imports:["_app/immutable/entry/start.DcLD--W9.js","_app/immutable/chunks/BFkOmnuw.js","_app/immutable/chunks/9ZkQc-hj.js","_app/immutable/chunks/AWGgylXS.js","_app/immutable/entry/app.BDgCAO1X.js","_app/immutable/chunks/AWGgylXS.js","_app/immutable/chunks/9ZkQc-hj.js","_app/immutable/chunks/CWj6FrbW.js","_app/immutable/chunks/BywFvj-s.js","_app/immutable/chunks/CFr9uBtg.js"],stylesheets:[],fonts:[],uses_env_dynamic_public:false},
		nodes: [
			__memo(() => import('./nodes/0.js')),
			__memo(() => import('./nodes/1.js')),
			__memo(() => import('./nodes/4.js'))
		],
		routes: [
			{
				id: "/sverdle",
				pattern: /^\/sverdle\/?$/,
				params: [],
				page: { layouts: [0,], errors: [1,], leaf: 2 },
				endpoint: null
			}
		],
		prerendered_routes: new Set(["/","/about","/sverdle/how-to-play"]),
		matchers: async () => {
			
			return {  };
		},
		server_assets: {}
	}
}
})();

export const prerendered = new Set(["/","/about","/sverdle/how-to-play"]);

export const base = "";