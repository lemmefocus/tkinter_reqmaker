from tkinter import Button, Entry, END
from tkinter import tix
from tkinter.tix import Tk
from tkinter import ttk
from tkinter import scrolledtext
import time
from tkinter.ttk import Combobox
from tkinter.ttk import Checkbutton
from get_functions import clicked, add_row, start, browse_files_get, save_config
from post_functions import browse_files_post, send_api_request, help_post


def main():
    window = Tk()
    window.geometry('450x300')
    window.resizable(False, False)
    window.title("Reqmaker")

    tab_control = ttk.Notebook(window)
    tab1 = ttk.Frame(tab_control)
    tab2 = ttk.Frame(tab_control)
    tab_control.add(tab1, text="GET")
    tab_control.add(tab2, text="POST")
    tab_control.pack(expand=1, fill='both')

    # GET tab ____________________________________________________________________________________

    url0 = Entry(tab1)
    url0.place(x=35, y=105, width=124, height=28)

    url1 = Entry(tab1)
    url1.place(x=285, y=105, width=124, height=28)

    url2 = Entry(tab1)
    url2.place(x=35, y=185, width=124, height=28)

    url3 = Entry(tab1)
    url3.place(x=285, y=185, width=124, height=28)

    urls = [url0, url1, url2, url3]

    tip = tix.Balloon()

    domen_input = Entry(tab1)
    domen_input.insert(END, "https://")
    domen_input.focus()
    domen_input.place(x=165, y=15, width=124, height=25)

    def wrapper():
        return clicked(urls, domen_input)

    button_accept = Button(tab1, text="Принять", command=wrapper)
    button_accept.place(x=197, y=50)

    add_button = Button(tab1, text="➕", command=lambda: add_row(urls, window, tab1, start_button))
    add_button.place(x=392, y=14, height=25)

    start_button = Button(tab1, text="Запустить", command=lambda: start(urls, tab1, tip))
    start_button.place(x=192, y=237)

    button_explore_get = Button(tab1, text="↑", command=lambda: browse_files_get(urls))
    button_explore_get.place(x=35, y=15, height=25)

    button_save_config = Button(tab1, text="↓", command=lambda: save_config(urls))
    button_save_config.place(x=65, y=15, height=25)

    # POST tab ___________________________________________________________________________________________

    button_post_help = Button(tab2, text="?", command=lambda: help_post())
    button_post_help.place(x=135, y=11, height=25)

    cookies_input = Entry(tab2)
    cookies_input.place(x=165, y=12, width=255.5, height=25)

    url_input = Entry(tab2)
    url_input.place(x=15, y=55, width=406, height=25)

    data_input = scrolledtext.ScrolledText(tab2)
    data_input.place(x=15, y=95, width=423, height=146)

    button_explore_post = Button(tab2, text="Заполнить данные",
                                 command=lambda: browse_files_post(cookies_input, data_input, url_input))
    button_explore_post.place(x=15, y=11, height=25)

    button_post_request = Button(tab2, text="Отправить",
                                 command=lambda: send_api_request(cookies_input, url_input, data_input))
    button_post_request.place(x=192, y=245)

    # Both tab ______________________________________________________________________________________________

    def on_tab_change(event):
        tab = event.widget.tab('current')['text']
        if tab == "POST":
            if len(urls) == 6:
                data_input.place(x=15, y=95, width=423, height=215)
                button_post_request.place(x=192, y=315)
            elif len(urls) >= 8:
                data_input.place(x=15, y=95, width=423, height=296)
                button_post_request.place(x=192, y=395)

    tab_control.bind('<<NotebookTabChanged>>', on_tab_change)

    window.mainloop()


if __name__ == "__main__":
    main()
