import tkinter as tk
import re
import bs4
import requests

URL = 'https://www.gismeteo.ru/news/'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:77.0) Gecko/20190101 Firefox/77.0'}


def libParse():
    response = requests.get(URL, headers=headers)
    htmlCode = response.text
    soup = bs4.BeautifulSoup(htmlCode, features="lxml")
    divs = soup.find_all("div", class_="item-description")
    result = ''
    for div in divs:
        time = div.find('div', class_='item-date').text
        title = div.find('div', class_='item-title').text
        result += f"{title} | {time}\n"
    return result.strip()

def regParse():
        response = requests.get(URL, headers=headers)
        htmlCode = response.text
        divs = re.split('item-description',htmlCode)
        result = ''
        for div in divs:
                match = re.search('title\">(.+?)<\/div><div class=\"item-excerpt\">.+?<\/div><div class=\"item-bottom\"><div class=\"item-date">(.+?[,] .+?:\d\d)<\/div>',div, flags=re.DOTALL)
                if match:
                    title, time = match.groups()
                    result += f'{title}|{time}\n'
        return result.strip()

def buttonClick(ctrl, method):
    ctrl.delete("1.0", tk.END)
    ctrl.insert(tk.END, libParse() if method == "lib" else regParse())

form = tk.Tk()
form.title('KT4 VARIANT 13')
editText = tk.Text(height = 30, width  = 100)
editText.pack()
libButton = tk.Button(text='By library', command=lambda :buttonClick(editText,method='lib'))
libButton.pack()
regButton = tk.Button(text='By regular', command=lambda :buttonClick(editText,method='reg'))
regButton.pack()
form.mainloop()
