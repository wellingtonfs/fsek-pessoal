#include <stdio.h>

int main()
{
    float a = 5, b = 7;
    float *p, *q;

    p = &a;
    q = &b;

    float A = *q - *p;
    float B = *q * *p;
    float C = 2**q**p*3;
    float D = (*q**q) - (*p**p);

    printf ("Alternativa a: %f\n", A);
    printf ("Alternativa b: %f\n", B);
    printf ("Alternativa c: %f\n", C);
    printf ("Alternativa d: %f\n", D);
}