#include <stdio.h>

int main()
{
    int *p;
    float *q;
    int a = 60;
    float b = 100;

    p = &a;

    printf ("Endereço de a: %p\n", p);
    printf ("Valor de a: %d\n", *p);

    q = &b;

    printf ("Endereço de b: %p\n", q);
    printf ("Valor de b: %f\n", *q);
}