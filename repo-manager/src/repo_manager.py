#!/usr/bin/env python3
"""
Repo Manager - A Tkinter GUI application for managing idea repository
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog, scrolledtext
import json
import os
from typing import Dict, List, Any, Optional
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
        
        # Load data
        self.load_repo_data()
        
        # Create GUI
        self.create_widgets()
        self.refresh_idea_list()

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
        scores_frame.columnconfigure(1, weight=1)
        scores_frame.columnconfigure(3, weight=1)
        scores_frame.columnconfigure(5, weight=1)
        
        # Maturity Score
        ttk.Label(scores_frame, text="Maturity:").grid(row=0, column=0, sticky=tk.W, padx=(0, 5))
        self.maturity_var = tk.IntVar()
        self.maturity_scale = ttk.Scale(scores_frame, from_=1, to=10, variable=self.maturity_var, orient=tk.HORIZONTAL)
        self.maturity_scale.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(0, 10))
        self.maturity_label = ttk.Label(scores_frame, text="1")
        self.maturity_label.grid(row=0, column=2, padx=(0, 10))
        self.maturity_scale.configure(command=self.update_maturity_label)
        
        # Personal Interest Score
        ttk.Label(scores_frame, text="Interest:").grid(row=0, column=3, sticky=tk.W, padx=(0, 5))
        self.interest_var = tk.IntVar()
        self.interest_scale = ttk.Scale(scores_frame, from_=1, to=10, variable=self.interest_var, orient=tk.HORIZONTAL)
        self.interest_scale.grid(row=0, column=4, sticky=(tk.W, tk.E), padx=(0, 10))
        self.interest_label = ttk.Label(scores_frame, text="1")
        self.interest_label.grid(row=0, column=5, padx=(0, 10))
        self.interest_scale.configure(command=self.update_interest_label)
        
        # Trend Score
        ttk.Label(scores_frame, text="Trend:").grid(row=1, column=0, sticky=tk.W, padx=(0, 5), pady=(10, 0))
        self.trend_var = tk.IntVar()
        self.trend_scale = ttk.Scale(scores_frame, from_=1, to=10, variable=self.trend_var, orient=tk.HORIZONTAL)
        self.trend_scale.grid(row=1, column=1, sticky=(tk.W, tk.E), padx=(0, 10), pady=(10, 0))
        self.trend_label = ttk.Label(scores_frame, text="1")
        self.trend_label.grid(row=1, column=2, padx=(0, 10), pady=(10, 0))
        self.trend_scale.configure(command=self.update_trend_label)
        
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
        ttk.Button(buttons_frame, text="Save to File", command=self.save_repo_data).pack(side=tk.LEFT)
        
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