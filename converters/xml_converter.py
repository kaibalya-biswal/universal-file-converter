from .base import BaseConverter
import xml.etree.ElementTree as ET
import html

class XMLConverter(BaseConverter):
    def __init__(self):
        super().__init__()
        self.supported_extensions = ['xml']
    
    def convert(self, input_text, output_path, options=None):
        self.validate_input(input_text)
        self.ensure_output_dir(output_path)
        
        root = ET.Element('document')
        root.set('type', 'text')
        
        lines = input_text.split('\n')
        for idx, line in enumerate(lines, start=1):
            line_elem = ET.SubElement(root, 'line')
            line_elem.set('number', str(idx))
            line_elem.text = html.escape(line)
        
        tree = ET.ElementTree(root)
        ET.indent(tree, space='  ')
        tree.write(output_path, encoding='utf-8', xml_declaration=True)
        
        return output_path
