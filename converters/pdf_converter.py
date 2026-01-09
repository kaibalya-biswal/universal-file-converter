from .base import BaseConverter
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch

class PDFConverter(BaseConverter):
    def __init__(self):
        super().__init__()
        self.supported_extensions = ['pdf']
    
    def convert(self, input_text, output_path, options=None):
        self.validate_input(input_text)
        self.ensure_output_dir(output_path)
        
        doc = SimpleDocTemplate(output_path, pagesize=letter)
        styles = getSampleStyleSheet()
        story = []
        
        lines = input_text.split('\n')
        for line in lines:
            if line.strip():
                para = Paragraph(line.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;'), styles['Normal'])
                story.append(para)
                story.append(Spacer(1, 0.2*inch))
            else:
                story.append(Spacer(1, 0.2*inch))
        
        doc.build(story)
        return output_path
