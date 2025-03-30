from typing import Any
from pyspark.sql.dataframe import DataFrame

from core.files.files import Files

class LeadingTransformPipe:
    def __init__(self, spark: Any):
        self.__spark = spark
        self.__files = Files()
        pass

    def execute(self):
        data_frame = self.__load_csv_file_and_generate_data_frame()
        self.__generate_parquets_by_data_frame(data_frame)
        pass

    def __load_csv_file_and_generate_data_frame(self) -> DataFrame:
        """Realizar a leitura do arquivo CSV gerado no get_data e criar um dataframe com estas informações"""
        return self.__spark.read.option("inferSchema",True).csv(self.__files.get_extract_csv())

    def __generate_parquets_by_data_frame(self, data_frame: DataFrame):
        """Criar arquivos parquet dos dados lidos do CSV"""
        data_frame.write.mode("overwrite").format("parquet").save(self.__files.get_parquet_leading_directory())