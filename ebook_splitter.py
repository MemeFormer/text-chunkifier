import os
import ebooklib
from ebooklib import epub
from bs4 import BeautifulSoup
import PyPDF2
import re

def clean_html_content(html_content):
    """Remove HTML tags and clean up the text."""
    soup = BeautifulSoup(html_content, 'html.parser')
    return soup.get_text().strip()

def process_epub(file_path, output_dir):
    """Process EPUB files and extract chapters."""
    book = epub.read_epub(file_path)
    chapters = []
    
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    chapter_number = 1
    for item in book.get_items():
        if item.get_type() == ebooklib.ITEM_DOCUMENT:
            content = item.get_content().decode('utf-8')
            clean_content = clean_html_content(content)
            
            if clean_content.strip():  # Only process non-empty content
                output_file = os.path.join(output_dir, f'chapter_{chapter_number}.txt')
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write(clean_content)
                print(f"Created {output_file}")
                chapter_number += 1

def process_txt(file_path, output_dir):
    """Process TXT files and split into chapters."""
    os.makedirs(output_dir, exist_ok=True)
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Split by "Chapter" keyword (can be customized based on your needs)
    chapters = re.split(r'(?i)chapter\s+\d+', content)
    
    # Write each chapter to a separate file
    for i, chapter in enumerate(chapters[1:], 1):  # Skip first split if it's empty
        output_file = os.path.join(output_dir, f'chapter_{i}.txt')
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(chapter.strip())
        print(f"Created {output_file}")

def main():
    # Get input from user
    file_path = input("Enter the path to your ebook file: ").strip()
    output_dir = input("Enter the output directory path (default: ./chapters): ").strip() or "./chapters"
    
    if not os.path.exists(file_path):
        print("Error: File not found!")
        return
    
    # Process based on file extension
    if file_path.lower().endswith('.epub'):
        process_epub(file_path, output_dir)
    elif file_path.lower().endswith('.txt'):
        process_txt(file_path, output_dir)
    else:
        print("Unsupported file format. Please use EPUB or TXT files.")

if __name__ == "__main__":
    main()