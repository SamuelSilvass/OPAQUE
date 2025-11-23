"""
OPAQUE Visual Tester - Professional GUI Application
A beautiful, user-friendly interface for testing OPAQUE validators
Perfect for non-programmers and demonstrations
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from opaque import Validators

class OpaqueVisualTester:
    def __init__(self, root):
        self.root = root
        self.root.title("OPAQUE Visual Tester - Professional Validator Testing")
        self.root.geometry("1200x800")
        self.root.configure(bg='#1e1e2e')
        
        # Configure style
        self.setup_styles()
        
        # Create main container
        main_container = ttk.Frame(root, style='Main.TFrame')
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Title
        title_label = ttk.Label(
            main_container,
            text="🛡️ OPAQUE VALIDATOR TESTER",
            style='Title.TLabel'
        )
        title_label.pack(pady=(0, 20))
        
        # Create two-column layout
        content_frame = ttk.Frame(main_container, style='Main.TFrame')
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Left panel - Input
        left_panel = ttk.Frame(content_frame, style='Panel.TFrame')
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        # Right panel - Results
        right_panel = ttk.Frame(content_frame, style='Panel.TFrame')
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(10, 0))
        
        self.create_input_panel(left_panel)
        self.create_results_panel(right_panel)
        
        # Status bar
        self.create_status_bar(main_container)
        
    def setup_styles(self):
        style = ttk.Style()
        style.theme_use('clam')
        
        # Main frame
        style.configure('Main.TFrame', background='#1e1e2e')
        style.configure('Panel.TFrame', background='#2d2d44', relief='raised', borderwidth=2)
        
        # Title
        style.configure('Title.TLabel',
                       background='#1e1e2e',
                       foreground='#89dceb',
                       font=('Segoe UI', 24, 'bold'))
        
        # Section headers
        style.configure('Header.TLabel',
                       background='#2d2d44',
                       foreground='#cdd6f4',
                       font=('Segoe UI', 14, 'bold'))
        
        # Normal labels
        style.configure('Normal.TLabel',
                       background='#2d2d44',
                       foreground='#cdd6f4',
                       font=('Segoe UI', 10))
        
        # Buttons
        style.configure('Action.TButton',
                       background='#89b4fa',
                       foreground='#1e1e2e',
                       font=('Segoe UI', 11, 'bold'),
                       borderwidth=0,
                       focuscolor='none')
        
        style.map('Action.TButton',
                 background=[('active', '#74c7ec')])
        
        # Combobox
        style.configure('TCombobox',
                       fieldbackground='#313244',
                       background='#313244',
                       foreground='#cdd6f4',
                       arrowcolor='#89b4fa')
        
    def create_input_panel(self, parent):
        # Header
        header = ttk.Label(parent, text="📝 INPUT", style='Header.TLabel')
        header.pack(pady=(10, 20))
        
        # Validator selection
        validator_frame = ttk.Frame(parent, style='Panel.TFrame')
        validator_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(validator_frame, text="Select Validator:", style='Normal.TLabel').pack(anchor=tk.W, pady=5)
        
        self.validator_var = tk.StringVar()
        self.validator_combo = ttk.Combobox(
            validator_frame,
            textvariable=self.validator_var,
            state='readonly',
            font=('Consolas', 10)
        )
        self.validator_combo.pack(fill=tk.X, pady=5)
        
        # Populate validators
        self.populate_validators()
        self.validator_combo.current(0)
        
        # Input field
        input_frame = ttk.Frame(parent, style='Panel.TFrame')
        input_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        ttk.Label(input_frame, text="Enter Value to Validate:", style='Normal.TLabel').pack(anchor=tk.W, pady=5)
        
        self.input_text = tk.Text(
            input_frame,
            height=4,
            font=('Consolas', 12),
            bg='#313244',
            fg='#cdd6f4',
            insertbackground='#89b4fa',
            relief='flat',
            padx=10,
            pady=10
        )
        self.input_text.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Quick examples
        examples_frame = ttk.Frame(parent, style='Panel.TFrame')
        examples_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(examples_frame, text="Quick Examples:", style='Normal.TLabel').pack(anchor=tk.W, pady=5)
        
        self.examples_text = scrolledtext.ScrolledText(
            examples_frame,
            height=8,
            font=('Consolas', 9),
            bg='#313244',
            fg='#a6adc8',
            relief='flat',
            padx=10,
            pady=10,
            state='disabled'
        )
        self.examples_text.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Bind validator change to update examples
        self.validator_combo.bind('<<ComboboxSelected>>', self.update_examples)
        self.update_examples()
        
        # Validate button
        validate_btn = ttk.Button(
            parent,
            text="🔍 VALIDATE",
            style='Action.TButton',
            command=self.validate_input
        )
        validate_btn.pack(pady=20, ipadx=20, ipady=10)
        
    def create_results_panel(self, parent):
        # Header
        header = ttk.Label(parent, text="✅ RESULTS", style='Header.TLabel')
        header.pack(pady=(10, 20))
        
        # Results display
        self.results_text = scrolledtext.ScrolledText(
            parent,
            font=('Consolas', 11),
            bg='#313244',
            fg='#cdd6f4',
            relief='flat',
            padx=15,
            pady=15,
            state='disabled'
        )
        self.results_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Configure tags for colored output
        self.results_text.tag_config('success', foreground='#a6e3a1', font=('Consolas', 12, 'bold'))
        self.results_text.tag_config('error', foreground='#f38ba8', font=('Consolas', 12, 'bold'))
        self.results_text.tag_config('info', foreground='#89dceb')
        self.results_text.tag_config('header', foreground='#f9e2af', font=('Consolas', 13, 'bold'))
        
        # Action buttons
        button_frame = ttk.Frame(parent, style='Panel.TFrame')
        button_frame.pack(fill=tk.X, padx=10, pady=10)
        
        clear_btn = ttk.Button(
            button_frame,
            text="🗑️ Clear",
            style='Action.TButton',
            command=self.clear_results
        )
        clear_btn.pack(side=tk.LEFT, padx=5, ipadx=10, ipady=5)
        
        copy_btn = ttk.Button(
            button_frame,
            text="📋 Copy Results",
            style='Action.TButton',
            command=self.copy_results
        )
        copy_btn.pack(side=tk.LEFT, padx=5, ipadx=10, ipady=5)
        
    def create_status_bar(self, parent):
        status_frame = ttk.Frame(parent, style='Main.TFrame')
        status_frame.pack(fill=tk.X, pady=(10, 0))
        
        self.status_label = ttk.Label(
            status_frame,
            text="Ready to validate | Total Validators: 77+",
            style='Normal.TLabel',
            font=('Segoe UI', 9)
        )
        self.status_label.pack(side=tk.LEFT)
        
        version_label = ttk.Label(
            status_frame,
            text="OPAQUE v2.0 Professional",
            style='Normal.TLabel',
            font=('Segoe UI', 9, 'italic')
        )
        version_label.pack(side=tk.RIGHT)
        
    def populate_validators(self):
        """Populate the validator dropdown with all available validators"""
        validators = []
        
        # Helper function to recursively get validators
        def get_validators(obj, prefix=""):
            for name in dir(obj):
                if name.startswith('_'):
                    continue
                attr = getattr(obj, name)
                if isinstance(attr, type) and hasattr(attr, 'validate'):
                    validators.append(f"{prefix}{name}")
                elif isinstance(attr, type):
                    get_validators(attr, f"{prefix}{name}.")
        
        get_validators(Validators)
        validators.sort()
        
        self.validator_combo['values'] = validators
        
    def update_examples(self, event=None):
        """Update examples based on selected validator"""
        validator_name = self.validator_var.get()
        
        examples = {
            'BR.CPF': [
                '✓ Valid: 529.982.247-25',
                '✓ Valid: 123.456.789-09',
                '✗ Invalid: 111.222.333-44',
                '✗ Invalid: 000.000.000-00'
            ],
            'BR.CNPJ': [
                '✓ Valid: 11.222.333/0001-81',
                '✓ Valid: 34.028.316/0001-03',
                '✗ Invalid: 00.000.000/0000-00'
            ],
            'FINANCE.CREDIT_CARD': [
                '✓ Valid: 4532-1488-0343-6467 (Visa)',
                '✓ Valid: 5425-2334-3010-9903 (Mastercard)',
                '✓ Valid: 3782-822463-10005 (Amex)',
                '✗ Invalid: 1234-5678-9012-3456'
            ],
            'INTERNATIONAL.EMAIL': [
                '✓ Valid: user@example.com',
                '✓ Valid: john.doe@company.co.uk',
                '✗ Invalid: invalid.email',
                '✗ Invalid: @example.com'
            ],
            'INTERNATIONAL.IPV4': [
                '✓ Valid: 192.168.1.1',
                '✓ Valid: 8.8.8.8',
                '✗ Invalid: 256.1.1.1',
                '✗ Invalid: 192.168.1'
            ],
            'CL.RUT': [
                '✓ Valid: 12.345.678-5',
                '✓ Valid: 11.111.111-1',
                '✗ Invalid: 12.345.678-0'
            ],
            'AR.DNI': [
                '✓ Valid: 12345678',
                '✓ Valid: 20123456',
                '✗ Invalid: 123'
            ]
        }
        
        default_examples = [
            'Select a validator to see examples',
            'Each validator has specific rules',
            'Try different values to test!'
        ]
        
        example_list = examples.get(validator_name, default_examples)
        
        self.examples_text.config(state='normal')
        self.examples_text.delete('1.0', tk.END)
        self.examples_text.insert('1.0', '\n'.join(example_list))
        self.examples_text.config(state='disabled')
        
    def validate_input(self):
        """Validate the input using the selected validator"""
        validator_path = self.validator_var.get()
        input_value = self.input_text.get('1.0', tk.END).strip()
        
        if not input_value:
            messagebox.showwarning("No Input", "Please enter a value to validate!")
            return
        
        try:
            # Get the validator class
            parts = validator_path.split('.')
            validator = Validators
            for part in parts:
                validator = getattr(validator, part)
            
            # Validate
            is_valid = validator.validate(input_value)
            
            # Display results
            self.display_result(validator_path, input_value, is_valid)
            
            # Update status
            status = "✓ VALID" if is_valid else "✗ INVALID"
            self.status_label.config(text=f"Last validation: {status}")
            
        except Exception as e:
            self.display_error(str(e))
            self.status_label.config(text=f"Error: {str(e)[:50]}")
            
    def display_result(self, validator, value, is_valid):
        """Display validation result in the results panel"""
        self.results_text.config(state='normal')
        
        # Add separator if not first result
        if self.results_text.get('1.0', tk.END).strip():
            self.results_text.insert(tk.END, '\n' + '='*60 + '\n\n')
        
        # Header
        self.results_text.insert(tk.END, f'Validator: {validator}\n', 'header')
        self.results_text.insert(tk.END, f'Input: {value}\n', 'info')
        
        # Result
        if is_valid:
            self.results_text.insert(tk.END, '\n✓ VALID\n', 'success')
            self.results_text.insert(tk.END, 'This value passed mathematical validation!\n', 'info')
        else:
            self.results_text.insert(tk.END, '\n✗ INVALID\n', 'error')
            self.results_text.insert(tk.END, 'This value failed mathematical validation.\n', 'info')
        
        self.results_text.insert(tk.END, '\n')
        self.results_text.see(tk.END)
        self.results_text.config(state='disabled')
        
    def display_error(self, error_msg):
        """Display error message"""
        self.results_text.config(state='normal')
        self.results_text.insert(tk.END, '\n⚠️ ERROR\n', 'error')
        self.results_text.insert(tk.END, f'{error_msg}\n\n', 'info')
        self.results_text.see(tk.END)
        self.results_text.config(state='disabled')
        
    def clear_results(self):
        """Clear the results panel"""
        self.results_text.config(state='normal')
        self.results_text.delete('1.0', tk.END)
        self.results_text.config(state='disabled')
        self.status_label.config(text="Results cleared | Ready to validate")
        
    def copy_results(self):
        """Copy results to clipboard"""
        results = self.results_text.get('1.0', tk.END)
        self.root.clipboard_clear()
        self.root.clipboard_append(results)
        messagebox.showinfo("Copied", "Results copied to clipboard!")

def main():
    root = tk.Tk()
    app = OpaqueVisualTester(root)
    root.mainloop()

if __name__ == '__main__':
    main()
