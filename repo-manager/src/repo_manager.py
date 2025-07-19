#!/usr/bin/env python3
"""
Repo Manager - A Tkinter GUI application for managing idea repository
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog, scrolledtext
import json
import os
import glob
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime


class RepoManager:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("EchoForge Repo Manager")
        self.root.geometry("1200x800")
        
        # Data storage
        self.repo_data: List[Dict[str, Any]] = []
        self.current_idea: Optional[Dict[str, Any]] = None
        self.repo_file_path = "../data/REPOSITORY/repo.json"
        
        # Source data paths
        self.json_logs_path = "../data/json-logs"
        self.md_logs_path = "../data/md-logs"
        self.evaluations_path = "../data/evaluations"
        self.source_data: Dict[str, Dict[str, Any]] = {}
        
        # Load data
        self.load_repo_data()
        self.load_source_data()
        
        # Create GUI
        self.create_widgets()
        self.refresh_idea_list()
        
        # Update status with source data info
        source_weeks = len(self.source_data)
        self.status_var.set(f"Ready - Loaded {len(self.repo_data)} ideas and {source_weeks} weeks of source data")

    def load_repo_data(self):
        """Load repository data from JSON file"""
        try:
            if os.path.exists(self.repo_file_path):
                with open(self.repo_file_path, 'r', encoding='utf-8') as f:
                    self.repo_data = json.load(f)
            else:
                self.repo_data = []
                messagebox.showwarning("Warning", f"Repository file not found: {self.repo_file_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load repository data: {str(e)}")
            self.repo_data = []

    def save_repo_data(self):
        """Save repository data to JSON file"""
        try:
            # Ensure directory exists
            os.makedirs(os.path.dirname(self.repo_file_path), exist_ok=True)
            
            with open(self.repo_file_path, 'w', encoding='utf-8') as f:
                json.dump(self.repo_data, f, indent=2, ensure_ascii=False)
            messagebox.showinfo("Success", "Repository data saved successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save repository data: {str(e)}")

    def load_source_data(self):
        """Load source data from JSON logs and markdown files"""
        try:
            # Load JSON logs
            json_files = glob.glob(os.path.join(self.json_logs_path, "*.json"))
            for json_file in json_files:
                week = os.path.basename(json_file).replace('.json', '')
                with open(json_file, 'r', encoding='utf-8') as f:
                    self.source_data[week] = json.load(f)
            
            # Load markdown logs
            md_files = glob.glob(os.path.join(self.md_logs_path, "*.md"))
            for md_file in md_files:
                week = os.path.basename(md_file).replace('.md', '')
                if week not in self.source_data:
                    self.source_data[week] = {}
                with open(md_file, 'r', encoding='utf-8') as f:
                    self.source_data[week]['markdown'] = f.read()
                    
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load source data: {str(e)}")

    def get_source_information(self, idea: Dict[str, Any]) -> str:
        """Get all source information for a given idea"""
        if not idea:
            return "No idea selected"
        
        related_items = idea.get('related_items', [])
        if not related_items:
            return f"No source information found for idea: {idea.get('idea_id', 'Unknown')}"
        
        source_info = []
        source_info.append(f"# Source Information for: {idea.get('title', 'Unknown Idea')}")
        source_info.append(f"Idea ID: {idea.get('idea_id', 'Unknown')}")
        source_info.append("=" * 60)
        source_info.append("")
        
        # Group items by week to avoid repetition
        weeks_data = {}
        for item in related_items:
            week = item.get('week', 'Unknown')
            if week not in weeks_data:
                weeks_data[week] = []
            weeks_data[week].append(item)
        
        for week, items in weeks_data.items():
            source_info.append(f"## Week: {week}")
            source_info.append("")
            
            if week in self.source_data:
                week_data = self.source_data[week]
                
                # Add metadata once per week
                if 'metadata' in week_data:
                    source_info.append("### Week Metadata:")
                    source_info.append(f"- Tools Used: {', '.join(week_data['metadata'].get('tools_used', []))}")
                    source_info.append(f"- Tags: {', '.join(week_data['metadata'].get('tags', []))}")
                    source_info.append(f"- Generated: {week_data['metadata'].get('generated_at', 'Unknown')}")
                    source_info.append("")
                
                # Add all JSON sources for this week
                source_info.append("### JSON Sources:")
                source_info.append("")
                
                for item in items:
                    item_id = item.get('item_id', 'Unknown')
                    section = item.get('section', 'Unknown')
                    
                    source_info.append(f"**Item: {item_id} | Section: {section}**")
                    
                    # Find the specific item in JSON data
                    if 'items' in week_data and section in week_data['items']:
                        items_data = week_data['items'][section]
                        for item_data in items_data:
                            if item_data.get('id') == item_id:
                                source_info.append("```json")
                                source_info.append(json.dumps(item_data, indent=2, ensure_ascii=False))
                                source_info.append("```")
                                source_info.append("")
                                break
                    else:
                        source_info.append(f"⚠️ Item {item_id} not found in section {section}")
                        source_info.append("")
            else:
                source_info.append(f"⚠️ No source data found for week: {week}")
                source_info.append("")
            
            source_info.append("-" * 40)
            source_info.append("")
        
        return "\n".join(source_info)

    def get_assessment_file_path(self, idea_id: str, assessment_type: str) -> str:
        """Get the file path for an assessment file"""
        return os.path.join(self.evaluations_path, f"{idea_id}_{assessment_type}.json")

    def load_assessment(self, idea_id: str, assessment_type: str) -> Optional[Dict[str, Any]]:
        """Load an assessment file for an idea"""
        file_path = self.get_assessment_file_path(idea_id, assessment_type)
        try:
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load {assessment_type} assessment: {str(e)}")
        return None

    def save_assessment(self, idea_id: str, assessment_type: str, assessment_data: Dict[str, Any]):
        """Save an assessment file for an idea"""
        try:
            # Ensure directory exists
            os.makedirs(self.evaluations_path, exist_ok=True)
            
            file_path = self.get_assessment_file_path(idea_id, assessment_type)
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(assessment_data, f, indent=2, ensure_ascii=False)
            
            messagebox.showinfo("Success", f"{assessment_type.title()} assessment saved successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save {assessment_type} assessment: {str(e)}")

    def upload_assessment(self, assessment_type: str):
        """Upload an assessment file for the current idea"""
        if not self.current_idea:
            messagebox.showwarning("Warning", "No idea selected!")
            return
        
        idea_id = self.current_idea.get('idea_id')
        if not idea_id:
            messagebox.showerror("Error", "Idea ID is required!")
            return
        
        # Create assessment input dialog
        self.show_assessment_input_dialog(idea_id, assessment_type)

    def show_assessment_input_dialog(self, idea_id: str, assessment_type: str):
        """Show dialog for assessment input (file upload or paste)"""
        # Create dialog window
        dialog = tk.Toplevel(self.root)
        dialog.title(f"Add {assessment_type.title()} Assessment - {idea_id}")
        dialog.geometry("600x500")
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Configure window
        dialog.columnconfigure(0, weight=1)
        dialog.rowconfigure(1, weight=1)
        
        # Create main frame
        main_frame = ttk.Frame(dialog, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(1, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text=f"Add {assessment_type.title()} Assessment", font=("Arial", 12, "bold"))
        title_label.grid(row=0, column=0, pady=(0, 10))
        
        # Input method selection
        method_frame = ttk.LabelFrame(main_frame, text="Input Method", padding="10")
        method_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # File upload button
        def upload_file():
            file_path = filedialog.askopenfilename(
                title=f"Select {assessment_type.title()} Assessment JSON",
                filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
            )
            
            if file_path:
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    text_widget.delete(1.0, tk.END)
                    text_widget.insert(1.0, content)
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to read file: {str(e)}")
        
        ttk.Button(method_frame, text="📁 Upload JSON File", command=upload_file).pack(side=tk.LEFT, padx=(0, 10))
        
        # Clear button
        def clear_text():
            text_widget.delete(1.0, tk.END)
        
        ttk.Button(method_frame, text="🗑️ Clear", command=clear_text).pack(side=tk.LEFT)
        
        # JSON input area
        input_frame = ttk.LabelFrame(main_frame, text=f"Paste {assessment_type.title()} Assessment JSON", padding="10")
        input_frame.grid(row=2, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        input_frame.columnconfigure(0, weight=1)
        input_frame.rowconfigure(0, weight=1)
        
        # Text widget for JSON input
        text_widget = scrolledtext.ScrolledText(input_frame, wrap=tk.WORD, font=("Consolas", 10), height=15)
        text_widget.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Instructions
        instructions = f"""Paste your {assessment_type} assessment JSON here, or upload a file above.

