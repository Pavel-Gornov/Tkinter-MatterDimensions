import json
import math
import threading
import time
from decimal import Decimal

import tkinter.filedialog as fd
import tkinter.messagebox as mb
from tkinter import *
from tkinter import Menu
from tkinter import ttk
from tkinter.ttk import Style


# noinspection PyAttributeOutsideInit


class Game:
    def __init__(self, font="Calibri", refresh_speed=33, saving=False, save_file_name="save.json"):
        self.font = font
        self.refresh_speed = refresh_speed
        self.window = Tk()
        self.new_game()
        self.speed = int(1000 / self.refresh_speed)
        self.load_save_from_file(save_file_name)
        self.alive = True
        self.start()
        self.init_ui()
        # Запуск цикла
        self.tab_control.focus_set()
        self.window.after(0, self.main_loop)
        self.window.mainloop()
        # Окно закрылось
        if saving:
            self.save(save_file_name)
        self.alive = False

    def start(self):
        self.calc_thread = threading.Thread(target=self.calculations)
        self.calc_thread.start()

    def init_ui(self):
        # Стили
        self.style = Style(self.window)
        self.style.theme_use("default")
        self.style.configure("g1.Vertical.TProgressbar", troughcolor='gray', background='green3', thickness=50)
        self.style.configure("g0.Vertical.TProgressbar", troughcolor='gray', background='green4', thickness=20)
        # Инициализация Интерфейса
        self.window.title("Измерения Материи")
        self.window.geometry("500x500")
        # Верхнее Меню
        self.menu = Menu(self.window)
        self.file_menu = Menu(self.menu, tearoff=0)
        self.file_menu.add_command(label='Сохранить', command=self.save)
        self.file_menu.add_command(label='Загрузить', command=self.get_save_file_name_and_load_from_it)
        self.menu.add_cascade(label='Файл', menu=self.file_menu)
        self.window.config(menu=self.menu)
        # Показатель материи
        self.m_txt = Label(self.window, font=self.font, background="light blue", height=2)
        self.m_txt.pack(anchor="n", fill=X)
        # Вкладки
        self.tab_control = ttk.Notebook(self.window)
        self.MD_tab = ttk.Frame(self.tab_control)
        self.stat_tab = ttk.Frame(self.tab_control)
        self.auto_tab = ttk.Frame(self.tab_control)
        self.singularity_tab = ttk.Frame(self.tab_control)
        self.tab_control.pack(expand=1, fill='both')
        self.tab_control.add(self.MD_tab, text='Измерения Материи')
        self.tab_control.add(self.singularity_tab, text='Сингулярность', state="hidden")
        self.tab_control.add(self.auto_tab, text='Автоматика', state="hidden")
        self.tab_control.add(self.stat_tab, text='Статистика')
        # Сингулярность
        self.singularity_txt = Label(self.singularity_tab, background="green3", height=2, font=self.font)
        self.s_grid = ttk.Frame(master=self.singularity_tab)
        self.singularity_xp_pb = ttk.Progressbar(self.s_grid, mode="determinate", orient="vertical",
                                                 style="g1.Vertical.TProgressbar", value=30)
        self.s_info = Label(self.s_grid, background="lime green", height=7, font=self.font, width=40)
        self.s_button1 = Button(self.s_grid, height=3, width=20, command=self.s_button1_click)
        self.s_button2 = Button(self.s_grid, height=3, width=20, command=self.s_button2_click)
        self.s_level_btn = Button(self.s_grid, height=3, width=45, command=self.s_levelup)
        self.s_button1_p = ttk.Progressbar(self.s_grid, mode="determinate", orient="horizontal",
                                           style="g0.Vertical.TProgressbar")
        self.s_button2_p = ttk.Progressbar(self.s_grid, mode="determinate", orient="horizontal",
                                           style="g0.Vertical.TProgressbar")
        self.singularity_txt.pack(anchor="n", fill=X)
        self.s_grid.pack(anchor="n", pady=(20, 0))
        self.singularity_xp_pb.grid(row=0, column=0, rowspan=5, padx=20)
        self.s_info.grid(row=0, column=1, rowspan=2, columnspan=3)
        self.s_button1.grid(row=3, column=1, sticky="w", padx=5)
        self.s_button2.grid(row=3, column=3, padx=(20, 0))
        self.s_button1_p.grid(row=4, column=1, sticky="wn", padx=5)
        self.s_button2_p.grid(row=4, column=3, sticky="en")
        self.s_level_btn.grid(row=2, column=1, columnspan=3)
        # Вкладка Автоматики
        self.tick_txt = Label(self.MD_tab, text="Скорость производства:", background="sky blue", height=1,
                              font=self.font)
        self.tick_txt.pack(anchor="n", fill=X)
        self.auto_grid = ttk.Frame(self.auto_tab, relief="solid", borderwidth=1)
        self.auto_grid.pack(anchor="n")
        self.auto = [
            Checkbutton(self.auto_grid, text="Авто-покупка 1-го Измерения Материи (1e55м)",
                        variable=self.auto_state[0], font=self.font, state="disabled", width=40, anchor="w"),
            Checkbutton(self.auto_grid, text="Авто-покупка 2-го Измерения Материи (1e60м)", variable=self.auto_state[1],
                        font=self.font, state="disabled", width=40, anchor="w"),
            Checkbutton(self.auto_grid, text="Авто-покупка 3-го Измерения Материи (1e70м)", variable=self.auto_state[2],
                        font=self.font, state="disabled", width=40, anchor="w"),
            Checkbutton(self.auto_grid, text="Авто-покупка 4-го Измерения Материи (1e75м)", variable=self.auto_state[3],
                        font=self.font, state="disabled", width=40, anchor="w"),
            Checkbutton(self.auto_grid, text="Авто-покупка Ускорителя Материи (1e80м)", variable=self.auto_state[4],
                        font=self.font, state="disabled", width=40, anchor="w"),
            Checkbutton(self.auto_grid, text="Авто-покупка Сжатия Измерений (1e90м)", variable=self.auto_state[5],
                        font=self.font, state="disabled", width=40, anchor="w")]
        for i in range(len(self.auto)):
            self.auto[i].grid(row=i, column=0)
        self.u1_btn = Button(self.auto_tab, height=2, width=49, bg="green3", fg="gray99", state="disabled",
                             command=self.u1,
                             text="Сломанная галактика (+25% к силе производства)\nЦена: 22+ сжатия измерения")
        self.u1_btn.pack(anchor="n", pady=(10, 0))
        if self.upgrades["galaxy"] == 1.25:
            self.u1_btn["text"] = "Сломанная галактика (+25% к силе множителя тиков)"
        self.u2_btn = Button(self.auto_tab, height=2, width=49, bg="green3", fg="gray99", state="disabled",
                             command=self.u2, text="Когерентная Сингулярность (x1 Энергии Сингулярности)"
                                                   "\nЦена: 10 Уровней Сингулярности")
        self.u2_btn.pack(anchor="n", pady=(10, 0))
        self.u3_btn = Button(self.auto_tab, height=2, width=49, bg="green3", fg="gray99", state="disabled",
                             command=self.u3,
                             text="Пространственный Множитель (Количество ИМ ^ 0.1)"
                                  "\nЦена: 25 Уровней Сингулярности")
        self.u3_btn.pack(anchor="n", pady=(10, 0))
        if self.upgrades["MD_mult"] == 0.1:
            self.u3_btn["text"] = "Пространственный Множитель (Количество ИМ ^ 0.1)"
        # Статистика
        self.Matter_all_stat = Label(self.stat_tab, width=10, height=2, background="light blue1", font=self.font)
        self.MD1_count = Label(self.stat_tab, font=self.font)
        self.MD2_count = Label(self.stat_tab, font=self.font)
        self.MD3_count = Label(self.stat_tab, font=self.font)
        self.MD4_count = Label(self.stat_tab, font=self.font)
        self.Matter_all_stat.pack(anchor="n", fill='both', padx=10, pady=5)
        self.MD1_count.pack(anchor="n", fill='both', padx=10, pady=5)
        self.MD2_count.pack(anchor="n", fill='both', padx=10, pady=5)
        self.MD3_count.pack(anchor="n", fill='both', padx=10, pady=5)
        self.MD4_count.pack(anchor="n", fill='both', padx=10, pady=5)
        # Измерения Материи
        self.d_grid = ttk.Frame(master=self.MD_tab, relief="solid", borderwidth=1, width=10, height=350)
        self.btn_grid = ttk.Frame(master=self.MD_tab, width=10, height=350)

        self.md1_txt = Label(self.d_grid, font=self.font, background="light blue3", anchor="w", padx=20, height=2,
                             width=34, justify="left")
        self.md1_btn = Button(self.d_grid, command=self.md1_btn_click, height=2)
        self.md2_txt = Label(self.d_grid, font=self.font, background="light blue", anchor="w", padx=20, height=2,
                             width=34, justify="left")
        self.md2_btn = Button(self.d_grid, command=self.md2_btn_click, height=2)

        self.md3_txt = Label(self.d_grid, font=self.font, justify="left", background="light blue3", anchor="w", padx=20,
                             height=2, width=34)
        self.md3_btn = Button(self.d_grid, command=self.md3_btn_click, height=2)

        self.md4_txt = Label(self.d_grid, font=self.font, justify="left", background="light blue", anchor="w", padx=20,
                             height=2, width=34)
        self.md4_btn = Button(self.d_grid, command=self.md4_btn_click, height=2)
        self.max_btn = Button(self.btn_grid, command=self.max, text="Купить всё", height=2, width=20)
        self.max2_btn = Button(self.btn_grid, command=self.max2, text="Купить всё 2.0", height=2, width=20)
        self.crunch_btn = Button(self.btn_grid, command=self.crunch, text="Сжатие Измерений", height=2, width=20)
        self.tick_btn = Button(self.btn_grid, command=self.tick_upgrade, text="Ускорение Материи", height=2, width=20)
        self.singularity_pb = ttk.Progressbar(self.MD_tab, mode="determinate", style="g0.Vertical.TProgressbar")
        self.to_singularity_txt = Label(self.MD_tab, font=self.font, background="green3")
        # Упаковка
        self.d_grid.pack(anchor="n", padx=10, pady=5)
        self.md1_txt.grid(row=0, column=0, padx=5, pady=5, columnspan=2, sticky="ew")
        self.md1_btn.grid(row=0, column=2, padx=5, pady=5)
        self.md2_txt.grid(row=1, column=0, padx=5, pady=5, columnspan=2)
        self.md2_btn.grid(row=1, column=2, padx=5, pady=5)
        self.md3_txt.grid(row=2, column=0, padx=5, pady=5, columnspan=2)
        self.md3_btn.grid(row=2, column=2, padx=5, pady=5)
        self.md4_txt.grid(row=3, column=0, padx=5, pady=5, columnspan=2)
        self.md4_btn.grid(row=3, column=2, padx=5, pady=5)
        # Кнопки
        self.btn_grid.pack(anchor="n", padx=10)
        self.max_btn.grid(row=0, column=0, padx=5, pady=5)
        self.max2_btn.grid(row=1, column=0, padx=5, pady=5)
        self.crunch_btn.grid(row=0, column=3, padx=(160, 5))
        self.tick_btn.grid(row=1, column=3, padx=(160, 5))
        self.to_singularity_txt.pack(anchor="nw", fill='x', padx=10, pady=10)
        self.singularity_pb.pack(anchor="nw", fill='x', padx=10)
        # Привязка клавиш
        self.window.bind(sequence="m", func=self.max)
        self.window.bind(sequence="c", func=self.crunch)
        self.window.bind(sequence="t", func=self.tick_upgrade)
        self.window.bind(sequence="<space>", func=self.max2)
        self.window.bind(sequence="1", func=self.md1_btn_click)
        self.window.bind(sequence="2", func=self.md2_btn_click)
        self.window.bind(sequence="3", func=self.md3_btn_click)
        self.window.bind(sequence="4", func=self.md4_btn_click)

    def md1_btn_click(self):
        if self.Matter >= self.MD1_price:
            self.MD1 += 1
            self.MD1_bought += 1
            self.Matter -= self.MD1_price
            self.MD1_price *= Decimal(1.1)

    def md2_btn_click(self):
        if self.Matter >= self.MD2_price:
            self.MD2 += 1
            self.MD2_bought += 1
            self.Matter -= self.MD2_price
            self.MD2_price *= Decimal(1.1)

    def md3_btn_click(self):
        if self.Matter >= self.MD3_price:
            self.MD3 += 1
            self.MD3_bought += 1
            self.Matter -= self.MD3_price
            self.MD3_price *= Decimal(1.1)

    def md4_btn_click(self):
        if self.Matter >= self.MD4_price:
            self.MD4 += 1
            self.MD4_bought += 1
            self.Matter -= self.MD4_price
            self.MD4_price *= Decimal(1.1)

    def max(self):
        while self.Matter >= self.MD1_price:
            self.md1_btn_click()
        while self.Matter >= self.MD2_price:
            self.md2_btn_click()
        while self.Matter >= self.MD3_price:
            self.md3_btn_click()
        while self.Matter >= self.MD4_price:
            self.md4_btn_click()

    def max2(self):
        while self.Matter >= self.MD4_price:
            self.md4_btn_click()
        while self.Matter >= self.MD3_price:
            self.md3_btn_click()
        while self.Matter >= self.MD2_price:
            self.md2_btn_click()
        while self.Matter >= self.MD1_price:
            self.md1_btn_click()

    def crunch(self):
        if self.MD4 >= int(round(self.MCrunch_cost)):
            self.MCrunch += 1
            self.MCrunch_cost *= Decimal(1.25)
            self.Matter = Decimal(10)
            self.MD1 = Decimal(0)
            self.MD2 = Decimal(0)
            self.MD3 = Decimal(0)
            self.MD4 = Decimal(0)
            self.MD1_bought = 0
            self.MD2_bought = 0
            self.MD3_bought = 0
            self.MD4_bought = 0
            self.MD1_mult = Decimal(1)
            self.MD2_mult = Decimal(1)
            self.MD3_mult = Decimal(1)
            self.MD4_mult = Decimal(1)
            self.MD1_price = Decimal(10)
            self.MD2_price = Decimal(100)
            self.MD3_price = Decimal(10_000)
            self.MD4_price = Decimal(1_000_000)
            self.tick_speed_price = Decimal(1000)
            self.tick_speed = 0

    def tick_upgrade(self):
        if self.Matter > self.tick_speed_price:
            self.tick_speed += 1
            self.tick_speed_price *= 10

    def u1(self):
        self.upgrades["galaxy"] = 1.25
        self.MCrunch = 0
        self.MCrunch_cost = Decimal(10)
        self.Matter = Decimal(10)
        self.MD1 = Decimal(0)
        self.MD2 = Decimal(0)
        self.MD3 = Decimal(0)
        self.MD4 = Decimal(0)
        self.MD1_bought = 0
        self.MD2_bought = 0
        self.MD3_bought = 0
        self.MD4_bought = 0
        self.MD1_mult = Decimal(1)
        self.MD2_mult = Decimal(1)
        self.MD3_mult = Decimal(1)
        self.MD4_mult = Decimal(1)
        self.MD1_price = Decimal(10)
        self.MD2_price = Decimal(100)
        self.MD3_price = Decimal(10_000)
        self.MD4_price = Decimal(1_000_000)
        self.tick_speed_price = Decimal(1000)
        self.tick_speed = 0
        self.u1_btn["text"] = "Сломанная галактика (+25% к силе множителя тиков)"

    def u2(self):
        self.upgrades["singularity"] = 1.1
        self.s_xp = 0.0
        self.s_xp_cost = 10
        self.s_b1_cost = 100
        self.s_b2_cost = 100
        self.s_level_b1 = 0
        self.s_level_b2 = 0
        self.s_level = 0

    def u3(self):
        self.upgrades["MD_mult"] = 0.1
        self.s_xp = 0.0
        self.s_xp_cost = 10
        self.s_b1_cost = 100
        self.s_b2_cost = 100
        self.s_level_b1 = 0
        self.s_level_b2 = 0
        self.s_level = 0
        self.u3_btn["text"] = "Пространственный Множитель (Количество ИМ ^ 0.1)"

    def s_levelup(self):
        if self.s_xp >= self.s_xp_cost:
            self.s_xp -= self.s_xp_cost
            self.s_level += 1
            self.s_xp_cost *= 1.75

    def s_button1_click(self):
        if self.s_xp >= self.s_b1_cost:
            self.s_level_b1 += 1
            self.s_xp -= self.s_b1_cost
            self.s_b1_cost *= 2.75

    def s_button2_click(self):
        if self.s_xp >= self.s_b2_cost:
            self.s_level_b1 += 1
            self.s_xp -= self.s_b2_cost
            self.s_b2_cost *= 3.75

    def main_loop(self):
        self.ui_refresh()
        self.unlocks()
        self.auto_buyers()
        self.window.after(self.refresh_speed, self.main_loop)

    def auto_buyers(self):
        data = list(map(decode_BooleanVar, self.auto_state))
        if data[0]:
            self.md1_btn_click()
        if data[1]:
            self.md2_btn_click()
        if data[2]:
            self.md3_btn_click()
        if data[3]:
            self.md4_btn_click()
        if data[4]:
            self.tick_upgrade()
        if data[5]:
            self.crunch()

    def unlocks(self):
        if self.Matter_all >= float("1e50") and self.tab_control.tab(2)["state"] != "normal":
            self.tab_control.tab(2, state="normal")
        if self.Matter_all >= float("1e55") and self.auto[0] != "normal":
            self.auto[0]["state"] = "normal"
            self.auto[0]["text"] = "Авто-покупка 1-го Измерения Материи"
        if self.Matter_all >= float("1e60") and self.auto[1] != "normal":
            self.auto[1]["state"] = "normal"
            self.auto[1]["text"] = "Авто-покупка 2-го Измерения Материи"
        if self.Matter_all >= float("1e70") and self.auto[2] != "normal":
            self.auto[2]["state"] = "normal"
            self.auto[2]["text"] = "Авто-покупка 3-го Измерения Материи"
        if self.Matter_all >= float("1e75") and self.auto[3] != "normal":
            self.auto[3]["state"] = "normal"
            self.auto[3]["text"] = "Авто-покупка 4-го Измерения Материи"
        if self.Matter_all >= float("1e80") and self.auto[4] != "normal":
            self.auto[4]["state"] = "normal"
            self.auto[4]["text"] = "Авто-покупка Ускорителя Материи"
        if self.Matter_all >= float("1e90") and self.auto[5] != "normal":
            self.auto[5]["state"] = "normal"
            self.auto[5]["text"] = "Авто-покупка Сжатия Измерений"
        if self.Matter >= float("1e100") and self.tab_control.tab(1)["state"] != "normal":
            self.tab_control.tab(1, state="normal")

    def ui_refresh(self):
        current_tab = self.tab_control.tab(self.tab_control.select(), "text")
        self.m_txt["text"] = f"У Вас: {num_notation(round(self.Matter))} ед. Материи"
        if current_tab == "Измерения Материи":
            self.md1_btn["state"] = "disabled" if self.MD1_price > self.Matter else "active"
            self.md2_btn["state"] = "disabled" if self.MD2_price > self.Matter else "active"
            self.md3_btn["state"] = "disabled" if self.MD3_price > self.Matter else "active"
            self.md4_btn["state"] = "disabled" if self.MD4_price > self.Matter else "active"
            self.crunch_btn["state"] = "disabled" if int(round(self.MCrunch_cost)) > self.MD4 else "active"
            self.tick_btn["state"] = "disabled" if self.tick_speed_price > self.Matter else "active"
            if self.t_tick_mult < Decimal("1e24"):
                self.tick_txt["text"] = f"Скорость производства: x{num_notation(round(self.t_tick_mult, 2))}"
            else:
                self.tick_txt["text"] = f"Скорость производства: x{num_notation(self.t_tick_mult)}"
            self.md1_txt["text"] = f"1-е Измерение Материи: {num_notation(round(self.MD1))}" \
                                   f"\nМножитель: x{num_notation(self.MD1_mult)}"
            self.md2_txt["text"] = f"2-е Измерение Материи: {num_notation(round(self.MD2))}" \
                                   f"\nМножитель: x{num_notation(self.MD2_mult)}"
            self.md3_txt["text"] = f"3-е Измерение Материи: {num_notation(round(self.MD3))}" \
                                   f"\nМножитель: x{num_notation(self.MD3_mult)}"
            self.md4_txt["text"] = f"4-е Измерение Материи: {num_notation(round(self.MD4))}" \
                                   f"\nМножитель: x{num_notation(self.MD4_mult)}"
            self.md1_btn["text"] = f"Купить 1-е измерение!\nЦена: {num_notation(int(self.MD1_price))} м."
            self.md2_btn["text"] = f"Купить 2-е измерение!\nЦена: {num_notation(int(self.MD2_price))} м."
            self.md3_btn["text"] = f"Купить 3-е измерение!\nЦена: {num_notation(int(self.MD3_price))} м."
            self.md4_btn["text"] = f"Купить 4-е измерение!\nЦена: {num_notation(int(self.MD4_price))} м."
            self.crunch_btn["text"] = f"Сжатие измерений: {self.MCrunch}" \
                                      f"\nЦена: {num_notation(int(round(self.MCrunch_cost)))} 4-х ИМ"
            self.tick_btn["text"] = f"Ускорение Материи\nЦена: {num_notation(self.tick_speed_price)} м."
            temp = min(math.log(max(self.Matter, Decimal(1)), 10), 100)
            self.singularity_pb['value'] = temp
            self.to_singularity_txt["text"] = f"Прогресс до сингулярности: {round(temp, 1)}%"
        elif current_tab == 'Статистика':
            self.Matter_all_stat["text"] = f"Всего было получено: {num_notation(round(self.Matter_all))} Материи."
            self.MD1_count["text"] = f"Куплено 1-х измерений: {self.MD1_bought}"
            self.MD2_count["text"] = f"Куплено 2-х измерений: {self.MD2_bought}"
            self.MD3_count["text"] = f"Куплено 3-х измерений: {self.MD3_bought}"
            self.MD4_count["text"] = f"Куплено 4-х измерений: {self.MD4_bought}"
        elif current_tab == 'Автоматика':
            self.u1_btn["state"] = "disabled" if self.upgrades["galaxy"] == 1.25 or self.MCrunch < 22 else "active"
            self.u2_btn["state"] = "disabled" if self.upgrades["singularity"] == 1.1 or self.s_level < 10 else "active"
            self.u3_btn["state"] = "disabled" if self.upgrades["MD_mult"] == 0.1 or self.s_level < 25 else "active"
            self.u1_btn["bg"] = "gray99" if self.upgrades["galaxy"] != 1.25 and self.MCrunch < 22 else "green3"
            self.u2_btn["bg"] = "gray99" if self.upgrades["singularity"] != 1.1 and self.s_level < 10 else "green3"
            self.u3_btn["bg"] = "gray99" if self.upgrades["MD_mult"] != 0.1 and self.s_level < 25 else "green3"

            self.u2_btn["text"] = f"Когерентная Сингулярность (x" \
                                  f"{max(round(self.s_level ** self.upgrades['singularity']), 1)} " \
                                  f"Энергии Сингулярности)"
            if self.upgrades['singularity'] == 0:
                self.u2_btn["text"] += "\nЦена: 10 Уровней Сингулярности"
        elif current_tab == 'Сингулярность':
            self.s_level_btn["state"] = "disabled" if self.s_xp_cost > self.s_xp else "active"
            self.s_button1["state"] = "disabled" if self.s_b1_cost > self.s_xp else "active"
            self.s_button2["state"] = "disabled" if self.s_b2_cost > self.s_xp else "active"
            temp = min(round((self.s_xp / self.s_xp_cost) * 100, 1), 100)
            self.singularity_txt["text"] = f"Создано {num_notation(round(self.s_energy, 1))} ед. энергии " \
                                           f"Сингулярности.\nВсего Опыта Сингулярности: " \
                                           f"{num_notation(int(self.s_xp))} " \
                                           f"({num_notation(round(self.delta_s_xp, 2))} О.С./сек.)"
            self.s_info["text"] = f"Показатели Сингулярности:\nУровень сингулярности: {self.s_level}\n" \
                                  f"Опыт Синг.: {num_notation(int(min(self.s_xp, self.s_xp_cost)))}" \
                                  f" из {num_notation(int(self.s_xp_cost))} ({temp}%)\n" \
                                  f"Бонус к Измерениям Материи:\n x{num_notation(self.t_sing_mult)}" \
                                  f" производительности измерений\nx{(self.s_level + 1)} множителя сжатия."
            self.s_level_btn["text"] = f"Повысить уровень Сингулярности до {self.s_level + 1}!"
            self.s_button1["text"] = f"Сингулярное ускорение\n" \
                                     f"Цена: {num_notation(round(self.s_b1_cost))} ос.\n" \
                                     f"(+30%) к скорости"
            self.s_button2["text"] = f"Усилитель времени\n" \
                                     f"Цена: {num_notation(round(self.s_b2_cost))} ос.\n" \
                                     f"(+50%) к скорости"
            self.singularity_xp_pb['value'] = temp
            self.s_button1_p['value'] = min(round((self.s_xp / self.s_b1_cost) * 100, 1), 100)
            self.s_button2_p['value'] = min(round((self.s_xp / self.s_b2_cost) * 100, 1), 100)

    def calculations(self):
        while self.alive:
            time.sleep(self.refresh_speed / 1000)
            # Временные множители
            self.t_sing_mult = 3 ** self.s_level
            self.t_crunch_mult = Decimal((2 * (self.s_level + 1)) ** self.MCrunch)
            self.t_tick_mult = Decimal((self.upgrades["galaxy"] * 1.125)) ** self.tick_speed
            self.delta_s_xp = (1.3 ** self.s_level_b1) * (1.5 ** self.s_level_b2) * self.s_energy
            # Основные вычисления
            temp = self.MD1 * self.MD1_mult * self.t_crunch_mult / self.speed * self.t_tick_mult * self.t_sing_mult
            self.Matter += temp
            self.Matter_all += temp
            self.MD1 += (self.MD2 * self.MD2_mult) / self.speed * self.t_tick_mult * self.t_sing_mult
            self.MD2 += (self.MD3 * self.MD3_mult) / self.speed * self.t_tick_mult * self.t_sing_mult
            self.MD3 += (self.MD4 * self.MD4_mult) / self.speed * self.t_tick_mult * self.t_sing_mult
            temp = Decimal(self.upgrades["MD_mult"])
            self.MD1_mult = ((self.MD1_bought // 10) + 1) * self.t_crunch_mult * (max(self.MD1, Decimal(1)) ** temp)
            self.MD2_mult = ((self.MD2_bought // 10) + 1) * self.t_crunch_mult * (max(self.MD2, Decimal(1)) ** temp)
            self.MD3_mult = ((self.MD3_bought // 10) + 1) * self.t_crunch_mult * (max(self.MD3, Decimal(1)) ** temp)
            self.MD4_mult = ((self.MD4_bought // 10) + 1) * self.t_crunch_mult * (max(self.MD4, Decimal(1)) ** temp)
            self.s_energy = float(self.Matter.logb() / 100) * (max(self.s_level ** self.upgrades["singularity"], 1))
            # if self.alive:
            #     if self.s_xp <= self.s_xp_cost and self.s_energy > 1 and self.tab_control.tab(1)["state"] == "normal":
            self.s_xp += self.delta_s_xp / self.speed

    def save(self, save_file_name):
        save = {"Matter": str(self.Matter), "Matter_all": str(self.Matter_all), "MD1": str(self.MD1),
                "MD2": str(self.MD2), "MD3": str(self.MD3),
                "MD4": str(self.MD4), "MD1_bought": self.MD1_bought, "MD2_bought": self.MD2_bought,
                "MD3_bought": self.MD3_bought, "MD4_bought": self.MD4_bought, "MD1_mult": str(self.MD1_mult),
                "MD2_mult": str(self.MD2_mult), "MD3_mult": str(self.MD3_mult), "MD4_mult": str(self.MD4_mult),
                "MD1_price": str(self.MD1_price), "MD2_price": str(self.MD2_price), "MD3_price": str(self.MD3_price),
                "MD4_price": str(self.MD4_price), "MCrunch": self.MCrunch, "MCrunch_cost": str(self.MCrunch_cost),
                "auto_state": list(map(decode_BooleanVar, self.auto_state)),
                "tick_speed_price": str(self.tick_speed_price), "tick_speed": self.tick_speed,
                "s_energy": self.s_energy, "s_xp": self.s_xp, "s_xp_cost": self.s_xp_cost, "s_b1_cost": self.s_b1_cost,
                "s_b2_cost": self.s_b2_cost, "s_level_b1": self.s_level_b1, "s_level_b2": self.s_level_b2,
                "s_level": self.s_level, "upgrades": self.upgrades}
        with open(save_file_name, mode="w") as f:
            f.write(json.dumps(save, indent=2))

    def get_save_file_name_and_load_from_it(self):
        filetypes = (("Файл json", "*.json"),
                     ("Любой", "*"))
        filename = fd.askopenfilename(title="Открыть файл", initialdir="/",
                                      filetypes=filetypes)
        if filename:
            try:
                self.load_save_from_file(filename)
                mb.showinfo("Успешно", "Сохранение загружено успешно!")
            except Exception as e:
                mb.showerror("Ошибка", "Произошла ошибка при загрузке файла!")
                print(e)

    def load_save_from_file(self, filename):
        with open(filename, mode="r") as f:
            self.load_values(json.load(f))

    def load_values(self, data):
        self.Matter = Decimal(data["Matter"])
        self.Matter_all = Decimal(data["Matter_all"])
        self.MD1 = Decimal(data["MD1"])
        self.MD2 = Decimal(data["MD2"])
        self.MD3 = Decimal(data["MD3"])
        self.MD4 = Decimal(data["MD4"])
        self.MD1_bought = data["MD1_bought"]
        self.MD2_bought = data["MD2_bought"]
        self.MD3_bought = data["MD3_bought"]
        self.MD4_bought = data["MD4_bought"]
        self.MD1_mult = Decimal(data["MD1_mult"])
        self.MD2_mult = Decimal(data["MD2_mult"])
        self.MD3_mult = Decimal(data["MD3_mult"])
        self.MD4_mult = Decimal(data["MD4_mult"])
        self.MD1_price = Decimal(data["MD1_price"])
        self.MD2_price = Decimal(data["MD2_price"])
        self.MD3_price = Decimal(data["MD3_price"])
        self.MD4_price = Decimal(data["MD4_price"])
        self.MCrunch = data["MCrunch"]
        self.MCrunch_cost = Decimal(data["MCrunch_cost"])
        self.auto_state = list(map(load_BoolVar, data["auto_state"]))
        self.tick_speed_price = Decimal(data["tick_speed_price"])
        self.tick_speed = data["tick_speed"]
        self.s_energy = data["s_energy"]
        self.s_xp = data["s_xp"]
        self.s_xp_cost = data["s_xp_cost"]
        self.s_b1_cost = data["s_b1_cost"]
        self.s_b2_cost = data["s_b2_cost"]
        self.s_level_b1 = data["s_level_b1"]
        self.s_level_b2 = data["s_level_b2"]
        self.s_level = data["s_level"]
        self.upgrades = data["upgrades"]

    def new_game(self):
        self.Matter = Decimal(10)
        self.Matter_all = Decimal(10)
        self.MD1 = Decimal(0)
        self.MD2 = Decimal(0)
        self.MD3 = Decimal(0)
        self.MD4 = Decimal(0)
        self.MD1_bought = 0
        self.MD2_bought = 0
        self.MD3_bought = 0
        self.MD4_bought = 0
        self.MD1_mult = Decimal(1)
        self.MD2_mult = Decimal(1)
        self.MD3_mult = Decimal(1)
        self.MD4_mult = Decimal(1)
        self.MD1_price = Decimal(10)
        self.MD2_price = Decimal(100)
        self.MD3_price = Decimal(10_000)
        self.MD4_price = Decimal(1_000_000)
        self.MCrunch = 0
        self.MCrunch_cost = Decimal(10)
        self.auto_state = [BooleanVar(), BooleanVar(), BooleanVar(), BooleanVar(), BooleanVar(), BooleanVar()]
        self.tick_speed_price = Decimal(1000.0)
        self.tick_speed = 0
        self.s_energy = 0
        self.s_xp = 0.0
        self.s_xp_cost = 10
        self.s_b1_cost = 100
        self.s_b2_cost = 100
        self.s_level_b1 = 0
        self.s_level_b2 = 0
        self.s_level = 0
        self.upgrades = {"galaxy": 1, "singularity": 0, "MD_mult": 0}
        # Временные множители
        self.t_tick_mult = (self.upgrades["galaxy"] * 1.125) ** self.tick_speed


def decode_BooleanVar(var: BooleanVar) -> bool:
    return var.get()


def load_BoolVar(var: bool) -> BooleanVar:
    return BooleanVar(value=var)


def format_e(n):
    return f"{n:.2E}".lower().replace("+", "")


def num_notation(num):
    if num >= float("1e33"):
        return format_e(Decimal(num))
    else:
        if num < 1000:
            return num
        else:
            d = [" тыс.", " млн.", " млрд.", " трил.", " квад.", " квинт.", " секст.", " септ.", " окт.", " нон."]
            e_num = format_e(num).split("e")
            e_num_1 = int(e_num[1]) % 3
            e_num_str = str(round(float(e_num[0]) * 10 ** e_num_1, 2))
            if int(e_num[1]) // 3 < len(d) + 1:
                return e_num_str + d[((int(e_num[1])) // 3) - 1]


if __name__ == "__main__":
    g = Game(saving=True)
