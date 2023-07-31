import unittest
import tempfile
import os
import json
from generate_xml import convert_input_to_xml

class TestConvertInputToXML(unittest.TestCase):

    def setUp(self):
        # Create temporary input and defaults JSON files for testing
        self.input_file_content = "init,workers=10,containers=1-5\nprepare,workers=20,containers=1-10,objects=1-50,sizes=2\nmain[,workers=30,containers=1-10,objects=1-10,sizes=4,pgd=100 0 0,runtime=0,totalOps=0,totalBytes=100\ncleanup,workers=40,containers=1-10,objects=1-50\n"
        self.defaults_file_content = '{"cluster_address": "10.105.10.80", "workers": 30, "start_containers": 1, "end_containers": 10, "start_objects": 1, "end_objects": 10, "sizes": 4, "put": 100, "get": 0, "delete": 0, "delay": 5}'
        
        self.input_file = tempfile.NamedTemporaryFile(mode='w', delete=False)
        self.input_file.write(self.input_file_content)
        self.input_file.close()

        self.defaults_file = tempfile.NamedTemporaryFile(mode='w', delete=False)
        self.defaults_file.write(self.defaults_file_content)
        self.defaults_file.close()

        # Create temporary output XML file for testing
        self.output_file = tempfile.NamedTemporaryFile(mode='w', delete=False)
        self.output_file.close()

    def tearDown(self):
        # Remove temporary files after the test
        os.remove(self.input_file.name)
        os.remove(self.defaults_file.name)
        os.remove(self.output_file.name)

    def test_convert_input_to_xml(self):
        # Call the function with the temporary files
        convert_input_to_xml(self.input_file.name, self.defaults_file.name, self.output_file.name)

        # Read the contents of the generated XML file
        with open(self.output_file.name, 'r') as xml_file:
            xml_content = xml_file.read()

        # Define the expected XML content for the "init" command
        expected_init_xml = '<?xml version="1.0" encoding="UTF-8" ?>\n<workload name="swift-sample" description="sample benchmark for swift">\n  <storage type="swift" />\n  <auth type="swauth" config="username=test:tester;password=testing;auth_url=http://10.105.10.80:8080/auth/v1.0" />\n  <workflow>\n\n    <workstage name="init">\n      <work type="init" workers="10" config="containers=r(1,5)" />\n    </workstage>\n\n    <workstage name="prepare">\n      <work type="prepare" workers="20" config="containers=r(1,10);objects=r(1,50);sizes=c(2)KB" />\n    </workstage>\n\n    <workstage name="main">\n    </workstage>\n\n  </workflow>\n</workload>\n'

        # Assert that the generated XML content matches the expected content for the "init" command
        self.assertEqual(xml_content.strip(), expected_init_xml.strip())

if __name__ == '__main__':
    unittest.main()
