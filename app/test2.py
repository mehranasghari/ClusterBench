import unittest
import os
from generate_xml import convert_input_to_xml
import random

# Define random number generator for input_Content
iw = random.randint(1,10)
ics = random.randint(1,10)
ice = random.randint(1,10)
pw = random.randint(1,10)
pcs = random.randint(1,10)
pce = random.randint(1,10)
s = random.randint(50,100)
pos = random.randint(1,10)
poe = random.randint(10,50)

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
        input_content = f'init,workers={iw},containers={ics}-{ice}\nprepare,workers={pw},containers={pcs}-{pce},objects={pos}-{poe},sizes={s}\nmain[,workers=1,containers=1-10,objects=1-100,sizes=100,pgd=100 0 0,runtime=3600]\ncleanup,workers=10,containers=1-15,objects=1-100\ndelay,time=600\n'
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

        expected_output = f'<?xml version="1.0" encoding="UTF-8" ?>\n<workload name="swift-sample" description="sample benchmark for swift">\n  <storage type="swift" />\n  <auth type="swauth" config="username=test:tester;password=testing;auth_url=http://localhost:8080/auth/v1.0" />\n  <workflow>\n\n    <workstage name="init">\n      <work type="init" workers="{iw}" config="containers=r({ics},{ice})" />\n    </workstage>\n\n    <workstage name="prepare">\n      <work type="prepare" workers="{pw}" config="containers=r({pcs},{pce});objects=r({pos},{poe});sizes=c({s})KB" />\n    </workstage>\n\n    <workstage name="main">\n      <work type="main" workers="1" config="containers=r(1,10);objects=r(1,100);sizes=c(100)KB;pgd=100 0 0;runtime=3600" />\n    </workstage>\n\n    <workstage name="cleanup">\n      <work type="cleanup" workers="10" config="containers=r(1,15);objects=r(1,100)" />\n    </workstage>\n\n    <workstage name="delay">\n      <work type="delay" time="600" />\n    </workstage>\n\n  </workflow>\n</workload>\n'
        self.assertEqual(output_content, expected_output)