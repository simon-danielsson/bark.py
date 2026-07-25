#include <stdio.h>

int main(int argc, char **argv) {
    if (argc < 2) {
        printf("No arguments were found");
        return 1;
    }
    printf("Hello world, again!\n");
    return 0;
}
