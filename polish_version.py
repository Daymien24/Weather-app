import tkinter as tk
import requests
from datetime import datetime
from PIL import Image, ImageTk



dni = ['Pon', 'Wt', 'Sr', 'Czw', 'Pt', 'Sob', 'Niedz', 'Pon', 'Wt', 'Sr', 'Czw']



def format_response(weather):
    try:        
        name = weather['city']['name']
        dzisiaj = datetime.today().weekday()
        result = ['Miasto: ', name, '\n']
        mnoznik = 1
        
        for i in range(0,4):
            dzien = dni[dzisiaj+i]
            
            if i == 0:
                temp = weather['list'][i]['main']['temp']
                data = weather['list'][i]['dt_txt']
            else:
                temp = weather['list'][i-2+7*mnoznik]['main']['temp']                
                mnoznik+=1
            final_str = f'{dzien}, Temp: {temp:.0f}°C\n\n'
            result.append(final_str)
    except:
        final_str = 'Houston, mamy problem!'
    return result

def format_response2(weather):
    try:
        name = weather['name']
        desc = weather['weather'][0]['description']
        temp = weather['main']['temp']
        ts_sunrise = int(weather['sys']['sunrise']+weather['timezone'])
        sunrise = datetime.utcfromtimestamp(ts_sunrise).strftime('%H:%M:%S')
        ts_sunset = int(weather['sys']['sunset']+weather['timezone'])
        sunset = datetime.utcfromtimestamp(ts_sunset).strftime('%H:%M:%S')
        wind = weather['wind']['speed']

        final_str = f'Miasto: {name} \nWarunki: {desc} \nAktualna Temperatura: {temp:.1f}C\nWschod Slonca: {sunrise} \nZachod Slonca: {sunset} \nWiatr: {wind}m/s'

    except:
        final_str = 'Houston, mamy problem!'
    return final_str

     

def get_weather(city):
    weather_key = '57981b1f7b6e3ffab26d7516b0c74b9b'
    url = 'https://api.openweathermap.org/data/2.5/forecast'
    params = {'APPID': weather_key, 'q': city, 'units': 'metric', 'cnt': 42, 'lang': 'pl'}
    response = requests.get(url, params=params)
    weather = response.json()

       
    wynik = format_response(weather)
    wynik2 = ''.join(str(e) for e in wynik)
    #print(wynik2)   
    #print(response.json())
    label['text'] = wynik2
    photos = []
    mnoznik=1

    for i in range(0,4):
        if i == 0:
            icon_name = weather['list'][i]['weather'][0]['icon']
            photos.append(icon_name)
        else:
            icon_name = weather['list'][i-2+7*mnoznik]['weather'][0]['icon']
            photos.append(icon_name)
            mnoznik+=1

    open_image(*photos)

def get_weather_today(city):
    weather_key = 'a4aa5e3d83ffefaba8c00284de6ef7c3'
    url = 'https://api.openweathermap.org/data/2.5/weather'
    params = {'APPID': weather_key, 'q': city, 'units': 'metric', 'lang': 'pl'}
    response = requests.get(url, params=params)
    weather = response.json()

    #print(response.json()) zeby zoabczyc jak wyglada jsonek
    label['text'] = ""

    label['text'] = format_response2(weather)
    print(weather)
    photos = []
    icon_name = weather['weather'][0]['icon']
    photos.append(icon_name)
    open_image_today(*photos)

photos_saved = []

def open_image(*photos):
    paddy = 10
    for i in range(0,4):
        if i==0:
            weather_icon.delete("all")
        size = int(lower_frame.winfo_height()*0.23)
        img = ImageTk.PhotoImage(Image.open('./img/'+photos[i]+'.png').resize((size, size)))
        #weather_icon.delete("all") # usuwa wszystkie ikony jake sa w canvasie
        weather_icon.create_image(0,0+paddy, anchor='nw', image=img)
        weather_icon.image = img
        photos_saved.append(img)
        paddy+=50

def open_image_today(*photos):    
    size = int(lower_frame.winfo_height()*0.25)
    img = ImageTk.PhotoImage(Image.open('./img/'+photos[0]+'.png').resize((size, size)))
    weather_icon.delete("all") # usuwa wszystkie ikony jake sa w canvasie
    weather_icon.create_image(10,45, anchor='nw', image=img)
    weather_icon.image = img
    photos_saved.append(img)


root = tk.Tk();
root.title("Pogodynka")
root.iconbitmap('ikona.ico')

canvas = tk.Canvas(root, height=575, width=600)
canvas.pack()



background_img = tk.PhotoImage(file='img2.png',)
background_label = tk.Label(root, image=background_img)
background_label.place(x=0,y=0, relwidth=1, relheight=1)

frame= tk.Frame(root, bg='#80c1ff', bd=5)
frame.place(relx=0.5, rely=0.3,relwidth=0.6, relheight=0.1, anchor='n') #resnponsive, change size ekranu, wypelnia kolorkiem okno


entry = tk.Entry(frame)
entry.insert(0,"Warsaw")
entry.place(relwidth=0.5, relheight=1)

button = tk.Button(frame, font=('Comic Sans MS', '10','bold'), text="Prognoza", bd = 3, activeforeground = 'green', command=lambda: get_weather(entry.get()))
button.place(relx=0.54, relwidth=0.2, relheight=1)
button2 = tk.Button(frame, font=('Comic Sans MS', '10','bold'), text="Teraz", bd = 3, activeforeground = 'green', command=lambda: get_weather_today(entry.get()))
button2.place(relx=0.8, relwidth=0.2, relheight=1)

lower_frame = tk.Frame(root, bg='#80c1ff', bd=10)
lower_frame.place(relx=0.5, rely=0.45, relwidth=0.6, relheight=0.4, anchor='n')


label = tk.Label(lower_frame, font = ('Comic Sans MS', '13','bold'), anchor='nw', justify='left', bd=4)
label.place( relwidth=1, relheight=1)

weather_icon = tk.Canvas(label, bd=0, highlightthickness=0)
weather_icon.place(relx=.8, relwidth=1)

root.mainloop()