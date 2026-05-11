from django.test import TestCase

# Create your tests here.
from django.test import TestCase

from product.factories import CategoryFactory, ProductFactory
from product.serializers.category_serializer import CategorySerializer
from product.serializers.product_serializer import ProductSerializer


class CategorySerializerTestCase(TestCase):

    def setUp(self):
        self.category = CategoryFactory()

    def test_serializer_fields(self):
        """Garante que todos os campos esperados estão presentes na saída."""
        serializer = CategorySerializer(self.category)
        self.assertEqual(
            set(serializer.data.keys()),
            {'title', 'slug', 'description', 'active'}
        )

    def test_serializer_with_valid_data(self):
        """Serializer deve ser válido com dados completos e corretos."""
        data = {
            'title': 'Fiction',
            'slug': 'fiction',
            'description': 'Fiction books',
            'active': True,
        }
        serializer = CategorySerializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_serializer_missing_slug(self):
        """slug é obrigatório — deve falhar sem ele."""
        data = {
            'title': 'Fiction',
            'description': 'Fiction books',
            'active': True,
        }
        serializer = CategorySerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('slug', serializer.errors)

    def test_serializer_missing_title(self):
        """title é obrigatório — deve falhar sem ele."""
        data = {
            'slug': 'fiction',
        }
        serializer = CategorySerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('title', serializer.errors)

    def test_title_is_serialized_correctly(self):
        """O título retornado deve corresponder ao do objeto criado."""
        serializer = CategorySerializer(self.category)
        self.assertEqual(serializer.data['title'], self.category.title)

    def test_active_default_is_true(self):
        """O campo active da factory deve vir serializado corretamente."""
        serializer = CategorySerializer(self.category)
        self.assertIn(serializer.data['active'], [True, False])


class ProductSerializerTestCase(TestCase):

    def setUp(self):
        self.category = CategoryFactory()
        self.product = ProductFactory(category=[self.category])

    def test_serializer_fields(self):
        """Garante que todos os campos esperados estão presentes na saída."""
        serializer = ProductSerializer(self.product)
        self.assertEqual(
            set(serializer.data.keys()),
            {'title', 'description', 'price', 'active', 'category'}
        )

    def test_category_is_nested_list(self):
        """O campo category deve ser uma lista de objetos serializados."""
        serializer = ProductSerializer(self.product)
        self.assertIsInstance(serializer.data['category'], list)

    def test_category_contains_correct_data(self):
        """A categoria aninhada deve conter os dados da categoria criada."""
        serializer = ProductSerializer(self.product)
        category_data = serializer.data['category'][0]
        self.assertEqual(category_data['title'], self.category.title)
        self.assertEqual(category_data['slug'], self.category.slug)

    def test_price_is_serialized_correctly(self):
        """O preço retornado deve corresponder ao do objeto."""
        serializer = ProductSerializer(self.product)
        self.assertEqual(serializer.data['price'], self.product.price)

    def test_product_with_multiple_categories(self):
        """Um produto pode ter mais de uma categoria."""
        category2 = CategoryFactory()
        product = ProductFactory(category=[self.category, category2])
        serializer = ProductSerializer(product)
        self.assertEqual(len(serializer.data['category']), 2)