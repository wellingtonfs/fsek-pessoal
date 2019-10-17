#include <stdio.h>

char strA[80] = "Te amo";
char strB[80] = "Te amo";
char c = 'a';

int ContaCaracter(char *p)
{
    int cnt=0;
    while(*p!='\0')
    {
        cnt++;
        p++;
    }
    return cnt;
}

int CaractFind(char *p)
{
    int cont = 0;
    while (*p != '\0')
    {
        if (*p == c)
        {
            cont++;
        }
        p++;
    }
    return cont;
}

void Invert(char *p)
{
    int i, tam = 0;

    for (i = 0; *p != '\0'; i++)
    {
        tam++;
        p++;
    }

    printf ("String invertida: ");

    for (i = 0; i <= tam; i++)
    {
        printf ("%c", *p);
        p--;
    }

    printf ("\n");
}

int Comp (char *p, char *q)
{
    int cont = 0;

    if (*p == *q)
    {
        cont++;
    }
    else
    {
        cont = 0;
    }

    return cont;
}

int Vog(char *p)
{
    int cont = 0;
    while(*p != '\0')
    {
         p++;
        if ((*p == 'a') || (*p == 'i') || (*p == 'e') || (*p == 'o') || (*p == 'u'))
        {
            cont++;
        }
    }
    return cont;
}

int Cons(char *p)
{
    int cont = 0, contc = 0;
    while(*p != '\0')
    {
        if ((*p == 'a') || (*p == 'i') || (*p == 'e') || (*p == 'o') || (*p == 'u'))
        {
            cont++;
        }
        else
        {
            contc++;
        }
        p++;
    }
    return contc;
}

void Convert (char *p)
{
    printf ("Conversao dos valores do caracteres: \n");
    while (*p != '\0')
    {
        printf ("%c: %i ", *p, *p);
        p++;
    }
}

void CaixaAlta (char *p)
{
    printf ("\nA string em caixa alta: ");

    while (*p != '\0')
    {
        if ((*p >= 'a') && (*p <= 'z'))
        {
            *p = *p - 32;
            printf ("%c", *p);
        }
        else
        {
            printf ("%c", *p);
        }
        
        p++;
    }
    printf ("\n");
}

void CaixaBaixa (char *p)
{
    printf ("A string em caixa baixa: ");

    while (*p != '\0')
    {
        if ((*p >= 'A') && (*p <= 'Z'))
        {
            *p = *p + 32;
            printf ("%c", *p);
        }
        else
        {
            printf ("%c", *p);
        }
        
        p++;
    }
    printf ("\n");
}

int main()
{
printf("Numero de caracteres: %d\n",ContaCaracter(strA));
printf ("Numero de repeticao: %d\n", CaractFind(strA));
Invert(strA);
printf ("Comparativo das strings: %d\n", Comp(strA, strB));
printf ("Numero de vogais: %d\n", Vog(strA));
printf ("Numero de consoantes: %d\n", Cons(strA));
Convert(strA);
CaixaAlta(strA);
CaixaBaixa(strA);
}