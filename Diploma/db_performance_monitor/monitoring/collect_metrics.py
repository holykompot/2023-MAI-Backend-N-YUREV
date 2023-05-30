import psycopg2
import pymysql
from datetime import datetime
from .models import Database, DatabaseMetric, Metric
from pymongo import MongoClient


# Функция для сбора метрики Disk I/O performance из PostgreSQL
def collect_postgresql_metrics(database):
    try:
        conn = psycopg2.connect(database=database.name, user=database.username,
                                password=database.password, host=database.host,
                                port=database.port)
        cur = conn.cursor()
        # Получение статистики производительности
        cur.execute("with  all_tables as "
                    "( SELECT  * FROM    ("
                    "     SELECT  'all'::text as table_name,"
                    "          sum( (coalesce(heap_blks_read,0)"
                    " + coalesce(idx_blks_read,0)"
                    " + coalesce(toast_blks_read,0)"
                    " + coalesce(tidx_blks_read,0)) ) as from_disk,"
                    "          sum( (coalesce(heap_blks_hit,0)  "
                    "+ coalesce(idx_blks_hit,0)  "
                    "+ coalesce(toast_blks_hit,0)  "
                    "+ coalesce(tidx_blks_hit,0))  ) as from_cache"
                    "     FROM    pg_statio_a")
        result = cur.fetchone()
        conn.close()

        # Сохранение метрик
        save_metric(database, 'overall_score', result[0])

    except Exception as e:
        print(f"Error collecting metrics from PostgreSQL: {e}")


# Функция для сбора метрик из MySQL
def collect_mysql_metrics(database):
    try:
        conn = pymysql.connect(database=database.name, user=database.username,
                               password=database.password, host=database.host,
                               port=database.port)
        cur = conn.cursor()
        # Получение статистики производительности
        cur.execute("SELECT table_schema, sum(data_length + index_length) \
                     FROM information_schema.TABLES \
                     WHERE table_schema = %s \
                     GROUP BY table_schema;", (database.name,))
        database_size = cur.fetchone()

        cur.execute("SHOW STATUS WHERE variable_name = 'Threads_connected';")
        connections = cur.fetchone()
        conn.close()

        # Сохранение метрик
        save_metric(database, 'database_size', database_size[1])
        save_metric(database, 'connections', connections[1])

    except Exception as e:
        print(f"Error collecting metrics from MySQL: {e}")


def collect_mongodb_metrics(database):
    try:
        client = MongoClient(host=database.host, port=database.port,
                             username=database.username, password=database.password)
        db = client[database.name]

        # Получение статистики производительности
        database_size = db.command('db.stats(1024*1024)')['dataSize']
        connections = db.command('serverStatus')['connections']['current']

        # Сохранение метрик
        save_metric(database, 'database_size', database_size)
        save_metric(database, 'connections', connections)

    except Exception as e:
        print(f"Error collecting metrics from MongoDB: {e}")


def collect_all_database_metrics():
    databases = Database.objects.all()
    for db in databases:
        if db.db_type == Database.DB_TYPE_CHOICES[0][0]: # PostgreSQL:
            collect_postgresql_metrics(db)
        elif db.db_type == Database.DB_TYPE_CHOICES[1][0]: # MySQL:
            collect_mysql_metrics(db)
        elif db.db_type == Database.DB_TYPE_CHOICES[2][0]: # MongoDB:
            collect_mongodb_metrics(db)


# Функция для сохранения метрик в модель данных
def save_metric(database, metric_name, value):
    metric = Metric.objects.get(name=metric_name)
    db_metric = DatabaseMetric(database=database, metric=metric, value=value, timestamp=datetime.now())
    db_metric.save()
