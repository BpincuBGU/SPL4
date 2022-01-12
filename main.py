import DTOs
import sqlite3
from Repository import repo


def parse_config():
    file = open("config.txt", "r")
    entries = file.readline().split(",")
    for i in range(int(entries[0])):
        arguments = file.readline().split(",")
        hat = DTOs.HatsDTO(arguments[0], arguments[1], arguments[2], arguments[3])
        repo.hats.insert(hat)
    for i in range(int(entries[1])):
        arguments = file.readline().split(",")
        supplier = DTOs.SuppliersDTO(arguments[0], arguments[1])
        repo.suppliers.insert(supplier)



def execute_orders():
    file = open("orders.txt", "r")
    id = 1
    for line in file:
        location, topping = line.split(",")
        hatid, supplierid = repo.hats.getSupplier(topping)
        repo.hats.updateSupplier(supplierid, topping)
        order = DTOs.OrdersDTO(id, location, hatid)
        id+=1
        repo.orders.insert(order)


def main():
    parse_config()
    execute_orders()


if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/


