# -*- coding: utf-8 -*-
# Author: Louis Manière <louismaniere@orange.fr>
# License: MIT

import tkinter as tk
from tkinter import filedialog
import pandas as pd

def choose_files():
    file_paths = filedialog.askopenfilenames(filetypes=[("CSV files", "*.csv")])
    if file_paths:
        all_dfs = []
        for file_path in file_paths:
            print("Selected file:", file_path)
            has_header = var_header.get()
            separator = entry_separator.get()
            decimal = entry_decimal.get()
            skiprows_min = int(entry_skiprows_min.get())
            skiprows_max = int(entry_skiprows_max.get())
            footer = int(entry_footer.get())
            datetime_field = entry_datetime.get()
            print("Header:", has_header)
            print("Separator:", separator)
            print("Decimal:", decimal)
            print("Date time field:", datetime_field)
            try:
                df = pd.read_csv(file_path, header=0 if has_header else None, sep=separator, engine='python', 
                                 skipfooter=footer, skiprows=range(skiprows_min, skiprows_max), 
                                 decimal=decimal, index_col=0)
                all_dfs.append(df)
            except Exception as e:
                print(f"Error reading file: {e}")
        if all_dfs:
            compiled_df = pd.concat(all_dfs, ignore_index=True)
            compiled_df.to_csv("compiled.csv", index=False)
            status_label.config(text="Compiled CSV file saved as 'compiled.csv'", fg="green")
        else:
            status_label.config(text="No CSV files were successfully processed.", fg="red")

# Create main window
root = tk.Tk()
root.title("Multiple CSV File Reader")

# File Path Entry
label_file_path = tk.Label(root, text="CSV File Paths:")
label_file_path.grid(row=0, column=0, padx=5, pady=5, sticky="w")

# Header Checkbox
var_header = tk.BooleanVar()
checkbox_header = tk.Checkbutton(root, text="Files have headers", variable=var_header)
checkbox_header.grid(row=1, column=0, padx=5, pady=5, sticky="w")

# Separator Entry
label_separator = tk.Label(root, text="Separator:")
label_separator.grid(row=2, column=0, padx=5, pady=5, sticky="w")
entry_separator = tk.Entry(root, width=2)
entry_separator.insert(tk.END, ",")  # Default value
entry_separator.grid(row=2, column=1, padx=5, pady=5)

# Decimal Entry
label_decimal = tk.Label(root, text="Decimal:")
label_decimal.grid(row=3, column=0, padx=5, pady=5, sticky="w")
entry_decimal = tk.Entry(root, width=2)
entry_decimal.insert(tk.END, ".")  # Default value
entry_decimal.grid(row=3, column=1, padx=5, pady=5)

# Skip rows
label_skiprows = tk.Label(root, text="Lines to skip (from - to):")
label_skiprows.grid(row=4, column=0, padx=5, pady=5, sticky="w")
entry_skiprows_min = tk.Entry(root, width=5)
entry_skiprows_max = tk.Entry(root, width=5)
entry_skiprows_min.insert(tk.END, "0")  # Default value
entry_skiprows_min.grid(row=4, column=1, padx=5, pady=5)
entry_skiprows_max.insert(tk.END, "0")  # Default value
entry_skiprows_max.grid(row=4, column=2, padx=5, pady=5)

# Footer Entry
label_footer = tk.Label(root, text="Footer lines to skip:")
label_footer.grid(row=5, column=0, padx=5, pady=5, sticky="w")
entry_footer = tk.Entry(root, width=5)
entry_footer.insert(tk.END, "1")  # Default value
entry_footer.grid(row=5, column=1, padx=5, pady=5)

# Date time Entry
label_datetime = tk.Label(root, text="Date time field:")
label_datetime.grid(row=6, column=0, padx=5, pady=5, sticky="w")
entry_datetime = tk.Entry(root, width=10)
entry_datetime.insert(tk.END, "date")  # Default value
entry_datetime.grid(row=6, column=1, padx=5, pady=5)

# Process Button
button_browse = tk.Button(root, text="Browse", command=choose_files)
button_browse.grid(row=7, column=0, padx=5, pady=5, sticky="w")

# Status Label
status_label = tk.Label(root, text="", fg="black")
status_label.grid(row=8, column=0, padx=5, pady=5, sticky="w")

root.mainloop()
