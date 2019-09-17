#include <stdio.h>

int main(){
    unsigned long int c = 0;
    for(int i=0; i<4500; i++){
        printf("%d\n", i);
        for(int j=0; j<4500; j++){
            for(int k=0; k<4500; k++){
                c++;
            }
        }
    }
    printf("\n%lu\n", c);
    return 0;
}