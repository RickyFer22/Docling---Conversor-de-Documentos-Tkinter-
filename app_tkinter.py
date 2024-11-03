import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import json
import threading
import os
from docling.document_converter import DocumentConverter

class ModernDoclingConverterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Docling - Document Converter")
        self.root.geometry("1100x750")
        self.root.minsize(900, 600)

        # Configure theme
        self.configure_theme()
        
        # Create interface
        self.create_widgets()
        
        # Initialize DocumentConverter
        self.converter = DocumentConverter()

    def configure_theme(self):
        # Modern dark theme colors
        self.colors = {
            'bg_dark': '#1e1e1e',
            'bg_medium': '#252526',
            'bg_light': '#333333',
            'accent': '#0d7377',
            'accent_hover': '#0f8589',
            'text': '#ffffff',
            'text_dim': '#cccccc',
            'border': '#404040'
        }
        
        self.root.configure(bg=self.colors['bg_dark'])
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Configure styles
        self.style.configure('Main.TFrame', background=self.colors['bg_dark'])
        self.style.configure('Card.TFrame', background=self.colors['bg_medium'])
        self.style.configure('Main.TLabelframe', background=self.colors['bg_medium'], foreground=self.colors['text'])
        self.style.configure('Header.TLabel', background=self.colors['bg_dark'], foreground=self.colors['text'], font=('Segoe UI', 20, 'bold'))
        self.style.configure('Info.TLabel', background=self.colors['bg_medium'], foreground=self.colors['text_dim'], font=('Segoe UI', 9))
        self.style.configure('Primary.TButton', background=self.colors['accent'], foreground=self.colors['text'], font=('Segoe UI', 10), padding=8)
        self.style.map('Primary.TButton', background=[('active', self.colors['accent_hover'])])

    def create_widgets(self):
        # Main Frame
        main_frame = ttk.Frame(self.root, style='Main.TFrame', padding=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Header
        self.create_header(main_frame)
        
        # Content Frame with two columns
        content_frame = ttk.Frame(main_frame, style='Main.TFrame')
        content_frame.pack(fill=tk.BOTH, expand=True, pady=20)
        
        # Left panel - Controls
        self.create_control_panel(content_frame)
        
        # Right panel - Results
        self.create_results_panel(content_frame)

    def create_header(self, parent):
        header_frame = ttk.Frame(parent, style='Main.TFrame')
        header_frame.pack(fill=tk.X, pady=(0, 20))
        
        title = ttk.Label(header_frame, text="Docling Document Converter", style='Header.TLabel')
        title.pack(side=tk.LEFT)
        
        supported_formats = ttk.Label(header_frame, text="Supported Formats: PDF, DOCX, TXT, MD, HTML, RTF", style='Info.TLabel')
        supported_formats.pack(side=tk.RIGHT, pady=10)

    def create_control_panel(self, parent):
        control_frame = ttk.LabelFrame(parent, text="Controls", style='Main.TLabelframe', padding=15)
        control_frame.pack(side=tk.LEFT, fill=tk.BOTH, padx=(0, 10))
        
        # File Selection
        file_frame = ttk.Frame(control_frame, style='Card.TFrame')
        file_frame.pack(fill=tk.X, pady=(0, 15))
        
        self.file_path = tk.StringVar()
        self.file_entry = ttk.Entry(file_frame, textvariable=self.file_path, width=40)
        self.file_entry.pack(side=tk.LEFT, padx=(0, 10))
        
        browse_btn = ttk.Button(file_frame, text="Browse", style='Primary.TButton', command=self.browse_file)
        browse_btn.pack(side=tk.LEFT)
        
        # Conversion Options
        self.create_conversion_options(control_frame)
        
        # Progress bar, convert button, and save button
        self.create_progress_section(control_frame)

    def create_conversion_options(self, parent):
        options_frame = ttk.LabelFrame(parent, text="Options", style='Main.TLabelframe', padding=10)
        options_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Output format
        self.output_format = tk.StringVar(value="markdown")
        ttk.Label(options_frame, text="Output Format:", style='Info.TLabel').pack(anchor=tk.W)
        
        formats_frame = ttk.Frame(options_frame, style='Card.TFrame')
        formats_frame.pack(fill=tk.X, pady=5)
        
        ttk.Radiobutton(formats_frame, text="Markdown", variable=self.output_format, value="markdown").pack(side=tk.LEFT, padx=10)
        ttk.Radiobutton(formats_frame, text="JSON", variable=self.output_format, value="json").pack(side=tk.LEFT, padx=10)

    def create_progress_section(self, parent):
        progress_frame = ttk.Frame(parent, style='Card.TFrame')
        progress_frame.pack(fill=tk.X, pady=(0, 15))
        
        self.progress = ttk.Progressbar(progress_frame, orient=tk.HORIZONTAL, length=200, mode='determinate')
        self.progress.pack(fill=tk.X, pady=(0, 5))
        
        self.status_var = tk.StringVar(value="Ready to convert")
        status_label = ttk.Label(progress_frame, textvariable=self.status_var, style='Info.TLabel')
        status_label.pack(fill=tk.X)
        
        convert_btn = ttk.Button(parent, text="Convert Document", style='Primary.TButton', command=self.start_conversion)
        convert_btn.pack(fill=tk.X, pady=(0, 10))

        save_btn = ttk.Button(parent, text="Save Converted Document", style='Primary.TButton', command=self.save_document)
        save_btn.pack(fill=tk.X, pady=(0, 10))

    def create_results_panel(self, parent):
        results_frame = ttk.LabelFrame(parent, text="Results", style='Main.TLabelframe', padding=15)
        results_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Converted Text Panel
        text_frame = ttk.Frame(results_frame, style='Card.TFrame')
        text_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        ttk.Label(text_frame, text="Converted Document:", style='Info.TLabel').pack(anchor=tk.W, padx=5, pady=5)
        
        self.output_text = tk.Text(text_frame, wrap=tk.WORD, bg=self.colors['bg_light'], fg=self.colors['text'])
        self.output_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Metadata Panel
        metadata_frame = ttk.Frame(results_frame, style='Card.TFrame')
        metadata_frame.pack(side=tk.LEFT, fill=tk.BOTH, padx=(10, 0))
        
        ttk.Label(metadata_frame, text="Metadata:", style='Info.TLabel').pack(anchor=tk.W, padx=5, pady=5)
        
        self.metadata_text = tk.Text(metadata_frame, wrap=tk.WORD, bg=self.colors['bg_light'], fg=self.colors['text'])
        self.metadata_text.pack(side=tk.LEFT, fill=tk.BOTH)

    def browse_file(self):
        filetypes = (
            ('PDF files', '*.pdf'),
            ('All files', '*.*')
        )
        filename = filedialog.askopenfilename(title="Open Document", filetypes=filetypes)
        if filename:
            self.file_path.set(filename)

    def start_conversion(self):
        if not self.file_path.get():
            messagebox.showerror("Error", "Please select a file.")
            return
        threading.Thread(target=self.convert_document, daemon=True).start()

    def convert_document(self):
        try:
            self.update_progress(0, "Starting conversion...")
            result = self.converter.convert(self.file_path.get())
            
            # Choose output format
            if self.output_format.get() == "markdown":
                converted_text = result.document.export_to_markdown()
            else:
                converted_text = result.document.export_to_json()

            self.update_progress(100, "Conversion completed")
            self.display_results(converted_text, result)

        except Exception as e:
            self.update_progress(0, "Conversion error")
            messagebox.showerror("Conversion Error", str(e))

    def update_progress(self, value, status):
        self.progress['value'] = value
        self.status_var.set(status)

    def display_results(self, converted_text, result):
        self.output_text.delete(1.0, tk.END)
        self.output_text.insert(tk.END, converted_text)
        
        metadata = {
            "Filename": os.path.basename(self.file_path.get()),
            "Attributes": dir(result.document)
        }
        self.metadata_text.delete(1.0, tk.END)
        self.metadata_text.insert(tk.END, json.dumps(metadata, indent=4))

    def save_document(self):
        filetypes = [('Markdown file', '*.md'), ('JSON file', '*.json')] if self.output_format.get() == "json" else [('Markdown file', '*.md')]
        filepath = filedialog.asksaveasfilename(defaultextension=".md" if self.output_format.get() == "markdown" else ".json", filetypes=filetypes)
        
        if filepath:
            try:
                with open(filepath, 'w', encoding='utf-8') as f:
                    if self.output_format.get() == "markdown":
                        f.write(self.output_text.get(1.0, tk.END))
                    else:
                        json_data = json.loads(self.output_text.get(1.0, tk.END))
                        json.dump(json_data, f, ensure_ascii=False, indent=4)
                messagebox.showinfo("Success", "Document saved successfully.")
            except Exception as e:
                messagebox.showerror("Save Error", str(e))

if __name__ == "__main__":
    root = tk.Tk()
    app = ModernDoclingConverterApp(root)
    root.mainloop()
