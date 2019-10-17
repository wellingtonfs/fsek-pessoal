#include <stdio.h>

int main()
{
    int *m, count;
    
    count = 6;
    m = &count;

    printf ("\%d\n", count);
    printf ("\%p\n", m);
    printf ("\%p\n", &count);
}

/*O código mostra no primeiro print o valor da variavel count 
nos outros dois print ele mostra o endereço de memória de formas
distintas, um atribuindo o endereço a uma variável, e no 
outro mostrando diretamente o endereço de memória*/