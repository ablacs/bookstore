from django.test import TestCase

# Create your tests here.
from django.test import TestCase

from order.factories import OrderFactory, UserFactory
from order.serializers.order_serializer import OrderSerializer
from product.factories import CategoryFactory, ProductFactory


class OrderSerializerTestCase(TestCase):

    def setUp(self):
        self.category = CategoryFactory()
        self.product1 = ProductFactory(category=[self.category], price=100)
        self.product2 = ProductFactory(category=[self.category], price=200)
        self.user = UserFactory()
        self.order = OrderFactory(
            user=self.user,
            product=[self.product1, self.product2]
        )

    def test_serializer_fields(self):
        """Garante que os campos product e total estão presentes."""
        serializer = OrderSerializer(self.order)
        self.assertIn('product', serializer.data)
        self.assertIn('total', serializer.data)

    def test_total_is_sum_of_product_prices(self):
        """O campo total deve ser a soma dos preços dos produtos do pedido."""
        serializer = OrderSerializer(self.order)
        expected_total = self.product1.price + self.product2.price
        self.assertEqual(serializer.data['total'], expected_total)

    def test_products_are_nested_list(self):
        """O campo product deve ser uma lista de produtos serializados."""
        serializer = OrderSerializer(self.order)
        self.assertIsInstance(serializer.data['product'], list)

    def test_correct_number_of_products(self):
        """A quantidade de produtos retornada deve bater com o pedido."""
        serializer = OrderSerializer(self.order)
        self.assertEqual(len(serializer.data['product']), 2)

    def test_total_with_single_product(self):
        """Pedido com um único produto — total deve ser o preço desse produto."""
        order = OrderFactory(user=self.user, product=[self.product1])
        serializer = OrderSerializer(order)
        self.assertEqual(serializer.data['total'], self.product1.price)

    def test_product_fields_in_order(self):
        """Cada produto no pedido deve ter os campos do ProductSerializer."""
        serializer = OrderSerializer(self.order)
        product_data = serializer.data['product'][0]
        self.assertIn('title', product_data)
        self.assertIn('price', product_data)
        self.assertIn('category', product_data)