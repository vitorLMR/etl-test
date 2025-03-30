# ETL Transformação de dados para análise e recomendação de produtos com base em clientes
from pyspark.sql import SparkSession
from core.lib.lib import Lib
from pipes.transform.leading_transform_pipe import LeadingTransformPipe


lib = Lib()

# Inicializar Spark
def create_spark_session():
    spark = SparkSession.builder \
        .appName("ETL - Transform (Leading)").config("spark.sql.shuffle.partitions", "200")\
        .getOrCreate() 
    return spark
spark = create_spark_session()

transform_leading = LeadingTransformPipe(spark)
transform_leading.execute()

spark.stop()