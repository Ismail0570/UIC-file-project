import os
from typing import List, Dict
from datetime import datetime


class FinanceManager:
    def __init__(self, data_file: str):
        self.data_file = data_file
        self.records = self.load_records()

    def load_records(self) -> List[Dict[str, str]]:
        if not os.path.exists(self.data_file):
            return []

        with open(self.data_file, 'r', encoding='utf-8') as file:
            lines = file.readlines()

        records = []
        for line in lines:
            date, category, amount, description = line.strip().split(';')
            records.append({
                'date': date,
                'category': category,
                'amount': float(amount),
                'description': description
            })
        return records

    def save_records(self) -> None:
        with open(self.data_file, 'w', encoding='utf-8') as file:
            for record in self.records:
                line = f"{record['date']};{record['category']};{record['amount']};{record['description']}\n"
                file.write(line)

    def add_record(self) -> None:
        date = self.get_user_input("Введите дату (ГГГГ-ММ-ДД): ")
        category = self.get_user_input("Введите категорию (Доход/Расход): ")
        amount = self.get_user_input("Введите сумму: ", float)
        description = self.get_user_input("Введите описание: ")

        self.records.append({
            'date': date,
            'category': category,
            'amount': amount,
            'description': description
        })
        self.save_records()

    def show_records(self, per_page: int = 5) -> None:
        total_records = len(self.records)
        total_pages = (total_records + per_page - 1) // per_page  

        for page in range(total_pages):
            print(f"\nСтраница {page + 1} из {total_pages}")
            start = page * per_page
            end = start + per_page
            for index, record in enumerate(self.records[start:end], start=start):
                print(f"{index}: {record['date']} - {record['category']} - {record['amount']} - {record['description']}")
            
            if page < total_pages - 1:
                input("Нажмите Enter для перехода на следующую страницу...")

    def edit_record(self) -> None:
        self.show_records()
        index = self.get_user_input("Введите номер записи для редактирования: ", int)
        if 0 <= index < len(self.records):
            record = self.records[index]
            while True:
                fields = self.get_user_input("\nВыберите поля для изменения (через запятую):\n1. Дата\n2. Категория\n3. Сумма\n4. Описание\nВаш выбор: ").split(',')

                self.update_fields(record, fields)

                self.records[index] = record
                self.save_records()

                more_changes = self.get_user_input("Хотите изменить другие поля? (да/нет): ").lower()
                if more_changes != 'да':
                    break
        else:
            print(f"Запись с индексом {index} не существует.")

    def update_fields(self, record: Dict[str, str], fields: List[str]) -> None:
        field_mapping = {
            '1': 'date',
            '2': 'category',
            '3': 'amount',
            '4': 'description'
        }

        for field in fields:
            field = field.strip()
            if field in field_mapping:
                if field == '3':  
                    record[field_mapping[field]] = self.get_user_input(f"Введите новую {field_mapping[field]}: ", float)
                else:
                    record[field_mapping[field]] = self.get_user_input(f"Введите новую {field_mapping[field]}: ")

    def show_balance(self) -> None:
        income = sum(record['amount'] for record in self.records if record['category'] == 'Доход')
        expense = sum(record['amount'] for record in self.records if record['category'] == 'Расход')
        balance = income - expense

        print(f"Текущий баланс: {balance}")
        print(f"Доходы: {income}")
        print(f"Расходы: {expense}")

    def search_records(self) -> None:
        keyword = self.get_user_input("Введите ключевое слово для поиска: ")
        results = [record for record in self.records if keyword.lower() in record['description'].lower()]
        for record in results:
            print(f"{record['date']} - {record['category']} - {record['amount']} - {record['description']}")

    @staticmethod
    def get_user_input(prompt: str, convert_func=None):
        while True:
            user_input = input(prompt)
            if convert_func:
                try:
                    return convert_func(user_input)
                except ValueError:
                    print("Некорректный ввод, попробуйте снова.")
            else:
                return user_input

    def run(self):
        actions = {
            '1': self.show_balance,
            '2': self.add_record,
            '3': self.edit_record,
            '4': self.search_records,
            '5': exit
        }

        while True:
            print("\nВыберите действие:")
            print("1. Показать баланс")
            print("2. Добавить запись")
            print("3. Редактировать запись")
            print("4. Поиск записей")
            print("5. Выйти")

            choice = self.get_user_input("Ваш выбор: ")

            action = actions.get(choice)
            if action:
                action()
            else:
                print("Некорректный выбор, попробуйте снова.")


if __name__ == "__main__":
    FinanceManager('finance_data.txt').run()