import unittest
from pathlib import Path
from ..utils.isolate import Isolate

PASS_NO = 1
FAIL_NO = 1000000000

class IsolateTestCasePass(unittest.TestCase):
    def setUp(self):
        self.isolate = Isolate(PASS_NO, Path.home() / 'arbanker_test')

    def test_hit_url(self):
        self.assertEqual(self.isolate.target,
                         self.isolate.basetarget+str("{:04d}".format(PASS_NO)))
    
    def test_hit_xml(self):
        self.assertIn('Metadata', self.isolate.hit_xml())

    def test_render_metadatatable(self):
        self.assertFalse(self.isolate.render_metadatatable(
                         self.isolate.hit_xml()['Metadata']).empty
                         )

    def test_render_datatables(self):
        self.assertFalse(self.isolate.render_datatable(
                         self.isolate.hit_xml()['MIC']).empty
                         )
        self.assertFalse(self.isolate.render_datatable(
                         self.isolate.hit_xml()['MMR']).empty
                         )

class IsolateTestCaseFail(unittest.TestCase):
    def setUp(self):
        self.isolate = Isolate(FAIL_NO, Path.home() / 'ARBanker' / 'test')

    def test_hit_url(self):
        self.assertEqual(self.isolate.target,
                         self.isolate.basetarget+str("{:03d}".format(FAIL_NO)))
    
    def test_hit_xml(self):
        self.assertIn('Metadata', self.isolate.hit_xml())

    def test_render_metadatatable(self):
        self.assertTrue(self.isolate.render_metadatatable(
                        self.isolate.hit_xml()['Metadata']).empty
                        )

    def test_render_datatables(self):
        self.assertTrue(self.isolate.render_datatable(
                        self.isolate.hit_xml()['MIC']).empty
                        )
        self.assertTrue(self.isolate.render_datatable(
                        self.isolate.hit_xml()['MMR']).empty
                        )
    