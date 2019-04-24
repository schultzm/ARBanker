import unittest
from pathlib import Path
from .utils.isolate import Isolate

class IsolateTestCase(unittest.TestCase):
    def setUp(self):
        self.isolate = Isolate(001, Path.home() / 'ARBanker' / 'test')

    def test_hit_xml(self):
        self.assertEqual(self.widget.size(), (50,50),
                         'incorrect default size')

    def test_widget_resize(self):
        self.widget.resize(100,150)
        self.assertEqual(self.widget.size(), (100,150),
                         'wrong size after resize')