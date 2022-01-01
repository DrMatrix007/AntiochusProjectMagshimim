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

#define EASY_TYPE_GUESS_COUNT 20
#define MEDIUM_TYPE_GUESS_COUNT 15
#define HARD_TYPE_GUESS_COUNT 10
#define CRAZY_TYPE_GUESS_COUNT randomRange(5, 25)

enum GuessingType
{
    EASY = 1,
    MEDIUM,
    HARD,
    CRAZY
};

int randomRange(int min, int max);

int countDigit(int number, int digit);

int generateCode();

void setRandomSeed();

int countHits(int code, int guess);

int countMiss(int code, int guess);

bool checkIfAllAllowedDigitsRepeatAtLeastOnce(int value);

int getAmountOfGuesses(enum GuessingType type);

bool getDoesShowGuessesLeft(enum GuessingType type);

int main()
{

    printf("you shouldn't run this");
    system("PAUSE");
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
        } while (countDigit(code, randValue));

        code *= DEVIDE_BY_FOR_NEXT_DIGIT;
        code += randValue;
    }
    return code;
}

/*
 set the seed to the time value
 input: none
 output: none
*/
void setRandomSeed()
{
    srand(time(NULL));
}

/*
 find the count of hits
 input: code (int); guess (int)
 output the count of hits (int)
*/
int countHits(int code, int guess)
{
    int count = 0;

    do
    {
        if (code % DEVIDE_BY_FOR_NEXT_DIGIT == guess % DEVIDE_BY_FOR_NEXT_DIGIT)
        {
            count++;
        }
        code /= DEVIDE_BY_FOR_NEXT_DIGIT;
        guess /= DEVIDE_BY_FOR_NEXT_DIGIT;
    } while (guess);
    return count;
}

/*
 find the count of misses
 input: code (int); guess (int)
 output the count of misses (int)
*/
int countMiss(int code, int guess)
{
    int count = 0;
    int devideCounterCode = 0;
    int devideCounterGuess = 0;
    int devidedGuess = 0;
    int currentGuessDigit = 0;
    int currentCodeDigit = 0;

    do
    {
        devidedGuess = code;
        devideCounterGuess = 0;
        currentCodeDigit = guess % DEVIDE_BY_FOR_NEXT_DIGIT;
        do
        {
            currentGuessDigit = devidedGuess % DEVIDE_BY_FOR_NEXT_DIGIT;

            if ((devideCounterCode != devideCounterGuess) && (currentCodeDigit == currentGuessDigit))
            {
                count++;
            }

            devidedGuess /= DEVIDE_BY_FOR_NEXT_DIGIT;
            devideCounterGuess++;
        } while (devidedGuess);
        guess /= DEVIDE_BY_FOR_NEXT_DIGIT;
        devideCounterCode++;

    } while (guess);
    return count;
}

/*
 checks if every ALLOWED digit repeats once, and returning the answer
 input: value (int)
 output: the requested bool (bool)
*/
bool checkIfAllAllowedDigitsRepeatAtLeastOnce(int value)
{
    int i;
    bool flag = true;

    for (i = CODE_MIN_DIGIT; i <= CODE_MAX_DIGIT; i++)
    {
        if (countDigit(value, i) > 1)
        {
            flag = false;
        }
    }
    return flag;
}

// gets the amount of guesses by the type
// input: the type (Guessing type)
// output: the requested amount
int getAmountOfGuesses(enum GuessingType type)
{

    int value = 0;

    switch (type)
    {
        case EASY:
            value = EASY_TYPE_GUESS_COUNT;
            break;
        case MEDIUM:
            value = MEDIUM_TYPE_GUESS_COUNT;
            break;
        case HARD:
            value = HARD_TYPE_GUESS_COUNT;
            break;
        case CRAZY:
            value = CRAZY_TYPE_GUESS_COUNT;
            break;
    }
    return value;
}

// gets the amount of guesses by the type
// input: the type (Guessing type)
// output: the requested amount
bool getDoesShowGuessesLeft(enum GuessingType type)
{
    bool value = false;
    switch (type)
    {
        case CRAZY:
            value = false;
            break;

        default:
            value = true;
            break;
    }
    return value;
}