import tkinter as tk
from tkinter import ttk, messagebox
import requests
import json
import os
from datetime import datetime

class CurrencyConverter:
    def __init__(self, root):
        self.root = root
        self.root.title("Currency Converter")
        self.root.geometry("600x500")

        # Загрузка истории
        self.history = self.load_history()

        self.setup_ui()

    def setup_ui(self):
        # Выбор валюты FROM
        ttk.Label(self.root, text="Из валюты:").grid(row=0, column=0, padx=10, pady=10)
        self.from_currency = ttk.Combobox(self.root, values=self.get_currencies())
        self.from_currency.grid(row=0, column=1, padx=10, pady=10)

        # Выбор валюты TO
        ttk.Label(self.root, text="В валюту:").grid(row=1, column=0, padx=10, pady=10)
        self.to_currency = ttk.Combobox(self.root, values=self.get_currencies())
        self.to_currency.grid(row=1, column=1, padx=10, pady=10)

        # Поле ввода суммы
        ttk.Label(self.root, text="Сумма:").grid(row=2, column=0, padx=10, pady=10)
        self.amount_entry = ttk.Entry(self.root)
        self.amount_entry.grid(row=2, column=1, padx=10, pady=10)

        # Кнопка конвертации
        self.convert_btn = ttk.Button(self.root, text="Конвертировать", command=self.convert_currency)
        self.convert_btn.grid(row=3, column=0, columnspan=2, pady=20)

        # Результат
        self.result_label = ttk.Label(self.root, text="")
        self.result_label.grid(row=4, column=0, columnspan=2, pady=10)

        # Таблица истории
        ttk.Label(self.root, text="История конвертаций:").grid(row=5, column=0, columnspan=2, pady=10)
        columns = ("Дата", "Сумма", "Из", "В", "Результат")
        self.history_tree = ttk.Treeview(self.root, columns=columns, show="headings", height=8)

        for col in columns:
            self.history_tree.heading(col, text=col)
            self.history_tree.column(col, width=100)

        self.history_tree.grid(row=6, column=0, columnspan=2, padx=10, pady=10)

        # Заполнение таблицы истории
        self.refresh_history_table()

    def get_currencies(self):
        # Список популярных валют
        return ['USD', 'EUR', 'GBP', 'JPY', 'CAD', 'AUD', 'CHF', 'CNY', 'RUB', 'INR']

    def get_exchange_rate(self, from_currency, to_currency):
        API_KEY = "YOUR_API_KEY"  # Замените на ваш ключ
        url = f"https://api.exchangerate-api.com/v4/latest/{from_currency}"

        try:
            response = requests.get(url)
            data = response.json()

            if response.status_code == 200 and to_currency in data['rates']:
                return data['rates'][to_currency]
            else:
                messagebox.showerror("Ошибка", "Не удалось получить курс валюты")
                return None
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка подключения: {e}")
            return None

    def load_history(self):
        if os.path.exists("history.json"):
            with open("history.json", "r", encoding="utf-8") as f:
                return json.load(f)
        return []

    def save_history(self):
        with open("history.json", "w", encoding="utf-8") as f:
            json.dump(self.history, f, ensure_ascii=False, indent=2)

    def add_to_history(self, amount, from_curr, to_curr, result):
        record = {
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "amount": amount,
            "from": from_curr,
            "to": to_curr,
            "result": result
        }
        self.history.append(record)
        self.save_history()
        self.refresh_history_table()

    def refresh_history_table(self):
        for item in self.history_tree.get_children():
            self.history_tree.delete(item)

        for record in self.history:
            self.history_tree.insert("", "end", values=(
                record["date"],
                record["amount"],
                record["from"],
                record["to"],
                record["result"]
            ))

    def convert_currency(self):
        from_curr = self.from_currency.get()
        to_curr = self.to_currency.get()

        try:
            amount = float(self.amount_entry.get())
            if amount <= 0:
                messagebox.showerror("Ошибка", "Сумма должна быть положительным числом")
                return
        except ValueError:
            messagebox.showerror("Ошибка", "Введите корректное число")
            return

        if not from_curr or not to_curr:
            messagebox.showerror("Ошибка", "Выберите валюты")
            return

        rate = self.get_exchange_rate(from_curr, to_curr)
        if rate:
            result = amount * rate
            result_text = f"{amount} {from_curr} = {result:.2f} {to_curr}"
            self.result_label.config(text=result_text)
            self.add_to_history(amount, from_curr, to_curr, f"{result:.2f}")

if __name__ == "__main__":
    root = tk.Tk()
    app = CurrencyConverter(root)
    root.mainloop()


    
