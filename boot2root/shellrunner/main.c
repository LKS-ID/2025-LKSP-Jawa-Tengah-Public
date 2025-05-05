#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <sys/mman.h>
#include <unistd.h>

#define CODE_ADDR 0x80000000
#define PAGE_SIZE 0x1000
#define MAX_CODE_SIZE 0x1000

int hex_char_to_int(char c) {
    if ('0' <= c && c <= '9') return c - '0';
    if ('a' <= c && c <= 'f') return c - 'a' + 10;
    if ('A' <= c && c <= 'F') return c - 'A' + 10;
    return -1;
}

int hex_to_bytes(const char *hex, uint8_t *out, size_t max_len) {
    size_t len = strlen(hex);
    if (len % 2 != 0) {
        fprintf(stderr, "[!] Hex string must have even length.\n");
        return -1;
    }
    size_t i;
    for (i = 0; i < len / 2 && i < max_len; i++) {
        int hi = hex_char_to_int(hex[2 * i]);
        int lo = hex_char_to_int(hex[2 * i + 1]);
        if (hi < 0 || lo < 0) {
            fprintf(stderr, "[!] Invalid hex character.\n");
            return -1;
        }
        out[i] = (hi << 4) | lo;
    }
    return i;
}

int main(int argc, char *argv[]) {
    if (argc < 2) {
        fprintf(stderr, "Usage: %s <hex_shellcode>\n", argv[0]);
        return 1;
    }

    uint8_t shellcode[MAX_CODE_SIZE];
    int code_size = hex_to_bytes(argv[1], shellcode, MAX_CODE_SIZE);
    if (code_size <= 0) {
        return 1;
    }

    void *addr = mmap((void *)CODE_ADDR, PAGE_SIZE,
                      PROT_READ | PROT_WRITE | PROT_EXEC,
                      MAP_PRIVATE | MAP_ANONYMOUS | MAP_FIXED, -1, 0);
    if (addr == MAP_FAILED) {
        perror("mmap");
        return 1;
    }

    memcpy(addr, shellcode, code_size);

    void (*func)() = (void (*)())addr;
    func();

    return 0;
}
