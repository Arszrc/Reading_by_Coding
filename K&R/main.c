#include <stdio.h>
#include <memory.h>


int main(void)
{
//    int a = -1, b = 4, k;
//    k = !((++a < 0) && !(b-- < 0));
//    printf("%d%d%d\n", k, a, b); //output: 104

//    int i;
//    i=1, ++i, ++i||++i, i;
//    printf("%d", i);  //output: 3

    char s[] = "\\141\141abc\t";
    int i;
    for(i = 0; i < strlen(s); i++)
        printf("%c\n", s[i]);

    return 0;
}
