# glue-template

## Requirements

|Tool|Version|
|---|---|
|[Rye](https://github.com/mitsuhiko/rye)|0.24.0
|[Finch](https://github.com/runfinch/finch)|1.1.1


Install Rye, enabled `uv` option.

```bash
./setup-rye.sh
```

## Installation

Install dependencies.
```bash
npm ci
npm run deps
```

Deploy AWS Resources.
```bash
cd packages/iac
npx cdk deploy
```

## Run glue test

Lunch container.
```bash
cd packages/src-glue/
finch compose up -d
```

Run test.
```bash
npm run test
# or
./run_test.sh <testName>
```
