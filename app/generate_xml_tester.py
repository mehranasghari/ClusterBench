# test_your_script.py
import unittest
import os
from generate_xml import convert_input_to_xml

iw = 10
ics = 1
ice = 5
pw = 1
pcs = 1
pce = 10
s = 100
pos = 1
poe = 50
class TestConvertInputToXml(unittest.TestCase):
    def setUp(self):
        # Create temporary input and defaults files for testing
        self.input_file = 'test_input.txt'
        self.defaults_file = 'test_defaults.json'
        self.output_file = 'test_output.xml'

    def tearDown(self):
        # Remove temporary files after testing
        os.remove(self.input_file)
        os.remove(self.defaults_file)
        os.remove(self.output_file)

    def test_convert_input_to_xml(self):
        # Create a sample input and defaults JSON for testing
        input_content = f'init,workers={iw},containers={ics}-{ice}\nprepare,workers={pw},containers={pcs}-{pce},objects={pos}-{poe},sizes={s}\n'
        defaults_content = '{"cluster_address": "localhost", "workers": 1, "start_containers": 1, "end_containers": 10, "start_objects": 1, "end_objects": 5, "sizes": 200, "put": 50, "get": 30, "delete": 20, "delay": 2}'
        
        with open(self.input_file, 'w') as f_input:
            f_input.write(input_content)

        with open(self.defaults_file, 'w') as f_defaults:
            f_defaults.write(defaults_content)

        # Call the function under test
        convert_input_to_xml(self.input_file, self.defaults_file, self.output_file)

        # Assert the content of the output XML file if it's correct
        with open(self.output_file, 'r') as f_output:
            output_content = f_output.read()

        expected_output = f'<?xml version="1.0" encoding="UTF-8" ?>\n<workload name="swift-sample" description="sample benchmark for swift">\n  <storage type="swift" />\n  <auth type="swauth" config="username=test:tester;password=testing;auth_url=http://localhost:8080/auth/v1.0" />\n  <workflow>\n\n    <workstage name="init">\n      <work type="init" workers="{iw}" config="containers=r({ics},{ice})" />\n    </workstage>\n\n    <workstage name="prepare">\n      <work type="prepare" workers="{pw}" config="containers=r({pcs},{pce});objects=r({pos},{poe});sizes=c({s})KB" />\n    </workstage>\n\n  </workflow>\n</workload>\n'
        self.assertEqual(output_content, expected_output)

if __name__ == '__main__':
    unittest.main()
