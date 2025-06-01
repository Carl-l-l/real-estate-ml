import os
import sys

# Ensure the app directory is in the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import unittest
from dbr.databricks_handler import DatabricksHandler

class TestDatabricksHandler(unittest.TestCase):
    def setUp(self):
        """ Set up the DatabricksHandler instance for testing """
        self.db_handler = DatabricksHandler()

    # Test connection to Databricks
    def test_connection(self):
        """ Test if the connection to Databricks is established """
        self.assertIsNotNone(self.db_handler.connection, "Databricks connection should be established")

if __name__ == '__main__':
    unittest.main()