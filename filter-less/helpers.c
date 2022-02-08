#include "helpers.h"
#include <math.h>

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    float average;
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            average = (image[i][j].rgbtRed + image[i][j].rgbtGreen + image[i][j].rgbtBlue) / 3.0;
            image[i][j].rgbtRed = round(average);
            image[i][j].rgbtGreen = round(average);
            image[i][j].rgbtBlue = round(average);
        }
    }
    return;
}

// Convert image to sepia
void sepia(int height, int width, RGBTRIPLE image[height][width])
{
    float sepiaRed;
    float sepiaGreen;
    float sepiaBlue;
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            sepiaRed = .393 * image[i][j].rgbtRed + .769 * image[i][j].rgbtGreen + .189 * image[i][j].rgbtBlue;
            sepiaGreen = .349 * image[i][j].rgbtRed + .686 * image[i][j].rgbtGreen + .168 * image[i][j].rgbtBlue;
            sepiaBlue = .272 * image[i][j].rgbtRed + .534 * image[i][j].rgbtGreen + .131 * image[i][j].rgbtBlue;
            if (round(sepiaRed) > 255)
            {
                sepiaRed = 255;
            }
            if (round(sepiaGreen) > 255)
            {
                sepiaGreen = 255;
            }
            if (round(sepiaBlue) > 255)
            {
                sepiaBlue = 255;
            }
            image[i][j].rgbtRed = round(sepiaRed);
            image[i][j].rgbtGreen = round(sepiaGreen);
            image[i][j].rgbtBlue = round(sepiaBlue);
        }
    }
    return;
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    int tmp1;
    int tmp2;
    int tmp3;

    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width / 2; j++)
        {
            tmp1 = image[i][j].rgbtRed;        // SWAPPING
            image[i][j].rgbtRed = image[i][width - 1 - j].rgbtRed;
            image[i][width - 1 - j].rgbtRed = tmp1;
            tmp2 = image[i][j].rgbtGreen;       // SWAPPING
            image[i][j].rgbtGreen = image[i][width - 1 - j].rgbtGreen;
            image[i][width - 1 - j].rgbtGreen = tmp2;
            tmp3 = image[i][j].rgbtBlue;        // SWAPPING
            image[i][j].rgbtBlue = image[i][width - 1 - j].rgbtBlue;
            image[i][width - 1 - j].rgbtBlue = tmp3;
        }
    }
    return;
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
float averageRed;
float averageGreen;
float averageBlue;
RGBTRIPLE copy[height][width];

    for (int k = 0; k < height; k++)
    {
        for (int h = 0; h < width; h++)
        {
            copy[k][h] = image[k][h];    // Copy image pixels to seperate array so they don't mess things up when we blur each pixel individually
        }
    }

    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            if (i == 0 && j == 0)                 // If located in the top left corner of image
            {
                averageRed = (copy[i][j].rgbtRed + copy[i + 1][j].rgbtRed + copy[i][j + 1].rgbtRed + copy[i + 1][j + 1].rgbtRed) / 4.0;
                averageGreen = (copy[i][j].rgbtGreen + copy[i + 1][j].rgbtGreen + copy[i][j + 1].rgbtGreen + copy[i + 1][j + 1].rgbtGreen) / 4.0;
                averageBlue = (copy[i][j].rgbtBlue + copy[i + 1][j].rgbtBlue + copy[i][j + 1].rgbtBlue + copy[i + 1][j + 1].rgbtBlue) / 4.0;
                image[i][j].rgbtRed = round(averageRed);
                image[i][j].rgbtGreen = round(averageGreen);
                image[i][j].rgbtBlue = round(averageBlue);
            }
            if (i == 0 && j == width - 1)
            {
                averageRed = (copy[i][width - 1].rgbtRed + copy[i + 1][width - 1].rgbtRed + copy[i][width - 2].rgbtRed + copy[i + 1][width - 2].rgbtRed) / 4.0;
                averageGreen = (copy[i][width - 1].rgbtGreen + copy[i + 1][width - 1].rgbtGreen + copy[i][width - 2].rgbtGreen + copy[i + 1][width - 2].rgbtGreen) / 4.0;
                averageBlue = (copy[i][width - 1].rgbtBlue + copy[i + 1][width - 1].rgbtBlue + copy[i][width - 2].rgbtBlue + copy[i + 1][width - 2].rgbtBlue) / 4.0;
                image[i][j].rgbtRed = round(averageRed);
                image[i][j].rgbtGreen = round(averageGreen);
                image[i][j].rgbtBlue = round(averageBlue);
            }
            if (i == height - 1 && j == 0)
            {
                averageRed = (copy[height - 1][j].rgbtRed + copy[i + 1][j].rgbtRed + copy[i][j + 1].rgbtRed + copy[i + 1][j + 1].rgbtRed) / 4.0;
                averageGreen = (copy[i][j].rgbtGreen + copy[i + 1][j].rgbtGreen + copy[i][j + 1].rgbtGreen + copy[i + 1][j + 1].rgbtGreen) / 4.0;
                averageBlue = (copy[i][j].rgbtBlue + copy[i + 1][j].rgbtBlue + copy[i][j + 1].rgbtBlue + copy[i + 1][j + 1].rgbtBlue) / 4.0;
            }
        }
    }
    return;
}
