from typing import Any
from core.files.files import Files
from pyspark.sql.dataframe import DataFrame
from config.config import Config
from config.utils.work_dimensional_database import ReturnsDataFrameDimensionalDatabase

class SilverTransformPipe:
    def __init__(self,spark: Any):
        self.__spark = spark
        self.__files = Files()
        self.__config = Config()
        pass
    
    def execute(self):
        data_frame = self.__read_delta_files_and_create_data_frame()
        dimensional_tables = self.__separate_data_frame_into_dimensional_tables(data_frame)
        self.__create_delta_folders_by_dimensional_tables(dimensional_tables)
        pass

    def __read_delta_files_and_create_data_frame(self) -> DataFrame:
        """Buscar arquivos delta gerados pela camada bronze e gerar um data frame"""
        return self.__spark.read.format('delta').load(self.__files.get_delta_bronze_directory())

    def __separate_data_frame_into_dimensional_tables(self, data_frame: DataFrame):
        """Separar data frame original em múltiplos data frames por tabela dimensional"""
        return self.__config.get_dimensional_tables_data_frames(data_frame)
    
    def __create_delta_folders_by_dimensional_tables(self,tables: list[ReturnsDataFrameDimensionalDatabase]):
        """Criar pastas com arquivos delta para cada banco dimensional"""
        for table in tables:
            table['data_frame'].write.format("delta")\
            .mode('overwrite')\
            .option("overwriteSchema", "true")\
            .save(self.__files.get_delta_silver_directory(table['table_name']))