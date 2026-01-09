from .base import BaseConverter
from ebooklib import epub
import html

class EPUBConverter(BaseConverter):
    def __init__(self):
        super().__init__()
        self.supported_extensions = ['epub']
    
    def convert(self, input_text, output_path, options=None):
        self.validate_input(input_text)
        self.ensure_output_dir(output_path)
        
        book = epub.EpubBook()
        book.set_identifier('converted_text')
        book.set_title('Converted Document')
        book.set_language('en')
        book.add_author('Text Converter')
        
        escaped_text = html.escape(input_text)
        lines = escaped_text.split('\n')
        html_lines = ['<p>' + line + '</p>' if line.strip() else '<br/>' for line in lines]
        
        chapter = epub.EpubHtml(title='Content', file_name='content.xhtml', lang='en')
        chapter.content = ''.join(html_lines)
        
        book.add_item(chapter)
        book.toc = [chapter]
        book.spine = ['nav', chapter]
        
        book.add_item(epub.EpubNcx())
        book.add_item(epub.EpubNav())
        
        epub.write_epub(output_path, book)
        return output_path
