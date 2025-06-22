
# Weather App

A modern, feature-rich weather application built with Python and Tkinter that provides current weather conditions, hourly forecasts, and 5-day weather predictions for any city worldwide.



## Screenshots

![App Screenshot](https://github.com/Subham-Semwal/Weather-App/blob/main/weather%20app.jpg)


## Features

- 🌦️ **Current Weather**: Real-time temperature, humidity, wind speed, and conditions
- ⏳ **Hourly Forecast**: 24-hour weather predictions with 3-hour intervals
- 📅 **5-Day Forecast**: Daily weather outlook with average temperatures
- 🌍 **Global Coverage**: Search for any city worldwide
- 🎨 **Modern UI**: Clean, intuitive interface with weather icons
- 🔄 **Auto-update**: Timestamp of last data refresh


## Requirement
- Python 3.6+
- Required Python packages:
  - `requests`
  - `Pillow`
  - `tkinter` (usually included with Python)
## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/weather-analytics-pro.git
   cd weather-analytics-pro
   
2. Install the required packages::
   ```bash
   pip install -r requirements.txt

3. Run the application:
   ```bash
   python weather_app.py

   

    
## Usage

1. Enter a city name in the search box

2. Click "Search" to view current weather

3. Use the tabs to switch between:

4. Current weather (default view)

5. day forecast (click "Forecast" button)

6. The hourly forecast is displayed at the bottom of the current weather tab


## ConfigurationThe 
app uses OpenWeatherMap API. To use your own API key:

1. Get a free API key from OpenWeatherMap
2. Replace the api_key variable in the code with your key:
   ```bash
   self.api_key = "your_api_key_here"  
## Future Enhancements
- Add weather maps
- Implement temperature unit switching (Celsius/Fahrenheit)
- Add location detection
- Include air quality data
- Add historical weather data
