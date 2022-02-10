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
        int i = 0;
        if (buffer[0] == 0xff & buffer[1] == 0xd8 & buffer[2] == 0xff & (buffer[3] && 0xf0) == 0xe0)
        {
            
        }
    }

}