class QueryDatabaseMain:
    query = """select  
                    integrator.cnpj as cnpj_integrator,
                    "user".id as user_id,
                    "user".email as user_email,
                    product.id as product_id,
                    product.erp_code as product_erp_code,
                    product_order.product_price as product_price,
                    delivery_address.id as id_address,
                    delivery_address.uf as uf_address,
                    delivery_address.city as city_address
                    from orders "order"
                    inner join integrator_users integrator on integrator.id = "order".billing_integrator_id
                    inner join users "user" on "user".integrator_id = integrator.id
                    inner join order_products as product_order on product_order.order_id = "order".id
                    inner join products product on product.id = product_order.product_id 
                    inner join addresses delivery_address on delivery_address.id = "order".delivery_address_id 
                    where "order".status not in ('OPEN','EXPIRED','CANCELED')"""