from config.utils.dimensional_database import DimensionalTable

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
