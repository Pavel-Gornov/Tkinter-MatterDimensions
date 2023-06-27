from tkinter import *
from tkinter import ttk


# noinspection PyAttributeOutsideInit


class Game:
    def __init__(self, font="Calibri"):
        self.font = font
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
        self.initUI()

    def initUI(self):
        # Вкладки
        self.window = Tk()
        self.window.title("Измерения Материи")
        self.window.geometry("500x500")
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

        # Измерения Материи

        self.md1_txt = Label(self.d_grid, text=f"1-е Измерение Материи: {self.MD1}\nx{self.MD1_mult}",
                             font=self.font, background="light blue3", anchor="w", padx=20, height=2, width=34)
        self.md1_btn = Button(self.d_grid, command=self.md1_btn_click,
                              text=f"Купить 1-е измерение!\nЦена: {int(self.MD1_price)} м.", height=2)

        self.md2_txt = Label(self.d_grid, text=f"2-е Измерение Материи: {self.MD1}\nx{self.MD2_mult}", font=self.font,
                             background="light blue", anchor="w", padx=20, height=2, width=34)
        self.md2_btn = Button(self.d_grid, command=self.md2_btn_click,
                              text=f"Купить 2-е измерение!\nЦена: {int(self.MD1_price)} м.", height=2)

        self.md3_txt = Label(self.d_grid, text=f"3-е Измерение Материи: {self.MD1}\nx{self.MD3_mult}", font=self.font,
                             background="light blue3", anchor="w", padx=20, height=2, width=34)
        self.md3_btn = Button(self.d_grid, command=self.md3_btn_click,
                              text=f"Купить 3-е измерение!\nЦена: {int(self.MD1_price)} м.", height=2)

        self.md4_txt = Label(self.d_grid, text=f"4-е Измерение Материи: {self.MD1}\nx{self.MD4_mult}", font=self.font,
                             background="light blue", anchor="w", padx=20, height=2, width=34)
        self.md4_btn = Button(self.d_grid, command=self.md4_btn_click,
                              text=f"Купить 4-е измерение!\nЦена: {int(self.MD1_price)} м.", height=2)

        self.d_grid.pack(anchor="n", fill='both', padx=10, pady=10)
        self.md1_txt.grid(row=0, column=0, padx=5, pady=5, columnspan=2)
        self.md1_btn.grid(row=0, column=2, padx=5, pady=5)
        self.md2_txt.grid(row=1, column=0, padx=5, pady=5, columnspan=2)
        self.md2_btn.grid(row=1, column=2, padx=5, pady=5)
        self.md3_txt.grid(row=2, column=0, padx=5, pady=5, columnspan=2)
        self.md3_btn.grid(row=2, column=2, padx=5, pady=5)
        self.md4_txt.grid(row=3, column=0, padx=5, pady=5, columnspan=2)
        self.md4_btn.grid(row=3, column=2, padx=5, pady=5)
        self.window.after(0, self.main_loop)
        self.window.mainloop()

    def md1_btn_click(self):
        self.MD1 += 1
        self.MD1_bought += 1
        self.Matter -= self.MD1_price
        self.MD1_price *= 1.1
        self.MD1_mult = int(self.MD1_bought / 10) + 1

    def md2_btn_click(self):
        self.MD2 += 1
        self.MD2_bought += 1
        self.Matter -= self.MD2_price
        self.MD2_price *= 1.1
        self.MD2_mult = int(self.MD2_bought / 10) + 1

    def md3_btn_click(self):
        self.MD3 += 1
        self.MD3_bought += 1
        self.Matter -= self.MD3_price
        self.MD3_price *= 1.1
        self.MD3_mult = int(self.MD3_bought / 10) + 1

    def md4_btn_click(self):
        self.MD4 += 1
        self.MD4_bought += 1
        self.Matter -= self.MD4_price
        self.MD4_price *= 1.1
        self.MD4_mult = int(self.MD4_bought / 10) + 1

    def main_loop(self):
        if self.MD1_price > self.Matter:
            self.md1_btn["state"] = "disabled"
        else:
            self.md1_btn["state"] = "active"

        if self.MD2_price > self.Matter:
            self.md2_btn["state"] = "disabled"
        else:
            self.md2_btn["state"] = "active"

        if self.MD3_price > self.Matter:
            self.md3_btn["state"] = "disabled"
        else:
            self.md3_btn["state"] = "active"

        if self.MD4_price > self.Matter:
            self.md4_btn["state"] = "disabled"
        else:
            self.md4_btn["state"] = "active"
        self.Matter += (self.MD1 * self.MD1_mult) / 20
        self.MD1 += (self.MD2 * self.MD2_mult) / 20
        self.MD2 += (self.MD3 * self.MD3_mult) / 20
        self.MD3 += (self.MD4 * self.MD4_mult) / 20
        self.m_txt["text"] = f"У Вас: {num_notation(round(self.Matter, 1))} ед. Материи"
        self.md1_txt["text"] = f"1-е Измерение Материи: {int(self.MD1)}\nx{self.MD1_mult}"
        self.md2_txt["text"] = f"2-е Измерение Материи: {int(self.MD2)}\nx{self.MD2_mult}"
        self.md3_txt["text"] = f"3-е Измерение Материи: {int(self.MD3)}\nx{self.MD3_mult}"
        self.md4_txt["text"] = f"4-е Измерение Материи: {int(self.MD4)}\nx{self.MD4_mult}"
        self.md1_btn["text"] = f"Купить 1-е измерение!\nЦена: {num_notation(int(self.MD1_price))} м."
        self.md2_btn["text"] = f"Купить 2-е измерение!\nЦена: {num_notation(int(self.MD2_price))} м."
        self.md3_btn["text"] = f"Купить 3-е измерение!\nЦена: {num_notation(int(self.MD3_price))} м."
        self.md4_btn["text"] = f"Купить 4-е измерение!\nЦена: {num_notation(int(self.MD4_price))} м."
        self.window.after(50, self.main_loop)


def num_notation(num):
    if num >= 1_000_000_000:
        return str(round(num / 1000000000, 2)) + " млрд."
    elif num >= 1_000_000:
        return str(round(num / 1000000, 2)) + " млн."
    elif num >= 1000:
        return str(round(num / 1000, 2)) + " тыс."
    else:
        return num


if __name__ == "__main__":
    g = Game()
