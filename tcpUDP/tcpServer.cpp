#include<Winsock2.h>
#include<cstdio>
#pragma comment(lib,"ws2_32.lib")
#define SERVER_PORT 8888
// windows cmake添加 link_libraries(ws2_32)
int main()
{
    WSADATA wsaData;
    SOCKET sockServer;
    SOCKADDR_IN addrServer;
    SOCKET sockClient;
    SOCKADDR_IN addrClient;

    WSAStartup(MAKEWORD(2, 2), &wsaData);
    //创建Socket
    sockServer = socket(AF_INET, SOCK_STREAM, 0);
    //准备通信地址
    addrServer.sin_addr.S_un.S_addr = htonl(INADDR_ANY);
    addrServer.sin_family = AF_INET;
    addrServer.sin_port = htons(SERVER_PORT);
    //绑定
    bind(sockServer, (SOCKADDR*)&addrServer, sizeof(SOCKADDR));
    //监听
    listen(sockServer, 5);
    printf("服务器已启动.......");
    int len = sizeof(SOCKADDR);
    char sendBuf[100] = "buf";
    char recvBuf[100];
    //监听连接
    sockClient = accept(sockServer, (SOCKADDR*)&addrClient, &len);
    printf("client connect\n");
    recv(sockClient, recvBuf, 100, 0);
    printf("%s\n", recvBuf);
    send(sockClient,sendBuf,100,0);
//   ################################
    closesocket(sockClient);
    WSACleanup();
}

