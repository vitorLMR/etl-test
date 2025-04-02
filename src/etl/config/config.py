import re
from pyspark.sql.dataframe import DataFrame

from config.definition.query_database_main import QueryDatabaseMain
from config.definition.config_dimensional_tables import ConfigDimensionalTables
from config.definition.config_views import ConfigViews

class Config:
    def __init__(self):
        self.__query = QueryDatabaseMain.query
        self.__columns = re.findall(r'as (\w+)', self.__query)
        self.__transform_dimensional = ConfigDimensionalTables()
        self.__config_views = ConfigViews()
        pass
    def get_query_to_get_data_in_database_main(self):
        """Buscar query que será responsável pela busca de dados no banco de dados principal"""
        return self.__query
    def format_column_names_in_parquet_files(self):
        """Formatar nome das colunas no carregamento dos arquivos parquet"""
        return {f"_c{index}": name for index, name in enumerate(self.__columns)}
    
    def get_dimensional_tables_data_frames(self,data_frame: DataFrame):
        """Buscar os data frames das tabelas dimensionais"""
        return self.__transform_dimensional.get_data_frames_of_dimensional_databases(data_frame)
    
    def get_dimensional_tables_names_to_create(self):
        """Buscar nomes das tabelas dimensionais na ordem para criação"""
        return self.__transform_dimensional.get_names_of_dimensional_tables_to_create()
    
    def get_dimensional_tables_names_to_delete(self):
        """Buscar nomes das tabelas dimensionais na ordem para deleção"""
        return self.__transform_dimensional.get_names_of_dimensional_tables_to_clear()
    
    def get_fact_tables(self):
        """Buscar tabelas fato"""
        return self.__transform_dimensional.get_fact_tables_data()
    
    def get_dim_table(self):
        """Buscar tabela dimensional"""
        return self.__transform_dimensional.get_dim_table_data()
    
    def get_views(self):
        """Buscar views da base de dados dimensional"""
        return self.__config_views.get_views()