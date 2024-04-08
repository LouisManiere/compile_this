from tkinter import messagebox  # Import the messagebox module separately
import pandas as pd
import os

class CSVCompiler:
    def __init__(self):

        self.header = 0
        self.separator = ";"
        self.footer = 1
        self.skiprows_min = 0
        self.skiprows_max = 50
        self.decimal = ","
        self.encoding = "latin1"
        self.datetime_field = "Date/time"
        self.sensor_name = "Piezo_A"
        self.level_field = "Pression[cmH2O]"
        self.temp_field = "Température[°C]"

        self.datetime_field_output = "date_time"
        self.level_field_output = "level_m"
        self.temp_field_output = "temp_c"

        self.filename_output = "compiled_data.csv"

        # Get the folder path where the program is located
        self.folder_path = os.path.dirname(__file__)

    def compile_csv_files(self):
        try:
            # List all files in the folder
            files = os.listdir(self.folder_path)
            csv_files = [file for file in files if file.lower().endswith('.csv')]
            
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
                combined_df.rename(columns={self.datetime_field: self.datetime_field_output,
                                            self.level_field: self.level_field_output,
                                            self.temp_field: self.temp_field_output}, inplace=True)
                combined_df[self.datetime_field_output] = pd.to_datetime(combined_df[self.datetime_field_output], format="%Y/%m/%d %H:%M:%S")
                combined_df.drop_duplicates(subset=self.datetime_field_output, inplace=True)
                combined_df[self.level_field_output] = combined_df[self.level_field_output]/100
                self.combined_df = combined_df.sort_values(by=self.datetime_field_output)
                self.combined_df = combined_df
            
            # write compiled data to a new CSV file
            output_file = f"{self.folder_path}/{self.sensor_name}_combine.csv"
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

