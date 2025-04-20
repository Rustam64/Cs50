// Modifies the volume of an audio file

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

// Number of bytes in .wav header
const int HEADER_SIZE = 44;

int main(int argc, char *argv[])
{
    // Check command-line arguments
    if (argc != 4)
    {
        printf("Usage: ./volume input.wav output.wav factor\n");
        return 1;
    }

    // Open files and determine scaling factor
    FILE *input = fopen(argv[1], "r");
    if (input == NULL)
    {
        printf("Could not open file.\n");
        return 1;
    }

    FILE *output = fopen(argv[2], "w");
    if (output == NULL)
    {
        printf("Could not open file.\n");
        fclose(input);
        return 1;
    }

    float factor = atof(argv[3]);

    // TODO: Copy header from input file to output file
    uint8_t *buffer = malloc(sizeof(uint8_t) * HEADER_SIZE);
    if (buffer == NULL)
    {
        printf("Memory allocation failed.\n");
        fclose(input);
        fclose(output);
        return 1;
    }
    if (fread(buffer, sizeof(uint8_t), HEADER_SIZE, input) != HEADER_SIZE)
    {
        printf("Failed to read wav header.\n");
        free(buffer);
        fclose(input);
        fclose(output);
        return 1;
    }
    if (fwrite(buffer, sizeof(uint8_t), HEADER_SIZE, output) != HEADER_SIZE)
    {
        printf("Failed to write wav header.\n");
        free(buffer);
        fclose(input);
        fclose(output);
        return 1;
    }
    free(buffer);
    fseek(input, HEADER_SIZE, SEEK_SET);

    // TODO: Read samples from input file and write updated data to output file
    short ch;
    while (fread(&ch, sizeof(short), 1, input) == 1)
    {
        int temp = ch;
        temp *= factor;
        ch = (short) temp;
        if (fwrite(&ch, sizeof(short), 1, output) != 1)
        {
            printf("Failed to write audio sample.\n");
            fclose(input);
            fclose(output);
            return 1;
        }
    }

    // Close files
    fclose(input);
    fclose(output);
}
