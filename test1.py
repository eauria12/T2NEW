import unittest
import xmlrunner

from main1 import DiningExperienceManagerV2, MenuItem

class TestDiningExperienceManagerV2(unittest.TestCase):
    def setUp(self):
        self.manager = DiningExperienceManagerV2()
        self.manager.order = []  # Clear the previous orders

    def test_add_to_order(self):
        # Test adding a valid meal
        self.assertEqual(self.manager.add_to_order("Chino", "Pollo Kung Pao", 2), "Plato añadido al pedido exitosamente.")

        # Test adding a meal with invalid category
        self.assertEqual(self.manager.add_to_order("Indio", "Pollo Kung Pao", 2), "Error: Pollo Kung Pao de la categoría Indio no está disponible en el menú.")

        # Test adding a meal that is not in the category
        self.assertEqual(self.manager.add_to_order("Chino", "Pizza Margarita", 2), "Error: Pizza Margarita de la categoría Chino no está disponible en el menú.")

        # Test adding a meal with quantity <= 0
        self.assertEqual(self.manager.add_to_order("Chino", "Pollo Kung Pao", 0), "Error: La cantidad debe ser un número entero positivo mayor que cero y menor o igual a 100.")

        # Test adding a meal with quantity > 100
        self.assertEqual(self.manager.add_to_order("Chino", "Pollo Kung Pao", 101), "Error: La cantidad debe ser un número entero positivo mayor que cero y menor o igual a 100.")

    def test_calculate_cost(self):
        # Test cost calculation for one meal
        self.manager.add_to_order("Chino", "Pollo Kung Pao", 2)
        self.assertAlmostEqual(self.manager.calculate_cost(), 10)

        # Clear the previous orders
        self.manager.order = []

        # Test cost calculation for multiple meals
        self.manager.add_to_order("Italiano", "Lasagna", 3)
        self.assertAlmostEqual(self.manager.calculate_cost(), 15)

        # Clear the previous orders
        self.manager.order = []

        # Test cost calculation with quantity discount
        self.manager.add_to_order("Pastelería", "Croissant", 3)
        self.manager.add_to_order("Chino", "Pollo Kung Pao", 2)
        self.manager.add_to_order("Italiano", "Lasagna", 1)
        self.assertAlmostEqual(self.manager.calculate_cost(), 27)  # With 10% discount

        # Clear the previous orders
        self.manager.order = []

        # Test cost calculation with total cost discount
        self.manager.add_to_order("Pastelería", "Pain au Chocolat", 11)
        self.assertAlmostEqual(self.manager.calculate_cost(), 44)  # With 20% discount and $10 discount

        # Clear the previous orders
        self.manager.order = []

        # Test cost calculation with Chef's Specials surcharge
        self.manager.add_to_order("Especialidades del Chef", "Caviar", 1)
        self.assertAlmostEqual(self.manager.calculate_cost(), 21)  # With 5% surcharge

    def test_complete_order(self):
        # Test finalizing order
        self.manager.add_to_order("Chino", "Pollo Kung Pao", 2)
        self.manager.add_to_order("Italiano", "Lasagna", 3)
        self.manager.add_to_order("Pastelería", "Croissant", 3)
        self.manager.add_to_order("Pastelería", "Pain au Chocolat", 6)
        self.manager.add_to_order("Especialidades del Chef", "Caviar", 1)
        order, cost = self.manager.complete_order()
        expected_order = [
            (MenuItem("Chino", "Pollo Kung Pao", 5), 2),
            (MenuItem("Italiano", "Lasagna", 5), 3),
            (MenuItem("Pastelería", "Croissant", 5), 3),
            (MenuItem("Pastelería", "Pain au Chocolat", 5), 6),
            (MenuItem("Especialidades del Chef", "Caviar", 20), 1)
        ]
        self.assertEqual([(item.menu_item, item.quantity) for item in order], expected_order)
        self.assertAlmostEqual(cost, 63)  # With 20% discount, $25 discount, and 5% surcharge

if __name__ == "__main__":
    suite = unittest.defaultTestLoader.discover(".", pattern="test.py")
    print(f"Running {suite.countTestCases()} tests:")
    result = xmlrunner.XMLTestRunner(output='test-reports').run(suite)
    print(f"Ran {result.testsRun} tests, {len(result.failures)} failed, {len(result.errors)} errors.")
