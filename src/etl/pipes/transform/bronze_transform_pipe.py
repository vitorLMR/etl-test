from typing import Any
from pyspark.sql.dataframe import DataFrame

from core.files.files import Files
from config.config import Config

class BronzeTransformPipe:
    def __init__(self, spark: Any):
        self.__spark = spark
        self.__files = Files()
        self.__config = Config()
        pass

    def execute(self):
        data_frame = self.__read_parquet_files_and_create_data_frame()
        data_frame = self.__format_columns_name_in_data_frame(data_frame)
        self.__create_delta_files_by_data_frame(data_frame)
        pass
    
    def __read_parquet_files_and_create_data_frame(self) -> DataFrame:
        """Realizar a leitura dos arquivos parquet e criar um data frame a partir deles"""
        return self.__spark.read.parquet(self.__files.get_parquet_leading_directory())
    
    def __format_columns_name_in_data_frame(self,data_frame: DataFrame):
        """Corrigir o nome das colunas nos arquivos parquet"""
        for old_name, new_name in self.__config.format_column_names_in_parquet_files().items():
            data_frame = data_frame.withColumnRenamed(old_name, new_name)
        return data_frame

    def  __create_delta_files_by_data_frame(self, data_frame: DataFrame):
        """Criar arquivos Delta com base no data frame"""
        data_frame.write.format("delta").mode('overwrite').option("overwriteSchema", "true").save(self.__files.get_delta_bronze_directory())