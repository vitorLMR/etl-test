from typing import Any
import shutil
import os

from core.env.env import Env
from core.files.files import Files
from config.config import Config


class GetDataExtractPipe:
    def __init__(self, spark: Any):
        self.__spark = spark
        self.__env = Env()
        self.__query =  Config().get_query_to_get_data_in_database_main()
        self.__file = Files()
        self.__folder_temporary_directory = self.__file.get_public_directory() + "/" + "data_extract"
        pass
    def execute(self):
        data_frame = self.__get_orders_data()
        self.__generate_csv(data_frame)
        self.__save_all_data_in_only_one_file()
        pass
    
    def __get_orders_data(self):
        """Buscar dados na base de dados principal"""
        return self.__spark.read.format("jdbc") \
        .option("url", f"jdbc:postgresql://{self.__env.database_main.host}:{self.__env.database_main.port}/{self.__env.database_main.name}") \
        .option("dbtable", f"({self.__query}) AS orders") \
        .option("user", self.__env.database_main.user) \
        .option("password", self.__env.database_main.password) \
        .option("driver", "org.postgresql.Driver") \
        .load()
    
    def __generate_csv(self,data_frame: Any):
        """Criar arquivos CSV para poder realizar a devida leitura"""
        data_frame.coalesce(1).write.csv(self.__folder_temporary_directory, header=False, mode="overwrite")

    def __save_all_data_in_only_one_file(self):
        """Realizar a leitura dos arquivos gerados e criar um único arquivo CSV com todos os dados"""
        files = [f for f in os.listdir(self.__folder_temporary_directory) if f.startswith("part-")]

        for file in files:
            if file:
                shutil.move(os.path.join(self.__folder_temporary_directory, file), self.__file.get_extract_csv())
        shutil.rmtree(self.__folder_temporary_directory)
