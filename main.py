
class ProductDescription:
    def __init__(self, item_id, description, price):
        self.item_id = item_id
        self.description = description
        self.price = price



class SalesLineItem:
    def __init__(self, product, quantity):
        self.product = product
        self.quantity = quantity

    def get_subtotal(self):
        return self.product.price * self.quantity



class Sale:
    def __init__(self, sale_id):
        self.sale_id = sale_id
        self.line_items = []
        self.amount_tendered = 0.0

    def make_line_item(self, desc, qty):
        self.line_items.append(SalesLineItem(desc, qty))

    def get_total(self):
        total = 0.0
        for item in self.line_items:
            total += item.get_subtotal()
        return total

    def make_payment(self, amount):
        self.amount_tendered = amount

    def get_balance(self):
        return self.amount_tendered - self.get_total()



class ProductCatalog:
    def __init__(self):
        self.products = [
            ProductDescription("1001", "Apple", 1.5),
            ProductDescription("1002", "Bread", 5.0),
            ProductDescription("1003", "Milk", 3.5)
        ]

        self.inventory = {"1001": 10, "1002": 10, "1003": 10}

    def get_product_description(self, item_id):
        for p in self.products:
            if p.item_id == item_id:
                return p
        return None



class Register:
    def __init__(self, catalog):
        self.catalog = catalog
        self.current_sale = None
        self.historical_sales = {}
        self.sale_counter = 1

    def make_new_sale(self):
        sale_id = f"S{self.sale_counter:03d}"
        self.current_sale = Sale(sale_id)
        print(f"--- New Sale Started (ID: {sale_id}) ---")

    def enter_item(self, item_id, quantity):
        desc = self.catalog.get_product_description(item_id)
        if desc:
            self.current_sale.make_line_item(desc, quantity)

            self.catalog.inventory[item_id] -= quantity
            print(f"Added: {desc.description} x{quantity} (Price: ${desc.price:.2f})")
        else:
            print(f"Error: Item ID {item_id} not found!")

    def end_sale_and_pay(self, cash_tendered):
        total = self.current_sale.get_total()
        print("\n--- Receipt ---")
        for item in self.current_sale.line_items:
            print(f"{item.product.description:<10} x{item.quantity}   ${item.get_subtotal():.2f}")
        print(f"Total:     ${total:.2f}")

        self.current_sale.make_payment(cash_tendered)
        print(f"Tendered:  ${cash_tendered:.2f}")
        print(f"Change:    ${self.current_sale.get_balance():.2f}")
        print("---------------\n")


        self.historical_sales[self.current_sale.sale_id] = self.current_sale
        self.sale_counter += 1
        self.current_sale = None



    def start_return(self, sale_id):
        print(f"--- Return Started (Looking up Sale ID: {sale_id}) ---")
        if sale_id in self.historical_sales:
            self.current_sale = self.historical_sales[sale_id]
            print("Sale found. Items available for return:")
            for item in self.current_sale.line_items:
                print(f" - {item.product.description} x{item.quantity}")
        else:
            print(f"Error: Sale ID {sale_id} not found!")

    def process_return_item(self, item_id, qty_to_return):
        if self.current_sale:
            for item in self.current_sale.line_items:
                if item.product.item_id == item_id and item.quantity >= qty_to_return:
                    refund = item.product.price * qty_to_return

                    item.quantity -= qty_to_return

                    self.catalog.inventory[item_id] += qty_to_return

                    print(f"\n--- Return Receipt ---")
                    print(f"Returned:  {item.product.description} x{qty_to_return}")
                    print(f"Refund:    ${refund:.2f}")
                    print("----------------------\n")
                    return
            print(f"Error: Cannot return item {item_id}. Invalid ID or quantity exceeded.")
        else:
            print("Error: No active return session. Please start a return first.")


if __name__ == "__main__":

    catalog = ProductCatalog()
    register = Register(catalog)


    register.make_new_sale()
    register.enter_item("1001", 2)
    register.enter_item("1002", 1)
    register.end_sale_and_pay(20.00)


    register.start_return("S001")
    register.process_return_item("1001", 1)