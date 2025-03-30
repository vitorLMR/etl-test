from pyspark.sql.dataframe import DataFrame
from config.utils.dimensional_database import DimensionalTable
from config.utils.work_dimensional_database import WorkDimensionalDatabase




class UserDimensionalTable(DimensionalTable):
    def __init__(self):
        super().__init__("fact_user", [
            {
                "new": "id",
                "old": "user_id"
            },
            {
                "new": "cnpj",
                "old": "cnpj_integrator"
            },
            {
                "new": "email",
                "old": "user_email"
            }
        ], "user_id", None)

class ProductDimensionalTable(DimensionalTable):
    def __init__(self):
        super().__init__("fact_product", [
            {
                "new": "id",
                "old": "product_id"
            },
            {
                "new": "code",
                "old": "product_erp_code"
            },
        ], "product_id",None)

class AddressDimensionalTable(DimensionalTable):
    def __init__(self):
        super().__init__("fact_address", [
            {
                "new": "id",
                "old": "id_address"
            },
            {
              "new": "uf",
              "old": "uf_address" 
            },
            {
                "new": "city",
                "old": "city_address"
            }
        ], "id_address",None)

class OrderDimensionalTable(DimensionalTable):
    def __init__(self):
        super().__init__("dim_orders", [
            {
                "new": "address_id",
                "old": "id_address"
            },
            {
                "new": "product_id",
                "old": "product_id"
            },
            {
                "new": "user_id",
                "old": "user_id"
            },
            {
                "new": "product_price",
                "old": "product_price"
            }
        ], None, [
            {
                "column": 'user_id',
                "table": 'fact_user'
            },
            {
                "column": 'address_id',
                "table": 'fact_address'
            },
            {
                "column": 'product_id',
                "table": 'fact_product'
            }
        ])


class TransformationToDimensionalDatabase(WorkDimensionalDatabase):
    def __init__(self):
        super().__init__([
            AddressDimensionalTable(),
            ProductDimensionalTable(),
            UserDimensionalTable()
            ], OrderDimensionalTable())
    