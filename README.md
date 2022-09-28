Первая попытка

## Описание

### app

/app - каталог с самим приложением

Для логов в json добавил json_log_formatter, описав зависимость в requirements.txt

Написал Dockerfile для установки зависимоти и запуска

Запуск: 

```shell
docker build -f app/Dockerfile -t app . 
docker run -d --name app app 
```

### ch

Запускается из контэйнера с дефолтным конфигом
Нужно только создать схему для сбора логов, что делается через маунт init.sql в контэйнер

Запуск:

```shell
docker run -d --name clickhouse -v "$(pwd)/init.sql:/docker-entrypoint-initdb.d/init.sql:ro" -p 8123:8123 clickhouse/clickhouse-server:22.9.2.7
```

### vector

Для работы нужен только конфиг - vector.toml, и сам контэйнер, в который этот конфиг подкладывается

Запуск: 

```shell
docker run -d --name vector -e "DOCKER_HOST=unix:///var/run/docker.sock" -v "$(pwd)/vector.toml:/etc/vector/vector.toml:ro" -v "/var/run/docker.sock:/var/run/docker.sock:ro" -p 8383:8383 timberio/vector:nightly-debian
```

## Мысли/заметки

Переделал вывод лога в нормальный json -> не придеться регулярками парсить поля на мету при передаче в систему хранения логов (хотя в случае с ch все равно придеться регулярками разбивать нужные поля в запросе при выборке/выделению в view, с котрой потом будет строиться алерт/монтиорнг в grafana, допустим)

Посмотрев на filebeat/logstash/fluentd, которые чаще всего используются для сбора логов из разных источников, не увидел у них возможности работы с ch

Можно было бы попробовать через http прокидывать запрос + есть <10 звезд кастомные решения, но не хочется использовать что-то непроверенное. Если в рамках работы такое потребуется, то будет больше времени на изучение кода/написания своего решения, чем при выполнении  тестового задания

Нашел vector, который из коробки умеет собирать логи и писать в ch, но в его доке/issue не удалось найти решение пары проблем, которые возникли при его запуске:

Если запускать его через docker-compose, то сам vector не видит ch (по ip, по имени контэйнера, через link, через bridge кастомную сеть и тд), при этом сам контэйнер, запущенный docker-compose ом отлично telnetит ch по нужному порту + отвечает по curl

Тк в рамках docker-compose котнэйнеры видели друг друга, а сам vector не видел, решил что проблема в нем

При запуске контэйнеров руками раздельно:
```shell
docker build -f app/Dockerfile -t app . 
docker run -d --name app app 

docker run -d --name clickhouse -v "$(pwd)/init.sql:/docker-entrypoint-initdb.d/init.sql:ro" -p 8123:8123 clickhouse/clickhouse-server:22.9.2.7

docker run -d --name vector -e "DOCKER_HOST=unix:///var/run/docker.sock" -v "$(pwd)/vector.toml:/etc/vector/vector.toml:ro" -v "/var/run/docker.sock:/var/run/docker.sock:ro" -p 8383:8383 timberio/vector:nightly-debian
```
p.s тк контэйнеры запускаются руками, а в таком случае обращение по имени контэйнера не работает, возможно потребуется поменять ip ch в vector.toml на ip, указанный в IPAddress вывода команды `docker inspect clickhouse` 
Задумка работала docker контэйнер c app > vector > ch. 
Логи попадали в ch, но vector выкидывал ошибки формата `Received out of order log message.` и связанные с rate limit ом, информации о котором найти не удалось.
Единственный найденный env VECTOR_INTERNAL_LOG_RATE_LIMIT=<цифра> желаемого результата не дал
Похожих ошибок не нашел ни в issues, ни в discord, в который они приглашают

Далее можно было бы развернуть grafana, указать ch в качестве datasource и нарисовать panel с нужными метриками/алерты, но тк нормально не заработало дальше не пошел

В итоге решил, что эта попытка могла бы сработать, но затрачиваемое время на поиск решения проблемы с достаточно молодой тулзой того не стоит (во всяком случае в рамках тестового задания)

Оставил для отчетности
