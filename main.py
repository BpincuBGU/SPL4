from DTOs import Hat, Supplier
from Repository import create_repository
import sys

def parse_config(config_file):
    with open(config_file, "r") as file:
        hats_count, suppliers_count = file.readline().rstrip('\n').split(",")
        hats = [Hat(*file.readline().rstrip('\n').split(",")) for i in range(int(hats_count))]
        suppliers = [Supplier(*file.readline().rstrip('\n').split(",")) for i in range(int(suppliers_count))]       
        return hats, suppliers

def clear_report(report_file):
    with open(report_file, "w"):
        pass

def report_order(repo, report_file, order):
    with open(report_file, "a+") as file:
        if file.tell() > 0:
            file.write("\n")
        hat = repo.hats.get_hat_by_id(order.hat)
        supplier = repo.suppliers.get_supplier_by_id(hat.supplier)
        file.write(f"{hat.topping},{supplier.name},{order.location}")

def handle_orders(repo, orders_file, report_file):
    order_id = 1
    with open(orders_file, "r") as file:
        for line in file:
            location, topping = line.rstrip('\n').split(",")
            order = repo.plan_order(order_id, location, topping)
            report_order(repo, report_file, order)
            repo.order(order)
            order_id += 1

def handle_config(repo, config_file):
    hats, suppliers = parse_config(config_file)
    {repo.hats.insert(hat) for hat in hats}
    {repo.suppliers.insert(supplier) for supplier in suppliers}

def main():
    if (len(sys.argv) != 5):
        print("Usage: python3 main.py <config_file> <orders_file> <report_file> <db_name>")
        sys.exit(1)
    config_file, orders_file, report_file, db_name = sys.argv[1:]
    repo = create_repository(db_name)
    clear_report(report_file)
    handle_config(repo, config_file)
    handle_orders(repo, orders_file, report_file)

if __name__ == '__main__':
    main()