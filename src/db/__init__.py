import mysql.connector
import os

from sqlalchemy import create_engine
from sqlalchemy.exc import DatabaseError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

def database_connection_string():
    conn = {
        'db_host': os.getenv('MYSQL_HOST', '127.0.0.1'),
        'db_user': os.getenv('MYSQL_USER', 'root'),
        'db_pass': os.getenv('MYSQL_PASS', 'password'),
        'db_name': os.getenv('MYSQL_NAME', 'pegasus'),
    }

    if conn['db_pass'] is None:
        return 'mysql+mysqlconnector://{0}@{1}/{2}'.format(conn['db_user'], conn['db_host'], conn['db_name'])
    else:
        return 'mysql+mysqlconnector://{0}:{1}@{2}/{3}'.format(conn['db_user'], conn['db_pass'], conn['db_host'], conn['db_name'])


database_engine = create_engine(database_connection_string(),
                                pool_size=20,
                                max_overflow=0,
                                echo=True)
database_session = scoped_session(sessionmaker(autocommit=False,
                                               autoflush=False,
                                               bind=database_engine))

class MyBase(object):
    def delete(self):
        database_session.delete(self)
        self._flush()

    def save(self):
        database_session.add(self)
        self._flush()
        return self

    def update(self, **kwargs):
        for attr, value in kwargs.items():
            setattr(self, attr, value)
        return self.save()

    def _flush(self):
        try:
            database_session.flush()
        except DatabaseError:
            database_session.rollback()
            raise


Base = declarative_base(cls=MyBase)
Base.query = database_session.query_property()


# def connection():
#     return mysql.connector.connect(
#       host=os.getenv('MYSQL_HOST', '127.0.0.1'),
#       user=os.getenv('MYSQL_USER', 'root'),
#       passwd=os.getenv('MYSQL_PASS', 'password'),
#       database=os.getenv('MYSQL_NAME', 'pegasus'),
#     )

# connection = mysql.connector.connect(
#   host=os.getenv('MYSQL_HOST', '127.0.0.1'),
#   user=os.getenv('MYSQL_USER', 'root'),
#   passwd=os.getenv('MYSQL_PASS', 'password'),
#   database=os.getenv('MYSQL_NAME', 'pegasus'),
# )
#
# cursor = pegasus.cursor()
#
# sql = "INSERT INTO currencies (name) VALUES (%s)"
# val = ("John",)
# cursor.execute(sql, val)
#
# connection.commit()
#
# cursor.close()
# connection.close()