Required fields for {assessment_type} assessment:
"""
        if assessment_type == "trend":
            instructions += """- trend_score (integer 1-10)
- justification (string)
- suggested_tags (array of strings)"""
        else:  # maturity
            instructions += """- maturity_score (integer 1-10)
- justification (string)
- suggested_next_steps (array of strings)"""
        
        instructions_label = ttk.Label(main_frame, text=instructions, font=("Arial", 9), foreground="gray")
        instructions_label.grid(row=3, column=0, pady=(0, 10))
        
        # Buttons frame
        buttons_frame = ttk.Frame(main_frame)
        buttons_frame.grid(row=4, column=0, pady=(0, 10))
        
        # Save button
        def save_assessment():
            try:
                # Get JSON content from text widget
                json_content = text_widget.get(1.0, tk.END).strip()
                
                if not json_content:
                    messagebox.showwarning("Warning", "Please enter JSON content!")
                    return
                
                # Parse JSON
                assessment_data = json.loads(json_content)
                
                # Validate required fields
                if assessment_type == "trend":
                    if 'trend_score' not in assessment_data:
                        raise ValueError("Missing 'trend_score' field in trend assessment")
                elif assessment_type == "maturity":
                    if 'maturity_score' not in assessment_data:
                        raise ValueError("Missing 'maturity_score' field in maturity assessment")
                
                # Save the assessment
                self.save_assessment(idea_id, assessment_type, assessment_data)
                
                # Update the scores in the form
                if assessment_type == "trend" and 'trend_score' in assessment_data:
                    self.trend_var.set(assessment_data['trend_score'])
                    self.trend_label.config(text=str(assessment_data['trend_score']))
                elif assessment_type == "maturity" and 'maturity_score' in assessment_data:
                    self.maturity_var.set(assessment_data['maturity_score'])
                    self.maturity_label.config(text=str(assessment_data['maturity_score']))
                
                self.status_var.set(f"Updated {assessment_type} assessment for {idea_id}")
                
                # Close dialog
                dialog.destroy()
                
            except json.JSONDecodeError as e:
                messagebox.showerror("JSON Error", f"Invalid JSON format: {str(e)}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to process {assessment_type} assessment: {str(e)}")
        
        ttk.Button(buttons_frame, text="💾 Save Assessment", command=save_assessment).pack(side=tk.LEFT, padx=(0, 10))
        
        # Cancel button
        def cancel():
            dialog.destroy()
        
        ttk.Button(buttons_frame, text="❌ Cancel", command=cancel).pack(side=tk.LEFT)
        
        # Focus on text widget
        text_widget.focus_set()

    def view_assessment(self, assessment_type: str):
        """View an assessment file for the current idea"""
        if not self.current_idea:
            messagebox.showwarning("Warning", "No idea selected!")
            return
        
        idea_id = self.current_idea.get('idea_id')
        if not idea_id:
            messagebox.showerror("Error", "Idea ID is required!")
            return
        
        assessment_data = self.load_assessment(idea_id, assessment_type)
        if not assessment_data:
            messagebox.showinfo("Info", f"No {assessment_type} assessment found for this idea.")
            return
        
        # Create assessment viewer window
        assessment_window = tk.Toplevel(self.root)
        assessment_window.title(f"{assessment_type.title()} Assessment - {idea_id}")
        assessment_window.geometry("800x600")
        
        # Configure window
        assessment_window.columnconfigure(0, weight=1)
        assessment_window.rowconfigure(0, weight=1)
        
        # Create main frame
        main_frame = ttk.Frame(assessment_window, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(1, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text=f"{assessment_type.title()} Assessment", font=("Arial", 14, "bold"))
        title_label.grid(row=0, column=0, pady=(0, 10))
        
        # Text area with scrollbar
        text_frame = ttk.Frame(main_frame)
        text_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        text_frame.columnconfigure(0, weight=1)
        text_frame.rowconfigure(0, weight=1)
        
        # Text widget
        text_widget = scrolledtext.ScrolledText(text_frame, wrap=tk.WORD, font=("Consolas", 10))
        text_widget.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Display assessment data
        assessment_text = json.dumps(assessment_data, indent=2, ensure_ascii=False)
        text_widget.insert(tk.END, assessment_text)
        text_widget.config(state=tk.DISABLED)  # Make read-only
        
        # Buttons frame
        buttons_frame = ttk.Frame(main_frame)
        buttons_frame.grid(row=2, column=0, pady=(10, 0))
        
        # Copy button
        def copy_to_clipboard():
            assessment_window.clipboard_clear()
            assessment_window.clipboard_append(assessment_text)
            messagebox.showinfo("Copied", f"{assessment_type.title()} assessment copied to clipboard!")
        
        ttk.Button(buttons_frame, text="Copy to Clipboard", command=copy_to_clipboard).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(buttons_frame, text="Close", command=assessment_window.destroy).pack(side=tk.LEFT)
        
        # Status
        status_label = ttk.Label(main_frame, text=f"Showing {assessment_type} assessment for: {idea_id}")
        status_label.grid(row=3, column=0, pady=(10, 0))

    def create_widgets(self):
        """Create the main GUI widgets"""
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(1, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="EchoForge Repository Manager", 
                               font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # Left panel - Idea list
        left_frame = ttk.LabelFrame(main_frame, text="Ideas", padding="10")
        left_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 10))
        left_frame.columnconfigure(0, weight=1)
        left_frame.rowconfigure(1, weight=1)
        
        # Idea list controls
        controls_frame = ttk.Frame(left_frame)
        controls_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Button(controls_frame, text="New Idea", command=self.new_idea).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(controls_frame, text="Delete", command=self.delete_idea).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(controls_frame, text="Refresh", command=self.refresh_idea_list).pack(side=tk.LEFT)
        
        # Idea listbox
        self.idea_listbox = tk.Listbox(left_frame, width=40)
        self.idea_listbox.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.idea_listbox.bind('<<ListboxSelect>>', self.on_idea_select)
        
        # Scrollbar for idea list
        idea_scrollbar = ttk.Scrollbar(left_frame, orient=tk.VERTICAL, command=self.idea_listbox.yview)
        idea_scrollbar.grid(row=1, column=1, sticky=(tk.N, tk.S))
        self.idea_listbox.configure(yscrollcommand=idea_scrollbar.set)
        
        # Right panel - Idea details
        right_frame = ttk.LabelFrame(main_frame, text="Idea Details", padding="10")
        right_frame.grid(row=1, column=1, sticky=(tk.W, tk.E, tk.N, tk.S))
        right_frame.columnconfigure(1, weight=1)
        
        # Idea ID
        ttk.Label(right_frame, text="Idea ID:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.idea_id_var = tk.StringVar()
        self.idea_id_entry = ttk.Entry(right_frame, textvariable=self.idea_id_var, width=30)
        self.idea_id_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), pady=2, padx=(10, 0))
        
        # Title
        ttk.Label(right_frame, text="Title:").grid(row=1, column=0, sticky=tk.W, pady=2)
        self.title_var = tk.StringVar()
        self.title_entry = ttk.Entry(right_frame, textvariable=self.title_var, width=50)
        self.title_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), pady=2, padx=(10, 0))
        
        # Description
        ttk.Label(right_frame, text="Description:").grid(row=2, column=0, sticky=tk.W, pady=2)
        self.description_text = scrolledtext.ScrolledText(right_frame, height=4, width=50)
        self.description_text.grid(row=2, column=1, sticky=(tk.W, tk.E), pady=2, padx=(10, 0))
        
        # Scores frame
        scores_frame = ttk.LabelFrame(right_frame, text="Scores", padding="5")
        scores_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10)
        scores_frame.columnconfigure(0, weight=1)
        
        # Maturity Score
        maturity_row = ttk.Frame(scores_frame)
        maturity_row.grid(row=0, column=0, columnspan=6, sticky=(tk.W, tk.E), pady=2)
        maturity_row.columnconfigure(1, weight=1)
        
        ttk.Label(maturity_row, text="Maturity:").grid(row=0, column=0, sticky=tk.W, padx=(0, 5))
        self.maturity_var = tk.IntVar()
        self.maturity_scale = ttk.Scale(maturity_row, from_=1, to=10, variable=self.maturity_var, orient=tk.HORIZONTAL)
        self.maturity_scale.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(0, 10))
        self.maturity_label = ttk.Label(maturity_row, text="1")
        self.maturity_label.grid(row=0, column=2, padx=(0, 10))
        self.maturity_scale.configure(command=self.update_maturity_label)
        
        # Maturity assessment buttons
        ttk.Button(maturity_row, text="📊", width=3, command=lambda: self.view_assessment("maturity")).grid(row=0, column=3, padx=(0, 5))
        ttk.Button(maturity_row, text="📁", width=3, command=lambda: self.upload_assessment("maturity")).grid(row=0, column=4, padx=(0, 5))
        
        # Personal Interest Score
        interest_row = ttk.Frame(scores_frame)
        interest_row.grid(row=1, column=0, columnspan=6, sticky=(tk.W, tk.E), pady=2)
        interest_row.columnconfigure(1, weight=1)
        
        ttk.Label(interest_row, text="Interest:").grid(row=0, column=0, sticky=tk.W, padx=(0, 5))
        self.interest_var = tk.IntVar()
        self.interest_scale = ttk.Scale(interest_row, from_=1, to=10, variable=self.interest_var, orient=tk.HORIZONTAL)
        self.interest_scale.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(0, 10))
        self.interest_label = ttk.Label(interest_row, text="1")
        self.interest_label.grid(row=0, column=2, padx=(0, 10))
        self.interest_scale.configure(command=self.update_interest_label)
        
        # Trend Score
        trend_row = ttk.Frame(scores_frame)
        trend_row.grid(row=2, column=0, columnspan=6, sticky=(tk.W, tk.E), pady=2)
        trend_row.columnconfigure(1, weight=1)
        
        ttk.Label(trend_row, text="Trend:").grid(row=0, column=0, sticky=tk.W, padx=(0, 5))
        self.trend_var = tk.IntVar()
        self.trend_scale = ttk.Scale(trend_row, from_=1, to=10, variable=self.trend_var, orient=tk.HORIZONTAL)
        self.trend_scale.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(0, 10))
        self.trend_label = ttk.Label(trend_row, text="1")
        self.trend_label.grid(row=0, column=2, padx=(0, 10))
        self.trend_scale.configure(command=self.update_trend_label)
        
        # Trend assessment buttons
        ttk.Button(trend_row, text="📊", width=3, command=lambda: self.view_assessment("trend")).grid(row=0, column=3, padx=(0, 5))
        ttk.Button(trend_row, text="📁", width=3, command=lambda: self.upload_assessment("trend")).grid(row=0, column=4, padx=(0, 5))
        
        # Tags
        ttk.Label(right_frame, text="Tags:").grid(row=4, column=0, sticky=tk.W, pady=2)
        self.tags_var = tk.StringVar()
        self.tags_entry = ttk.Entry(right_frame, textvariable=self.tags_var, width=50)
        self.tags_entry.grid(row=4, column=1, sticky=(tk.W, tk.E), pady=2, padx=(10, 0))
        ttk.Label(right_frame, text="(comma-separated)").grid(row=4, column=2, sticky=tk.W, pady=2)
        
        # Related Items
        ttk.Label(right_frame, text="Related Items:").grid(row=5, column=0, sticky=tk.W, pady=2)
        self.related_items_text = scrolledtext.ScrolledText(right_frame, height=6, width=50)
        self.related_items_text.grid(row=5, column=1, sticky=(tk.W, tk.E), pady=2, padx=(10, 0))
        ttk.Label(right_frame, text="(JSON format)").grid(row=5, column=2, sticky=tk.W, pady=2)
        
        # Action buttons
        buttons_frame = ttk.Frame(right_frame)
        buttons_frame.grid(row=6, column=0, columnspan=2, pady=20)
        
        ttk.Button(buttons_frame, text="Save Changes", command=self.save_idea).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(buttons_frame, text="Clear Form", command=self.clear_form).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(buttons_frame, text="Save to File", command=self.save_repo_data).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(buttons_frame, text="View Sources", command=self.show_source_information).pack(side=tk.LEFT)
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(10, 0))

    def update_maturity_label(self, value):
        self.maturity_label.config(text=str(int(float(value))))

    def update_interest_label(self, value):
        self.interest_label.config(text=str(int(float(value))))

    def update_trend_label(self, value):
        self.trend_label.config(text=str(int(float(value))))

    def refresh_idea_list(self):
        """Refresh the idea listbox"""
        self.idea_listbox.delete(0, tk.END)
        for idea in self.repo_data:
            display_text = f"{idea.get('idea_id', 'N/A')}: {idea.get('title', 'No Title')}"
            self.idea_listbox.insert(tk.END, display_text)
        self.status_var.set(f"Loaded {len(self.repo_data)} ideas")

    def on_idea_select(self, event):
        """Handle idea selection from listbox"""
        selection = self.idea_listbox.curselection()
        if selection:
            index = selection[0]
            self.current_idea = self.repo_data[index]
            self.load_idea_to_form(self.current_idea)

    def load_idea_to_form(self, idea: Dict[str, Any]):
        """Load idea data into the form"""
        self.idea_id_var.set(idea.get('idea_id', ''))
        self.title_var.set(idea.get('title', ''))
        
        # Clear and set description
        self.description_text.delete(1.0, tk.END)
        self.description_text.insert(1.0, idea.get('description', ''))
        
        # Set scores
        self.maturity_var.set(idea.get('maturity_score', 1))
        self.interest_var.set(idea.get('personal_interest_score', 1))
        self.trend_var.set(idea.get('trend_score', 1))
        
        # Update labels
        self.maturity_label.config(text=str(self.maturity_var.get()))
        self.interest_label.config(text=str(self.interest_var.get()))
        self.trend_label.config(text=str(self.trend_var.get()))
        
        # Set tags
        tags = idea.get('tags', [])
        self.tags_var.set(', '.join(tags))
        
        # Set related items
        self.related_items_text.delete(1.0, tk.END)
        related_items = idea.get('related_items', [])
        self.related_items_text.insert(1.0, json.dumps(related_items, indent=2))
        
        # Load existing assessments if available
        idea_id = idea.get('idea_id', '')
        if idea_id:
            # Check for maturity assessment
            maturity_assessment = self.load_assessment(idea_id, "maturity")
            if maturity_assessment and 'maturity_score' in maturity_assessment:
                self.maturity_var.set(maturity_assessment['maturity_score'])
                self.maturity_label.config(text=str(maturity_assessment['maturity_score']))
            
            # Check for trend assessment
            trend_assessment = self.load_assessment(idea_id, "trend")
            if trend_assessment and 'trend_score' in trend_assessment:
                self.trend_var.set(trend_assessment['trend_score'])
                self.trend_label.config(text=str(trend_assessment['trend_score']))

    def clear_form(self):
        """Clear all form fields"""
        self.current_idea = None
        self.idea_id_var.set('')
        self.title_var.set('')
        self.description_text.delete(1.0, tk.END)
        self.maturity_var.set(1)
        self.interest_var.set(1)
        self.trend_var.set(1)
        self.tags_var.set('')
        self.related_items_text.delete(1.0, tk.END)
        
        # Update labels
        self.maturity_label.config(text="1")
        self.interest_label.config(text="1")
        self.trend_label.config(text="1")
        
        # Clear selection
        self.idea_listbox.selection_clear(0, tk.END)

    def new_idea(self):
        """Create a new idea"""
        self.clear_form()
        self.idea_id_var.set(f"I-{datetime.now().strftime('%Y%m%d-%H%M%S')}")
        self.status_var.set("New idea form ready")

    def save_idea(self):
        """Save current idea (new or existing)"""
        # Validate required fields
        idea_id = self.idea_id_var.get().strip()
        title = self.title_var.get().strip()
        
        if not idea_id or not title:
            messagebox.showerror("Error", "Idea ID and Title are required!")
            return
        
        # Get form data
        description = self.description_text.get(1.0, tk.END).strip()
        maturity_score = self.maturity_var.get()
        personal_interest_score = self.interest_var.get()
        trend_score = self.trend_var.get()
        
        # Parse tags
        tags_text = self.tags_var.get().strip()
        tags = [tag.strip() for tag in tags_text.split(',') if tag.strip()] if tags_text else []
        
        # Parse related items
        related_items_text = self.related_items_text.get(1.0, tk.END).strip()
        try:
            related_items = json.loads(related_items_text) if related_items_text else []
        except json.JSONDecodeError:
            messagebox.showerror("Error", "Invalid JSON format in Related Items!")
            return
        
        # Create idea object
        idea_data = {
            'idea_id': idea_id,
            'title': title,
            'description': description,
            'maturity_score': maturity_score,
            'personal_interest_score': personal_interest_score,
            'trend_score': trend_score,
            'tags': tags,
            'related_items': related_items
        }
        
        # Update or add to repo data
        if self.current_idea:
            # Update existing idea
            for i, idea in enumerate(self.repo_data):
                if idea.get('idea_id') == self.current_idea.get('idea_id'):
                    self.repo_data[i] = idea_data
                    break
            self.status_var.set(f"Updated idea: {idea_id}")
        else:
            # Add new idea
            self.repo_data.append(idea_data)
            self.status_var.set(f"Added new idea: {idea_id}")
        
        # Refresh list and select the current idea
        self.refresh_idea_list()
        self.current_idea = idea_data
        
        # Select the idea in the list
        for i, idea in enumerate(self.repo_data):
            if idea.get('idea_id') == idea_id:
                self.idea_listbox.selection_set(i)
                self.idea_listbox.see(i)
                break

    def delete_idea(self):
        """Delete the currently selected idea"""
        if not self.current_idea:
            messagebox.showwarning("Warning", "No idea selected!")
            return
        
        idea_id = self.current_idea.get('idea_id')
        if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete idea '{idea_id}'?"):
            self.repo_data = [idea for idea in self.repo_data if idea.get('idea_id') != idea_id]
            self.clear_form()
            self.refresh_idea_list()
            self.status_var.set(f"Deleted idea: {idea_id}")

    def show_source_information(self):
        """Show source information for the current idea in a new window"""
        if not self.current_idea:
            messagebox.showwarning("Warning", "No idea selected!")
            return
        
        # Create new window
        source_window = tk.Toplevel(self.root)
        source_window.title(f"Source Information - {self.current_idea.get('title', 'Unknown Idea')}")
        source_window.geometry("1000x800")
        
        # Configure window
        source_window.columnconfigure(0, weight=1)
        source_window.rowconfigure(0, weight=1)
        
        # Create main frame
        main_frame = ttk.Frame(source_window, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(1, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="Source Information", font=("Arial", 14, "bold"))
        title_label.grid(row=0, column=0, pady=(0, 10))
        
        # Text area with scrollbar
        text_frame = ttk.Frame(main_frame)
        text_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        text_frame.columnconfigure(0, weight=1)
        text_frame.rowconfigure(0, weight=1)
        
        # Text widget
        text_widget = scrolledtext.ScrolledText(text_frame, wrap=tk.WORD, font=("Consolas", 10))
        text_widget.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Get source information
        source_text = self.get_source_information(self.current_idea)
        text_widget.insert(tk.END, source_text)
        text_widget.config(state=tk.DISABLED)  # Make read-only
        
        # Buttons frame
        buttons_frame = ttk.Frame(main_frame)
        buttons_frame.grid(row=2, column=0, pady=(10, 0))
        
        # Copy button
        def copy_to_clipboard():
            source_window.clipboard_clear()
            source_window.clipboard_append(source_text)
            messagebox.showinfo("Copied", "Source information copied to clipboard!")
        
        ttk.Button(buttons_frame, text="Copy to Clipboard", command=copy_to_clipboard).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(buttons_frame, text="Close", command=source_window.destroy).pack(side=tk.LEFT)
        
        # Status
        status_label = ttk.Label(main_frame, text=f"Showing source information for: {self.current_idea.get('idea_id')}")
        status_label.grid(row=3, column=0, pady=(10, 0))


def main():
    """Main function to run the application"""
    root = tk.Tk()
    app = RepoManager(root)
    
    # Configure window close behavior
    def on_closing():
        if messagebox.askokcancel("Quit", "Do you want to save changes before quitting?"):
            app.save_repo_data()
        root.destroy()
    
    root.protocol("WM_DELETE_WINDOW", on_closing)
    
    # Start the application
    root.mainloop()


if __name__ == "__main__":
    main() 