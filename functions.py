def infix_to_rpn(expression):
    """Преобразует инфиксное выражение в обратную польскую запись (ОПЗ)."""
    output_string = []
    operator_stack = []
    prior_oper = {"+": 1, "-": 1, "*": 2, "/": 2}

    for element in expression:
        try:
            float(element)
            output_string.append(element)
        except ValueError:
            if element in prior_oper:
                while operator_stack and operator_stack[-1] != "(" and prior_oper.get(operator_stack[-1], 0) >= prior_oper[element]:
                    output_string.append(operator_stack.pop())
                operator_stack.append(element)
            elif element == ")":
                while operator_stack and operator_stack[-1] != "(":
                    output_string.append(operator_stack.pop())
                operator_stack.pop()
            elif element == "(":
                operator_stack.append(element)

    while operator_stack:
        output_string.append(operator_stack.pop())

    return output_string


def evaluate_rpn(rpn_expression):
    """Вычисляет значение выражения в обратной польской записи (ОПЗ)."""
    stack = []

    for term in rpn_expression:
        try:
            stack.append(float(term))
        except ValueError:
            if len(stack) >= 2:
                b = stack.pop()
                a = stack.pop()
                if term == "+":
                    stack.append(a + b)
                elif term == "-":
                    stack.append(a - b)
                elif term == "*":
                    stack.append(a * b)
                elif term == "/":
                    if b == 0:
                        raise ZeroDivisionError("Деление на ноль!")
                    stack.append(a / b)

    return stack[0]