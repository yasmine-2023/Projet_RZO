#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <arpa/inet.h>
#include <sys/socket.h>
#include "reseaux.h"

int main() {
    pid_t pid = fork();

    if (pid == 0) {
        // Processus enfant: envoi après un délai pour s'assurer que le serveur est prêt
        sleep(1);
        envoi("Hello from client!"); // Assurez-vous que c'est le nouveau message ici
    } else if (pid > 0) {
        // Processus parent: réception
        
        char *receivedMessage = reception();

        if(receivedMessage) {
            printf("jlai recup: %s\n", receivedMessage); // Utilisez \n pour forcer le vidage du tampon
            
            
        } else {
            printf("No message received or allocation failed.\n");
        }
        
    } else {
        perror("fork failed");
        exit(EXIT_FAILURE);
    }
    return 0;
}
