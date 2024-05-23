CC = gcc
CFLAGS = -g -W -Wall -fPIC
LDFLAGS = -shared
OBJ = main.o envoi.o reception.o
LIBRARY = libprojetReseau.so
EXECUTABLE = projetReseau

# Cible par défaut
all: $(LIBRARY) $(EXECUTABLE)

# Crée une bibliothèque partagée
$(LIBRARY): envoi.o reception.o
		$(CC) envoi.o reception.o $(LDFLAGS) -o $(LIBRARY)

# Crée un exécutable
$(EXECUTABLE): main.o
		$(CC) main.o -o $(EXECUTABLE) -L. -lprojetReseau

main.o: main.c reseaux.h
		$(CC) $(CFLAGS) -c main.c

envoi.o: envoi.c reseaux.h
		$(CC) $(CFLAGS) -c envoi.c

reception.o: reception.c reseaux.h
		$(CC) $(CFLAGS) -c reception.c

clean:
		rm -f $(OBJ) $(LIBRARY) $(EXECUTABLE)
