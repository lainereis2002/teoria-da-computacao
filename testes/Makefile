CC = gcc
CFLAGS = -std=c11 -O2 -Wall -Wextra -Wpedantic
TARGET = test_ordenacao.exe

all: $(TARGET)

$(TARGET): test_ordenacao.c ../c/ordenacao.c ../c/ordenacao.h
	$(CC) $(CFLAGS) test_ordenacao.c ../c/ordenacao.c -o $(TARGET)

run: $(TARGET)
	./$(TARGET)

clean:
	$(RM) $(TARGET)
