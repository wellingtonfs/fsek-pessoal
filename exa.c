#include <stdio.h>

int ContCarct(char*);

int ContCarct(char* ppal) //Ponteiro para palavra
{
    int cta;
    while(*ppal != '\0')
    {
        cta = cta + 1;
        ppal = ppal + 1;
    }
    return cta;
}

int Inverte(char* ppal)
{
    char invertida[50];
    int tam, i;

    tam = ContCarct(ppal);

    for (i = 0; i <= tam; i++)
    {
        invertida[i] = * (ppal+tam-i-1);
    }
}

int main()
{
    char palavra[50];
    int n;

    printf("Digite uma palavra: ");
    scanf("%s", palavra);
    getchar();

    n = ContCarct(palavra);

    printf ("Numero de caracteres: %d", n);
}