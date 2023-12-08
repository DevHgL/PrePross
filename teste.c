#include <stdio.h>
#include "stdlib.h"
#define cst 65321
#define SOMA(a, b) ((a) + (b))


int main()
{





    // Lorem Ips incorrectly
    // Lorem ipsum dolor sit amet, consect

    /*
        Lorem ipsum dolor sit amet, consectetur adipiscing el aspect, sed do eiusmod tempor
        let cod Sign et dolore magna aliqu fugiat nulla pariatur
        let org
    */





    int x = 100; // alô
    float y; 
    char z = 'a'; 
    unsigned long long int B = 100;
    char C[100] = {"AAAAA AAAAA AAAA"};
    
    y = (int) z + x + B;
    printf("%d\n", SOMA(10, 20));
    printf("%f\n", y);
    if(x > cst)
    {
        printf("HAHAHAH   AHAHA   HA\n");
    }

    for(int i = 0; i < 20; i++)
    {
        printf("%c", C[i]);
    }

    
    return 1;
}
