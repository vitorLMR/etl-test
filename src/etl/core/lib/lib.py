import os

class Lib:
    __postgres_jar = 'postgresql-42.7.5.jar'

    def get_postgres_jar(self):
        return self.__get_lib_directory(self.__postgres_jar)

    def __get_lib_directory(self, file_name: str):
        directory = os.path.abspath(__file__)
        root_directory = os.path.abspath(os.path.join(directory, "..", "..",'..','..','..','lib'))
        return root_directory + "/" + file_name
