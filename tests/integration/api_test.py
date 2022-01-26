from django.test import TestCase


class ApiTests(TestCase):
    def test_api_root(self):
        """
        Test if all api end-points are available.
        """
        response = self.client.get('/api/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 11)
        self.assertContains(response, 'effectors')
        self.assertNotContains(response, 'promoters')
