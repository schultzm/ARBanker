import unittest
from ..tests.test_isolate import IsolateTestCasePass, IsolateTestCaseFail

def suite():
    """
    This is the test suite.
    """
    suite = unittest.TestSuite()
    suite.addTest(IsolateTestCasePass('test_hit_url'))
    suite.addTest(IsolateTestCasePass('test_hit_xml'))
    suite.addTest(IsolateTestCasePass('test_render_metadatatable'))
    suite.addTest(IsolateTestCasePass('test_render_datatables'))

    suite.addTest(IsolateTestCaseFail('test_hit_url'))
    suite.addTest(IsolateTestCaseFail('test_hit_xml'))
    suite.addTest(IsolateTestCaseFail('test_render_metadatatable'))
    suite.addTest(IsolateTestCaseFail('test_render_datatables'))
    return suite
