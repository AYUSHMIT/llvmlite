# llvmlite Fork — Amazing JIT Demo

A fork of [llvmlite](https://github.com/numba/llvmlite) showcasing Python-driven LLVM IR generation, JIT compilation, and performance visualization:
- One-click Codespaces Dev Container
- CI matrix across Python versions
- IR generation + MCJIT execution
- Benchmarking and plots, published artifacts

## Quickstart

```bash
export LLVM_CONFIG=/usr/bin/llvm-config-15
pip install -e .
pip install numpy matplotlib
python demo/run.py --benchmark --save
```

See [`docs/demo.md`](docs/demo.md) for detailed steps.

## CI and Artifacts

Every push runs CI, builds the package (editable if possible), executes demo samples, and uploads artifacts from `demo/out/`.

## What's Inside

- `.devcontainer/` — Codespaces setup with Python + LLVM
- `.github/workflows/ci.yml` — Build + demo artifact upload
- `.github/workflows/pages.yml` — Publish `docs/` via GitHub Pages
- `demo/` — JIT utilities, kernels, and runner
- `docs/` — Tutorial for the demo

## Notes on LLVM Version

llvmlite pins to specific LLVM versions. This demo uses LLVM 15 by default.
If your environment differs, set `LLVM_CONFIG` to match your installed version.

## Credits

Original project: [numba/llvmlite](https://github.com/numba/llvmlite)
