#include <stdio.h>
#include <stdlib.h>
#include <time.h>

void regenerate_positions(int cursor_pos, long file_size, const char *pos_file) {
    srand(cursor_pos); 
    FILE *file = fopen(pos_file, "w");
    if (!file) {
        perror("[x] Error opening file to write positions");
        return;
    }
    for (int i = 0; i < 240; i++) {
       
        int pos = cursor_pos + (rand() % (file_size - cursor_pos)); 
        fprintf(file, "%d\n", pos); 
    }
    fclose(file); 
    printf("[+] Positions successfully regenerated and saved to %s\n", pos_file);
}

int main(int argc, char *argv[]) {
    if (argc != 3) {
        fprintf(stderr, "Usage: %s <cursor position> <file size>\n", argv[0]);
        return 1;
    }
    int cursor_pos = atoi(argv[1]);
    long file_size = atol(argv[2]);
    const char *pos_file = "regenerated_pos.txt";
    regenerate_positions(cursor_pos, file_size, pos_file);

    return 0;
}
