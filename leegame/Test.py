import unittest
import numpy as np

class A:
    a = 10

aa = A()
aa.aaa = A()


class MyTestCase(unittest.TestCase):
    aa = A()
    def test_something(self):
        a = np.array([3, 2])
        b = np.array([2, 3])
        c = a*b
        print(c)
        self.assertEqual(False, False)
    def test_aa(self):
        print(aa.aaa.a)





if __name__ == '__main__':
    unittest.main()
