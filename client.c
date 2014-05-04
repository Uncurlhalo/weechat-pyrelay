#include <stdio.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <netdb.h>
#include <stdlib.h>
#include <string.h>
#include <arpa/inet.h>

#include "decode.c"

void error(char *msg)
{
    perror(msg);
    exit(0);
}

int socket_init(int argc, char *argv[])
{
    int sockfd;
    struct sockaddr_in serv_addr;
    struct hostent *server;
    
    if (argc < 3)
    {
        fprintf(stderr, "usage %s hostname port\n", argv[0]);
        exit(-1);
    }
    
    int portno = atoi(argv[2]);
    sockfd = socket(PF_INET, SOCK_STREAM, IPPROTO_TCP);
    
    if (sockfd < 0)
        error("error opening socket");
        
    server = gethostbyname(argv[1]);
    if (server == NULL)
    {
        fprintf(stderr, "ERROR, no such host\n");
        exit(-1);
    }
    
    bzero((char*) &serv_addr, sizeof(serv_addr));
    serv_addr.sin_family = AF_INET;
    serv_addr.sin_addr.s_addr = inet_addr(argv[1]);
    serv_addr.sin_port = htons(portno);
    
    if (connect(sockfd, (struct sockaddr*)&serv_addr, sizeof(serv_addr)) < 0)
        error("ERROR connecting");
        
    return sockfd;
}

int main(int argc, char *argv[])
{
    char buffer[256];
    int sockfd = socket_init(argc, argv);
    
    char* init_str = "init password=reeelay\n";
    
    if (send(sockfd, init_str, strlen(init_str), 0) != strlen(init_str))
        error("okjadiofj");
        
    while (1)
    {
        printf("Enter message: ");
        bzero(buffer, 256);
        
        fgets(buffer, 255, stdin);
        int n = send(sockfd, buffer, strlen(buffer), 0);
        if (n < 0)
            error("werfj");
        bzero(buffer, 256);
        n=recv(sockfd, buffer, 255, 0);
        if (n < 0)
            error("io;jawdfk");
        printf("%s\n", decode(buffer));
    }
}
