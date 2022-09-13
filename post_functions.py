from tkinter import Label, END, Entry
from validator_collection import checkers
from tkinter import filedialog
from tkinter import messagebox
import requests
import json
import time

labels = []

def browse_files_post(cookies_input, data_input, url_input):

    try:
        filename = filedialog.askopenfilename(initialdir="/",
                                              title="Select a File",
                                              filetypes=(("Text files",
                                                          "*.txt*"),
                                                         ("all files",
                                                          "*.*")))

        text_file = open(filename, "r")
        rows = text_file.readlines()

        correct_data = [row.rstrip('\n') for row in rows[0:2]]

        cookies_input.delete(0, END)
        cookies_input.insert(0, correct_data[0])

        url_input.delete(0, END)
        url_input.insert(0, correct_data[1])

        body = ''
        for _ in rows[2::]:
            body = body + _.strip('\n').strip("")

        data_input.delete(1.0, END)
        data_input.insert(1.0, body)

        text_file.close()

    except FileNotFoundError:
        pass


def help_post():
    messagebox.showinfo('Справка', '1. В поле с cookies введите данные вместе с фигурными скобками \n2. В поле с endpoint введите данные с ковычками \n3. В поле с body введите данные вместе с фигурными скобками')


def send_api_request(cookies_input, url_input, data_input, post_checkbutton, delete_checkbutton, put_checkbutton):

    fields = [checkers.is_not_empty(cookies_input.get()), checkers.is_not_empty(url_input.get()), len(data_input.get('1.0', END)) != 1]

    checkbutton_dict = {"post": post_checkbutton, "delete": delete_checkbutton, "put": put_checkbutton}

    method = ''

    for key, value in checkbutton_dict.items():
        if value.get() == 1:
            method = key

    if fields.count(True) == 3:
        headers = {
            "sec-ch-ua-platform": "Windows",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "cross-site",
            "Sec-Fetch-User": "?1",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36"
        }

        response = getattr(requests, method)
        if method == "post":

            messages_response = response(url=url_input.get().replace("\'", ""), data=json.loads(data_input.get('1.0', END)),
                                     cookies=json.loads(cookies_input.get()), headers=headers)
        else:
            messages_response = response(url=url_input.get().replace("\'", ""),
                                         cookies=json.loads(cookies_input.get()), headers=headers)
        messagebox.showinfo('', f'{messages_response.status_code}')


    else:
        messagebox.showwarning('', 'Некоторые поля не заполнены')
