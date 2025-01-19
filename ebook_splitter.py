import os
import ebooklib
from ebooklib import epub
from bs4 import BeautifulSoup
import PyPDF2
import re
import tkinter as tk
from tkinter import filedialog, messagebox
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.tableview import Tableview
from ttkbootstrap.scrolled import ScrolledFrame

class ChapterSplitterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Ebook Chapter Splitter")
        self.root.geometry("800x600")
        
        # Store chapters info
        self.chapters = []
        self.output_dir = os.path.join(os.path.expanduser("~"), "Downloads", "chapters")
        
        self.create_widgets()
        
    def create_widgets(self):
        # File selection frame
        file_frame = ttk.Frame(self.root, padding="10")
        file_frame.pack(fill=X, padx=5, pady=5)
        
        ttk.Button(
            file_frame, 
            text="Select Ebook", 
            command=self.select_file,
            style='primary.TButton'
        ).pack(side=LEFT, padx=5)
        
        ttk.Button(
            file_frame, 
            text="Change Output Directory", 
            command=self.select_output_dir
        ).pack(side=LEFT, padx=5)
        
        # Output directory label
        self.dir_label = ttk.Label(file_frame, text=f"Output: {self.output_dir}")
        self.dir_label.pack(side=LEFT, padx=5)
        
        # Create table frame
        table_frame = ttk.Frame(self.root, padding="10")
        table_frame.pack(fill=BOTH, expand=YES, padx=5, pady=5)
        
        # Configure table columns
        columns = [
            {"text": "Chapter", "stretch": False, "width": 70},
            {"text": "Size (bytes)", "stretch": False, "width": 100},
            {"text": "Preview", "stretch": True},
        ]
        
        self.table = Tableview(
            table_frame,
            coldata=columns,
            searchable=False,
            autofit=False,
            height=20,
        )
        self.table.pack(fill=BOTH, expand=YES)
        
        # Download buttons frame
        download_frame = ttk.Frame(self.root, padding="10")
        download_frame.pack(fill=X, padx=5, pady=5)
        
        ttk.Button(
            download_frame,
            text="Download Selected",
            command=self.download_selected,
            style='primary.TButton'
        ).pack(side=LEFT, padx=5)
        
        ttk.Button(
            download_frame,
            text="Download All",
            command=self.download_all,
            style='secondary.TButton'
        ).pack(side=LEFT, padx=5)

    def select_file(self):
        file_path = filedialog.askopenfilename(
            filetypes=[
                ("Ebook files", "*.epub *.txt"),
                ("EPUB files", "*.epub"),
                ("Text files", "*.txt"),
                ("All files", "*.*")
            ]
        )
        if file_path:
            self.process_file(file_path)
    
    def select_output_dir(self):
        dir_path = filedialog.askdirectory(
            initialdir=self.output_dir,
            title="Select Output Directory"
        )
        if dir_path:
            self.output_dir = dir_path
            self.dir_label.config(text=f"Output: {self.output_dir}")

    def clean_html_content(self, html_content):
        """Remove HTML tags and clean up the text."""
        soup = BeautifulSoup(html_content, 'html.parser')
        return soup.get_text().strip()

    def process_epub(self, file_path):
        """Process EPUB files and extract chapters."""
        book = epub.read_epub(file_path)
        self.chapters = []
        
        chapter_number = 1
        for item in book.get_items():
            if item.get_type() == ebooklib.ITEM_DOCUMENT:
                content = item.get_content().decode('utf-8')
                clean_content = clean_html_content(content)
                
                if clean_content.strip():
                    self.chapters.append({
                        'number': chapter_number,
                        'content': clean_content,
                        'size': len(clean_content)
                    })
                    chapter_number += 1
        
        self.update_table()

    def process_txt(self, file_path):
        """Process TXT files and split into chapters."""
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Split by "Chapter" keyword
        chapter_texts = re.split(r'(?i)chapter\s+\d+', content)
        self.chapters = []
        
        for i, chapter_text in enumerate(chapter_texts[1:], 1):
            clean_text = chapter_text.strip()
            if clean_text:
                self.chapters.append({
                    'number': i,
                    'content': clean_text,
                    'size': len(clean_text)
                })
        
        self.update_table()

    def process_file(self, file_path):
        try:
            if file_path.lower().endswith('.epub'):
                self.process_epub(file_path)
            elif file_path.lower().endswith('.txt'):
                self.process_txt(file_path)
            else:
                messagebox.showerror("Error", "Unsupported file format")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to process file: {str(e)}")

    def update_table(self):
        # Clear existing rows
        self.table.delete_rows()
        
        # Add new rows
        for chapter in self.chapters:
            preview = chapter['content'][:100] + "..." if len(chapter['content']) > 100 else chapter['content']
            self.table.insert_row('end', [
                f"Chapter {chapter['number']}", 
                f"{chapter['size']:,}", 
                preview
            ])

    def save_chapter(self, chapter):
        """Save a single chapter to a file."""
        os.makedirs(self.output_dir, exist_ok=True)
        output_file = os.path.join(self.output_dir, f'chapter_{chapter["number"]}.txt')
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(chapter['content'])
        return output_file

    def download_selected(self):
        selected_indices = self.table.get_rows(selected=True)
        if not selected_indices:
            messagebox.showinfo("Info", "No chapters selected")
            return
            
        saved_files = []
        for idx in selected_indices:
            chapter = self.chapters[idx]
            saved_files.append(self.save_chapter(chapter))
        
        messagebox.showinfo("Success", f"Saved {len(saved_files)} chapters to {self.output_dir}")

    def download_all(self):
        if not self.chapters:
            messagebox.showinfo("Info", "No chapters to download")
            return
            
        saved_files = []
        for chapter in self.chapters:
            saved_files.append(self.save_chapter(chapter))
        
        messagebox.showinfo("Success", f"Saved all {len(saved_files)} chapters to {self.output_dir}")

def main():
    root = ttk.Window(themename="darkly")
    app = ChapterSplitterApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()