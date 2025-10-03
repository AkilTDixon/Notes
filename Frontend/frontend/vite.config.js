import { defineConfig } from 'vite';
import plugin from '@vitejs/plugin-react';
import path from 'path'

// https://vitejs.dev/config/
export default defineConfig({
    plugins: [plugin()],
    server: {
        port: 63401,
    },
    resolve: {
        alias: {
            '@': path.resolve(__dirname, './src'),
        },
    },
});