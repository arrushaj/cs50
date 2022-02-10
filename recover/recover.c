#include <stdio.h>
#include <stdlib.h>

int main(int argc, char *argv[])
{
    const int BLOCK_SIZE = 512;
    typedef uint8_t BYTE;
    BYTE jpeg[BLOCK_SIZE];

    FILE *file = fopen(argv[1], "r");

    while (fread(jpeg, BYTE, BLOCK_SIZE, file) == 512)
    {
        
    }

}