"""Convert all Markdown files to Word format."""

from docx import Document
from docx.shared import Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
from pathlib import Path
import re

def markdown_to_word(md_path, output_path):
    """Convert a markdown file to Word format."""
    with open(md_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    doc = Document()
    
    lines = content.split('\n')
    in_code_block = False
    in_list = False
    
    for line in lines:
        stripped = line.strip()
        
        # Code blocks
        if stripped.startswith('```'):
            in_code_block = not in_code_block
            continue
        
        if in_code_block:
            p = doc.add_paragraph(line)
            p.style = 'No Spacing'
            continue
        
        # Headers
        if stripped.startswith('# '):
            doc.add_heading(stripped[2:], 0)
        elif stripped.startswith('## '):
            doc.add_heading(stripped[3:], 1)
        elif stripped.startswith('### '):
            doc.add_heading(stripped[4:], 2)
        elif stripped.startswith('#### '):
            doc.add_heading(stripped[5:], 3)
        elif stripped.startswith('##### '):
            doc.add_heading(stripped[6:], 4)
        elif stripped.startswith('###### '):
            doc.add_heading(stripped[7:], 5)
        
        # Horizontal rule
        elif stripped.startswith('---') or stripped.startswith('***'):
            doc.add_paragraph('_' * 50)
        
        # Lists
        elif stripped.startswith('- ') or stripped.startswith('* '):
            p = doc.add_paragraph(stripped[2:], style='List Bullet')
        elif stripped.startswith('1. '):
            p = doc.add_paragraph(stripped[3:], style='List Number')
        
        # Empty lines
        elif not stripped:
            doc.add_paragraph()
        
        # Regular paragraphs
        else:
            # Handle inline formatting
            text = stripped
            # Bold
            text = re.sub(r'\*\*(.*?)\*\*', r'\1', text)
            # Italic
            text = re.sub(r'\*(.*?)\*', r'\1', text)
            # Code
            text = re.sub(r'`(.*?)`', r'\1', text)
            
            if text:
                doc.add_paragraph(text)
    
    doc.save(output_path)
    print(f"Converted: {md_path.name} -> {output_path.name}")

def convert_all_md_files():
    """Convert all markdown files in the Report_Submission_New folder."""
    base_path = Path('C:/Users/Nishant/OneDrive/Desktop/Submission_Folder/Report_Submission_New')
    
    md_files = list(base_path.rglob('*.md'))
    
    for md_file in md_files:
        if md_file.name == 'step3-visual-label-review.DOCX.md':
            continue  # Skip this one as it seems to already be DOCX
        
        output_file = md_file.with_suffix('.docx')
        try:
            markdown_to_word(md_file, output_file)
        except Exception as e:
            print(f"Error converting {md_file.name}: {e}")

if __name__ == "__main__":
    convert_all_md_files()
