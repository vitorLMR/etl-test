from config.utils.dimensional_database import DimensionalTable
from typing import TypedDict
from pyspark.sql.dataframe import DataFrame

class ReturnsDataFrameDimensionalDatabase(TypedDict):
    table_name: str
    data_frame: DataFrame

class WorkDimensionalDatabase:
    def __init__(self, fact_tables: list[DimensionalTable], dim_table: DimensionalTable):
        self.__fact_tables = fact_tables
        self.__dim_table = dim_table
        pass

    def get_data_frames_of_dimensional_databases(self, data_frame: DataFrame) -> list[ReturnsDataFrameDimensionalDatabase]:
        """Buscar data frames separado por tabelas dimensionais com base em um data frame base"""
        data_frames:list[ReturnsDataFrameDimensionalDatabase] = []
        for table in self.__get_tables():
            data_frames.append(table.get_data_frame(data_frame))
        return data_frames

    def get_names_of_dimensional_tables_to_create(self):
        """Buscar nomes das tabelas dimensionais"""
        table_names: list[str] = []
        for table in self.__get_tables():
            table_names.append(table.name)
        return table_names
    
    def get_names_of_dimensional_tables_to_clear(self):
        """Buscar nomes das tabelas dimensionais na ordem correta para deleção"""
        data = self.get_names_of_dimensional_tables_to_create()
        data.reverse()
        return data

    def get_dimensional_tables_data(self) -> list[DimensionalTable]:
        return self.__get_tables()
    
    def get_fact_tables_data(self)->list[DimensionalTable]:
        return self.__fact_tables
    
    def get_dim_table_data(self)->DimensionalTable:
        return self.__dim_table
    
    def __get_tables(self)->list[DimensionalTable]:
        data = self.__fact_tables.copy()
        data.append(self.__dim_table)
        return data