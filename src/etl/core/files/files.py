import os

class Files:
    __extract_csv = 'extract.csv'
    __parquet_leading_directory = 'leading_parquet'
    __delta_bronze_directory = 'bronze_delta'
    __delta_silver_directory = 'silver_delta'

    def get_extract_csv(self):
        return self.__get_public_directory(self.__extract_csv)
    
    def get_parquet_leading_directory(self):
        return self.__get_public_directory(self.__parquet_leading_directory)
    
    def get_delta_bronze_directory(self):
        return self.__get_public_directory(self.__delta_bronze_directory)
    
    def get_delta_silver_directory(self,table: str):
        return self.__get_public_directory(self.__delta_silver_directory + "/" + table)

    def get_public_directory(self):
        directory = os.path.abspath(__file__)
        return os.path.abspath(os.path.join(directory, "..", "..",'..','..','..','public'))

    def __get_public_directory(self, file_name: str):
        root_directory = self.get_public_directory()
        return root_directory + "/" + file_name