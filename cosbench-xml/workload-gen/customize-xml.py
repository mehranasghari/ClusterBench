import xml.etree.ElementTree as ET
from xml.dom import minidom
import os

def prettify(elem):
    """Return a pretty-printed XML string for the Element."""
    rough_string = ET.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    xml_content = reparsed.toprettyxml(indent="  ")
    
    # Remove the XML declaration added by minidom
    xml_lines = xml_content.split('\n')
    if xml_lines[0].strip() == '<?xml version="1.0" ?>':
        xml_content = '\n'.join(xml_lines[1:])
    
    return xml_content
    
#_#_#_#_#_#_#_#_#_# change your test config #_#_#_#_#_#_#_#_#_#

def generate_swift_config_sample():
    config = ET.Element('workload', name='swift-sample', description='sample benchmark for swift')

    storage = ET.SubElement(config, 'storage', type='swift')

    auth = ET.SubElement(config, 'auth', type='swauth',
                         config='username=test:tester;password=testing;auth_url=http://<IP>:8080/auth/v1.0')

    workflow = ET.SubElement(config, 'workflow')

    init = ET.SubElement(workflow, 'workstage', name='init')
    ET.SubElement(init, 'work', type='init', workers='1', config='containers=r(1,32)')

    prepare = ET.SubElement(workflow, 'workstage', name='prepare')
    ET.SubElement(prepare, 'work', type='prepare', workers='1', config='containers=r(1,32);objects=r(1,50);sizes=c(64)KB')

    main = ET.SubElement(workflow, 'workstage', name='main')
    work = ET.SubElement(main, 'work', name='main', workers='8', rampup='100', runtime='300')

    ET.SubElement(work, 'operation', type='read', ratio='70', config='containers=u(1,32);objects=u(1,50)')
    ET.SubElement(work, 'operation', type='write', ratio='20', config='containers=u(1,32);objects=u(51,100);sizes=c(64)KB')
    ET.SubElement(work, 'operation', type='delete', ratio='10', config='containers=c(51,100);objects=u(1,32)')

    cleanup = ET.SubElement(workflow, 'workstage', name='cleanup')
    ET.SubElement(cleanup, 'work', type='cleanup', workers='1', config='containers=r(1,32);objects=r(1,100)')

    dispose = ET.SubElement(workflow, 'workstage', name='dispose')
    ET.SubElement(dispose, 'work', type='dispose', workers='1', config='containers=r(1,32)')

#_#_#_#_#_#_#_#_#_#_# end of test config #_#_#_#_#_#_#_#_#_#_#
    
    # Save the XML content to a file with pretty formatting
    xml_content = prettify(config)

    # Generate a unique file name with a counter
    counter = 1
    filename = f'swift_config_sample_{counter}.xml'
    while os.path.exists(filename):
        counter += 1
        filename = f'swift_config_sample_{counter}.xml'

    with open(filename, 'w', encoding='utf-8') as file:
        file.write('<?xml version="1.0" encoding="UTF-8" ?>\n')
        file.write(xml_content)

    print(f"Generated {filename}")


if __name__ == "__main__":
    generate_swift_config_sample()
