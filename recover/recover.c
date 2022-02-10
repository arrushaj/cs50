#include <stdio.h>
#include <stdlib.h>
#include <cs50.h>

int main(int argc, char *argv[])
{
    const int BLOCK_SIZE = 512;
    typedef uint8_t BYTE;
    BYTE jpeg[BLOCK_SIZE];

    FILE *file = fopen(argv[1], "r");
    int i = 1;

    while (fread(jpeg, BYTE, BLOCK_SIZE, file) == 512)
    {
        if (buffer[0] == 0xff & buffer[1] == 0xd8 & buffer[2] == 0xff & (buffer[3] && 0xf0) == 0xe0)
        {
            string filename;
            sprintf(filename, "%03i.jpg", i);
            i++;
            FILE *img = fopen(filename, "w");
            
        }
    }

}