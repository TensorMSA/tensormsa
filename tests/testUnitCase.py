from unittest import TestCase
#from django.utils import unittest
import unitCase

TestMethod = unitCase.TestMethod()

class testUnitCase(TestCase):

    def setUp(self):
        print('Start HOYA AI test 1')

    def tearDown(self):
        print('Finish HOYA AI test 2')

    def test_returnValue(self):
        print('Finish HOYA AI test 3')
        self.assertEqual(TestMethod.returnString(), 'successful')

    def test_upper(self):
        print('Finish HOYA AI test 4')
        test = 'test'
        self.assertEqual(TestMethod.returnUpper(test), 'TEST')

    def test_isupper(self):
        test = 'TEST'
        self.assertTrue(TestMethod.checkUpper(test))
        #self.assertFalse(TestMethod.checkUpper(test))

    def test_split(self):
        test = 'HOYAAI Test'
        # check that s.split fails when the separator is not a string
        self.assertRaises(TypeError, TestMethod.splitString(test))
        self.assertEqual(TestMethod.splitString(test), ['HOYAAI', 'Test'])
