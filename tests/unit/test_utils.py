from unittest import TestCase
from result_server import verify_file_ext


class TestUtils(TestCase):

    def test_verify_file_ext(self):
        connection_conf_file = verify_file_ext("connections.cfg", ".cfg")
        self.assertEqual(connection_conf_file, "connections.cfg")
