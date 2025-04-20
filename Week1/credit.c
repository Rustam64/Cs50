#include <cs50.h>
#include <stdio.h>
#include <string.h>

int sum = 0;
int counter = 0;

bool check_digit();
void count(int arr[], int length);
string iterate(long number);

int main()
{
    long number = get_long("Number: ");
    while (number <= 0)
    {
        printf("INVALID\n");
        number = get_long("Number: ");
    }

    int arr[16] = {0};
    int arrind = 0;
    string Answer = iterate(number);

    if (check_digit())
    {
        printf("%s\n", Answer);
    }
    else
    {
        printf("INVALID\n");
    }
}

bool check_digit()
{
    return sum % 10 == 0;
}

void count(int arr[], int length)
{
    sum = 0;
    counter = 0;
    for (int i = 0; i <= length; i++)
    {
        if (counter % 2 == 0)
        {
            sum += arr[i];
            printf("%d \n", sum);
        }
        else
        {
            int doubled = arr[i] * 2;
            if (doubled >= 10)
            {
                sum += doubled % 10;
                sum += doubled / 10;
                printf("%d \n", sum);
            }
            else
            {
                sum += doubled;
                printf("%d \n", sum);
            }
        }
        counter++;
    }
}

string iterate(long number)
{
    int arr[16];
    int arrind = 0;
    while (number > 0)
    {
        arr[arrind] = number % 10;
        arrind++;
        number /= 10;
    }

    count(arr, arrind);
    if ((arrind == 13 || arrind == 16) && arr[arrind - 1] == 4)
    {
        return "VISA";
    }
    else if (arrind == 15 && arr[arrind - 1] == 3 && (arr[arrind - 2] == 4 || arr[arrind - 2] == 7))
    {
        return "AMEX";
    }
    else if (arrind == 16 && arr[arrind - 1] == 5 && (arr[arrind - 2] >= 1 && arr[arrind - 2] <= 5))
    {
        return "MASTERCARD";
    }
    else
    {
        return "INVALID";
    }
}
