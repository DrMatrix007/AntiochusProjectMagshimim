#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#define DIGIT_BOUNDRY_MIN 0
#define DIGIT_BOUNDRY_MAX 9
#define DEVIDE_BY_FOR_NEXT_DIGIT 10
#define CODE_LENGTH 4
#define CODE_MIN_DIGIT 1
#define CODE_MAX_DIGIT 6




int randomRange(int min, int max);

int countDigit(int number, int digit);

int generateCode();

int main()
{
    srand(time(NULL));

    for (size_t i = 0; i < 10; i++)
    {
        printf("%d\n",generateCode());
    }
    
    printf("nice\n");
    return 0;
}
/*
 return a random int between the requested range
 input: min (int); max(int) - they are the range
 output: int between the requested range
*/
int randomRange(int min, int max)
{
    return rand() % (max - min + 1) + min;
}

/*
 returns the count of the digit in the number
 if the digit is a number greater than 9 or smaller than 0, it will return 0.
 input: number (int); digit (int) 
*/
int countDigit(int number, int digit)
{
    int count = 0;
    if (digit < DIGIT_BOUNDRY_MIN || digit > DIGIT_BOUNDRY_MAX)
    {
        return count;
    }

    do
    {
        if (number % DEVIDE_BY_FOR_NEXT_DIGIT == digit)
        {
            count++;
        }
        number /= DEVIDE_BY_FOR_NEXT_DIGIT;
    } while (number);
    return count;
}

/*
 generate the code by the requirements (digits between 1-6 without repeats)
 input:none
 output: random code
*/
int generateCode()
{
    int i = 0;
    int code = 0;
    int randValue = 0;

    for (int i = 0; i < CODE_LENGTH; i++)
    {
        do 
        {
            randValue = randomRange(CODE_MIN_DIGIT, CODE_MAX_DIGIT);
        } while(countDigit(code, randValue));

        code*=DEVIDE_BY_FOR_NEXT_DIGIT;
        code+=randValue;
    }
    return code;
}