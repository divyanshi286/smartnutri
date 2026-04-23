#!/usr/bin/env python3
"""
Convert Markdown files to PDF
Usage: python convert_to_pdf.py
"""

import os
import re
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT, TA_JUSTIFY

# Files to convert
files_to_convert = [
    'FREE_DEPLOYMENT_GUIDE.md',
    'ROADMAP.md'
]

class MarkdownToPDF:
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self.style_dict = {}
        self.setup_styles()
    
    def setup_styles(self):
        """Setup custom styles for markdown elements"""
        self.style_dict['h1'] = ParagraphStyle(
            'h1',
            parent=self.styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#2c3e50'),
            spaceAfter=12,
            spaceBefore=12,
            borderPadding=10,
            borderRadius=2
        )
        self.style_dict['h2'] = ParagraphStyle(
            'h2',
            parent=self.styles['Heading2'],
            fontSize=18,
            textColor=colors.HexColor('#2c3e50'),
            spaceAfter=10,
            spaceBefore=10
        )
        self.style_dict['h3'] = ParagraphStyle(
            'h3',
            parent=self.styles['Heading3'],
            fontSize=14,
            textColor=colors.HexColor('#34495e'),
            spaceAfter=8,
            spaceBefore=8
        )
        self.style_dict['body'] = ParagraphStyle(
            'body',
            parent=self.styles['BodyText'],
            fontSize=11,
            alignment=TA_JUSTIFY,
            spaceAfter=10
        )
        self.style_dict['code'] = ParagraphStyle(
            'code',
            parent=self.styles['BodyText'],
            fontSize=9,
            fontName='Courier',
            leftIndent=20,
            rightIndent=20,
            spaceAfter=10,
            backColor=colors.HexColor('#f5f5f5')
        )
    
    def parse_markdown(self, content):
        """Parse markdown content and return list of reportlab elements"""
        elements = []
        lines = content.split('\n')
        i = 0
        
        while i < len(lines):
            line = lines[i]
            
            # Skip empty lines
            if not line.strip():
                elements.append(Spacer(1, 0.1*inch))
                i += 1
                continue
            
            # H1
            if line.startswith('# '):
                text = line[2:].strip()
                elements.append(Paragraph(text, self.style_dict['h1']))
                elements.append(Spacer(1, 0.2*inch))
                i += 1
            
            # H2
            elif line.startswith('## '):
                text = line[3:].strip()
                elements.append(Paragraph(text, self.style_dict['h2']))
                elements.append(Spacer(1, 0.15*inch))
                i += 1
            
            # H3
            elif line.startswith('### '):
                text = line[4:].strip()
                elements.append(Paragraph(text, self.style_dict['h3']))
                elements.append(Spacer(1, 0.1*inch))
                i += 1
            
            # Code block
            elif line.startswith('```'):
                code_lines = []
                i += 1
                while i < len(lines) and not lines[i].startswith('```'):
                    code_lines.append(lines[i])
                    i += 1
                if code_lines:
                    code_text = '\n'.join(code_lines)
                    elements.append(Paragraph(f"<font color=\"#2c3e50\"><b>Code:</b></font>", self.style_dict['h3']))
                    elements.append(Paragraph(code_text.replace('<', '&lt;').replace('>', '&gt;'), self.style_dict['code']))
                    elements.append(Spacer(1, 0.1*inch))
                i += 1
            
            # Regular content
            else:
                # Convert markdown formatting
                text = line.strip()
                text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', text)  # Bold
                text = re.sub(r'\*(.*?)\*', r'<i>\1</i>', text)      # Italic
                text = re.sub(r'\`(.*?)\`', r'<font face="Courier" size="9">\1</font>', text)  # Inline code
                
                elements.append(Paragraph(text, self.style_dict['body']))
                i += 1
        
        return elements
    
    def convert(self, markdown_file):
        """Convert markdown file to PDF"""
        output_file = markdown_file.replace('.md', '.pdf')
        
        try:
            print(f"Converting {markdown_file} to {output_file}...")
            
            # Read markdown file
            with open(markdown_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Create PDF document
            doc = SimpleDocTemplate(output_file, pagesize=letter)
            story = self.parse_markdown(content)
            
            # Build PDF
            doc.build(story)
            print(f"✅ Successfully created: {output_file}")
            return True
            
        except Exception as e:
            print(f"❌ Error converting {markdown_file}: {str(e)}")
            import traceback
            traceback.print_exc()
            return False


def main():
    print("=" * 60)
    print("Markdown to PDF Converter")
    print("=" * 60)
    
    converter = MarkdownToPDF()
    success_count = 0
    
    for markdown_file in files_to_convert:
        if os.path.exists(markdown_file):
            if converter.convert(markdown_file):
                success_count += 1
        else:
            print(f"❌ File not found: {markdown_file}")
    
    print("\n" + "=" * 60)
    print(f"Conversion Complete: {success_count}/{len(files_to_convert)} files")
    print("=" * 60)
    
    # List generated PDFs
    print("\nGenerated PDFs:")
    for markdown_file in files_to_convert:
        pdf_file = markdown_file.replace('.md', '.pdf')
        if os.path.exists(pdf_file):
            size_kb = os.path.getsize(pdf_file) / 1024
            print(f"  ✓ {pdf_file} ({size_kb:.1f} KB)")

if __name__ == '__main__':
    main()
