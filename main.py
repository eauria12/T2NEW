from collections import namedtuple

# Crear una tupla nombrada para manejar el menú y los pedidos
MenuItem = namedtuple('MenuItem', ['category', 'name', 'price'])
OrderItem = namedtuple('OrderItem', ['menu_item', 'quantity'])

class DiningExperienceManagerV2:
    MENU = [
        MenuItem("Chino", "Pollo Kung Pao", 5), MenuItem("Chino", "Cerdo Agridulce", 5), MenuItem("Chino", "Arroz Frito", 5),
        MenuItem("Italiano", "Espagueti Boloñesa", 5), MenuItem("Italiano", "Pizza Margarita", 5), MenuItem("Italiano", "Lasagna", 5),
        MenuItem("Pastelería", "Croissant", 5), MenuItem("Pastelería", "Baguette", 5), MenuItem("Pastelería", "Pain au Chocolat", 5),
        MenuItem("Especialidades del Chef", "Lobster Thermidor", 15), MenuItem("Especialidades del Chef", "Caviar", 20), MenuItem("Especialidades del Chef", "Pasta de Trufa", 10),
    ]

    def __init__(self):
        self.order = []

    def add_to_order(self, category, meal, quantity):
        menu_item = next((item for item in self.MENU if item.category == category and item.name == meal), None)
        if menu_item is None:
            return f"Error: {meal} de la categoría {category} no está disponible en el menú."
        if quantity <= 0 or quantity > 100:
            return "Error: La cantidad debe ser un número entero positivo mayor que cero y menor o igual a 100."
        self.order.append(OrderItem(menu_item, quantity))
        return "Plato añadido al pedido exitosamente."

    def calculate_discount(self, total_cost, total_quantity):
        if total_quantity > 10:
            total_cost *= 0.8
        elif total_quantity > 5:
            total_cost *= 0.9
        if total_cost > 100:
            total_cost -= 25
        elif total_cost > 50:
            total_cost -= 10
        return total_cost

    def calculate_special_cost(self, total_cost):
        special_cost = sum(item.menu_item.price * item.quantity * 0.05 for item in self.order if item.menu_item.category == "Especialidades del Chef")
        return total_cost + special_cost

    def calculate_cost(self):
        total_cost = sum(item.menu_item.price * item.quantity for item in self.order)
        total_quantity = sum(item.quantity for item in self.order)
        total_cost = self.calculate_discount(total_cost, total_quantity)
        total_cost = self.calculate_special_cost(total_cost)
        return total_cost

    def complete_order(self):
        return self.order, self.calculate_cost()

if __name__ == '__main__':
    manager = DiningExperienceManagerV2()
    print(manager.add_to_order("Chino", "Pollo Kung Pao", 2))
    print(manager.add_to_order("Italiano", "Lasagna", 3))
    print(manager.add_to_order("Especialidades del Chef", "Caviar", 1))
    order, cost = manager.complete_order()
    print("Pedido:", [(item.menu_item.category, item.menu_item.name, item.quantity) for item in order])
    print("Costo Total:", cost)
