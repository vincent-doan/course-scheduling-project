import tkinter as tk
from tkinter import filedialog, ttk, font, messagebox
import csv
from solution_by_backtracking import *
from solution_by_value_ordering import *
import time

import sys

sys.setrecursionlimit(50000)

data = []
header = []
sort_order = {}

selected_algorithm = None

def process_input_csv(input_path: str) -> None:
    global selected_algorithm
    try:
        input_size = input_path.split("_")[2].split(".")[0]
    except:
        input_size = 'all'
    
    if selected_algorithm == 'Backtracking':
        output_path = "output/backtracking_" + input_size + ".csv"
        solution_algorithm = SolutionByBacktracking(path_to_all_courses=input_path, output_path=output_path)
    elif selected_algorithm == 'Value Ordering':
        output_path = "output/value_ordering_" + input_size + ".csv"
        solution_algorithm = SolutionByValueOrdering(path_to_all_courses=input_path, output_path=output_path)
    # elif selected_algorithm == 'Forward Checking':
    #     output_path = "output/forward_checking_" + input_size + ".csv"
    #     solution_algorithm = SolutionByForwardChecking(path_to_all_courses=input_path, output_path=output_path)
    else:
        raise ValueError("Invalid algorithm selected.")
    
    solution_algorithm.get_solution()
    return output_path

def enable_open_button():
    open_button.config(state=tk.NORMAL)

def disable_open_button():
    open_button.config(state=tk.DISABLED)

def on_algorithm_selected(event):
    global selected_algorithm
    selected_algorithm = algorithm_combobox.get()
    if selected_algorithm != "Select Algorithm":
        enable_open_button()
    else:
        disable_open_button()

def open_csv_file():
    global data, header, sort_order, selected_algorithm

    input_file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv"), ("All files", "*.*")])
    start = time.time()
    output_file_path = process_input_csv(input_file_path)
    time_taken = time.time() - start
    
    with open("output/time_taken.txt", "a") as f:
        f.write(f"{selected_algorithm} - {input_file_path.split('/')[-1][:-4]} - {round(time_taken, 2)}\n")
    
    if output_file_path:
        try:
            with open(output_file_path, 'r') as file:
                csv_reader = csv.reader(file)
                header = next(csv_reader)
                data = [row for row in csv_reader]

            # Initialize sorting order for each column
            sort_order = {col: 'asc' for col in header}

            # Clear previous content
            for item in tree.get_children():
                tree.delete(item)

            # Insert header
            tree['columns'] = header
            for col in header:
                tree.heading(col, text=col, command=lambda c=col: sort_column(c), anchor='w')
                tree.column(col, anchor='w', width=font.Font().measure(col))

            # Insert data
            for row in data:
                tree.insert('', 'end', values=row)

            # Update the filter column dropdown menu
            update_filter_dropdown()

            # Update the time taken label
            time_taken_label.config(text=f"Time Taken: {time_taken:.2f} seconds")

        except Exception as e:
            tree.delete(1.0, tk.END)
            tree.insert(tk.END, f"Error reading CSV file: {str(e)}")

def sort_column(col):
    global data, header, sort_order
    # Toggle sorting order (asc <-> desc)
    sort_order[col] = 'desc' if sort_order[col] == 'asc' else 'asc'
    
    # Function to sort data based on the selected column and order
    data.sort(key=lambda x: x[header.index(col)], reverse=(sort_order[col] == 'desc'))
    refresh_table()

def refresh_table():
    global data
    # Function to refresh the table with sorted data
    for item in tree.get_children():
        tree.delete(item)

    for row in data:
        tree.insert('', 'end', values=row)

def filter_table(event):
    global data
    # Function to filter data based on the selected column and input text
    filter_column = filter_var.get()
    filter_text = filter_entry.get().lower()
    
    if filter_column and filter_text:
        filtered_data = [row for row in data if filter_text in str(row[header.index(filter_column)]).lower()]
        display_filtered_data(filtered_data)
    else:
        refresh_table()

def display_filtered_data(filtered_data):
    # Function to display filtered data in the table
    for item in tree.get_children():
        tree.delete(item)

    for row in filtered_data:
        tree.insert('', 'end', values=row)

def update_filter_dropdown():
    # Function to update the filter column dropdown menu
    filter_var.set('')  # Clear the current selection
    filter_menu['menu'].delete(0, 'end')  # Clear the current menu items
    
    for col in header:
        filter_menu['menu'].add_command(label=col, command=tk._setit(filter_var, col))

# Create the main window
root = tk.Tk()
root.title("Scheduler")

# Styling
font_style = ("Helvetica", 10)
background_color = "#EAEAEA"

# Create a variable for the algorithm selection
algorithm_var = tk.StringVar(root)
algorithm_var.set("Select Algorithm")

# Create a Combobox for algorithm selection
algorithm_combobox = ttk.Combobox(root, textvariable=algorithm_var, values=['Backtracking', 'Value Ordering', 'Forward Checking'])
algorithm_combobox.pack(pady=10)

# Create a Treeview widget to display the table
tree = ttk.Treeview(root, style="Custom.Treeview", height=25)
tree["show"] = "headings"
tree.pack(padx=10, pady=10)

# Configure style for the Treeview
style = ttk.Style()
style.configure("Custom.Treeview", background=background_color, font=font_style)

# Create a label to display the time taken
time_taken_label = tk.Label(root, text="", font=font_style)
time_taken_label.pack(pady=5)

# Create an Entry widget for the filter text field
filter_entry = tk.Entry(root, font=font_style)
filter_entry.pack(pady=10, padx=10, side=tk.TOP, anchor=tk.W)
filter_entry.bind("<KeyRelease>", filter_table)

# Create a filter column dropdown menu
filter_var = tk.StringVar(root)
filter_menu = ttk.OptionMenu(root, filter_var, '', '')
filter_menu.pack(pady=10, padx=10, side=tk.TOP, anchor=tk.W)

# Create a button to open a CSV file
open_button = tk.Button(root, text="Open CSV File", command=open_csv_file, font=font_style, state=tk.DISABLED)
open_button.pack(pady=10)

# Create an exit button
exit_button = tk.Button(root, text="Exit", command=root.destroy, font=font_style)
exit_button.pack(pady=10)

# Bind the algorithm selection to enable the "Open CSV File" button
algorithm_combobox.bind("<<ComboboxSelected>>", on_algorithm_selected)

# Start the Tkinter event loop
root.mainloop()
