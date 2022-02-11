#include <stdio.h>
#include <stdlib.h>
#include <cs50.h>
#include <stdint.h>

int main(int argc, char *argv[])
{
    if (argc != 2)
    {
        printf("Usage: ./recover <forensic_file>\n");
        return 1;
    }
    
    const int BLOCK_SIZE = 512;
    typedef uint8_t BYTE;
    BYTE jpeg[BLOCK_SIZE];

    FILE *file = fopen(argv[1], "r");
    int i = 0;
    char filename[8];
    FILE *img;

    while (fread(jpeg, 1, BLOCK_SIZE, file) == 512)
    {
        if (jpeg[0] == 0xff & jpeg[1] == 0xd8 & jpeg[2] == 0xff & (jpeg[3] & 0xf0) == 0xe0)     // IF BLOCK BELONGS TO JPEG
        {
            if (i == 0)                     // IF ITS THE FIRST JPEG YOU FOUND
            {
                sprintf(filename, "%03i.jpg", i);
                img = fopen(filename, "w");
                fwrite(jpeg, 1, BLOCK_SIZE, img);
                i++;
            }
            else if (i > 0)
            {
                fclose(img);
                sprintf(filename, "%03i.jpg", i);
                img = fopen(filename, "w");
                fwrite(jpeg, 1, BLOCK_SIZE, img);
                i++;
            }
        }
        else                                // IF BLOCK DOESNT BEGIN WITH JPEG
        {
            if (i > 0)                      // IF YOU HAVE ALREADY FOUND JPEG
            {
                fwrite(jpeg, 1, BLOCK_SIZE, img);               // KEEP WRITING
            }
        }
    }
    fclose(img);
    fclose(file);
}