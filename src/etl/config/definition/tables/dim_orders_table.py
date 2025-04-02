from config.utils.dimensional_database import DimensionalTable

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

