import unittest

class UrlQueryTestCase(unittest.TestCase):
    def setUp(self):
        self.baseurl = 'https://wwwn.cdc.gov/ARIsolateBank/Panel/IsolateDetail?IsolateID='

    def test_fail_table(self):
        self.assertEqual(self.widget.size(), (50,50),
                         'incorrect default size')

    def test_widget_resize(self):
        self.widget.resize(100,150)
        self.assertEqual(self.widget.size(), (100,150),
                         'wrong size after resize')
