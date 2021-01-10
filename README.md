# Отчет  
### Инструкция по по сборке/установке и использованию
1. Скомпилировать все файлы .java в папках *DNSClient/src* *TFTPServer/src*, используя команду
```sh
$ javac * .java
```
2. Для запуска сервера и клиента ввести команду:
- Dns Client:
```sh
$ java [-mx|-ns] [-p port] @server DNSClient
```

- TFTP Server:
```sh
$ java TFTPServer
```

### Описание используемого протокола.
Для реализации клиента и сервера был использован  UDP протокол.  
DatagramPacket и DatagramSocket - два основных класса, которые используются для реализации клиент-серверного приложения UDP. DatagramPacket - это контейнер данных, а DatagramSocket - это механизм для отправки и получения DatagramPackets.  
В терминах UDP передаваемые данные инкапсулируются в блок, называемый datagram. Datagram - это независимое, автономное сообщение, отправляемое по сети, прибытие, время прибытия и содержание которого не гарантируются. А в Java DatagramPacket представляет собой datagram.  
Cоздать объект DatagramPacket, используя один из следующих конструкторов:  
*DatagramPacket(byte[] buf, int length)*  
*DatagramPacket(byte[] buf, int length, InetAddress address, int port)*  
Данные должны быть в виде массива байтов. 
Первый конструктор используется для создания получаемого пакета DatagramPacket.  
Второй конструктор создает пакет DatagramPacket для отправки, поэтому нужно указать адрес и номер порта хоста назначения.  
Параметр length указывает количество данных в используемом байтовом массиве, обычно это длина массива (buf.length).  
Использовать DatagramSocket для отправки и получения пакетов DatagramPackets. DatagramSocket представляет UDP-соединение между двумя компьютерами в сети.  
В Java мы используем DatagramSocket как для клиента, так и для сервера.  
Создать объект DatagramSocket, чтобы установить UDP-соединение для отправки и получения datagram, используя один из следующих конструкторов:  
DatagramSocket()  
DatagramSocket(int port)  
DatagramSocket(int port, InetAddress laddr)  
Конструктор no-arg используется для создания клиента, который привязывается к произвольному номеру порта.  
Второй конструктор используется для создания сервера, который привязывается к определенному номеру порта, чтобы клиенты знали, как подключиться.  
И третий конструктор привязывает сервер к указанному IP-адресу (в случае, если у компьютера несколько IP-адресов).  
Ключевые методы DatagramSocket включают:  
send (DatagramPacket p): отправляет пакет datagram.  
получить (DatagramPacket p): принимает пакет datagram.  
setSoTimeout (int timeout): устанавливает время ожидания в миллисекундах, ограничивая время ожидания при получении данных. Если время ожидания истекает, возникает исключение SocketTimeoutException.  
close (): закрывает сокет.