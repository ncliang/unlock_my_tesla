import unittest

import lambda_function


class LamdaFunctionTest(unittest.TestCase):
    def test_unlock(self):
        lambda_function.lambda_handler({'clickType': 'SINGLE'}, None)

    def test_pop_frunk(self):
        lambda_function.lambda_handler({'clickType': 'DOUBLE'}, None)


if __name__ == '__main__':
    unittest.main()
