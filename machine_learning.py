import tkinter as tk
from tkinter import ttk
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error
from datetime import timedelta
import re
from sklearn.impute import SimpleImputer

csv_file_path = 'c:\\Users\\iamta\\Desktop\\WSD 2.0\\Code\\IoT\\esting2\\temperature_data.csv'

df = pd.read_csv(csv_file_path)

df["Date"] = pd.to_datetime(df["Date"])
df["Time"] = pd.to_datetime(df["Time"], errors='coerce').dt.time  # Convert 'Time' to time and handle NaT values

df["DateTime"] = pd.to_datetime(df["Date"].astype(str) + " " + df["Time"].astype(str))

X = df["DateTime"].dt.hour.values.reshape(-1, 1)
y = df["Temperature"]

imputer = SimpleImputer(strategy='mean')

df["Temperature"] = imputer.fit_transform(df["Temperature"].values.reshape(-1, 1))
df = df.dropna(subset=['DateTime'])

X = df["DateTime"].dt.hour.values.reshape(-1, 1)
y = df["Temperature"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

regressor = DecisionTreeRegressor(random_state=42)
regressor.fit(X_train, y_train)

y_pred = regressor.predict(X_test)

mae = mean_absolute_error(y_test, y_pred)
mse = mean_squared_error(y_test, y_pred)

# Tkinter GUI
class TemperaturePredictorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Temperature Predictor")
        self.root.geometry("700x500")

        self.label_date = ttk.Label(root, text="Enter Date (YYYY-MM-DD):")
        self.entry_date = ttk.Entry(root)

        self.label_time = ttk.Label(root, text="Enter Time (HH:MM):")
        self.entry_time = ttk.Entry(root)

        self.btn_predict = ttk.Button(root, text="Predict Temperature", command=self.predict_temperature)

        self.label_result = ttk.Label(root, text="Predicted Temperature:")
        self.label_prediction = ttk.Label(root, text="")
        
        self.label_mae = ttk.Label(root, text=f"Mean Absolute Error: {mae:.2f}")
        self.label_mse = ttk.Label(root, text=f"Mean Squared Error: {mse:.2f}")

        self.label_date.place(relx=0.5, rely=0.1, anchor=tk.CENTER)
        self.entry_date.place(relx=0.5, rely=0.15, anchor=tk.CENTER)

        self.label_time.place(relx=0.5, rely=0.25, anchor=tk.CENTER)
        self.entry_time.place(relx=0.5, rely=0.3, anchor=tk.CENTER)

        self.btn_predict.place(relx=0.5, rely=0.4, anchor=tk.CENTER)

        self.label_result.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        self.label_prediction.place(relx=0.5, rely=0.55, anchor=tk.CENTER)

        #self.label_mae.place(relx=0.5, rely=0.65, anchor=tk.CENTER)
        self.label_mse.place(relx=0.5, rely=0.75, anchor=tk.CENTER)

        self.entry_date.config(state="normal")
        self.entry_time.config(state="normal")

    def predict_temperature(self):
        try:
            entered_date = pd.to_datetime(self.entry_date.get())
            entered_time = pd.to_datetime(self.entry_time.get(), errors='coerce').hour

            entered_datetime = entered_date + timedelta(hours=entered_time)

            # Skip prediction if entered_datetime has NaN values
            if pd.isna(entered_datetime):
                self.label_prediction.config(text="Invalid input")
                return

            predicted_temperature = regressor.predict([[entered_datetime.hour]])[0]
            self.label_prediction.config(text=f"{predicted_temperature:.2f} °C")

        except Exception as e:
            self.label_prediction.config(text="Invalid input")


def parse_sensor_data(line):
    temperature_match = re.search(r"Temperature: (\d+\.\d+)", line)
    if temperature_match:
        temperature = float(temperature_match.group(1))
        return temperature
    return None


if __name__ == "__main__":
    try:
        root = tk.Tk()
        app = TemperaturePredictorGUI(root)
        root.mainloop()
    except Exception as e:
        print(f"An error occurred: {e}")

        # Read data from the serial monitor
        line = "Temperature: 25.20°C"
        temperature = parse_sensor_data(line)
        if temperature is not None:
            print(f"Temperature: {temperature} °C")

