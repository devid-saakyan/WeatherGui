import tkinter as tk
from tkinter import ttk, messagebox
import requests
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import datetime
from dotenv import load_dotenv
import os

load_dotenv()

class WeatherApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Weather Forecast App")
        self.root.geometry('800x600')

        self.api_key = os.getenv('API_KEY')
        self.base_url = 'http://api.openweathermap.org/data/2.5/forecast?'

        self.location_entry = ttk.Entry(root, width=50)
        self.location_entry.pack(pady=5)

        self.unit_var = tk.StringVar(value='metric')
        ttk.Radiobutton(root, text='Celsius', variable=self.unit_var, value='metric').pack()
        ttk.Radiobutton(root, text='Fahrenheit', variable=self.unit_var, value='imperial').pack()

        ttk.Button(root, text="Fetch Weather", command=self.fetch_weather).pack(pady=20)

        self.data_frame = tk.Frame(root)
        self.data_frame.pack(fill=tk.BOTH, expand=True)

    def fetch_weather(self):
        location = self.location_entry.get()
        units = self.unit_var.get()
        try:
            url = f"{self.base_url}q={location}&appid={self.api_key}&units={units}&cnt=80"
            response = requests.get(url)
            response.raise_for_status()
            forecast_data = response.json()
            self.plot_weekly_forecast(forecast_data, units)
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Error", str(e))

    def plot_weekly_forecast(self, data, units):
        dates = []
        temperatures = []

        for day in data['list']:
            date = datetime.datetime.fromtimestamp(day['dt']).strftime('%Y-%m-%d')
            temp = day['main']['temp']

            if date not in dates:
                dates.append(date)
                temperatures.append(temp)

        for widget in self.data_frame.winfo_children():
            widget.destroy()

        fig, ax = plt.subplots(figsize=(10, 4))
        ax.plot(dates, temperatures, marker='o', linestyle='-', color='b')
        ax.set(title='6-day Temperature Forecast', xlabel='Date', ylabel=f"Temperature (°{'C' if units == 'metric' else 'F'})")

        canvas = FigureCanvasTkAgg(fig, master=self.data_frame)
        canvas.draw()
        canvas.get_tk_widget().pack()

def main():
    root = tk.Tk()
    app = WeatherApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
