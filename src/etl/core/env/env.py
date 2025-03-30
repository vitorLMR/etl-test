import os
from dotenv import load_dotenv

load_dotenv()

class EnvDatabaseMain:
    host = os.getenv('DATABASE_MAIN_HOST')
    name = os.getenv('DATABASE_MAIN_NAME')
    user = os.getenv('DATABASE_MAIN_USER')
    password = os.getenv('DATABASE_MAIN_PASS')
    port = os.getenv('DATABASE_MAIN_PORT')

class EnvDatabaseDim:
    host = os.getenv('DATABASE_DIM_HOST')
    name = os.getenv('DATABASE_DIM_NAME')
    user = os.getenv('DATABASE_DIM_USER')
    password = os.getenv('DATABASE_DIM_PASS')
    port = os.getenv('DATABASE_DIM_PORT')

class Env:
    database_main = EnvDatabaseMain()
    database_dim = EnvDatabaseDim()

    