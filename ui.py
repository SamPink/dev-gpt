import subprocess
import time
import uuid
import openai
import config
import re
import os
import json
from typing import List, Dict, Union
import tkinter as tk
from tkinter import ttk
from datetime import datetime


class GPT4UI:
    def __init__(self, gpt4_instance):
        self.gpt4 = gpt4_instance
        self.root = tk.Tk()
        self.root.title("GPT-4 Assistant")
        self.create_widgets()
        self.session = {
            "session_id": str(uuid.uuid4()),
            "folder_name": None,
            "start_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }

    def create_widgets(self):
        mainframe = ttk.Frame(self.root, padding="5")
        mainframe.grid(column=0, row=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        query_label = ttk.Label(mainframe, text="Choose a query:")
        query_label.grid(column=0, row=0, sticky=tk.W)

        self.query_var = tk.StringVar()
        query_options = [
            "create a python doodle jump game using pygame",
            "create a python script print 10 + 10",
            "create an application that tracks all the starlink satellites in the sky and plots them on a globe",
            "Custom"
        ]
        query_dropdown = ttk.OptionMenu(
            mainframe, self.query_var, query_options[0], *query_options
        )
        query_dropdown.grid(column=0, row=1, sticky=(tk.W, tk.E))

        self.query_entry = ttk.Entry(mainframe, width=80)
        self.query_entry.grid(column=0, row=2, sticky=(tk.W, tk.E))

        submit_button = ttk.Button(
            mainframe, text="Submit", command=self.submit_query
        )
        submit_button.grid(column=1, row=2, sticky=tk.W)

        self.message_display = tk.Text(
            mainframe, wrap=tk.WORD, width=80, height=20
        )
        self.message_display.grid(column=0, row=3, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))

        self.projects_var = tk.StringVar()
        self.projects_var.set("Select a Project")
        projects_dropdown = ttk.OptionMenu(
            mainframe,
            self.projects_var,
            self.projects_var.get(),
            *self.gpt4.get_project_list(),
        )
        projects_dropdown.grid(column=0, row=4, sticky=(tk.W, tk.E))

        run_button = ttk.Button(
            mainframe, text="Run", command=self.run_selected_project
        )
        run_button.grid(column=1, row=4, sticky=tk.W)

        ''' new_session_button = ttk.Button(
            mainframe, text="New Session", command=self.new_session
        )
        new_session_button.grid(column=2, row=4, sticky=tk.W) '''

        self.update_message_display()

    def submit_query(self):
        selected_query = self.query_var.get()
        if selected_query == "Custom":
            user_query = self.query_entry.get()
        else:
            user_query = selected_query
            
        self.query_entry.delete(0, tk.END)
        self.gpt4.add_message(user_query)
            
        if self.session['folder_name'] is None:
            folder_name = self.gpt4.extract_filename_from_query(user_query)
            
            query_folder = f"{self.gpt4.output_folder}/{folder_name}"
            
            os.makedirs(query_folder, exist_ok=True)
            
            self.session['folder_name'] = folder_name
        else:
            query_folder = f"{self.gpt4.output_folder}/{self.session['folder_name']}"
            

        output_filename = f"{query_folder}/code.py"
        self.gpt4.generate_and_save_response(output_filename)
        self.gpt4.run_code_and_add_output_to_messages(output_filename)
        self.update_message_display()

    def update_message_display(self):
        self.message_display.delete(1.0, tk.END)
        for message in self.gpt4.messages:
            tag = message['role'].capitalize()
            content = f"{tag}: {message['content']}\n"

            # Assign color based on role
            if tag == "User":
                color = "blue"
            elif tag == "GPT4":
                color = "green"
            else:
                color = "black"

            self.message_display.insert(tk.END, content, (tag,))
            self.message_display.tag_configure(tag, foreground=color)
        self.message_display.see(tk.END)  # Scroll to the bottom

    def run_selected_project(self):
        project_name = self.projects_var.get()
        if project_name == "Select a Project":
            return
        
        self.gpt4.save_sessions_to_file()
        self.gpt4.load_sessions_from_file()

        file_path = os.path.join(self.gpt4.output_folder, project_name, "code.py")
        if not os.path.isfile(file_path):
            tk.messagebox.showerror(
                "Error",
                f"Cannot find 'code.py' in the selected project folder: {project_name}",
            )
            return
        
        
        self.update_message_display()

        result = subprocess.run(["python", file_path], capture_output=True, text=True)
        output = result.stdout.strip()
        error = result.stderr.strip()

        self.message_display.delete(1.0, tk.END)
        if error:
            self.message_display.insert(
                tk.END, f"Error occurred while running the code:\n{error}\n"
            )
        else:
            self.message_display.insert(
                tk.END, f"Output from running the code:\n{output}\n"
            )

    def run(self):   
        self.message_display.config(font=("TkDefaultFont", 10), spacing1=5)         
        self.root.mainloop()
        
