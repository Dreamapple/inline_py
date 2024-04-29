# inline-python
Inline Python code directly in your C++ code.
Inspired by rust project [inline-python](https://docs.rs/inline-python/latest/inline_python/)!

# Example
```C++
#include <stdio.h>
#include "inline_py.h"
int main() {
    int a = 0, b = 0;
    python (a, b) (
        print("hello world") 
        b = a + 1 
        if a >= 0:
            b += 1 
        b *= 2 
    );
    printf("a=%d, b=%d\n", a, b);
    return 0;
}
```

# How to use
Use the `python (args...) ( ...code...)` macro to write Python code directly in your C++ code.

NOTE: xmake toolchain is required. You need a `xmake.lua` like this:
```lua
target("sample")
    set_kind("binary")
    set_languages("c++17")
    add_rules("inline_py")
    add_packages("pybind11")
    add_files("sample.cc")
```
If you use mac, this line might useful `add_rpathdirs("/Library/Developer/CommandLineTools/Library/Frameworks/")`


Then you can run these command lines:
```shell
xmake build sample  # build this sample
xmake run sample  # run this sample
```

# Using C++ variables
To reference C++ variables, let macro capture it, as shown in the example above. The output is
```shell
a=0, b=4
```

# TODO

- Export this package to xmake-repo.
