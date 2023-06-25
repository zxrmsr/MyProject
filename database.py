import psycopg2
from config import read_config


database = psycopg2.connect(
    host="localhost",
    user="postgres",
    password="Pa$$w0rd ",
    database="apache_logs"
)


def view_logs(filter_ip=None, filter_start_date=None, filter_end_date=None):
    cursor = database.cursor()
    sql = "select * from logs"
    conditions = []

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

    for row in result:
        print(row)


view_logs(filter_ip='127.0.0.1')

view_logs(filter_start_date='2023-01-01', filter_end_date='2023-12-31')

view_logs(filter_ip='127.0.0.1', filter_start_date='2023-01-01',
          filter_end_date='2023-12-31')

log_path, log_file_mask = read_config('config.ini')

database.close()
