from config.utils.dimensional_database import DimensionalTable

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