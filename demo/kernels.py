from llvmlite import ir

def build_add_i32_module():
    """
    Build a simple module with: i32 add(i32 a, i32 b)
    """
    module = ir.Module(name="add_module")
    func_ty = ir.FunctionType(ir.IntType(32), [ir.IntType(32), ir.IntType(32)])
    func = ir.Function(module, func_ty, name="add")
    block = func.append_basic_block(name="entry")
    builder = ir.IRBuilder(block)
    sumv = builder.add(func.args[0], func.args[1], name="sum")
    builder.ret(sumv)
    return str(module)

def build_sum_array_module():
    """
    Build a module with: double sum(double* a, i32 n)
    Loops from i=0..n-1 and accumulates a[i] into a running sum.
    """
    module = ir.Module(name="sum_module")

    double = ir.DoubleType()
    i32 = ir.IntType(32)
    ptr_double = double.as_pointer()

    func_ty = ir.FunctionType(double, [ptr_double, i32])
    func = ir.Function(module, func_ty, name="sum")
    a_ptr, n = func.args
    a_ptr.name = "a"
    n.name = "n"

    entry = func.append_basic_block("entry")
    loop = func.append_basic_block("loop")
    after = func.append_basic_block("after")

    builder = ir.IRBuilder(entry)
    sum_alloca = builder.alloca(double, name="sum")
    i_alloca = builder.alloca(i32, name="i")

    builder.store(ir.Constant(double, 0.0), sum_alloca)
    builder.store(ir.Constant(i32, 0), i_alloca)

    # i < n ?
    i_val = builder.load(i_alloca, name="i_val")
    cmp = builder.icmp_signed("<", i_val, n, name="cmp")
    builder.cbranch(cmp, loop, after)

    # loop body
    builder.position_at_end(loop)
    i_val = builder.load(i_alloca, name="i_val_loop")
    elem_ptr = builder.gep(a_ptr, [i_val], inbounds=True, name="elem_ptr")
    elem = builder.load(elem_ptr, name="elem")
    cur_sum = builder.load(sum_alloca, name="cur_sum")
    new_sum = builder.fadd(cur_sum, elem, name="new_sum")
    builder.store(new_sum, sum_alloca)
    next_i = builder.add(i_val, ir.Constant(i32, 1), name="next_i")
    builder.store(next_i, i_alloca)

    # loop continue
    cmp2 = builder.icmp_signed("<", next_i, n, name="cmp2")
    builder.cbranch(cmp2, loop, after)

    # after block
    builder.position_at_end(after)
    final_sum = builder.load(sum_alloca, name="final_sum")
    builder.ret(final_sum)

    return str(module)
