# Sprint 1 completed - 2026
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
    def __init__(self):
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

    def get_product_description(self, item_id):
        for p in self.products:
            if p.item_id == item_id:
                return p
        return None



class Register:
    def __init__(self, catalog):
        self.catalog = catalog
        self.current_sale = None

    def make_new_sale(self):
        self.current_sale = Sale()
        print("--- New Sale Started ---")

    def enter_item(self, item_id, quantity):
        desc = self.catalog.get_product_description(item_id)
        if desc:
            self.current_sale.make_line_item(desc, quantity)
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



if __name__ == "__main__":

    catalog = ProductCatalog()
    register = Register(catalog)
    register.make_new_sale()
    register.enter_item("1001", 2)  
    register.enter_item("1002", 1)  

    register.end_sale_and_pay(20.00)