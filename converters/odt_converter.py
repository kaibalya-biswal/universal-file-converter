from .base import BaseConverter
from odf.opendocument import OpenDocumentText
from odf.text import P
from odf.style import Style, TextProperties

class ODTConverter(BaseConverter):
    def __init__(self):
        super().__init__()
        self.supported_extensions = ['odt']
    
    def convert(self, input_text, output_path, options=None):
        self.validate_input(input_text)
        self.ensure_output_dir(output_path)
        
        doc = OpenDocumentText()
        
        lines = input_text.split('\n')
        for line in lines:
            if line.strip():
                para = P(text=line)
                doc.text.addElement(para)
            else:
                para = P()
                doc.text.addElement(para)
        
        doc.save(output_path)
        return output_path
