#pragma once

#define ARG_N(                                     \
_1,  _2,  _3,  _4,  _5,  _6,  _7,  _8,  _9,  _10,  \
_11, _12, _13, _14, _15, _16, _17, _18, _19, _20,  \
_21, _22, _23, _24, _25, _26, _27, _28, _29, _30,  \
_31, _32, _33, _34, _35, _36, _37, _38, _39, _40,  \
_41, _42, _43, _44, _45, _46, _47, _48, _49, _50,  \
_51, _52, _53, _54, _55, _56, _57, _58, _59, _60,  \
_61, _62, _63,   N, ...)                           \
N

#define RSEQ_N                           \
63, 62, 61, 60,                          \
59, 58, 57, 56, 55, 54, 53, 52, 51, 50,  \
49, 48, 47, 46, 45, 44, 43, 42, 41, 40,  \
39, 38, 37, 36, 35, 34, 33, 32, 31, 30,  \
29, 28, 27, 26, 25, 24, 23, 22, 21, 20,  \
19, 18, 17, 16, 15, 14, 13, 12, 11, 10,  \
 9,  8,  7,  6,  5,  4,  3,  2,  1,  0

#define NARG_(...) ARG_N(__VA_ARGS__)
#define NARG(...) NARG_(__VA_ARGS__, RSEQ_N)


#define JOIN_IMPL1( x ) x
#define JOIN_IMPL2( x, y ) x##_##y
#define JOIN_IMPL3( x, y, z ) x##_##y##_##z
#define JOIN_IMPL4( x, y, z, a ) x##_##y##_##z##_##a

#define MACRO_CONCAT_IMPL(x, y) x##y
#define MACRO_CONCAT(x, y) MACRO_CONCAT_IMPL(x, y)

#define MACRO_JOINT(...) MACRO_CONCAT(JOIN_IMPL, NARG(__VA_ARGS__))( __VA_ARGS__ )


#ifndef compile_time_inline
#include <stdio.h>
#define inner(x) printf(#x "\n");
#define python(...) inner
#else
#include <pybind11/embed.h>
namespace py = pybind11;

py::scoped_interpreter& pyactive() {
    static py::scoped_interpreter guard{};
    return guard;
}

#include "inline_py_gen.h"
#define python(...) MACRO_JOINT(__PyCode, __VA_ARGS__, __LINE__)
#endif
