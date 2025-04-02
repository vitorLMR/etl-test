from config.utils.dimensional_database import DimensionalTable

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