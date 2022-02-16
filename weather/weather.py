import tkinter as tk
import requests
import time
import sqlite3

''' Creating a database as weather.db and connecting it'''
conn = sqlite3.connect('weather.db')
c = conn.cursor()


'''Creating a canvas for weather details to show up using tkinter library'''
def getWeather(canvas):
    city = textfield.get()
    api = "http://api.openweathermap.org/data/2.5/weather?q=" + city +"&appid=ba91e931326e40738534796eef2330ba"
    json_data = requests.get(api).json()
    condition = json_data['weather'][0]['main']
    temp = int(json_data['main']['temp'] - 273.15)
    min_temp = int(json_data['main']['temp_min'] - 273.15)
    max_temp = int(json_data['main']['temp_max'] - 273.15)
    pressure = json_data['main']['pressure']
    humidity = json_data['main']['humidity']
    sunrise = time.strftime("%I:%M:%S", time.gmtime(json_data['sys']['sunrise'] - 21600))
    sunset = time.strftime("%I:%M:%S", time.gmtime(json_data['sys']['sunset'] - 21600))
    
    c.execute('CREATE TABLE IF NOT EXISTS info (temp INT,min_temp INT,max_temp INT, pressure REAL, humidity REAL, sunrise TIME, sunset TIME)')

    c.execute("INSERT INTO info (temp, min_temp, max_temp, pressure, humidity, sunrise, sunset ) VALUES(?, ?, ?, ?, ?, ?, ?)",
                                                  (temp, min_temp, max_temp, pressure, humidity, sunrise, sunset ))
 
    
    c.execute("SELECT * FROM info")
    results = c.fetchall()
    print(results)
    
    
    conn.commit()

    final_info = condition + "\n" + str(temp) + "C"
    final_data = "\n" + "Max Temp" + str(max_temp) + "\n" + "Min Temp:" + str(min_temp) + "\n" + "Pressure" + str(pressure) + "\n" + "Humidity" + str(humidity) + "\n" + "Sunrise" + sunrise + "\n" + "Sunset: " + sunset
    label1.config(text = final_info)
    label2.config(text = final_data)




''' Creating a canvas outline with the title'''
canvas = tk.Tk()
canvas.geometry("600x500")
canvas.title("Weather App")


''' Assigning font style with size ''' 
f = ("poppins", 15, "bold")
t= ("poppins", 35, " bold")

textfield = tk.Entry(canvas, font = t)
textfield.pack(pady = 20)
textfield.focus();
textfield.bind('<Return>', getWeather)

label1 = tk.Label(canvas, font = t)
label1.pack()
label2 = tk.Label(canvas, font = f)
label2.pack()

canvas.mainloop()


c.close()
conn.close()