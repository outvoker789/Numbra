from functions import infix_to_rpn, evaluate_rpn
import re

class Calculator:
    def __init__(self):
        """Инициализация калькулятора."""
        self.history = []  # История вычислений хранится в памяти

    def parse_expression(self, input_expression):
        """Разбивает входное выражение на токены."""
        return re.findall(r'\d+\.\d+|\d+|[\+\-\*/\(\)]', input_expression)

    def calculate(self, input_expression):
        """Выполняет вычисление выражения."""
        tokens = self.parse_expression(input_expression)
        rpn = infix_to_rpn(tokens)
        result = evaluate_rpn(rpn)
        self.save_to_history(input_expression, result)  # Сохраняем результат в историю
        return result

    def save_to_history(self, expression, result):
        """Сохраняет результат вычисления в историю (в памяти)."""
        entry = f"{expression} = {result}"
        self.history.append(entry)  # Добавляем запись в историю

    def show_history(self):
        """Выводит историю вычислений."""
        if not self.history:
            print("История пуста.")
        else:
            print("История вычислений:")
            for entry in self.history:
                print(entry)