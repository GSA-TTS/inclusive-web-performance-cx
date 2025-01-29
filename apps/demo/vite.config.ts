import { defineConfig } from 'vite';
import { viteMockServe } from 'vite-plugin-mock';


export default defineConfig({
	plugins: [
		viteMockServe({
			mockPath: "mock",
			enable: true
		})
	],
	css: {
		preprocessorOptions: {
			scss: {
				loadPaths: [
					"./node_modules/@uswds",
                    "./node_modules/@uswds/uswds/packages",
				]
			}
		}
	}
});
