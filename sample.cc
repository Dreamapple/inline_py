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

