from tkinter import messagebox  # Import the messagebox module separately
import pandas as pd
import os
import sys

class CSVCompiler:
    def __init__(self):

        self.header = 0
        self.separator = ";"
        self.footer = 0
        self.skiprows_min = 0
        self.skiprows_max = 11
        self.decimal = ","
        self.encoding = "latin1"
        self.date_field = "Date"
        self.time_field = "Time"
        self.level_field = "LEVEL"
        self.temp_field = "TEMPERATURE"

        self.datetime_field_output = "date_time"
        self.level_field_output = "level_m"
        self.temp_field_output = "temp_c"

        # determine if application is a script file or frozen exe
        if getattr(sys, 'frozen', False):
            self.folder_path = os.path.dirname(sys.executable)
        elif __file__:
            self.folder_path = os.path.dirname(__file__)

    def compile_csv_files(self):
        try:
            # List all files in the folder
            files = os.listdir(self.folder_path)
            csv_files = [file for file in files if file.lower().endswith('.csv') and not file.lower().endswith('_combine.csv')]
            
            # Check if there are any CSV files in the folder
            if not csv_files:
                raise FileNotFoundError("No CSV files found in the folder.")
            
            # Compile CSV files
            compiled_data = []
            for file in csv_files:
                df = pd.read_csv(file, header = self.header, sep=self.separator, engine='python', 
                                    skipfooter=self.footer, skiprows=range(self.skiprows_min, self.skiprows_max), 
                                    decimal=self.decimal, encoding=self.encoding)
                compiled_data.append(df)  # Append the dataframe to the "compiled_data" list
            
            if compiled_data:
                combined_df = pd.concat(compiled_data, ignore_index=True)
                combined_df[self.datetime_field_output] = pd.to_datetime(combined_df[self.date_field] + ' ' + combined_df[self.time_field], 
                                                                        format='%d/%m/%Y %H:%M:%S') # Combine date and time fields

                combined_df.rename(columns={self.level_field: self.level_field_output,
                                            self.temp_field: self.temp_field_output}, inplace=True)
                combined_df = combined_df.drop(columns=[self.date_field, self.time_field, "ms"]) # remove the "ms" column
                combined_df = combined_df[[self.datetime_field_output] + list(combined_df.columns[:-1])] # rearrange columns

                combined_df.drop_duplicates(subset=self.datetime_field_output, inplace=True) # remove duplicate rows from datetime_field_output

                combined_df = combined_df.sort_values(by=self.datetime_field_output) # sort the dataframe by datetime_field_output
                self.combined_df = combined_df
            
            # write compiled data to a new CSV file
            output_file = f"{os.path.basename(self.folder_path)}_combine.csv"
            self.combined_df.to_csv(output_file, index=False)
            messagebox.showinfo("Save Complete", f"Combined CSV file saved to:\n{output_file}")  # Use the messagebox module from tkinter
        
        except Exception as e:
            messagebox.showerror("Error", str(e))

def main():
    
    # Create an instance of CSVCompiler class with desired parameters
    compiler = CSVCompiler()
    
    # Compile CSV files using the CSVCompiler instance
    compiler.compile_csv_files()

if __name__ == "__main__":
    main()

