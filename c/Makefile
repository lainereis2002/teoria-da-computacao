CC = gcc
CFLAGS = -std=c11 -O2 -Wall -Wextra -Wpedantic
TARGET = executar.exe

all: $(TARGET)

$(TARGET): executar.c ordenacao.c ordenacao.h
	$(CC) $(CFLAGS) executar.c ordenacao.c -o $(TARGET)

clean:
	$(RM) $(TARGET)
