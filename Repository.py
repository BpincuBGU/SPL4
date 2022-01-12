import sqlite3
import DAOs
import atexit

class _Repository:
    def __init__(self):
        self._conn = sqlite3.connect('database.db')
        self.hats = DAOs.HatsDAO(self._conn)
        self.suppliers = DAOs.SuppliersDAO(self._conn)
        self.orders = DAOs.OrdersDAO(self._conn)

    def _close(self):
        self._conn.commit()
        self._conn.close()


'''
    def create_tables(self):
        _conn.executescript("""
        CREATE TABLE students (
            id      INT         PRIMARY KEY,
            name    TEXT        NOT NULL
        );

        CREATE TABLE assignments (
            num                 INT     PRIMARY KEY,
            expected_output     TEXT    NOT NULL
        );

        CREATE TABLE grades (
            student_id      INT     NOT NULL,
            assignment_num  INT     NOT NULL,
            grade           INT     NOT NULL,

            FOREIGN KEY(student_id)     REFERENCES students(id),
            FOREIGN KEY(assignment_num) REFERENCES assignments(num),

            PRIMARY KEY (student_id, assignment_num)
        );
    """)
'''

repo = _Repository()
atexit.register(repo._close)