import os

DATABASE = {
    'drivername': 'postgres',
    'host': os.getenv('OPENSHIFT_POSTGRESQL_DB_HOST','localhost'),
    'port': os.getenv('OPENSHIFT_POSTGRESQL_DB_PORT','5432'),
    'username': 'adminq3lqhtw',
    'password': 'RBUtalL4hRxQ',
    'database': 'pyramidapp'
}