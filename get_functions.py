from tkinter import Label, END, Entry
from validator_collection import checkers
from tkinter import filedialog
from tkinter import messagebox
from idlelib.tooltip import Hovertip
import customtkinter
import asyncio
import aiohttp
import time

labels = []


def clear_labels():
    if labels:
        for _ in labels:
            _.destroy()


def clicked(urls, domen_input):
    clear_labels()

    for url in urls:
        url.delete(0, END)
        url.insert(0, domen_input.get())


def add_row(urls, window, tab1, start_button):
    if labels and len(urls) < 9:
        for _ in labels:
            _.destroy()

    if 340 <= int(window.winfo_height()) < 420:
        window.geometry(f'450x{int(window.winfo_height()) + int(80)}')
        start_button.place(x=185, y=int(start_button.winfo_y()) + 78)
    if int(window.winfo_height()) < 340:
        window.geometry(f'450x{int(window.winfo_height()) + int(70)}')
        start_button.place(x=185, y=int(start_button.winfo_y()) + 73)

    if len(urls) < 8:
        row_list_copy = urls.copy()
        for _ in range(1):
            left = customtkinter.CTkEntry(tab1)
            left.place(x=row_list_copy[-2].winfo_x(), y=row_list_copy[-2].winfo_y() + 80, width=124, height=28)
            right = customtkinter.CTkEntry(tab1)
            right.place(x=row_list_copy[-1].winfo_x(), y=row_list_copy[-1].winfo_y() + 80, width=124, height=28)
            urls.extend((left, right))


def remove_row(urls, window, start_button, raw_elements):
    if len(urls) > 4:
        if len(urls) == 6:
            window.geometry(f'450x{int(window.winfo_height()) - int(70)}')
            start_button.place(x=185, y=int(start_button.winfo_y()) - 73)
        elif len(urls) == 8:
            window.geometry(f'450x{int(window.winfo_height()) - int(80)}')
            start_button.place(x=185, y=int(start_button.winfo_y()) - 78)

        urls[-1].destroy()
        urls[-2].destroy()

        for _ in range(2):
            del urls[-1]

        if len(raw_elements) == 10:
            raw_elements[-1].destroy()
            raw_elements[-2].destroy()

            for _ in range(2):
                del raw_elements[-1]

        if len(raw_elements) == 12:
            raw_elements[-1].destroy()
            raw_elements[-2].destroy()
            raw_elements[-3].destroy()
            raw_elements[-4].destroy()

            for _ in range(4):
                del raw_elements[-1]

        if 14 <= len(raw_elements) <= 16:
            raw_elements[-1].destroy()
            raw_elements[-2].destroy()
            raw_elements[-3].destroy()
            raw_elements[-4].destroy()
            raw_elements[-5].destroy()
            raw_elements[-6].destroy()

            for _ in range(6):
                del raw_elements[-1]


def start(urls, tab1):
    start_time = time.time()

    def total_time():
        general_time = time.time() - start_time
        label_total_time = Label(tab1, font=("Arial Bold", 7), bg='#a7aeb8')
        label_total_time.configure(text="Общее время: " + str(round(general_time, 2)))
        label_total_time.place(x=int(tab1.winfo_width()) - 100, y=int(tab1.winfo_height()) - 28)
        labels.append(label_total_time)

    clear_labels()

    async def main():
        try:
            async with aiohttp.ClientSession() as session:
                for url in urls:
                    if not checkers.is_url(url.get()):
                        label_mark = Label(tab1, font=("Arial Bold", 14))
                        label_mark.configure(text="‼", fg="red", bg='#a7aeb8')
                        label_mark.place(x=url.winfo_x() + 126, y=url.winfo_y())
                        labels.append(label_mark)
                        continue
                    async with session.get(url.get()) as response:
                        label = Label(tab1, font=("Arial Bold", 12))
                        if response.status == 200:
                            label.configure(text="✅", fg="green", bg='#a7aeb8')
                        else:
                            label.configure(text="❌", fg="red", bg='#a7aeb8')
                            Hovertip(label, f'{response.status}', hover_delay=0)
                        label.place(x=url.winfo_x() + 125, y=url.winfo_y() + 1.5)
                    labels.append(label)
        except aiohttp.client.ClientConnectionError:
            total_time()
            messagebox.showwarning('', f'Please check the correctness of the entered data for:\n {url.get()}')

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())

    total_time()


def browse_files_get(urls):
    clear_labels()

    try:
        filename = filedialog.askopenfilename(initialdir="/",
                                              title="Select a File",
                                              filetypes=(("Text files",
                                                          "*.txt*"),
                                                         ("all files",
                                                          "*.*")))

        text_file = open(filename, "r")
        rows = text_file.readlines()

        correct_data = [row.rstrip('\n') for row in rows]

        i = 0
        for url in urls:
            url.delete(0, END)
            url.insert(0, correct_data[i])
            i = i + 1

        text_file.close()

    except FileNotFoundError:
        pass


def save_config(urls):
    empty_str = ''
    for i in urls:
        empty_str = empty_str + i.get()

    if len(empty_str) != 0 and checkers.is_url(urls[0].get()) is True:
        with open('configs.txt', 'w') as file:
            for url in urls:
                file.write(url.get() + "\n")
        messagebox.showinfo('', 'Файл сохранен')
    else:
        messagebox.showwarning('', 'Нечего сохранить')
