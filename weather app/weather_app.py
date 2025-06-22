import requests
from datetime import datetime
from tkinter import *
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import io

class WeatherApp:
    def __init__(self, root):
        self.root = root
        self.root.title("WEATHER ANALYTICS PRO")
        self.root.geometry("1000x700")
        self.root.configure(bg='#2c3e50')
        
        # Variables
        self.current_city = StringVar()
        self.api_key = "96cd03e854c0838ca4c828057ce2a1a3"
        
        # Custom fonts
        self.title_font = ('Helvetica', 24, 'bold')
        self.header_font = ('Helvetica', 16, 'bold')
        self.normal_font = ('Helvetica', 12)
        self.small_font = ('Helvetica', 10)
        
        # Setup UI
        self.create_widgets()
        
        # Load default city
        self.fetch_weather_data("Delhi")
    
    def create_widgets(self):
        """Create all UI components"""
        # Header with gradient background
        header = Frame(self.root, bg='#3498db', height=80)
        header.pack(fill=X)
        
        # App title with icon
        title_frame = Frame(header, bg='#3498db')
        title_frame.pack(pady=15)
        
        Label(title_frame, text="☀️", font=('Arial', 24), bg='#3498db').pack(side=LEFT)
        Label(title_frame, text="WEATHER ANALYTICS PRO", font=self.title_font, 
              bg='#3498db', fg='white').pack(side=LEFT, padx=10)
        
        # Search Frame with rounded corners
        search_frame = Frame(self.root, bg='#34495e', bd=0, 
                           highlightbackground='#7f8c8d', highlightthickness=1)
        search_frame.pack(fill=X, padx=20, pady=15)
        
        # Modern search input
        self.city_entry = Entry(search_frame, textvariable=self.current_city, 
                              font=self.normal_font, width=30, bd=0,
                              highlightthickness=0, bg='#2c3e50', fg='white',
                              insertbackground='white')
        self.city_entry.pack(side=LEFT, padx=15, pady=10, ipady=5)
        
        # Modern buttons with hover effects
        button_style = {'font': self.normal_font, 'bd': 0, 'padx': 15, 'pady': 8,
                       'activebackground': '#2980b9', 'activeforeground': 'white'}
        
        Button(search_frame, text="🔍 Search", command=self.fetch_weather_data, 
               bg='#2ecc71', fg='white', **button_style).pack(side=LEFT, padx=5)
        
        Button(search_frame, text="📅 Forecast", command=self.show_forecast,
               bg='#3498db', fg='white', **button_style).pack(side=LEFT, padx=5)
        
        # Main Display Area with notebook style
        style = ttk.Style()
        style.theme_create('custom', parent='alt', settings={
            'TNotebook': {'configure': {'background': '#34495e', 'borderwidth': 0}},
            'TNotebook.Tab': {
                'configure': {'padding': [15, 5], 'background': '#34495e', 'foreground': 'white'},
                'map': {'background': [('selected', '#2c3e50')]}
            }
        })
        style.theme_use('custom')
        
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=BOTH, expand=True, padx=20, pady=(0, 20))
        
        # Current Weather Tab
        self.current_tab = Frame(self.notebook, bg='#2c3e50')
        self.notebook.add(self.current_tab, text="Current Weather")
        
        # Current weather display with card-like design
        current_display = Frame(self.current_tab, bg='#34495e', padx=20, pady=20,
                               highlightbackground='#7f8c8d', highlightthickness=1)
        current_display.pack(fill=BOTH, expand=True, padx=10, pady=10)
        
        # Weather Icon and basic info
        self.top_frame = Frame(current_display, bg='#34495e')
        self.top_frame.pack(fill=X, pady=(0, 20))
        
        self.icon_label = Label(self.top_frame, bg='#34495e')
        self.icon_label.pack(side=LEFT)
        
        self.city_label = Label(self.top_frame, font=('Helvetica', 20, 'bold'), 
                               bg='#34495e', fg='white')
        self.city_label.pack(side=LEFT, padx=20)
        
        self.temp_label = Label(self.top_frame, font=('Helvetica', 48, 'bold'), 
                               bg='#34495e', fg='white')
        self.temp_label.pack(side=LEFT)
        
        # Weather details in a grid layout
        details_frame = Frame(current_display, bg='#34495e')
        details_frame.pack(fill=X)
        
        # Row 1
        self.feels_like_label = Label(details_frame, font=self.normal_font, 
                                     bg='#34495e', fg='white', anchor='w')
        self.feels_like_label.grid(row=0, column=0, sticky=W, padx=10, pady=5)
        
        self.humidity_label = Label(details_frame, font=self.normal_font, 
                                   bg='#34495e', fg='white', anchor='w')
        self.humidity_label.grid(row=0, column=1, sticky=W, padx=10, pady=5)
        
        # Row 2
        self.min_max_label = Label(details_frame, font=self.normal_font, 
                                  bg='#34495e', fg='white', anchor='w')
        self.min_max_label.grid(row=1, column=0, sticky=W, padx=10, pady=5)
        
        self.wind_label = Label(details_frame, font=self.normal_font, 
                               bg='#34495e', fg='white', anchor='w')
        self.wind_label.grid(row=1, column=1, sticky=W, padx=10, pady=5)
        
        # Row 3
        self.conditions_label = Label(details_frame, font=self.normal_font, 
                                     bg='#34495e', fg='white', anchor='w')
        self.conditions_label.grid(row=2, column=0, sticky=W, padx=10, pady=5)
        
        self.update_label = Label(details_frame, font=self.small_font, 
                                 bg='#34495e', fg='#bdc3c7', anchor='w')
        self.update_label.grid(row=2, column=1, sticky=W, padx=10, pady=5)
        
        # Hourly Forecast Section
        hourly_header = Frame(current_display, bg='#34495e')
        hourly_header.pack(fill=X, pady=(20, 10))
        
        Label(hourly_header, text="Hourly Forecast", font=self.header_font, 
              bg='#34495e', fg='white').pack(side=LEFT)
        
        self.hourly_frame = Frame(current_display, bg='#34495e')
        self.hourly_frame.pack(fill=BOTH, expand=True)
        
        # Forecast Tab
        self.forecast_tab = Frame(self.notebook, bg='#2c3e50')
        self.notebook.add(self.forecast_tab, text="5-Day Forecast", state='hidden')
        
        # Status Bar
        self.status = Label(self.root, text="Ready", bd=1, relief=SUNKEN, 
                          anchor=W, bg='#34495e', fg='white')
        self.status.pack(fill=X, side=BOTTOM)
    
    def fetch_weather_data(self, city=None):
        """Fetch weather data from API"""
        city = city or self.current_city.get()
        if not city:
            messagebox.showwarning("Warning", "Please enter a city name")
            return
        
        try:
            # Current weather
            url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={self.api_key}&units=metric"
            response = requests.get(url)
            data = response.json()
            
            if data['cod'] != 200:
                messagebox.showerror("Error", data['message'])
                return
            
            # Forecast data
            forecast_url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={self.api_key}&units=metric"
            forecast_data = requests.get(forecast_url).json()
            
            self.display_current(data)
            self.display_forecast(forecast_data)
            self.display_hourly(forecast_data)
            
            self.status.config(text=f"Showing weather for {data['name']}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to fetch data: {str(e)}")
            self.status.config(text="Error fetching data")
    
    def display_current(self, data):
        """Display current weather information"""
        # Weather icon
        icon_url = f"http://openweathermap.org/img/wn/{data['weather'][0]['icon']}@4x.png"
        img = Image.open(io.BytesIO(requests.get(icon_url).content))
        img = img.resize((150, 150), Image.Resampling.LANCZOS)
        self.weather_icon = ImageTk.PhotoImage(img)
        self.icon_label.config(image=self.weather_icon)
        
        # Update all labels
        self.city_label.config(text=f"{data['name']}, {data['sys']['country']}")
        self.temp_label.config(text=f"{data['main']['temp']:.1f}°C")
        self.feels_like_label.config(text=f"Feels like: {data['main']['feels_like']:.1f}°C")
        self.humidity_label.config(text=f"Humidity: {data['main']['humidity']}%")
        self.min_max_label.config(text=f"Min/Max: {data['main']['temp_min']:.1f}°C / {data['main']['temp_max']:.1f}°C")
        self.wind_label.config(text=f"Wind: {data['wind']['speed']} m/s")
        self.conditions_label.config(text=f"Conditions: {data['weather'][0]['description'].title()}")
        self.update_label.config(text=f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        
        # Show current weather tab
        self.notebook.select(self.current_tab)
    
    def display_hourly(self, data):
        """Display hourly forecast data"""
        for widget in self.hourly_frame.winfo_children():
            widget.destroy()
        
        # Get first 8 forecasts (24 hours, 3-hour intervals)
        hourly_data = data['list'][:8]
        
        # Create scrollable frame
        canvas = Canvas(self.hourly_frame, bg='#34495e', height=180, highlightthickness=0)
        scrollbar = Scrollbar(self.hourly_frame, orient="horizontal", command=canvas.xview)
        scrollable_frame = Frame(canvas, bg='#34495e')
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(xscrollcommand=scrollbar.set)
        
        canvas.pack(side="top", fill="both", expand=True)
        scrollbar.pack(side="bottom", fill="x")
        
        # Display hourly items
        for item in hourly_data:
            time = datetime.fromtimestamp(item['dt']).strftime('%H:%M')
            temp = item['main']['temp']
            icon = item['weather'][0]['icon']
            desc = item['weather'][0]['description']
            
            hour_frame = Frame(scrollable_frame, bg='#2c3e50', bd=0, 
                             highlightbackground='#7f8c8d', highlightthickness=1)
            hour_frame.pack(side=LEFT, padx=5, pady=5, ipadx=10, ipady=10)
            
            # Time label
            Label(hour_frame, text=time, font=self.small_font, 
                 bg='#2c3e50', fg='white').pack()
            
            # Weather icon
            icon_url = f"http://openweathermap.org/img/wn/{icon}.png"
            img = Image.open(io.BytesIO(requests.get(icon_url).content))
            img = img.resize((50, 50), Image.Resampling.LANCZOS)
            icon_img = ImageTk.PhotoImage(img)
            icon_label = Label(hour_frame, image=icon_img, bg='#2c3e50')
            icon_label.image = icon_img
            icon_label.pack()
            
            # Temperature
            Label(hour_frame, text=f"{temp:.1f}°C", font=self.normal_font, 
                 bg='#2c3e50', fg='white').pack()
            
            # Description
            Label(hour_frame, text=desc.title(), font=self.small_font, 
                 bg='#2c3e50', fg='#bdc3c7', wraplength=80).pack()
    
    def display_forecast(self, data):
        """Prepare 5-day forecast data"""
        for widget in self.forecast_tab.winfo_children():
            widget.destroy()
        
        # Group forecast by day
        forecast = {}
        for item in data['list']:
            date = datetime.fromtimestamp(item['dt']).strftime('%Y-%m-%d')
            if date not in forecast:
                forecast[date] = []
            forecast[date].append(item)
        
        # Display forecast
        for i, (date, items) in enumerate(forecast.items()):
            if i >= 5:  # Show only 5 days
                break
                
            # Forecast card
            day_frame = Frame(self.forecast_tab, bg='#34495e', bd=0,
                            highlightbackground='#7f8c8d', highlightthickness=1)
            day_frame.pack(fill=X, padx=10, pady=5, ipadx=10, ipady=10)
            
            # Date header
            Label(day_frame, 
                  text=datetime.strptime(date, '%Y-%m-%d').strftime('%A, %b %d'), 
                  font=self.header_font, bg='#34495e', fg='white').pack(anchor=W)
            
            # Get weather icon for the day
            icon_url = f"http://openweathermap.org/img/wn/{items[0]['weather'][0]['icon']}.png"
            img = Image.open(io.BytesIO(requests.get(icon_url).content))
            img = img.resize((50, 50), Image.Resampling.LANCZOS)
            icon_img = ImageTk.PhotoImage(img)
            icon_label = Label(day_frame, image=icon_img, bg='#34495e')
            icon_label.image = icon_img
            icon_label.pack(side=LEFT, padx=10)
            
            # Day summary
            temps = [item['main']['temp'] for item in items]
            avg_temp = sum(temps) / len(temps)
            condition = items[0]['weather'][0]['description']
            
            summary_frame = Frame(day_frame, bg='#34495e')
            summary_frame.pack(side=LEFT, fill=X, expand=True)
            
            Label(summary_frame, 
                  text=f"🌡 Avg: {avg_temp:.1f}°C", 
                  font=self.normal_font, bg='#34495e', fg='white').pack(anchor=W)
            
            Label(summary_frame, 
                  text=f"☁ {condition.title()}", 
                  font=self.normal_font, bg='#34495e', fg='white').pack(anchor=W)
            
            Label(summary_frame, 
                  text=f"💧 Humidity: {items[0]['main']['humidity']}%", 
                  font=self.normal_font, bg='#34495e', fg='white').pack(anchor=W)
    
    def show_forecast(self):
        """Show forecast tab"""
        if not self.current_city.get():
            messagebox.showwarning("Warning", "Please search for a city first")
            return
            
        self.notebook.tab(self.forecast_tab, state='normal')
        self.notebook.select(self.forecast_tab)

if __name__ == "__main__":
    root = Tk()
    app = WeatherApp(root)
    root.mainloop()