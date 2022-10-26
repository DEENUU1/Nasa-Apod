from tkinter import *
import tkinter as tk
from tkcalendar import DateEntry
from PIL import ImageTk, Image
import webbrowser
import requests
import json
from urllib.request import urlopen
from pprint import pformat

#TKINTER WINDOWS CLASS
class Root(tk.Tk):
    def __init__(self):
        super().__init__()

if __name__ == '__main__':
    root = Tk()
    root.title("Kosmiczny katalog")
    root.resizable(False, False)

#FUNCTION FOR HYPERLINK OPPENING
def callback(url):
    webbrowser.open_new_tab(url)

#FUNCTION TO DISPLAY USER DATE
def showdate():
    label2.config(text=cal.get_date())
    user_date = label2.cget("text")
    return user_date

#MAIN APP FUNCTION
def showapp(event):
    #CLOSSING WIDGET
    for widget in first_frame.winfo_children():
        widget.destroy()
    for widget in second_frame.winfo_children():
        widget.destroy()

    #LINK DISPLAY
    link = tk.Label(second_frame, text="Image in full quality", font=('Helveticabold', 10), bg='#121212',
                    fg='green',
                    cursor="hand2")

    link_2 = tk.Label(second_frame, text="Nasa APOD", font=('Helveticabold', 10), bg='#121212', fg='green',
                      cursor="hand2")


    #HERE YOU CAN PASTE YOUR API KEY BETWEEN EMPTY '' 
    #https://api.nasa.gov/ if you don't know what to do
    #Look at readme file
    api_key = ''
    URL_APOD = 'https://api.nasa.gov/planetary/apod'

    #PARAMS FOR API
    date = showdate()
    params = {
        'api_key': api_key,
        'date': date,
        'hd': 'True'
    }

    response_image = requests.get(URL_APOD, params=params)

    json_data = json.loads(response_image.text)
    image_url = json_data['hdurl']
    image_descrip = json_data['explanation']
    image_title = json_data['title']

    image_descrip_2 = pformat(image_descrip)
    chars_to_remove = ["(", ")", "'"]
    for char in chars_to_remove:
        image_descrip_2 = image_descrip_2.replace(char, "")

    imageUrl = image_url
    with urlopen(imageUrl) as fd:
        image = Image.open(fd).resize((600,600))

    my_img = ImageTk.PhotoImage(image)
    canvas2.create_image(300,300, image=my_img)
    canvas2.nasa_img = my_img

    text_label = tk.Label(first_frame, text=image_title + "\n\n" + image_descrip_2, bg='#121212', fg='white')
    text_label.pack()

    link.bind("<Button-1>", lambda e: callback(image_url))
    link.pack()

    link_2.bind("<Button-1>", lambda e: callback("https://apod.nasa.gov/apod/astropix.html"))
    link_2.pack()


#Tło aplikacji
HEIGHT = 700
WIDTH = 1200
canvas = tk.Canvas(root, height = HEIGHT, width = WIDTH, bg = '#1D2022')
canvas.pack()

#Pola wyznaczone dla tekstu
first_frame = tk.Frame(root, bg='#121212')
first_frame.place(relx=0.64, rely=0.1, relheight=0.685, relwidth=0.35)

second_frame = tk.Frame(root, bg='#121212')
second_frame.place(relx=0.64, rely=0.79, relheight=0.2, relwidth=0.35)

#IMAGE DISPLAY CANVAS
canvas2 = Canvas(root, width=400, height=400, bg='#1D2022', highlightthickness=0, bd=0, relief='ridge')
canvas2.pack()
canvas2.place(relx=0.03, rely=0.05, relheight=0.9, relwidth=0.6)

#CALENDAR
cal = DateEntry(root, width=16, background='black', foreground='white', bd=2)
cal.place(relx=0.80, rely=0.01, relheight=0.05, relwidth=0.1)

label2 = Label(canvas, text="")
label2.place(relx=0.80, rely=0.01, relheight=0.05, relwidth=0.1)

button3 = Button(canvas, text="Choose date", command=showdate)
button3.place(relx=0.89, rely=0.01, relheight=0.05, relwidth=0.1)

button2 = tk.Button(canvas, text = "Comfirm")
button2.bind('<Button-1>', showapp)
button2.place(relx=0.70, rely=0.01, relheight=0.05, relwidth=0.1)

root.mainloop()

