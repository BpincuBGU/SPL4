from DTOs import Hat, Order, Supplier

class Hats:
    def __init__(self, conn):
        self.conn = conn

    def insert(self, hat):
        self.conn.execute("""INSERT INTO hats
                        VALUES('{}','{}','{}','{}')""".format(hat.id, hat.topping, hat.supplier, hat.quantity))

    def get_hat_by_id(self, id):
        c = self.conn.cursor()
        hat_data = c.execute("""SELECT * FROM hats WHERE id = {}""".format(id)).fetchone()
        return Hat(*hat_data)

    def get_hat_by_topping(self, topping):
        c = self.conn.cursor()
        hat_data = c.execute("""SELECT * FROM hats WHERE topping = "{}"
                                        ORDER BY supplier""".format(topping)).fetchone()
        return Hat(*hat_data)
    
    def order_from_supplier(self, supplier_id, topping):
        query = """UPDATE hats 
                SET quantity = (SELECT quantity-1 FROM hats WHERE supplier = {} AND topping = "{}")
                WHERE supplier = {} AND topping = "{}" """.format(supplier_id, topping, supplier_id, topping)
        self.conn.execute(query)
        self.delete_empty_suppliers()

    def delete_empty_suppliers(self):
        self.conn.execute("DELETE FROM hats WHERE quantity = 0")

    def delete(self):
        self.conn.execute("DROP TABLE IF EXISTS hats")


class Suppliers:
    def __init__(self, conn):
        self.conn = conn
    
    def get_supplier_by_id(self, id):
        c = self.conn.cursor()
        supplier_data = c.execute("""SELECT * FROM suppliers WHERE id = {}""".format(id)).fetchone()
        return Supplier(*supplier_data)

    def insert(self, supplier):
        self.conn.execute("INSERT INTO suppliers VALUES ('{}','{}')".format(supplier.id, supplier.name))

    def delete(self):
        self.conn.execute("DROP TABLE IF EXISTS suppliers")


class Orders:
    def __init__(self, conn):
        self.conn = conn

    def insert(self, order):
        self.conn.execute("INSERT INTO orders VALUES ('{}','{}','{}')".format(order.id, order.location, order.hat))
    
    def delete(self):
        self.conn.execute("DROP TABLE IF EXISTS orders")
