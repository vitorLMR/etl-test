
from typing import Any,TypedDict
from pyspark.sql.dataframe import DataFrame
from config.config import Config
from core.files.files import Files
from core.env.env import Env
import psycopg2

class DataFrameWithTableName(TypedDict):
    name: str
    data_frame: DataFrame

base_postgres_url = "jdbc:postgresql://host:port/name"
class GoldTransformPipe:
    def __init__(self, spark: Any):
        self.__spark = spark
        self.__config = Config()
        self.__files = Files()
        self.__env = Env()

        self.__postgres_url = base_postgres_url
        self.__postgres_url = self.__postgres_url.replace("host",self.__env.database_dim.host)
        self.__postgres_url = self.__postgres_url.replace("port",self.__env.database_dim.port)
        self.__postgres_url = self.__postgres_url.replace("name",self.__env.database_dim.name)

        self.__postgres_properties = {
            "user": self.__env.database_dim.user,
            "password": self.__env.database_dim.password,
            "driver": "org.postgresql.Driver"
        }
        pass

    def execute(self):
        dimensional_tables = self.__get_dimensional_tables_names()
        data_frames = self.__read_delta_files_and_create_data_frames(dimensional_tables)
        self.__delete_dimensional_tables()
        self.__create_dimensional_tables(data_frames)
        self.__create_primary_keys_into_fact_tables()
        self.__create_primary_key_into_dim_table()
        self.__create_foreign_key_into_dim_table()
        pass

    def __get_dimensional_tables_names(self):
        """Buscar tabelas dimensionais que serão geradas"""
        return self.__config.get_dimensional_tables_names_to_create()

    def __read_delta_files_and_create_data_frames(self, dimensional_tables: list[str])->list[DataFrameWithTableName]:
        """Ler arquivos delta e criar Data frames para cada tabela dimensional"""
        data_frames: list[DataFrameWithTableName] = []
        for table in dimensional_tables:
            data_frame = self.__spark.read.format('delta').load(self.__files.get_delta_silver_directory(table))
            data_frames.append(
                {
                    "name": table,
                    "data_frame": data_frame
                }
            )
        return data_frames

    def __delete_dimensional_tables(self):
        """Limpar tabelas dimensionais para a nova importação"""
        tables_names = self.__config.get_dimensional_tables_names_to_delete()
        conn = psycopg2.connect(
                dbname=self.__env.database_dim.name,
                user=self.__env.database_dim.user,
                password=self.__env.database_dim.password,
                host=self.__env.database_dim.host,
                port=self.__env.database_dim.port
            )
        cursor = conn.cursor()

        for table_name in tables_names:
            cursor.execute("DROP TABLE IF EXISTS " + table_name)
            conn.commit()
        conn.close()

    def __create_dimensional_tables(self,data_frames: list[DataFrameWithTableName]):
        """Criar tabelas dimensionais"""
        for data_frame in data_frames:
            data_frame['data_frame'].write.jdbc(url=self.__postgres_url, table=data_frame['name'], mode="overwrite", properties=self.__postgres_properties)

    def __create_primary_keys_into_fact_tables(self):
        """Adicionar chaves primárias nas tabelas fato"""
        conn = psycopg2.connect(
                dbname=self.__env.database_dim.name,
                user=self.__env.database_dim.user,
                password=self.__env.database_dim.password,
                host=self.__env.database_dim.host,
                port=self.__env.database_dim.port
            )
        cursor = conn.cursor()

        query = "ALTER TABLE table ADD CONSTRAINT pk_table PRIMARY KEY (id)"
        fact_tables = self.__config.get_fact_tables()

        for fact_table in fact_tables:
            query_data = query.replace("table",fact_table.name)
            query_data = query_data.replace("pk_table","pk_"+fact_table.name)
            cursor.execute(query_data)
            conn.commit()
        conn.close()

    def __create_primary_key_into_dim_table(self):
        """Adicionar chaves primárias para a tabela dimensão"""
        conn = psycopg2.connect(
                dbname=self.__env.database_dim.name,
                user=self.__env.database_dim.user,
                password=self.__env.database_dim.password,
                host=self.__env.database_dim.host,
                port=self.__env.database_dim.port
            )
        cursor = conn.cursor()

        query = "ALTER TABLE table ADD CONSTRAINT pk_table PRIMARY KEY (columns)"
        dim_table = self.__config.get_dim_table()

        query = query.replace("table",dim_table.name)
        query = query.replace("pk_table","pk_" + dim_table.name)
        query = query.replace("columns", ",".join(dim_table.get_fk_names()))
        cursor.execute(query)
        conn.commit()
        conn.close()

    def __create_foreign_key_into_dim_table(self):
        """Criar chaves estrangeiras na tabela dimensional"""
        conn = psycopg2.connect(
                dbname=self.__env.database_dim.name,
                user=self.__env.database_dim.user,
                password=self.__env.database_dim.password,
                host=self.__env.database_dim.host,
                port=self.__env.database_dim.port
            )
        cursor = conn.cursor()

        query = "ALTER TABLE table ADD CONSTRAINT fk_name FOREIGN KEY (column) REFERENCES fknm(id);"
        dim_table = self.__config.get_dim_table()
        for fk in dim_table.fks:
            query_data = query.replace("table",dim_table.name)
            query_data = query_data.replace("fk_name","fk_"+dim_table.name+"_"+fk["table"])
            query_data = query_data.replace("column",fk['column'])
            query_data = query_data.replace('fknm',fk["table"])
            cursor.execute(query_data)
            conn.commit()
        conn.close()
