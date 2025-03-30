# ETL Transformação de dados para análise e recomendação de produtos com base em clientes
from pyspark.sql import SparkSession
from core.lib.lib import Lib
from pipes.extract.get_data_extact_pipe import GetDataExtractPipe


lib = Lib()



# Inicializar Spark
def create_spark_session():
    spark = SparkSession.builder \
        .appName("ETL - Extract").config("spark.sql.shuffle.partitions", "200")\
        .config("spark.driver.extraClassPath", lib.get_postgres_jar()) \
        .config("spark.executor.extraClassPath", lib.get_postgres_jar()) \
        .getOrCreate() 
    return spark
spark = create_spark_session()

# Extrair dados e criar um CSV
get_data_pipe = GetDataExtractPipe(spark).execute()

spark.stop()