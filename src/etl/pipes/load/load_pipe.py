from config.config import Config
from core.env.env import Env
import psycopg2

class LoadPipe:
    def __init__(self):
        self.__config = Config()
        self.__env = Env()
        pass

    def execute(self):
        views = self.__config.get_views()
        conn = psycopg2.connect(
                dbname=self.__env.database_dim.name,
                user=self.__env.database_dim.user,
                password=self.__env.database_dim.password,
                host=self.__env.database_dim.host,
                port=self.__env.database_dim.port
            )
        cursor = conn.cursor()

        for view in views:
            cursor.execute(view.get_query_to_create())
            conn.commit()
        conn.close()