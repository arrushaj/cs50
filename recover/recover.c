#include <stdio.h>
#include <stdlib.h>
#include <cs50.h>
#include <stdint.h>

int main(int argc, char *argv[])
{
    const int BLOCK_SIZE = 512;
    typedef uint8_t BYTE;
    BYTE jpeg[BLOCK_SIZE];

    FILE *file = fopen(argv[1], "r");
    int i = 1;
    string filename = NULL;

    while (fread(jpeg, 1, BLOCK_SIZE, file) == 512)
    {
        if (jpeg[0] == 0xff & jpeg[1] == 0xd8 & jpeg[2] == 0xff & (jpeg[3] & 0xf0) == 0xe0)
        {
            if (i == 1)
            {
                sprintf(filename, "%03i.jpg", i);
                FILE *img = fopen(filename, "w");
                fwrite(jpeg, 1, BLOCK_SIZE, img);
                i++;
            }
            else if (i > 1)
            {
                fclose(img);
            }
        }
    }
}