import requests
from bs4 import BeautifulSoup
import tkinter as tk
from tkinter import messagebox, ttk


class CurrencyConverter:
    def __init__(self):
        self.exchange_rate = self.scrape_exchange_rate()

    def scrape_exchange_rate(self):
        try:
            url = 'https://privatbank.ua/rates-archive'
            response = requests.get(url)

            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                rate_element = soup.find('div', class_='purchase')

                if rate_element:
                    rate_text = rate_element.text.strip()
                    rate = float(rate_text.split()[0].replace(',', '.'))
                    return rate

            raise ValueError("Не удалось найти курс валют")

        except Exception as e:
            messagebox.showerror("Ошибка", f"Сбой при парсинге: {e}")
            return None

    def convert(self, amount):
        if self.exchange_rate is None:
            return None
        return amount / self.exchange_rate


class CurrencyConverterGUI:
    def __init__(self, master):
        self.master = master
        master.title("Конвертер валют")

        self.converter = CurrencyConverter()

        master.columnconfigure(0, weight=1)
        master.columnconfigure(1, weight=1)
        master.rowconfigure(0, weight=1)
        master.rowconfigure(1, weight=1)

        self.left_frame = tk.Frame(master)
        self.left_frame.grid(row=0, column=0, sticky="nsew")

        tk.Label(self.left_frame, text="Введите сумму в гривнах (UAH):").pack(fill="x")
        self.amount_entry = tk.Entry(self.left_frame)
        self.amount_entry.pack(fill="x")

        convert_button = tk.Button(self.left_frame, text="Конвертировать", command=self.perform_conversion)
        convert_button.pack(fill="x")

        self.result_label = tk.Label(self.left_frame, text="", font=("Arial", 14), fg="green")
        self.result_label.pack(fill="x")

        self.right_frame = tk.Frame(master)
        self.right_frame.grid(row=0, column=1, sticky="nsew")

        tk.Label(self.right_frame, text="Курсы валют (USD → UAH)", font=("Arial", 16, "bold")).pack()

        self.table = ttk.Treeview(self.right_frame, columns=("Валюта", "Курс"), show="headings", height=8)
        self.table.heading("Валюта", text="Валюта")
        self.table.heading("Курс", text="Курс (1 USD в UAH)")
        self.table.pack(fill="both", expand=True)

        self.populate_table()

    def perform_conversion(self):
        try:
            amount = float(self.amount_entry.get())
            result = self.converter.convert(amount)

            if result is not None:
                self.result_label.config(text=f"{amount} UAH = {result:.2f} USD")
            else:
                messagebox.showerror("Ошибка", "Не удалось выполнить конвертацию")

        except ValueError:
            messagebox.showerror("Ошибка", "Введите корректное число")

    def populate_table(self):

        if self.converter.exchange_rate is not None:
            self.table.insert("", "end", values=("USD", f"{self.converter.exchange_rate:.2f} UAH"))


def main():
    root = tk.Tk()
    root.geometry("600x300")
    app = CurrencyConverterGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
