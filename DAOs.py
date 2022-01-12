import sqlite3

class HatsDAO:
    def __init__(self, conn):
        self.conn = conn

    def insert(self, hat):
        self.conn.execute("INSERT INTO hats VALUES ('{}','{}','{}','{}') ;".format(hat.id, hat.topping, hat.supplier, hat.quantity))

    def getSupplier(self, topping):
        c = self.conn.cursor()
        topping = topping.rstrip('\n')
        id, supplier = c.execute("""SELECT id,supplier
                                FROM hats
                                WHERE topping = "{}"
                                ORDER BY supplier""".format(topping)).fetchone()
        return id, supplier

    def deleteEmpty(self):
        self.conn.execute("""DELETE FROM hats WHERE quantity = 0""")

    def updateSupplier(self, supplier, topping):
        topping = topping.rstrip('\n')
        querry = """UPDATE hats SET quantity = (SELECT quantity-1 FROM hats where supplier = {} and topping = "{}") where supplier = {} and topping = "{}" """.format(supplier, topping, supplier, topping)
        self.conn.execute(querry)
        self.deleteEmpty()



class SuppliersDAO:
    def __init__(self, conn):
        self.conn = conn

    def insert(self, supplier):
        self.conn.execute("INSERT INTO suppliers VALUES ('{}','{}') ;".format(supplier.id, supplier.name))


class OrdersDAO:
    def __init__(self, conn):
        self.conn = conn

    def insert(self, order):
        self.conn.execute("INSERT INTO orders VALUES ('{}','{}','{}') ;".format(order.id, order.location, order.hat))
