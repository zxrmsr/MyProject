from flask import Flask, jsonify, request
import psycopg2


database = psycopg2.connect(
    host="localhost",
    user="postgres",
    password="Pa$$w0rd ",
    dbname="apache_logs"
)

app = Flask(__name__)


@app.route('/logs', methods=['GET'])
def get_logs():
    cursor = database.cursor()
    sql = "SELECT * FROM logs"
    conditions = []

    filter_ip = request.args.get('ip')
    filter_start_date = request.args.get('start_date')
    filter_end_date = request.args.get('end_date')

    if filter_ip:
        conditions.append("ip = %s")
    if filter_start_date:
        conditions.append("date >= %s")
    if filter_end_date:
        conditions.append("date <= %s")

    if conditions:
        sql += " WHERE " + " AND ".join(conditions)

    values = []
    if filter_ip:
        values.append(filter_ip)
    if filter_start_date:
        values.append(filter_start_date)
    if filter_end_date:
        values.append(filter_end_date)

    cursor.execute(sql, tuple(values))
    result = cursor.fetchall()

    logs = []
    for row in result:
        log = {
            'id': row[0],
            'ip': row[1],
            'date': row[2].strftime("%Y-%m-%d %H:%M:%S")
        }
        logs.append(log)

    return jsonify(logs)


@app.route('/')
def index():
    return 'Добро пожаловать! Добавьте в адресной строке "/logs" для получения всех логов.'


if __name__ == '__main__':
    app.run()

database.close()
