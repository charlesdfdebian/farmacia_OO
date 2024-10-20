# test_math_functions.py
import unittest
from math_functions import soma
from models.clientes import Clientes
from models.usuario import Usuario
from db_config import get_db_connection



class TestecClienteUsuario(unittest.TestCase):
    def test_soma(self):
        self.assertEqual(soma(2, 3), 5)
        self.assertEqual(soma(-1, 1), 0)
        self.assertEqual(soma(0, 0), 0)

if __name__ == '__main__':
    unittest.main()
