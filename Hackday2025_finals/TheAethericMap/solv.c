/* 
	Tool developed during CTF  
*/
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void extract_LSB(const char *filename, const char *positions_file) {
	FILE *file = fopen(filename, "rb");
	if (!file) {
		perror("[x] Error opening file");
		return;
	}
	
	FILE *pos_file = fopen(positions_file, "r");
	if (!pos_file) {
		perror("[x] Error opening positions file");
		fclose(file);
		return;
	}
	
	char extracted_message[1024] = {0};
	int flag_index = 0;
	int pos;
	unsigned char byte;
	
	while (fscanf(pos_file, "%d", &pos) != EOF) {
		if (fseek(file, pos, SEEK_SET) != 0) {
			perror("[x] Error seeking file");
			break;
		}
		if (fread(&byte, 1, 1, file) != 1) {
			perror("[x] Error reading file");
			break;
		}
		extracted_message[flag_index / 8] |= ((byte & 1) << (7 - (flag_index % 8))); 
		flag_index++;
	}
	
	fclose(file);
	fclose(pos_file);
	
	extracted_message[flag_index / 8] = '\0'; 
	printf("\n[+] Extracted message: %s\n", extracted_message);
}

int main(int argc, char *argv[]) {
	if (argc != 3) {
		fprintf(stderr, "Usage: %s <file> <positions file>\n", argv[0]);
		return 1;
	}
	
	extract_LSB(argv[1], argv[2]);
	
	return 0;
}
