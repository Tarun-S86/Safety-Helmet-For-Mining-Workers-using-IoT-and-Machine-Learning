import tkinter as tk
from tkinter import ttk
import subprocess
import serial
import csv
from datetime import datetime

class TemperatureUploaderGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Temperature Uploader")
        self.root.geometry("700x500")

        self.text_output = tk.Text(root, height=12, width=70)
        self.text_output.pack(padx=10, pady=10)

        self.start_button = ttk.Button(root, text="Start Uploading", command=self.start_uploading, style="Custom.TButton")
        self.start_button.pack(pady=10)

        # self.stop_button = ttk.Button(root, text="Stop Uploading", command=self.stop_uploading)
        # self.stop_button.pack(pady=10)
        # self.stop_button.config(state="disabled")

        self.exit_button = ttk.Button(root, text="Exit", command=self.exit_uploader, style="Custom.TButton")
        self.exit_button.pack(pady=10)

        # Replace 'COM9' with the appropriate serial port, it will be different for each USB port
        self.ser = serial.Serial('COM3', 9600, timeout=1)

        # Define the CSV file path in your laptop 
        self.csv_file_path = 'C:\\Users\\iamta\\Desktop\\WSD 2.0\\Code\\IoT\\esting2\\temperature_data.csv'

      
        self.csvfile = open(self.csv_file_path, 'a', newline='')
        self.fieldnames = ['Date', 'Time', 'Temperature']
        self.writer = csv.DictWriter(self.csvfile, fieldnames=self.fieldnames)

     
        if self.csvfile.tell() == 0:
            self.writer.writeheader()

        self.update_interval = 1000  

    def start_uploading(self):
        self.start_button.config(state="disabled")
        self.upload_temperature()

    def upload_temperature(self):
        line = self.ser.readline().decode('utf-8').strip()

        if line.startswith("Temperature:"):
            temperature_str = line.split(":")[1].split("°")[0].strip()

            try:
                temperature = float(temperature_str)
                current_datetime = datetime.now()
                date_str = current_datetime.strftime('%Y-%m-%d')
                time_str = current_datetime.strftime('%H:%M:%S')

                output_text = f'Date: {date_str}, Time: {time_str}, Temperature: {temperature}\n'
                self.text_output.insert(tk.END, output_text)
                self.text_output.see(tk.END)

                self.writer.writerow({'Date': date_str, 'Time': time_str, 'Temperature': temperature})

            except ValueError as e:
                print(f'Error converting to float: {e}')

        
        self.root.after(self.update_interval, self.upload_temperature)

    # def stop_uploading(self):
    #     self.start_button.config(state="normal")
    #     self.stop_button.config(state="disabled")

    def exit_uploader(self):
        self.csvfile.close()
        self.root.destroy()

class SafetyHelmetGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Safety Helmet")
        self.root.geometry("700x500")


        custom_style = ttk.Style()
        custom_style.configure("Custom.TButton", font=("Helvetica", 22), padding=(8, 8))

        self.label_title = ttk.Label(text="Safety Helmet", font=("Helvetica", 28, "bold"))
        self.label_title.pack(pady=10)

        self.btn_upload_temp = ttk.Button(text="Upload Temperature", command=self.run_upload_temp, style="Custom.TButton")
        self.btn_upload_temp.pack(pady=10)

        self.btn_predict_temp = ttk.Button(text="Predict Temperature", command=self.run_predict_temp, style="Custom.TButton")
        self.btn_predict_temp.pack(pady=10)

        self.btn_upload_temp.pack(pady=(120, 10), side=tk.TOP, anchor=tk.CENTER)
        self.btn_predict_temp.pack(pady=(10, 120), side=tk.TOP, anchor=tk.CENTER)

        self.ser = None  

    def run_upload_temp(self):

        uploader_window = tk.Toplevel(self.root)
        uploader_app = TemperatureUploaderGUI(uploader_window)

    def run_predict_temp(self):
        url = "C:\\Users\\iamta\\Desktop\\WSD 2.0\\Code\\IoT\\esting2\\machine_learning.py" # Change path according to your file location
        subprocess.Popen(['python', url])

        if self.ser:
            self.ser.close()
            print("Connection to COM9 closed")

if __name__ == "__main__":
    root = tk.Tk()
    app = SafetyHelmetGUI(root)
    root.mainloop()
