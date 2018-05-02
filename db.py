import json
import pymysql
from peewee import *
from config import *


db = MySQLDatabase(DB_NAME, host=DB_HOST, password=DB_PASSWORD, user=DB_USER)


class JSONField(TextField):
    def db_value(self, value):
        return json.dumps(value)

    def python_value(self, value):
        if value is not None:
            return json.loads(value)


class Permission(Model):
    app_id = CharField()
    hl = CharField()
    permissions = JSONField()

    class Meta:
        database = db
        table_name = 'permissions'
        primary_key = CompositeKey('app_id', 'hl')


def create_table():
    db.connect()
    db.create_tables([Permission])
    print('created')


def create_db():
    conn = pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD)
    conn.cursor().execute('CREATE DATABASE IF NOT EXISTS %s;' % DB_NAME)
    conn.close()


if __name__ == '__main__':
    create_db()
    create_table()