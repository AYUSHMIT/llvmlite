#!/usr/bin/env python3
import argparse
import ctypes
import os
import time
from typing import Tuple

import numpy as np
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt

from demo.jit_utils import create_execution_engine, compile_ir, get_function_address
from demo.kernels import build_add_i32_module, build_sum_array_module

OUT_DIR = "demo/out"
os.makedirs(OUT_DIR, exist_ok=True)

def save_ir(name: str, ir_text: str):
    path = os.path.join(OUT_DIR, f"{name}.ll")
    with open(path, "w") as f:
        f.write(ir_text)
    print(f"[*] Saved IR: {path}")

def wrap_cfunc(addr: int, restype, argtypes):
    """
    Wrap a function pointer address as a ctypes callable.
    """
    functype = ctypes.CFUNCTYPE(restype, *argtypes)
    return functype(addr)

def demo_add(engine):
    ir_text = build_add_i32_module()
    save_ir("add", ir_text)
    mod = compile_ir(engine, ir_text)
    addr = get_function_address(engine, "add")
    cfunc = wrap_cfunc(addr, ctypes.c_int32, [ctypes.c_int32, ctypes.c_int32])
    res = cfunc(7, 35)
    print(f"add(7,35) JIT -> {res}")

def py_sum(arr: np.ndarray) -> float:
    return float(np.sum(arr))

def jit_sum(engine, arr: np.ndarray) -> float:
    ir_text = build_sum_array_module()
    save_ir("sum", ir_text)
    compile_ir(engine, ir_text)
    addr = get_function_address(engine, "sum")
    cfunc = wrap_cfunc(addr, ctypes.c_double, [ctypes.POINTER(ctypes.c_double), ctypes.c_int32])
    # Ensure contiguous double array
    arr = np.ascontiguousarray(arr, dtype=np.float64)
    ptr = arr.ctypes.data_as(ctypes.POINTER(ctypes.c_double))
    return cfunc(ptr, arr.size)

def benchmark_sum(engine, n: int = 1_000_000, trials: int = 5) -> Tuple[float, float]:
    arr = np.random.rand(n).astype(np.float64)

    # Warmup
    _ = jit_sum(engine, arr)

    py_times = []
    jit_times = []

    for _ in range(trials):
        t0 = time.perf_counter()
        py_res = py_sum(arr)
        py_times.append(time.perf_counter() - t0)

        t0 = time.perf_counter()
        jit_res = jit_sum(engine, arr)
        jit_times.append(time.perf_counter() - t0)

    # Save summary
    summary_md = os.path.join(OUT_DIR, "summary.md")
    with open(summary_md, "w") as f:
        f.write("# llvmlite Demo Summary\n")
        f.write(f"- Array length: {n}\n")
        f.write(f"- Trials: {trials}\n")
        f.write(f"- Python mean time: {np.mean(py_times):.6f}s\n")
        f.write(f"- JIT mean time: {np.mean(jit_times):.6f}s\n")
        f.write(f"- Speedup (Python/JIT): {np.mean(py_times)/np.mean(jit_times):.2f}x\n")
    print(f"[*] Saved summary: {summary_md}")

    # Plot
    plt.figure(figsize=(6,4))
    plt.plot(py_times, label="Python (numpy.sum)", marker="o")
    plt.plot(jit_times, label="JIT (llvmlite)", marker="o")
    plt.xlabel("Trial")
    plt.ylabel("Seconds")
    plt.title("Sum Benchmark")
    plt.legend()
    plot_path = os.path.join(OUT_DIR, "benchmark.png")
    plt.tight_layout()
    plt.savefig(plot_path)
    print(f"[*] Saved plot: {plot_path}")

    return np.mean(py_times), np.mean(jit_times)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--benchmark", action="store_true", help="Run performance benchmark")
    parser.add_argument("--save", action="store_true", help="Save IR and outputs")
    parser.add_argument("--generate-only", action="store_true", help="Generate IR only without running benchmarks")
    args = parser.parse_args()

    engine = create_execution_engine()

    demo_add(engine)

    if args.generate_only:
        # Save sum IR without running
        save_ir("sum", build_sum_array_module())
        return

    if args.benchmark:
        py_t, jit_t = benchmark_sum(engine)
        print(f"Python mean: {py_t:.6f}s; JIT mean: {jit_t:.6f}s; Speedup: {py_t/jit_t:.2f}x")
    else:
        # Small demo run
        arr = np.random.rand(1000).astype(np.float64)
        res = jit_sum(engine, arr)
        print(f"JIT sum({arr.size}) -> {res:.6f}")

if __name__ == "__main__":
    main()
