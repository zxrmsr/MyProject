Убедитесь, что у вас установлен Python и установщик пакетов "pip". Если он скачен, то теперь нужно ввести в терминал "pip install flask", "pip install psycopg2", "pip install click" и "pip install configparser".

Теперь создайте пустую базу данных в PostgreSQL.

В файлах API.py, database.py, config.ini и app.py вставьте данные о своей базе данных в host, user, password и database. 
Пример: 
host="localhost", user="postgres", password="Pa$$w0rd", database="apache_logs"

Вставьте пути до файла access в файлах main.py и config.ini в "log_file", а также путь до папки ProjectWork в файле config.ini в "log_path" 
Мой пример: 
log_file = C:/MyProject/access.log
log_file = C:/MyProject/
Ваш пример:
log_file = D:/Downloads/Browser/MyProject-main/access.log
log_path = D:/Downloads/Browser/MyProject-main/

Запустите файл app.py

После этого, перейдите в PgAdmin и введите команду "select * from logs;" чтобы просмотреть таблицу.

Теперь запустите файл API.py.

У вас должна появиться ссылка. 
Пример: http://127.0.0.1:5000

Скопируйте её и вставьте в браузер, либо же зажмите Ctrl и нажмите на ссылку, чтобы перейти на главную страницу.

Добавьте в адресной строке "/logs" для получения всех логов.

После этого у вса должны появиться все логи из файла "access.log".

Теперь измените "/logs" на "/?start_date=YYYY-MM-DD&end_date=YYYY-MM-DD" 

После этого у вас должны появиться логи, отсортированные по указанным датам.

Теперь измените "/?start_date=YYYY-MM-DD&end_date=YYYY-MM-DD" на "?ip=...", где вместо "..." напишите любой ip.

После этого у вас должны появиться логи, которые имеют данный ip.
