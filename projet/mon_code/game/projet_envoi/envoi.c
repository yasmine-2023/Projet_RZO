#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <arpa/inet.h>
#include <sys/socket.h>
#include "reseaux.h"

#define PORT 37020

void envoi(const char *message) 
{
    int sockfd;
    struct sockaddr_in broadcastAddr;
    int broadcastPermission = 1;  // Activer la diffusion en broadcast

    // Création de la socket UDP
    if ((sockfd = socket(AF_INET, SOCK_DGRAM, 0)) < 0) {
        perror("socket creation failed");
        exit(EXIT_FAILURE);
    }

    // Configuration de la socket pour autoriser les envois en broadcast
    if (setsockopt(sockfd, SOL_SOCKET, SO_BROADCAST, &broadcastPermission, sizeof(broadcastPermission)) < 0) {
        perror("setsockopt() for SO_BROADCAST failed");
        close(sockfd);
        exit(EXIT_FAILURE);
    }

    memset(&broadcastAddr, 0, sizeof(broadcastAddr));
    
    // Configuration de l'adresse de broadcast
    broadcastAddr.sin_family = AF_INET;
    broadcastAddr.sin_port = htons(PORT);
    broadcastAddr.sin_addr.s_addr = htonl(INADDR_BROADCAST);
    
    // Envoi du message en broadcast
    if (sendto(sockfd, message, strlen(message), 0, (struct sockaddr *) &broadcastAddr, sizeof(broadcastAddr)) < 0) {
        perror("sendto() failed");
        close(sockfd);
        exit(EXIT_FAILURE);
    }

    printf("Message sent on broadcast address.\n");
    
    close(sockfd);
}