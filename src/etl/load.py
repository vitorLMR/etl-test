# ETL Transformação de dados para análise e recomendação de produtos com base em clientes
from pyspark.sql import SparkSession
from core.lib.lib import Lib
from pipes.load.load_pipe import LoadPipe

lib = Lib()



# Inicializar Spark
def create_spark_session():
    spark = SparkSession.builder \
        .appName("ETL - Load").config("spark.sql.shuffle.partitions", "200")\
        .config("spark.driver.extraClassPath", lib.get_postgres_jar()) \
        .config("spark.executor.extraClassPath", lib.get_postgres_jar()) \
        .getOrCreate() 
    return spark
spark = create_spark_session()

# Extrair dados e criar um CSV
load_pipe = LoadPipe().execute()

spark.stop()