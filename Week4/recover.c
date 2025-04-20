#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
const int READ = 512;

bool check_header(unsigned char arr[]);

int main(int argc, char *argv[])
{
    if (argc != 2)
    {
        printf("Usage: ./recover name of a forensic image.");
        return 1;
    }
    FILE *inptr = fopen(argv[1], "r");
    if (inptr == NULL)
    {
        printf("Could not open file.\n");
        return 1;
    }
    unsigned char *buffer = malloc(sizeof(unsigned char) * READ);
    if (buffer == NULL)
    {
        printf("Memory allocation failed.\n");
        fclose(inptr);
        return 1;
    }
    FILE *outptr = NULL;
    int images = 0;
    char filename[8];

    while (fread(buffer, sizeof(unsigned char), READ, inptr) == READ)
    {
        if (check_header(buffer))
        {
            if (outptr != NULL)
            {
                fclose(outptr);
            }
            sprintf(filename, "%03i.jpg", images);
            images += 1;

            outptr = fopen(filename, "w");
            if (outptr == NULL)
            {
                printf("Could not open file.\n");
                free(buffer);
                fclose(outptr);
                return 1;
            }
        }
        if (outptr != NULL)
        {
            fwrite(buffer, sizeof(unsigned char), READ, outptr);
        }
    }
    free(buffer);
    fclose(inptr);
    if (outptr != NULL)
    {
        fclose(outptr);
    }
    return 0;
}

bool check_header(unsigned char arr[])
{
    return (arr[0] == 0xff && arr[1] == 0xd8 && arr[2] == 0xff &&
            (arr[3] >= 0xe0 && arr[3] <= 0xef));
}
