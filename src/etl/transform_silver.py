# ETL Transformação de dados para análise e recomendação de produtos com base em clientes
from pyspark.sql import SparkSession
from core.lib.lib import Lib
from pipes.transform.silver_transform_pipe import SilverTransformPipe
from delta import configure_spark_with_delta_pip

lib = Lib()



# Inicializar Spark
def create_spark_session():
    spark = configure_spark_with_delta_pip(SparkSession.builder) \
        .appName("ETL - Transform (Silver)").config("spark.sql.shuffle.partitions", "200")\
        .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
        .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog") \
        .getOrCreate() 
    return spark
spark = create_spark_session()

transform_silver = SilverTransformPipe(spark)
transform_silver.execute()

spark.stop()