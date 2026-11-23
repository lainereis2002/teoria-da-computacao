CC = gcc
CFLAGS = -std=c11 -O2 -Wall -Wextra -Wpedantic
TARGET = medir_c.exe

all: $(TARGET)

$(TARGET): medir_c.c ../c/ordenacao.c ../c/ordenacao.h
	$(CC) $(CFLAGS) medir_c.c ../c/ordenacao.c -o $(TARGET)

clean:
	$(RM) $(TARGET)
