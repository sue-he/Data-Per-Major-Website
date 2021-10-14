import unittest
from datasource import *


class DataSourceTester(unittest.TestCase):
    def test_CheckIfMajorExists(self):
        major = 'Psychology'
        ds = DataSource()
        test_var = ds.getMaxInstitutionPopularity(major)
        self.assertEqual(test_var[0][0], "Private, non-profit institution")
        self.assertEqual(test_var[0][1], 888)

    def test_ReturnMaxOfNonExistentMajor(self):
        major = 'adsfa;dsf'
        ds = DataSource()
        test_var = ds.getMaxInstitutionPopularity(major)
        self.assertEqual(test_var, None)

    def test_ReturnNumberOfMaxInstitutions(self):
        major = 'Sample major'
        ds = DataSource()
        test_var = ds.getMaxInstitutionPopularity(major)
        self.assertEqual(test_var[0][0], "Private, non-profit institution")
        self.assertEqual(test_var[1][0], "Public institution")
        self.assertEqual(test_var[0][1], 50)
        self.assertEqual(test_var[1][1], 50)

if __name__ == '__main__':
    unittest.main()