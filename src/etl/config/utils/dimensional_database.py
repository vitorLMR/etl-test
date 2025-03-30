from typing import TypedDict
from pyspark.sql.dataframe import DataFrame
from pyspark.sql.functions import col

class TransformationMainToDimensional(TypedDict):
    old: str
    new: str

class FKs(TypedDict):
    column: str
    table: str

class DimensionalTable:
    def __init__(self, 
                 name: str,
                 transform: list[TransformationMainToDimensional],
                 column_identifier: str | None,
                 fks: list[FKs] | None
                 ):
        self.name = name
        self.__transform = transform
        self.__column_id = column_identifier
        self.fks = fks
        pass


    def get_data_frame(self,data_frame: DataFrame):
        """Buscar banco dimensional no formato de data frame"""
        values_to_dimensional_database = self.__get_values_in_original_data_frame(data_frame)
        if(self.__column_id != None):
            values_to_dimensional_database = self.__format_id(values_to_dimensional_database)
        data_frame =  self.__format_columns(values_to_dimensional_database)
        return {
            "data_frame": data_frame,
            "table_name": self.name
        }
    
    def get_fk_names(self):
        return [item["column"] for item in self.fks]

    def __get_values_in_original_data_frame(self, data_frame: DataFrame) -> DataFrame:
        """Buscar dados no data frame original"""
        original_columns = [item["old"] for item in self.__transform]
        return data_frame.select(*original_columns)
    
    def __format_id(self, data_frame)->DataFrame:
        """Formatar campo que será utilizando como identificador"""
        id_formatted = data_frame.withColumn(self.__column_id, col(self.__column_id).cast("integer"))
        return id_formatted.dropDuplicates([self.__column_id])
    
    def __format_columns(self,data_frame)->DataFrame:
        """Formatar colunas para seguirem o novo padrão de nome"""
        dimensional_table = data_frame
        for transform in self.__transform:
            dimensional_table = dimensional_table.withColumnRenamed(transform['old'], transform["new"])
        return dimensional_table
        

