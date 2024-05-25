#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <arpa/inet.h>
#include <sys/socket.h>
#include "reseaux.h" 
#include <errno.h> 

#define PORT 37020

char *reception() 
{
    int sockfd;
    struct sockaddr_in recvAddr;
    char buffer[1024];
    struct timeval tv;

    // Création de la socket UDP
    if ((sockfd = socket(AF_INET, SOCK_DGRAM, 0)) < 0) {
        perror("socket creation failed");
        exit(EXIT_FAILURE);
    }

    memset(&recvAddr, 0, sizeof(recvAddr));
    recvAddr.sin_family = AF_INET;
    recvAddr.sin_addr.s_addr = htonl(INADDR_ANY);
    recvAddr.sin_port = htons(PORT);

    int yes = 1;
    if (setsockopt(sockfd, SOL_SOCKET, SO_REUSEADDR, &yes, sizeof(yes)) < 0) 
    {
        perror("setsockopt SO_REUSEADDR failed");
        close(sockfd);
        exit(EXIT_FAILURE);
    }

    // Définir un timeout de 3 secondes sur la socket pour recvfrom
    tv.tv_sec = 3;  // Timeout en secondes
    tv.tv_usec = 0;  // Timeout en microsecondes
    if (setsockopt(sockfd, SOL_SOCKET, SO_RCVTIMEO, (const char*)&tv, sizeof tv) < 0) {
        perror("setsockopt (SO_RCVTIMEO) failed");
        close(sockfd);
        exit(EXIT_FAILURE);
    }

    // Liaison de la socket
    if (bind(sockfd, (struct sockaddr *) &recvAddr, sizeof(recvAddr)) < 0) {
        perror("bind failed");
        close(sockfd);
        exit(EXIT_FAILURE);
    }

    printf("Waiting to receive broadcast...\n");
    socklen_t len = sizeof(recvAddr);

    // Réception du message
    int n = recvfrom(sockfd, buffer, sizeof(buffer) - 1, 0, (struct sockaddr *) &recvAddr, &len);
    if (n < 0) {
        if (errno == EWOULDBLOCK) {
            printf("recvfrom() timed out.\n");
            close(sockfd);
            return NULL; 
        } else {
            perror("recvfrom() failed");
            close(sockfd);
            exit(EXIT_FAILURE);
        }
    }

    buffer[n] = '\0'; 
    printf("Received message: %s\n", buffer);

    close(sockfd);

   
    char* result = strdup(buffer);
    return result; 
}



void ferme_socket() 
{
    char command[256];

    // Utilisation de lsof pour trouver le PID écoutant sur le port et kill pour terminer le processus
    snprintf(command, sizeof(command), "kill -9 $(lsof -t -i:%d -sTCP:LISTEN)", PORT);

    // Exécution de la commande
    int result = system(command);
    
    // Vérifiez si la commande a réussi
    if (result == 0) {
        printf("Processus écoutant sur le port %d terminé.\n", PORT);
    } else {
        fprintf(stderr, "Échec de l'exécution de la commande pour fermer le socket.\n");
    }
}



