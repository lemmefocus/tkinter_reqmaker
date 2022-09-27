import tkinter
from tkinter import TclError
from tkinter.ttk import Radiobutton
from tkinter import Button, Entry, END
from tkinter import tix, IntVar
from tkinter.tix import Tk
from tkinter import ttk
from tkinter import scrolledtext
from idlelib.tooltip import Hovertip
from tkinter.ttk import Combobox
from tkinter.ttk import Checkbutton
from get_functions import clicked, add_row, start, browse_files_get, save_config, remove_row
from post_functions import browse_files_post, send_api_request, help_post, raw_vision, formdata_vision
import customtkinter

customtkinter.set_appearance_mode("dark")  # Mgodes: system (default), light, dark
customtkinter.set_default_color_theme("dark-blue")  # Themes: blue (default), dark-blue, green


def main():
    window = customtkinter.CTk()
    window.geometry('450x300')
    window.resizable(False, False)
    window.title("Reqmaker")

    style = ttk.Style()
    style.configure("TNotebook", background="")

    tab_control = ttk.Notebook(window)
    tab1 = customtkinter.CTkFrame(tab_control, fg_color="#a7aeb8", bg_color="#a7aeb8")
    tab2 = customtkinter.CTkFrame(tab_control, fg_color="#a7aeb8", bg_color="#a7aeb8")
    tab_control.add(tab1, text="GET")
    tab_control.add(tab2, text="API")
    tab_control.pack(expand=1, fill='both')

    # GET tab ____________________________________________________________________________________

    url0 = customtkinter.CTkEntry(tab1)
    url0.place(x=35, y=105, width=124, height=28)

    url1 = customtkinter.CTkEntry(tab1)
    url1.place(x=285, y=105, width=124, height=28)

    url2 = customtkinter.CTkEntry(tab1)
    url2.place(x=35, y=185, width=124, height=28)

    url3 = customtkinter.CTkEntry(tab1)
    url3.place(x=285, y=185, width=124, height=28)

    urls = [url0, url1, url2, url3]

    domen_input = customtkinter.CTkEntry(tab1)
    domen_input.insert(END, "https://")
    domen_input.focus()
    domen_input.place(x=165, y=15, width=124, height=25)

    def wrapper():
        return clicked(urls, domen_input)

    button_accept = customtkinter.CTkButton(tab1, width=30, height=20, text="Accept", command=wrapper)
    button_accept.place(x=190, y=50, width=80)

    add_button = customtkinter.CTkButton(tab1, width=25, text="Add input row",
                                         command=lambda: add_row(urls, window, tab1, start_button))
    add_button.place(x=312, y=14, height=25, width=120)

    remove_button = customtkinter.CTkButton(tab1, width=25, text="Remove input row",
                                         command=lambda: remove_row(urls, window, start_button, raw_elements))
    remove_button.place(x=312, y=44, height=25, width=120)

    start_button = customtkinter.CTkButton(tab1, width=25, height=22, text="Execute",
                                           command=lambda: start(urls, tab1))
    start_button.place(x=185, y=237, width=80)

    #todo
    # photo = tkinter.PhotoImage(file=r"C:\Gf123g\circle.png")
    #
    # # Resizing image to fit on button
    # photoimage = photo.subsample(3, 3)

    button_explore_get = customtkinter.CTkButton(tab1, width=25, text="↑", command=lambda: browse_files_get(urls))
    button_explore_get.place(x=35, y=15, height=25)

    button_save_config = customtkinter.CTkButton(tab1, width=25, text="↓", command=lambda: save_config(urls))
    button_save_config.place(x=68, y=15, height=25)

    # POST tab ___________________________________________________________________________________________

    button_post_help = customtkinter.CTkButton(tab2, width=25, text_font=("Arial", 8), text="?",
                                               command=lambda: help_post())
    button_post_help.place(x=135, y=11, height=25)

    cookies_input = customtkinter.CTkEntry(tab2, placeholder_text="cookies")
    cookies_input.place(x=167, y=11.3, width=270, height=25)

    url_input = customtkinter.CTkEntry(tab2, placeholder_text="url")
    url_input.place(x=15, y=55, width=421.5, height=25)

    data_input = scrolledtext.ScrolledText(tab2, bg='#3c3c3c', fg="white")
    data_input.focus()
    data_input.lift()
    data_input.place(x=15, y=95, width=423, height=146)

    button_explore_post = customtkinter.CTkButton(tab2, width=20, text_font=("Arial", 8), text="Заполнить данные",
                                                  command=lambda: browse_files_post(cookies_input, data_input,
                                                                                    url_input, selected))
    button_explore_post.place(x=15, y=11, height=25)

    def change_postcheckbutton():
        if post_checkbutton.get() == 0:
            post_checkbutton.set(0)
        else:
            delete_checkbutton.set(0)
            put_checkbutton.set(0)
            post_checkbutton.set(1)

    def change_deletecheckbutton():
        if delete_checkbutton.get() == 0:
            delete_checkbutton.set(0)
            data_input.delete('1.0', END)
        else:
            delete_checkbutton.set(1)
            put_checkbutton.set(0)
            post_checkbutton.set(0)
            data_input.delete('1.0', END)

    def change_putcheckbutton():
        if put_checkbutton.get() == 0:
            put_checkbutton.set(0)
        else:
            delete_checkbutton.set(0)
            put_checkbutton.set(1)
            post_checkbutton.set(0)

    post_checkbutton = IntVar()
    post_checkbutton.set(0)
    post_checkbox = customtkinter.CTkCheckBox(tab2, width=20, height=20, text_font=("Arial", 8),
                                              border_color="black", border_width=2,
                                              text_color="black", text="POST", variable=post_checkbutton,
                                              command=change_postcheckbutton)
    post_checkbox.place(x=13, y=248)

    delete_checkbutton = IntVar()
    delete_checkbutton.set(0)
    delete_checkbox = customtkinter.CTkCheckBox(tab2, width=20, height=20, text_font=("Arial", 8),
                                                border_color="black", border_width=2,
                                                text_color="black", text="DELETE", variable=delete_checkbutton,
                                                command=change_deletecheckbutton)
    delete_checkbox.place(x=70, y=248)

    put_checkbutton = IntVar()
    put_checkbutton.set(0)
    put_checkbox = customtkinter.CTkCheckBox(tab2, width=20, height=20, text_font=("Arial", 8),
                                             border_color="black", border_width=2,
                                             text_color="black", text="PUT", variable=put_checkbutton,
                                             command=change_putcheckbutton)
    put_checkbox.place(x=140, y=248)

    button_post_request = customtkinter.CTkButton(tab2, width=30, height=20, text_font=("Arial", 8), text="Отправить",
                                                  command=lambda: send_api_request(cookies_input, url_input, data_input,
                                                                                   post_checkbutton, delete_checkbutton,
                                                                                   put_checkbutton, raw_radio, raw_elements))
    button_post_request.place(x=192, y=248)

    Hovertip(delete_checkbox, 'Поле с body при delete запросе не будет учитываться', hover_delay=0)

    selected = IntVar()
    raw_radio = customtkinter.CTkRadioButton(tab2, width=20, height=20, text_font=("Arial", 8),
                                             border_color="black", value=1,
                                             text_color="black", text="raw", variable=selected,
                                             command=lambda: raw_vision(data_input, tab2, formdata_radio, raw_elements, urls, add_two_raw_elements, add_six_raw_elements))

    raw_radio.place(x=302, y=248)

    formdata_radio = customtkinter.CTkRadioButton(tab2, width=20, height=20, text_font=("Arial", 8),
                                             border_color="black", border_width_unchecked=6,
                                             text_color="black", text="form-data", variable=selected,
                                             command=lambda: formdata_vision(data_input, urls, raw_elements))


    formdata_radio.place(x=360, y=248)

    raw_elements = []

    def add_two_raw_elements():
        raw_entry7 = tkinter.Entry(tab2)
        raw_entry7.place(x=33, y=240, width=145, height=28)

        raw_entry8 = tkinter.Entry(tab2)
        raw_entry8.place(x=265, y=240, width=145, height=28)

        raw_elements.extend([raw_entry7, raw_entry8])

    def add_six_raw_elements():
        raw_entry7 = tkinter.Entry(tab2)
        raw_entry7.place(x=33, y=240, width=145, height=28)

        raw_entry8 = tkinter.Entry(tab2)
        raw_entry8.place(x=265, y=240, width=145, height=28)

        raw_entry9 = tkinter.Entry(tab2)
        raw_entry9.place(x=33, y=285, width=145, height=28)

        raw_entry10 = tkinter.Entry(tab2)
        raw_entry10.place(x=265, y=285, width=145, height=28)

        raw_entry11 = tkinter.Entry(tab2)
        raw_entry11.place(x=33, y=330, width=145, height=28)

        raw_entry12 = tkinter.Entry(tab2)
        raw_entry12.place(x=265, y=330, width=145, height=28)

        raw_elements.extend([raw_entry7, raw_entry8,
                             raw_entry9, raw_entry10,
                             raw_entry11, raw_entry12])

    # Both tab ______________________________________________________________________________________________

    def on_tab_change(event):
        try:
            data_input.focus()
        except TclError:
            pass
        tab = event.widget.tab('current')['text']
        if tab == "API":
            try:
                if len(urls) == 4:
                    button_post_request.place(x=192, y=248)
                    put_checkbox.place(x=140, y=248)
                    delete_checkbox.place(x=70, y=248)
                    post_checkbox.place(x=13, y=248)
                    raw_radio.place(x=302, y=247)
                    formdata_radio.place(x=360, y=247)
                    if selected.get() == 0:
                        data_input.place(x=15, y=95, width=423, height=146)
                if len(urls) == 6:
                    button_post_request.place(x=192, y=317)
                    post_checkbox.place(x=13, y=318)
                    delete_checkbox.place(x=70, y=318)
                    put_checkbox.place(x=140, y=318)
                    raw_radio.place(x=302, y=317)
                    formdata_radio.place(x=360, y=317)
                    if selected.get() == 0:
                        data_input.place(x=15, y=95, width=423, height=215)
                    if (selected.get() == 1 and len(raw_elements) == 10) or (selected.get() == 1 and len(raw_elements) == 8):
                        add_two_raw_elements()
                elif len(urls) >= 8:
                    button_post_request.place(x=192, y=397.5)
                    post_checkbox.place(x=13, y=398)
                    delete_checkbox.place(x=70, y=398)
                    put_checkbox.place(x=140, y=398)
                    raw_radio.place(x=302, y=397)
                    formdata_radio.place(x=360, y=397)
                    if selected.get() == 0:
                        data_input.place(x=15, y=95, width=423, height=296)
                    if (selected.get() == 1 and len(raw_elements) == 10) or (selected.get() == 1 and len(raw_elements) >= 8):
                        add_six_raw_elements()
            except TclError:
                pass

    tab_control.bind('<<NotebookTabChanged>>', on_tab_change)

    window.mainloop()


if __name__ == "__main__":
    main()