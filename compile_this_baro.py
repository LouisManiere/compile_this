import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox  # Import the messagebox module separately
from tkinter import ttk  # Import the ttk module separately
import pandas as pd

class CSVCombinerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("CSV Combiner App")
        
        self.input_files = []
        
        # Create GUI elements
        self.file_list_label = tk.Label(root, text="Selected Files:")
        self.file_list_label.grid(row=0, column=0, sticky=tk.W)
        
        self.file_listbox = tk.Listbox(root, selectmode=tk.MULTIPLE, width=50, height=10)
        self.file_listbox.grid(row=1, column=0, columnspan=2, padx=5, pady=5)
        
        self.add_button = tk.Button(root, text="Add Files", command=self.add_files)
        self.add_button.grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
        
        self.combine_button = tk.Button(root, text="Combine Files", command=self.combine_files)
        self.combine_button.grid(row=2, column=1, padx=5, pady=5, sticky=tk.E)

        self.sensor_name_label = tk.Label(root, text="Sensor Name:")
        self.sensor_name_label.grid(row=3, column=0, padx=5, pady=5, sticky=tk.W)
        self.sensor_name_entry = tk.Entry(root, width=10)
        self.sensor_name_entry.grid(row=3, column=1, padx=5, pady=5, sticky=tk.W)
        self.sensor_name_entry.insert(tk.END, "Diver_A")  # Default value

        self.date_field_label = tk.Label(root, text="Date Field:")
        self.date_field_label.grid(row=4, column=0, padx=5, pady=5, sticky=tk.W)
        self.date_field_entry = tk.Entry(root, width=10)
        self.date_field_entry.grid(row=4, column=1, padx=5, pady=5, sticky=tk.W)
        self.date_field_entry.insert(tk.END, "Date")

        self.time_field_label = tk.Label(root, text="Time Field:")
        self.time_field_label.grid(row=4, column=2, padx=5, pady=5, sticky=tk.W)
        self.time_field_entry = tk.Entry(root, width=10)
        self.time_field_entry.grid(row=4, column=3, padx=5, pady=5, sticky=tk.W)
        self.time_field_entry.insert(tk.END, "Time")

        self.header_var = tk.BooleanVar()
        self.header_checkbox = tk.Checkbutton(root, text="Files have headers", variable=self.header_var)
        self.header_checkbox.grid(row=5, column=0, columnspan=2, padx=5, pady=5)
        self.header_var.set(True)

        self.separator_label = tk.Label(root, text="Separator:")
        self.separator_label.grid(row=6, column=0, padx=5, pady=5, sticky=tk.W)
        self.separator_entry = tk.Entry(root, width=2)
        self.separator_entry.grid(row=6, column=1, padx=5, pady=5, sticky=tk.W)
        self.separator_entry.insert(tk.END, ";")

        self.decimal_label = tk.Label(root, text="Decimal:")
        self.decimal_label.grid(row=7, column=0, padx=5, pady=5, sticky=tk.W)
        self.decimal_entry = tk.Entry(root, width=2)
        self.decimal_entry.grid(row=7, column=1, padx=5, pady=5, sticky=tk.W)
        self.decimal_entry.insert(tk.END, ",")

        self.skiprows_label = tk.Label(root, text="Lines to skip (from - to):")
        self.skiprows_label.grid(row=8, column=0, padx=5, pady=5, sticky=tk.W)
        self.skiprows_min_entry = tk.Entry(root, width=5)
        self.skiprows_max_entry = tk.Entry(root, width=5)
        self.skiprows_min_entry.grid(row=8, column=1, padx=5, pady=5, sticky=tk.W)
        self.skiprows_max_entry.grid(row=8, column=2, padx=5, pady=5, sticky=tk.W)
        self.skiprows_min_entry.insert(tk.END, "0")
        self.skiprows_max_entry.insert(tk.END, "9")

        self.footer_label = tk.Label(root, text="Footer lines to skip:")
        self.footer_label.grid(row=9, column=0, padx=5, pady=5, sticky=tk.W)
        self.footer_entry = tk.Entry(root, width=5)
        self.footer_entry.grid(row=9, column=1, padx=5, pady=5, sticky=tk.W)
        self.footer_entry.insert(tk.END, "0")

        self.encoding_label = tk.Label(root, text="Encoding:")
        self.encoding_label.grid(row=10, column=0, padx=5, pady=5, sticky=tk.W)
        self.encoding_values = ["utf-8", "latin1"]
        self.encoding_combobox = ttk.Combobox(root, values=self.encoding_values)
        self.encoding_combobox.grid(row=10, column=1, padx=5, pady=5, sticky=tk.W)
        self.encoding_combobox.set(self.encoding_values[1])

        self.save_button = tk.Button(root, text="Save Combined CSV", command=self.save_combined_csv)
        self.save_button.grid(row=11, column=0, columnspan=2, padx=5, pady=5)

        self.save_excel_button = tk.Button(root, text="Save Combined Excel", command=self.save_combined_excel)
        self.save_excel_button.grid(row=12, column=0, columnspan=2, padx=5, pady=5)
    
    def add_files(self):
        files = filedialog.askopenfilenames(filetypes=[("CSV Files", "*.csv"), ("All files", "*.*")])
        for file in files:
            self.input_files.append(file)
            self.file_listbox.insert(tk.END, file)
    
    def combine_files(self):
        if not self.input_files:
            messagebox.showwarning("No Files", "Please select CSV files to combine.")  # Use the messagebox module from tkinter
            return
        try:
            all_dfs = []  # Declare the missing "all_dfs" list
            for file_path in self.input_files:
                has_header = self.header_var.get()  # Define the "has_header" variable
                separator = self.separator_entry.get()  # Define the "separator" variable
                footer = int(self.footer_entry.get())  # Define the "footer" variable
                skiprows_min = int(self.skiprows_min_entry.get())  # Define the "skiprows_min" variable
                skiprows_max = int(self.skiprows_max_entry.get())  # Define the "skiprows_max" variable
                decimal = self.decimal_entry.get()  # Define the "decimal" variable
                encoding = self.encoding_combobox.get()  # Define the "encoding" variable
                date_field = self.date_field_entry.get() # Define date field name
                time_field = self.time_field_entry.get() # Define time field name
                
                df = pd.read_csv(file_path, header=0 if has_header else None, sep=separator, engine='python', 
                                 skipfooter=footer, skiprows=range(skiprows_min, skiprows_max), 
                                 decimal=decimal, encoding=encoding)
                all_dfs.append(df)  # Append the dataframe to the "all_dfs" list
        except Exception as e:
            print(f"Error reading file: {e}")

        if all_dfs:
            combined_df = pd.concat(all_dfs, ignore_index=True)
            combined_df.drop_duplicates(subset=date_time_field, inplace=True)
            self.combined_df = combined_df.sort_values(by=date_time_field)
            self.combined_df = combined_df
            messagebox.showinfo("Combination Complete", "Files have been combined successfully.")
            
    def save_combined_csv(self):
        if not hasattr(self, 'combined_df'):
            messagebox.showwarning("No Combined Data", "Please combine CSV files first.")  # Use the messagebox module from tkinter
            return
                
        output_folder = filedialog.askdirectory()
        if output_folder:
            timestamp = pd.Timestamp.now().strftime("%Y%m%d%H%M%S")
            output_file = f"{output_folder}/{timestamp}_{self.sensor_name_entry.get()}_combine.csv"
            self.combined_df.to_csv(output_file, index=False)
            messagebox.showinfo("Save Complete", f"Combined CSV file saved to:\n{output_file}")  # Use the messagebox module from tkinter

        
    def save_combined_excel(self):
        if not hasattr(self, 'combined_df'):
            messagebox.showwarning("No Combined Data", "Please combine CSV files first.")  # Use the messagebox module from tkinter
            return
                    
        output_folder = filedialog.askdirectory()
        if output_folder:
            timestamp = pd.Timestamp.now().strftime("%Y%m%d%H%M%S")
            output_file = f"{output_folder}/{timestamp}_{self.sensor_name_entry.get()}_combine.xlsx"
            self.combined_df.to_excel(output_file, sheet_name=self.sensor_name_entry.get(), index=False)
            messagebox.showinfo("Save Complete", f"Combined Excel file saved to:\n{output_file}")  # Use the messagebox module from tkinter

if __name__ == "__main__":
    root = tk.Tk()
    app = CSVCombinerApp(root)
    root.mainloop()
