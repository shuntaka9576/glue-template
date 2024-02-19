import { defineConfig } from 'vitest/config';

export default defineConfig({
  test: {
    name: 'test',
    dir: 'test',
    globals: true,
  },
});
