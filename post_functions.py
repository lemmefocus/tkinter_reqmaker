import tkinter
from tkinter import END
from tkinter import scrolledtext
import customtkinter
from validator_collection import checkers
from tkinter import filedialog
from tkinter import messagebox
import requests
import json

labels = []

def browse_files_post(cookies_input, data_input, url_input, selected):
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

        if selected.get() != 1:
            data_input.delete(1.0, END)
            data_input.insert(1.0, body)

        text_file.close()

    except FileNotFoundError:
        pass


def help_post():
    messagebox.showinfo('Справка',
                        '1. В поле с cookies введите данные вместе с фигурными скобками \n2. В поле с endpoint введите данные с ковычками \n3. В поле с body введите данные вместе с фигурными скобками')


def send_api_request(cookies_input, url_input, data_input, post_checkbutton, delete_checkbutton, put_checkbutton, raw_radio, raw_elements):
    fields = [checkers.is_not_empty(cookies_input.get()), checkers.is_not_empty(url_input.get()),
              len(data_input.get('1.0', END)) != 1]

    checkbutton_dict = {"post": post_checkbutton, "delete": delete_checkbutton, "put": put_checkbutton}

    headers = {
        "sec-ch-ua-platform": "Windows",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "cross-site",
        "Sec-Fetch-User": "?1",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36"
    }

    method = ''

    for key, value in checkbutton_dict.items():
        if value.get() == 1:
            method = key

    raw_elements_dict = {raw_elements[i].get(): raw_elements[i + 1].get() for i in range(2, len(raw_elements), 2) if len(raw_elements[i].get()) != 0}

    try:
        response = getattr(requests, method)
        if raw_radio.value == 1:

            if method == "post" or method == "put":
                try:
                    messages_response = response(url=url_input.get().replace("\'", ""),
                                                 data=raw_elements_dict,
                                                 cookies=json.loads(cookies_input.get()), headers=headers)

                    messagebox.showinfo('', f'{messages_response.status_code}')

                except ValueError:
                    messagebox.showwarning('', 'Некоторые поля заполнены не по синтаксису')
            else:
                if (fields[0] is True) and (fields[1] is True):
                    try:
                        messages_response = response(url=url_input.get().replace("\'", ""),
                                                     cookies=json.loads(cookies_input.get()), headers=headers)
                        messagebox.showinfo('', f'{messages_response.status_code}')

                    except ValueError:
                        messagebox.showwarning('', 'Некоторые поля заполнены не по синтаксису')
                else:
                    messagebox.showwarning('', 'Некоторые поля не заполнены')
        else:
            if method == "post" or method == "put":
                if fields.count(True) == 3:
                    try:
                        messages_response = response(url=url_input.get().replace("\'", ""),
                                                     data=json.loads(data_input.get('1.0', END)),
                                                     cookies=json.loads(cookies_input.get()), headers=headers)

                        messagebox.showinfo('', f'{messages_response.status_code}')

                    except ValueError:
                        messagebox.showwarning('', 'Некоторые поля заполнены не по синтаксису')
                else:
                    messagebox.showwarning('', 'Некоторые поля не заполнены')

            else:
                if (fields[0] is True) and (fields[1] is True):
                    try:
                        messages_response = response(url=url_input.get().replace("\'", ""),
                                                     cookies=json.loads(cookies_input.get()), headers=headers)
                        messagebox.showinfo('', f'{messages_response.status_code}')

                    except ValueError:
                        messagebox.showwarning('', 'Некоторые поля заполнены не по синтаксису')
                else:
                    messagebox.showwarning('', 'Некоторые поля не заполнены')

    except AttributeError:
        messagebox.showwarning('', 'Выберите тип запроса')


def raw_vision(data_input, tab2, formdata_radio, raw_elements, urls, add_two_raw_elements, add_six_raw_elements):
    #todo
    formdata_radio.configure(border_width=3)
    data_input.place(x=10000, y=10000, width=322, height=322)
    key = customtkinter.CTkLabel(tab2)
    key.configure(text="key", fg_color="#a7aeb8", bg_color='#a7aeb8', text_color="black", text_font=("Arial", 9, "bold"))
    key.place(x=34, y=86.5, height=15)

    value = customtkinter.CTkLabel(tab2)
    value.configure(text="value", fg_color="#a7aeb8", bg_color='#a7aeb8', text_color="black", text_font=("Arial", 9, "bold"))
    value.place(x=267.7, y=86.5, height=15)

    raw_entry1 = tkinter.Entry(tab2)
    raw_entry1.place(x=33, y=105, width=145, height=28)

    raw_entry2 = tkinter.Entry(tab2)
    raw_entry2.place(x=265, y=105, width=145, height=28)

    raw_entry3 = tkinter.Entry(tab2)
    raw_entry3.place(x=33, y=150, width=145, height=28)

    raw_entry4 = tkinter.Entry(tab2)
    raw_entry4.place(x=265, y=150, width=145, height=28)

    raw_entry5 = tkinter.Entry(tab2)
    raw_entry5.place(x=33, y=195, width=145, height=28)

    raw_entry6 = tkinter.Entry(tab2)
    raw_entry6.place(x=265, y=195, width=145, height=28)

    raw_elements.extend([key, value,
                         raw_entry1, raw_entry2, raw_entry3,
                         raw_entry4, raw_entry5, raw_entry6])

    if len(urls) == 6:
        add_two_raw_elements()

    if len(urls) == 8:
        add_six_raw_elements()


def formdata_vision(data_input, urls, raw_elements):
    for i in raw_elements:
        i.destroy()

    for _ in range(len(raw_elements)):
        del raw_elements[-1]
    if len(urls) == 4:
        data_input.place(x=15, y=95, width=423, height=146)
    elif len(urls) == 6:
        data_input.place(x=15, y=95, width=423, height=215)
    elif len(urls) >= 8:
        data_input.place(x=15, y=95, width=423, height=296)