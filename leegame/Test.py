import unittest


class A:
    a = 10

aa = A()
aa.aaa = A()


class MyTestCase(unittest.TestCase):
    aa = A()
    def test_something(self):
        print(1)
        self.assertEqual(False, False)
    def test_aa(self):
        print(aa.aaa.a)





if __name__ == '__main__':
    unittest.main()
