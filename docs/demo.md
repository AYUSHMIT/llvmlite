# llvmlite JIT Demo

This demo uses `llvmlite.ir` to build LLVM IR for simple functions, JIT-compiles them with `llvmlite.binding` (MCJIT), and compares performance against pure Python/NumPy.

## Prerequisites

- LLVM toolchain and development libraries (e.g., 15)
- Python 3.10–3.12
- NumPy, Matplotlib

Codespaces and CI install everything automatically.

## Quickstart (Local)

```bash
# Install LLVM (example for Ubuntu; adjust version/path as needed)
sudo apt-get install -y llvm-15 llvm-15-dev clang-15
export LLVM_CONFIG=/usr/bin/llvm-config-15

# Build llvmlite from the fork
python -m pip install -U pip
pip install -e .

# Run the demo
pip install numpy matplotlib
python demo/run.py --benchmark --save
```

Artifacts will be in `demo/out/`:
- `add.ll`, `sum.ll`: IR for demo functions
- `summary.md`: benchmark summary
- `benchmark.png`: performance plot

## Building IR

`demo/kernels.py` constructs IR for:
- `i32 add(i32, i32)` — basic arithmetic
- `double sum(double* a, i32 n)` — loop with pointer arithmetic

Use `llvmlite.ir` types (`IntType`, `DoubleType`) and `IRBuilder` to create blocks, loops, and GEPs.

## JIT Compilation

We JIT via `llvmlite.binding`:
- Initialize, create `TargetMachine`, and MCJIT `ExecutionEngine`
- `compile_ir(engine, str(module))` to add and finalize module
- Get function addresses via `engine.get_function_address`
- Wrap addresses with `ctypes.CFUNCTYPE` to call from Python

## Performance Notes

- JIT overhead is non-zero; warm up before timing
- Avoid Python overhead in tight loops by operating on raw pointers
- Ensure arrays are contiguous (`np.ascontiguousarray`) and `float64`

## Troubleshooting

- Match `LLVM_CONFIG` to the installed version (e.g., `/usr/bin/llvm-config-15`)
- If editable build fails in CI, the workflow falls back to `pip install llvmlite`
- On macOS, use `brew install llvm@15` and set `LLVM_CONFIG` accordingly
