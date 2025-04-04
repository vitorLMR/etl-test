
from config.utils.view import View,DefineView
from core.env.env import Env
import psycopg2

class DefineDatasetAiView(DefineView):
    def __init__(self, env: Env):
        self.env = env
        super().__init__()

    def get_select(self):
        products_code = self.get_products()
        fields = """
                    "user".email as email,
                    address.uf as uf,
                    address.city as city
                    """
        
        for code in products_code:
            fields = f"""
                        {fields},
                        (
                        CASE
                            WHEN '{code}' = ANY(array_agg(product.code)) THEN 1 ELSE 0
                        END
                        ) as "{code}"
                        """
        select = f"""
                    SELECT 
                    {fields}
                    FROM dim_orders orders
                    inner join fact_user "user" on "user".id = orders.user_id
                    inner join fact_address address on address.id = orders.address_id
                    inner join fact_product product on product.id = orders.product_id
                    group by "user".email, address.uf, address.city
                  """
        print(select)
        return select

    def get_products(self) -> list[str]:
        conn = psycopg2.connect(
            dbname=self.env.database_dim.name,
            user=self.env.database_dim.user,
            password=self.env.database_dim.password,
            host=self.env.database_dim.host,
            port=self.env.database_dim.port
        )
        cur = conn.cursor()
        cur.execute("SELECT code FROM fact_product;")

        # Pegando os resultados
        rows = cur.fetchall()
        products:list[str] = []
        for row in rows:
            products.append(row[0])
        return products

class DatasetAiView(View):
    def __init__(self,env:Env):
        super().__init__("VW_DATASET_AI", None, DefineDatasetAiView(env))
