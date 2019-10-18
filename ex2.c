#include <stdio.h>

int main()
{
    int *pi, *pj;
    int i = 1, j = 3, aux;
    pi = &i;
    pj = &j;

    printf ("Valor antes de i = %d e de j = %d\n", *pi, *pj);
  
    aux = *pi;   
    *pi = *pj;   
    *pj = aux;  
    printf("Valor depois de i = %d e de j = %d\n", *pi, *pj);
}