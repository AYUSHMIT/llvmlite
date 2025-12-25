import llvmlite.binding as llvm

# Initialize LLVM (deprecated in newer versions, but kept for compatibility)
try:
    llvm.initialize()
except RuntimeError:
    # Newer versions of llvmlite handle initialization automatically
    pass

# Initialize native target (required for JIT)
try:
    llvm.initialize_native_target()
    llvm.initialize_native_asmprinter()
except RuntimeError:
    pass

def create_execution_engine():
    """
    Create an ExecutionEngine suitable for JIT code generation on
    the host CPU. The engine is reusable across modules.
    """
    target = llvm.Target.from_default_triple()
    target_machine = target.create_target_machine()
    backing_mod = llvm.parse_assembly("")
    engine = llvm.create_mcjit_compiler(backing_mod, target_machine)
    return engine

def compile_ir(engine, llvm_ir: str):
    """
    Compile the LLVM IR string with the given engine.
    Returns the compiled module.
    """
    mod = llvm.parse_assembly(llvm_ir)
    mod.verify()
    engine.add_module(mod)
    engine.finalize_object()
    engine.run_static_constructors()
    return mod

def get_function_address(engine, name: str) -> int:
    """
    Retrieve the address of a function by name.
    """
    return engine.get_function_address(name)
