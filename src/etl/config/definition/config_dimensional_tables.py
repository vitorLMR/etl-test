from pyspark.sql.dataframe import DataFrame
from config.utils.dimensional_database import DimensionalTable
from config.utils.work_dimensional_database import WorkDimensionalDatabase

from config.definition.tables.fact_user_table import UserDimensionalTable
from config.definition.tables.fact_product_table import ProductDimensionalTable
from config.definition.tables.fact_address_table import AddressDimensionalTable
from config.definition.tables.dim_orders_table import OrderDimensionalTable


class ConfigDimensionalTables(WorkDimensionalDatabase):
    def __init__(self):
        super().__init__([
            AddressDimensionalTable(),
            ProductDimensionalTable(),
            UserDimensionalTable()
            ], OrderDimensionalTable())
    