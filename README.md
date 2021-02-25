# Лабораторная N 1b TCP чат на неблокирующих сокетах 

Пользователь может отправлять сообщения только от своего имени
Время в сообщение должно соответствовать реальному времени отправления сообщения
Пользователи разных временных зон должны видеть корректное для себя время
Протокол должен быть описан так, чтобы не знакомый с вашей имплементацией разработчик мог написать свою на любом другом языке так, чтобы она оказалась совместима с вашей. Например, если вы используете строки, то необходимо указать их кодировку.

Требования к ПО:
ПО имеет консольный интерфейс
Прямое использование TCP сокетов (без дополнительных абстракций)
К одному серверу может подключаются множество клиентов
Отправляемое сообщение отображается у каждого подключенного в этот момент клиента (т.е. хранение и отображение истории реализовывать не требуется)
Всем пользователям приходит уведомление о подключение/отключение очередного пользователя



## Инструкция по использованию.
сначала запускается сервер, потом запускается клиент. 

Запускается без сборки командой
... путь\nonb_server.py   - сервер
... путь\nonb_client.py   - клиент. 

При запуске клиента, нужно указать IP, и порт на котором работает сервер. 
По умолчанию сервер запускается на 0.0.0.0 и 1234 порту а клиент на 127.0.0.1 1234
Как задать опции:
... путь\nonb_server.py --ip [ip] --port [port]
... путь\nonb_client.py --ip [ip] --port [port]

Опции не являются обязательными, если их не указать будут использоваться значения по умолчанию.

При запуске сервера, он начинает слушать соединения по указаным параметрам.
Как только запускается клиент, потребуется ввести имя пользователя которое не будет совпадать уже с имеющимися именами в чате. 
После указания ника, он отсылается на сервер, там оно проверяется на совпадения, и сервер (если нет совпадений) записывает в список клиентов clients[connection] 
clients - это некий массив пользователей, ключом к которым является соединение по сокету,а значением - имя клиента. 
После записи клиента сервер отвечает клиенту сообщением с значением успеха, либо же в случае уже дублирующего имени, будет об этом сообщено клиенту. 

Как только сервер записал клиента, клиенту разрешено вступать в чат - сервер оповещает клиентов о новом человеке в чате. 
далее начинается общение. 

Завершается соединение - клиент пишет close chat  - и серверу отправляется сообщение что пользователь выходит из чата, далее сервер удаляет этого клиента и оповещает остальных о том что кто-то покинул чат.
Сервер закрывается просто по Ctrl+C  и тогда будет переслано сообщение что сервер отключается и пользователи будут отключены. 

Время теперь определяется только на клиенте, чтобы избежать проблем с разными часовыми поясами допустим. 

## Описание протокола
Коды: 

TYPE_INIT = 1  - код сообщения, свидетельствующий о том что этот пакет является инициализацией клиента.
TYPE_DATA = 2 - код сообщений в чате. С этим кодом передаются пакеты с сообщением. 
TYPE_OKNAME = 3 - Код пакетов, которые отправляет сервер, в случае когда имя годится для записи клиента
TYPE_DUP = 4  - код пакетов, которые отправляет сервер, в случае когда имя не годится(повторяется) для записи клиента.
TYPE_END = 5 - код пакетов, сигнализирующий о разрыве соединения как со стороны сервера, так и со стороны клиента.
TYPE_LEN = 6 - код пакета, который отправляет сервер в случае несоответствия размерам имени.
Пакет инициализации, который отправляется на сервер при включении клиента:

1 байт | массив байт  
------ | ------------ 
код    | Имя клиента  

Код должен быть 1 в соответствии с TYPE_INIT
Имя не больше 1023 байта.
Так как буфер на сервере имеет размерность в 1024, а сообщение инициализации имеет еще один байт отведенный под код.

После того как пакет поступил на сервер, сервер обрабатывает имя клиента, проверяет чтобы ник соответсвовал размерам не больше 20 и не дублировалось имя
Пакет от сервера клиенту в ответ на пакет с кодом TYPE_INIT
В случае успеха:

1 байт | max 20       | 13 байт  
------ | ------------ | -----------
код    | Имя клиента  | сообщение

Код должен быть TYPE_OKNAME 
Имя  - ник клиента который подключаается
Сообщение - сообщение размером в 13 байт " вошел в чат!"

В случае неудачного ввода отправляется один байт с кодом либо TYPE_LEN либо TYPE_DUP

Формат клиентских сообщений серверу:  

1 байт | max 1023  
------ | ------------ 
код    | сообщение

Код должен быть TYPE_DATA 
сообщение - само сообщение которое ввел клиент.
Имя указывать не нужно, так как сервер сам определит кто прислал сообщение по clients[connection] 

Сервер пересылает сообщение:
Если сообщение слишком длинное сервер его обрежет.

1 байт | max 20       | 1 байт  | 1020    | 1 байт
------ | ------------ | ------- | ------- | --------
код    | Имя клиента  | 0       | сообщ.  |  0

Код должен быть TYPE_DATA 
Байты 0 - это разделительные байты которые сигнализируют об окончании имени, и начале сообщения, и об окончании сообщения. 

Пакеты завершения: 

Клиент отправляет серверу:

1 байт который соответствует значению TYPE_END

Если сервер завершает работу посылается пустое сообщение и клиенты отключаются. 
