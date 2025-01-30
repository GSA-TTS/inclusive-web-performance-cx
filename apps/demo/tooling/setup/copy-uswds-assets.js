import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// Define the source and destination paths
const paths = [
  {
    source: path.resolve(
      __dirname,
      '../../node_modules/@uswds/uswds/dist/fonts'
    ),
    destination: path.resolve(__dirname, '../../public/uswds/fonts'),
  },
  {
    source: path.resolve(
      __dirname,
      '../../node_modules/@uswds/uswds/dist/img/sprite.svg'
    ),
    destination: path.resolve(__dirname, '../../public/uswds/img/sprite.svg'),
  },
];

// There are files that are provided by USWDS, but it's easier to have them
// in the project directory so we can reference them directly in the HTML source or
// have the paths to font files work out of the box.
async function copyUswdsAssets() {
  try {
    for (const { source, destination } of paths) {
      if (!fs.existsSync(source)) {
        console.error(`Source not found: ${source}`);
        continue;
      }

      const stat = await fs.promises.stat(source);
      if (stat.isFile()) {
        const destinationDir = path.dirname(destination);
        if (!fs.existsSync(destinationDir)) {
          console.log(`Creating directory: ${destinationDir}`);
          await fs.promises.mkdir(destinationDir, { recursive: true });
        }

        await fs.promises.copyFile(source, destination);
        console.log(`Copied file from "${source}" to "${destination}"`);
      } else if (stat.isDirectory()) {
        if (!fs.existsSync(destination)) {
          console.log(`Creating directory: ${destination}`);
          await fs.promises.mkdir(destination, { recursive: true });
        }

        await fs.promises.cp(source, destination, { recursive: true });
        console.log(`Copied directory from "${source}" to "${destination}"`);
      } else {
        console.log(`Skipping unsupported type: "${source}"`);
      }
    }
  } catch (error) {
    console.error('Error copying files or directories:', error);
  }
}

copyUswdsAssets();
