import json
import math
import tkinter.filedialog as fd
import tkinter.messagebox as mb
from tkinter import *
from tkinter import Menu
from tkinter import ttk


# noinspection PyAttributeOutsideInit


class Game:
    def __init__(self, font="Calibri", refresh_speed=33, saving=False):
        self.font = font
        self.refresh_speed = refresh_speed
        self.new_game()
        self.speed = 1000 / self.refresh_speed
        if saving:
            try:
                with open("save.json", mode="r") as f:
                    data = json.load(f)
                    self.load(data)
            except Exception as e:
                print(e)
        self.initUI()

    def initUI(self):
        # Вкладки
        self.window = Tk()
        self.window.title("Измерения Материи")
        self.window.geometry("500x500")

        self.menu = Menu(self.window)
        self.file_menu = Menu(self.menu, tearoff=0)
        self.file_menu.add_command(label='Сохранить', command=self.save)
        self.file_menu.add_command(label='Загрузить', command=self.load_save_from_file)
        self.menu.add_cascade(label='Файл', menu=self.file_menu)
        self.window.config(menu=self.menu)

        self.tab_control = ttk.Notebook(self.window)
        self.m_txt = Label(self.window, text=f"У Вас: {self.Matter} ед. Материи", font=self.font,
                           background="light blue", height=2)
        self.m_txt.pack(anchor="n", fill=X)
        self.MD_tab = ttk.Frame(self.tab_control)
        self.stat_tab = ttk.Frame(self.tab_control)
        self.tab_control.pack(expand=1, fill='both')
        self.tab_control.add(self.MD_tab, text='Измерения Материи')
        self.tab_control.add(self.stat_tab, text='Статистика')
        self.d_grid = ttk.Frame(master=self.MD_tab, relief="solid", borderwidth=1, width=10, height=350)
        self.btn_grid = ttk.Frame(master=self.MD_tab, width=10, height=350)
        # Статистика
        self.MD1_count = Label(self.stat_tab, text=f"Куплено 1-х измерений: {self.MD1_bought}")
        self.MD2_count = Label(self.stat_tab, text=f"Куплено 2-х измерений: {self.MD2_bought}")
        self.MD3_count = Label(self.stat_tab, text=f"Куплено 3-х измерений: {self.MD3_bought}")
        self.MD4_count = Label(self.stat_tab, text=f"Куплено 4-х измерений: {self.MD4_bought}")
        self.MD1_count.pack(anchor="n", fill='both', padx=10, pady=5)
        self.MD2_count.pack(anchor="n", fill='both', padx=10, pady=5)
        self.MD3_count.pack(anchor="n", fill='both', padx=10, pady=5)
        self.MD4_count.pack(anchor="n", fill='both', padx=10, pady=5)

        # Измерения Материи

        self.md1_txt = Label(self.d_grid, text=f"1-е Измерение Материи: {self.MD1}\nМножитель: x{self.MD1_mult}",
                             font=self.font, background="light blue3", anchor="w", padx=20, height=2, width=34,
                             justify="left")
        self.md1_btn = Button(self.d_grid, command=self.md1_btn_click,
                              text=f"Купить 1-е измерение!\nЦена: {int(self.MD1_price)} м.", height=2)

        self.md2_txt = Label(self.d_grid, text=f"2-е Измерение Материи: {self.MD1}\nМножитель: x{self.MD2_mult}",
                             font=self.font, background="light blue", anchor="w", padx=20, height=2, width=34,
                             justify="left")
        self.md2_btn = Button(self.d_grid, command=self.md2_btn_click,
                              text=f"Купить 2-е измерение!\nЦена: {int(self.MD1_price)} м.", height=2)

        self.md3_txt = Label(self.d_grid, text=f"3-е Измерение Материи: {self.MD1}\nМножитель: x{self.MD3_mult}",
                             font=self.font, justify="left",
                             background="light blue3", anchor="w", padx=20, height=2, width=34)
        self.md3_btn = Button(self.d_grid, command=self.md3_btn_click,
                              text=f"Купить 3-е измерение!\nЦена: {int(self.MD1_price)} м.", height=2)

        self.md4_txt = Label(self.d_grid, text=f"4-е Измерение Материи: {self.MD1}\nМножитель: x{self.MD4_mult}",
                             font=self.font, justify="left",
                             background="light blue", anchor="w", padx=20, height=2, width=34)
        self.md4_btn = Button(self.d_grid, command=self.md4_btn_click,
                              text=f"Купить 4-е измерение!\nЦена: {int(self.MD1_price)} м.", height=2)
        self.max_btn = Button(self.btn_grid, command=self.max,
                              text="Купить всё", height=2, width=20)
        self.max2_btn = Button(self.btn_grid, command=self.max2,
                               text="Купить всё 2.0", height=2, width=20)
        self.crunch_btn = Button(self.btn_grid, command=self.crunch,
                                 text="Сжатие измерений", height=2, width=20)
        self.singularity_pb = ttk.Progressbar(self.MD_tab, mode="determinate")
        self.to_singularity_txt = Label(self.MD_tab, text="Прогресс до сингулярности:", font=self.font,
                                        background="green3")

        # Упаковка
        self.d_grid.pack(anchor="n", padx=10, pady=10)
        self.md1_txt.grid(row=0, column=0, padx=5, pady=5, columnspan=2, sticky="ew")
        self.md1_btn.grid(row=0, column=2, padx=5, pady=5)
        self.md2_txt.grid(row=1, column=0, padx=5, pady=5, columnspan=2)
        self.md2_btn.grid(row=1, column=2, padx=5, pady=5)
        self.md3_txt.grid(row=2, column=0, padx=5, pady=5, columnspan=2)
        self.md3_btn.grid(row=2, column=2, padx=5, pady=5)
        self.md4_txt.grid(row=3, column=0, padx=5, pady=5, columnspan=2)
        self.md4_btn.grid(row=3, column=2, padx=5, pady=5)

        self.btn_grid.pack(anchor="n", padx=10, pady=10)
        self.max_btn.grid(row=0, column=0, padx=5, pady=5)
        self.max2_btn.grid(row=1, column=0, padx=5, pady=5)
        self.crunch_btn.grid(row=0, column=3, padx=[160, 5])
        self.to_singularity_txt.pack(anchor="nw", fill='x', padx=10, pady=10)
        self.singularity_pb.pack(anchor="nw", fill='x', padx=10)

        self.window.after(0, self.main_loop)
        self.window.mainloop()

    def md1_btn_click(self):
        if self.Matter >= self.MD1_price:
            self.MD1 += 1
            self.MD1_bought += 1
            self.Matter -= self.MD1_price
            self.MD1_price *= 1.1

    def md2_btn_click(self):
        if self.Matter >= self.MD2_price:
            self.MD2 += 1
            self.MD2_bought += 1
            self.Matter -= self.MD2_price
            self.MD2_price *= 1.1

    def md3_btn_click(self):
        if self.Matter >= self.MD3_price:
            self.MD3 += 1
            self.MD3_bought += 1
            self.Matter -= self.MD3_price
            self.MD3_price *= 1.1

    def md4_btn_click(self):
        if self.Matter >= self.MD4_price:
            self.MD4 += 1
            self.MD4_bought += 1
            self.Matter -= self.MD4_price
            self.MD4_price *= 1.1

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
            self.MCrunch_cost *= 1.25
            self.Matter = 10
            self.MD1 = 0
            self.MD2 = 0
            self.MD3 = 0
            self.MD4 = 0
            self.MD1_bought = 0
            self.MD2_bought = 0
            self.MD3_bought = 0
            self.MD4_bought = 0
            self.MD1_mult = 1
            self.MD2_mult = 1
            self.MD3_mult = 1
            self.MD4_mult = 1
            self.MD1_price = 10
            self.MD2_price = 100
            self.MD3_price = 10_000
            self.MD4_price = 1_000_000

    def main_loop(self):
        self.calculations()
        self.UI_refresh()
        self.window.after(self.refresh_speed, self.main_loop)

    def UI_refresh(self):
        current_tab = self.tab_control.tab(self.tab_control.select(), "text")
        self.m_txt["text"] = f"У Вас: {num_notation(round(self.Matter, 1))} ед. Материи"
        if current_tab == "Измерения Материи":
            self.md1_btn["state"] = "disabled" if self.MD1_price > self.Matter else "active"
            self.md2_btn["state"] = "disabled" if self.MD2_price > self.Matter else "active"
            self.md3_btn["state"] = "disabled" if self.MD3_price > self.Matter else "active"
            self.md4_btn["state"] = "disabled" if self.MD4_price > self.Matter else "active"
            self.crunch_btn["state"] = "disabled" if int(round(self.MCrunch_cost)) > self.MD4 else "active"
            self.md1_txt["text"] = f"1-е Измерение Материи: {num_notation(int(self.MD1))}" \
                                   f"\nМножитель: x{num_notation(self.MD1_mult)}"
            self.md2_txt["text"] = f"2-е Измерение Материи: {num_notation(int(self.MD2))}" \
                                   f"\nМножитель: x{num_notation(self.MD2_mult)}"
            self.md3_txt["text"] = f"3-е Измерение Материи: {num_notation(int(self.MD3))}" \
                                   f"\nМножитель: x{num_notation(self.MD3_mult)}"
            self.md4_txt["text"] = f"4-е Измерение Материи: {num_notation(int(self.MD4))}" \
                                   f"\nМножитель: x{num_notation(self.MD4_mult)}"
            self.md1_btn["text"] = f"Купить 1-е измерение!\nЦена: {num_notation(int(self.MD1_price))} м."
            self.md2_btn["text"] = f"Купить 2-е измерение!\nЦена: {num_notation(int(self.MD2_price))} м."
            self.md3_btn["text"] = f"Купить 3-е измерение!\nЦена: {num_notation(int(self.MD3_price))} м."
            self.md4_btn["text"] = f"Купить 4-е измерение!\nЦена: {num_notation(int(self.MD4_price))} м."
            self.crunch_btn["text"] = f"Сжатие измерений: {self.MCrunch}" \
                                      f"\nЦена: {num_notation(int(round(self.MCrunch_cost)))} 4-х ИМ"
            temp = min(math.log(max(self.Matter, 1), 10), 100)
            self.singularity_pb['value'] = temp
            self.to_singularity_txt["text"] = f"Прогресс до сингулярности: {round(temp, 1)}%"
        elif current_tab == 'Статистика':
            self.MD1_count["text"] = f"Куплено 1-х измерений: {self.MD1_bought}"
            self.MD2_count["text"] = f"Куплено 2-х измерений: {self.MD2_bought}"
            self.MD3_count["text"] = f"Куплено 3-х измерений: {self.MD3_bought}"
            self.MD4_count["text"] = f"Куплено 4-х измерений: {self.MD4_bought}"

    def calculations(self):
        self.Matter += (self.MD1 * self.MD1_mult * (2 ** self.MCrunch)) / self.speed
        self.MD1 += (self.MD2 * self.MD2_mult * (2 ** self.MCrunch)) / self.speed
        self.MD2 += (self.MD3 * self.MD3_mult * (2 ** self.MCrunch)) / self.speed
        self.MD3 += (self.MD4 * self.MD4_mult * (2 ** self.MCrunch)) / self.speed
        self.MD1_mult = ((self.MD1_bought // 10) + 1) * (2 ** self.MCrunch)
        self.MD2_mult = ((self.MD2_bought // 10) + 1) * (2 ** self.MCrunch)
        self.MD3_mult = ((self.MD3_bought // 10) + 1) * (2 ** self.MCrunch)
        self.MD4_mult = ((self.MD4_bought // 10) + 1) * (2 ** self.MCrunch)

    def save(self):
        save = {"Matter": self.Matter, "MD1": self.MD1, "MD2": self.MD2, "MD3": self.MD3, "MD4": self.MD4,
                "MD1_bought": self.MD1_bought, "MD2_bought": self.MD2_bought, "MD3_bought": self.MD3_bought,
                "MD4_bought": self.MD4_bought, "MD1_mult": self.MD1_mult, "MD2_mult": self.MD2_mult,
                "MD3_mult": self.MD3_mult, "MD4_mult": self.MD4_mult, "MD1_price": self.MD1_price,
                "MD2_price": self.MD2_price, "MD3_price": self.MD3_price, "MD4_price": self.MD4_price,
                "MCrunch": self.MCrunch, "MCrunch_cost": self.MCrunch_cost}
        with open("save.json", mode="w") as f:
            f.write(json.dumps(save, indent=2))

    def load_save_from_file(self):
        filetypes = (("Файл json", "*.json"),
                     ("Любой", "*"))
        filename = fd.askopenfilename(title="Открыть файл", initialdir="/",
                                      filetypes=filetypes)
        if filename:
            with open(filename, mode="r") as f:
                try:
                    self.load(json.load(f))
                    mb.showinfo("Успешно", "Сохранение загружено успешно!")
                except Exception as e:
                    mb.showerror("Ошибка", "Произошла ошибка при загрузке файла!")
                    print(e)

    def load(self, data):
        self.Matter = data["Matter"]
        self.MD1 = data["MD1"]
        self.MD2 = data["MD2"]
        self.MD3 = data["MD3"]
        self.MD4 = data["MD4"]
        self.MD1_bought = data["MD1_bought"]
        self.MD2_bought = data["MD2_bought"]
        self.MD3_bought = data["MD3_bought"]
        self.MD4_bought = data["MD4_bought"]
        self.MD1_mult = data["MD1_mult"]
        self.MD2_mult = data["MD2_mult"]
        self.MD3_mult = data["MD3_mult"]
        self.MD4_mult = data["MD4_mult"]
        self.MD1_price = data["MD1_price"]
        self.MD2_price = data["MD2_price"]
        self.MD3_price = data["MD3_price"]
        self.MD4_price = data["MD4_price"]
        self.MCrunch = data["MCrunch"]
        self.MCrunch_cost = data["MCrunch_cost"]

    def new_game(self):
        self.Matter = 10
        self.MD1 = 0
        self.MD2 = 0
        self.MD3 = 0
        self.MD4 = 0
        self.MD1_bought = 0
        self.MD2_bought = 0
        self.MD3_bought = 0
        self.MD4_bought = 0
        self.MD1_mult = 1
        self.MD2_mult = 1
        self.MD3_mult = 1
        self.MD4_mult = 1
        self.MD1_price = 10
        self.MD2_price = 100
        self.MD3_price = 10_000
        self.MD4_price = 1_000_000
        self.MCrunch = 0
        self.MCrunch_cost = 10


def format_e(n):
    a = f"{n:.2E}".lower().replace("+", "")
    return a


def num_notation(num):
    if num > 10 ** 20:
        return format_e(num)
    else:
        if num < 1000:
            return num
        else:
            d = [" тыс.", " млн.", " млрд.", " трил.", " квад.", " квинт."]
            e_num = format_e(num).split("e")
            e_num_1 = int(e_num[1]) % 3
            e_num_str = str(round(float(e_num[0]) * 10 ** e_num_1, 2))
            if int(e_num[1]) // 3 < len(d) + 1:
                return e_num_str + d[((int(e_num[1])) // 3) - 1]


if __name__ == "__main__":
    try:
        g = Game(saving=True)
    finally:
        g.save()
