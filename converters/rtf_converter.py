from .base import BaseConverter
import html

class RTFConverter(BaseConverter):
    def __init__(self):
        super().__init__()
        self.supported_extensions = ['rtf']
    
    def convert(self, input_text, output_path, options=None):
        self.validate_input(input_text)
        self.ensure_output_dir(output_path)
        
        def escape_rtf(text):
            text = text.replace('\\', '\\\\')
            text = text.replace('{', '\\{')
            text = text.replace('}', '\\}')
            text = text.replace('\n', '\\par\n')
            return text
        
        rtf_content = r"""{\rtf1\ansi\deff0
{\fonttbl{\f0 Times New Roman;}}
\f0\fs24
"""
        rtf_content += escape_rtf(input_text)
        rtf_content += "\n}"
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(rtf_content)
        
        return output_path
