import { defineConfig } from 'vite';

export default defineConfig({
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
