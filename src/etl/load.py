# ETL Transformação de dados para análise e recomendação de produtos com base em clientes
from pyspark.sql import SparkSession
from core.lib.lib import Lib
from delta import configure_spark_with_delta_pip

from pipes.load.load_pipe import LoadPipe

lib = Lib()



# Inicializar Spark
def create_spark_session():
    spark = configure_spark_with_delta_pip(SparkSession.builder) \
        .appName("ETL - Load").config("spark.sql.shuffle.partitions", "200")\
        .config("spark.driver.extraClassPath", lib.get_postgres_jar()) \
        .config("spark.executor.extraClassPath", lib.get_postgres_jar()) \
        .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
        .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog") \
        .getOrCreate() 
    return spark
spark = create_spark_session()

# Extrair dados e criar um CSV
load_pipe = LoadPipe(spark).execute()

spark.stop()