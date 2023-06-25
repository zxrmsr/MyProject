import re
import datetime
import psycopg2
import click
import argparse
import configparser


database = psycopg2.connect(
    host="localhost",
    user="postgres",
    password="Pa$$w0rd ",
    dbname="apache_logs"
)

cursor = database.cursor()
cursor.execute("DROP TABLE IF EXISTS logs")
cursor.execute(
    "CREATE TABLE logs (ID SERIAL PRIMARY KEY, IP VARCHAR(30), date TIMESTAMP, user_agent TEXT, status_code INTEGER)")

log_file = "C:\\MyProject\\access.log"
log_pattern = r'(\d+\.\d+\.\d+\.\d+)\s-\s-\s\[(.*?)\]\s\"(.*?)\"\s(\d+)'

with open(log_file, 'r') as file:
    for line in file:
        match = re.search(log_pattern, line)
        if match:
            ip = match.group(1)
            date_str = match.group(2)
            user_agent = match.group(3)
            status_code = match.group(4)

            date = datetime.datetime.strptime(date_str, "%d/%b/%Y:%H:%M:%S %z")

            sql = "INSERT INTO logs (ip, date, user_agent, status_code) VALUES (%s, %s, %s, %s)"
            values = (ip, date, user_agent, status_code)
            try:
                cursor.execute(sql, values)
            except psycopg2.DataError as e:
                print(f"DataError: {e}")
                database.rollback()

database.commit()


def view_logs(ip=None, start_date=None, end_date=None):
    sql_query = 'SELECT * FROM logs'
    conditions = []

    if ip:
        conditions.append(f"ip = '{ip}'")
    if start_date and end_date:
        conditions.append(f"date BETWEEN '{start_date}' AND '{end_date}'")
    elif start_date:
        conditions.append(f"date >= '{start_date}'")
    elif end_date:
        conditions.append(f"date <= '{end_date}'")

    if conditions:
        sql_query += " WHERE " + " AND ".join(conditions)

    cursor.execute(sql_query)

    result = cursor.fetchall()
    for r in result:
        print(r)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Filter logs by IP and/or date')
    parser.add_argument('--ip', type=str, help='Filter logs by IP')
    parser.add_argument('--start-date', type=str,
                        help='Start date for date range filter (YYYY-MM-DD)')
    parser.add_argument('--end-date', type=str,
                        help='End date for date range filter (YYYY-MM-DD)')
    parser.add_argument('--config-file', type=str,
                        help='Path to the config file')

    args = parser.parse_args()

    if args.config_file:
        config = configparser.ConfigParser()
        config.read(args.config_file)
        log_path = config.get('Server', 'log_path')
        log_file_mask = config.get('Server', 'log_file_mask')
        view_logs(args.ip, args.start_date, args.end_date)
    else:
        view_logs(args.ip, args.start_date, args.end_date)

cursor.close()
database.close()
