CC = gcc
CFLAGS = -std=c11 -O2 -Wall -Wextra -Wpedantic
TARGET = gerar_entradas.exe

all: $(TARGET)

$(TARGET): gerar_entradas.c
	$(CC) $(CFLAGS) gerar_entradas.c -o $(TARGET)

run: $(TARGET)
	cd .. && gerador/$(TARGET)

clean:
	$(RM) $(TARGET)
