from __future__ import with_statement
from alembic import context
from sqlalchemy import engine_from_config, pool, create_engine
from logging.config import fileConfig

import os


def database_connection_string():
    conn = {
        'db_host': os.getenv('MYSQL_HOST', '127.0.0.1'),
        'db_user': os.getenv('MYSQL_USER', 'root'),
        'db_pass': os.getenv('MYSQL_PASS', 'password'),
        'db_name': os.getenv('MYSQL_NAME', 'pegasus'),
    }

    if conn['db_pass'] is None:
        return 'mysql+pymysql://{0}@{1}/{2}'.format(conn['db_user'], conn['db_host'], conn['db_name'])
    else:
        return 'mysql+pymysql://{0}:{1}@{2}/{3}'.format(conn['db_user'], conn['db_pass'], conn['db_host'], conn['db_name'])


def run_migrations_offline():
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    print('Running mode: offline')

    context.configure(
        url=config.get_main_option('sqlalchemy.url'),
        target_metadata=target_metadata,
        literal_binds=True,
        version_table=config.get_main_option('version_table_name'),
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    print('Running mode: online')

    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix='sqlalchemy.',
        poolclass=pool.NullPool)

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            version_table=config.get_main_option('version_table_name'),
        )

        with context.begin_transaction():
            context.run_migrations()

# Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
target_metadata = None

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.

# Update the url to use sqlalchemy.url option
config.set_main_option('sqlalchemy.url', database_connection_string())

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
