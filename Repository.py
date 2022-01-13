from DTOs import Order
import sqlite3
import DAOs
import atexit

class _Repository:
    def __init__(self, db_name):
        self._conn = sqlite3.connect(db_name)
        self.hats = DAOs.Hats(self._conn)
        self.suppliers = DAOs.Suppliers(self._conn)
        self.orders = DAOs.Orders(self._conn)
        self.delete_tables()
        self.create_tables()
    
    def delete_tables(self):
        self.hats.delete()
        self.suppliers.delete()
        self.orders.delete()

    def plan_order(self, order_id, location, topping):
        hat = self.hats.get_hat_by_topping(topping)
        return Order(order_id, location, hat.id)

    def order(self, order):
        hat = self.hats.get_hat_by_id(order.hat)
        self.hats.order_from_supplier(hat.supplier, hat.topping)
        self.orders.insert(order)

    def create_tables(self):
        self._conn.executescript("""
        CREATE TABLE "hats" (
            "id"	INTEGER,
            "topping"	TEXT NOT NULL,
            "supplier"	INTEGER,
            "quantity"	INTEGER NOT NULL,
            FOREIGN KEY("supplier") REFERENCES "suppliers"("id"),
            PRIMARY KEY("id")
        );

        CREATE TABLE "orders" (
            "id"	INTEGER,
            "location"	TEXT NOT NULL,
            "hat"	INTEGER,
            FOREIGN KEY("hat") REFERENCES "hats"("id"),
            PRIMARY KEY("id")
        );

        CREATE TABLE "suppliers" (
            "id"	INTEGER,
            "name"	TEXT NOT NULL,
            PRIMARY KEY("id")
        );
    """)

    def _close(self):
        self._conn.commit()
        self._conn.close()

def create_repository(db_name):
    repo = _Repository(db_name)
    atexit.register(repo._close)
    return repo
