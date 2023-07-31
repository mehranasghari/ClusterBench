import os
import tempfile
import xml.etree.ElementTree as ET
import unittest
from generate_xml import convert_input_to_xml
 

class TestConvertInputToXml(unittest.TestCase):
    def setUp(self):
        self.input_data = 'init,workers=10,containers=1-10\nprepare,workers=20,containers=1-5,objects=1-100,sizes=1024\nmain[,workers=30,containers=1-5,objects=1-100,sizes=1024,pgd=0.6 0.3 0.1,runtime=3600]\ncleanup,workers=10,containers=1-10,objects=1-100\ndelay,time=600\ndispose,workers=10,containers=1-10'

        self.defaults_data = '{"cluster_address": "127.0.0.1", "workers": 10, "start_containers": 1, "end_containers": 10, "start_objects": 1, "end_objects": 100, "sizes": 1024, "put": 0.6, "get": 0.3, "delete": 0.1, "delay": 0}'

    def test_convert_input_to_xml(self):
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as input_file, \
             tempfile.NamedTemporaryFile(mode='w', delete=False) as defaults_file, \
             tempfile.NamedTemporaryFile(mode='w', delete=False) as output_file:

            input_file.write(self.input_data)
            defaults_file.write(self.defaults_data)

            input_file.flush()
            defaults_file.flush()

            convert_input_to_xml(input_file.name, defaults_file.name, output_file.name)

            output_file.flush()

            # Check that the output file is valid XML by parsing it with ElementTree
            try:
                ET.parse(output_file.name)
            except ET.ParseError:
                self.fail('Output file contains invalid XML')

            # Check that the output file is not empty
            self.assertGreater(os.stat(output_file.name).st_size, 0, 'Output file is empty')