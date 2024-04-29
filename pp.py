import re

class PyCode:
    def __init__(self):
        self._lines = []

    def set_params(self, params, lineno, indent):
        self.params = params
        self.lineno = lineno
        self.indent = indent

    def add_line(self, line):
        assert line[:self.indent].strip() == ""
        self._lines.append('    ' + line[self.indent:].rstrip())

    def gen(self):
        result = []
        emit = result.append
        params = self.params.strip().strip('()').split(',')
        params = [k.strip() for k in params]

        # template<class T1, class T2>
        classT = ', '.join("class T" + str(k+1) for k in range(len(params)))
        emit(f"template<{classT}>")  

        # void __CPP_PyCode_a_b_12(T1& a, T2& b) {
        params_s = '_'.join(params)
        cpp_name = f"__CPP_PyCode_{params_s}_{self.lineno}"
        params_a = ', '.join("T{}& {}".format(i, k) for i, k in enumerate(params, start=1))
        emit(f"void {cpp_name}({params_a}) {{")

        # pyactive
        emit("    auto& guard = pyactive();")

        # py::dict local;local["a"] = a;local["b"] = b; 
        local_names = ""
        for p in params:
            local_name = f'local["{p}"] = {p};'
            local_names += local_name
        emit(f'    py::dict local;{local_names}')

        # py::exec(R"xxx(b = a + 1)xxx", py::globals(), local); 
        code = '\n'.join(self._lines)
        emit(f'''    py::exec(R"(
{code}
    )", py::globals(), local);''')

        # a = local["a"].cast<T1>(); b = local["a"].cast<T2>(); 
        cast_outs = "    "
        for i, p in enumerate(params, start=1):
            cast = f'{p} = local["{p}"].cast<T{i}>();'
            cast_outs += cast

        emit(cast_outs)

        emit("}")

        # #define __PyCode_a_b_12(x) [&] { __CPP_PyCode_a_b_12(a, b); }()
        macro_name = f"__PyCode_{params_s}_{self.lineno}"
        params_l = ', '.join(params)
        emit(f"#define {macro_name}(x) [&] {{ {cpp_name}({params_l}); }}()")

        return '\n'.join(result)

def generate_gen_file(fname, outf):
    pycode = None
    stack = []
    with open(fname) as f:
        for lineno, line in enumerate(f, start=1):
            if not pycode:
                m = re.match(r"python\s+(\([^]]*\))?", line.strip())
                if m:
                    params = m.group(1)
                    pycode = PyCode()
                    pycode.set_params(params, lineno, line.find('python'))
                    if line.strip().endswith("("):
                        stack.append(')')
            else:
                if not stack and line.strip().endswith("("):
                    stack.append(')')
                if line.strip().endswith(');'):
                    stack.pop()
                    outf.write(pycode.gen())
                    pycode = None
                else:
                    pycode.add_line(line)

    if pycode:
        outf.write(pycode.gen())

if __name__ == "__main__":
    import sys
    sources = []
    target = None

    iters = iter(sys.argv)
    next(iters)

    try:
        while True:
            prefix = next(iters)
            path = next(iters)
            if prefix == '-i':
                sources.append(path)
            elif prefix == '-o':
                target = path
    except StopIteration:
        pass

    # source = "inline_py.cc"
    # target = "inline_py_gen2.h"

    with open(target, "w") as f:
        for source in sources:
            generate_gen_file(source, f)


# python3 pp.py -o inline_py_gen2.h -i inline_py.cc -i inline_py2.cc