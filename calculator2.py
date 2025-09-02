"""
Простой калькулятор арифметических выражений.
Допущение: между числами и операторами всегда стоят пробелы.
Пример: "2 + 5 * ( 3 - 7 )"
"""
def operation(a, b, token):
    if token == '+':
        return a + b
    if token == '-':
        return a - b
    if token == '*':
        return a * b
    if token == '/':
        return a / b
    if token == '%':
        return a % b
    if token == '^':
        return a ** b
    raise ValueError(f"Это зачем?: {token}")

def calculate(input_string: str) -> float:
    """
    Главная функция: принимает строку-выражение и возвращает результат вычислений.
    """
    tokens = tokenize(input_string)
    postfix = to_postfix(tokens)
    result = eval_postfix(postfix)
    return result


def tokenize(expression: str) -> list[str]:
    
    """
    Разбивает строку на токены (числа, скобки, операторы).
    Пример: "2 + 5 * ( 3 - 7 )" -> ["2", "+", "5", "*", "(", "3", "-", "7", ")"]
    """
    tokens = expression.split()
    return tokens


def to_postfix(tokens: list[str]) -> list[str]:
    """
    Преобразует выражение в постфиксную форму (обратная польская запись).

    Здесь мы используем ДВА "стека":
      1. output = []   # выходной список (сюда складываем готовые токены в постфиксе)
      2. stack = []    # стек операторов и скобок

    🔹 Примеры:
    ["2", "+", "3"]                -> ["2", "3", "+"]
    ["2", "+", "3", "*", "4"]      -> ["2", "3", "4", "*", "+"]
    ["(", "2", "+", "3", ")", "*", "4"] -> ["2", "3", "+", "4", "*"]
    ["2", "+", "5", "*", "(", "3", "-", "7", ")"] -> ["2", "5", "3", "7", "-", "*", "+"]
    """
    output: list[str] = []  # сюда пойдут числа и операторы в порядке постфикса
    stack: list[str] = []   # временный стек для операторов и скобок
    operations = ["+", "-", "*", "/", "^", "%", "(", ")"]
    priority = {'+': 0,
                '-': 0,
                '(' : -2, 
                ')': -1,
                '*' : 2,
                '/' : 2,
                '%' : 1, 
                '^' : 2 }
    for token in tokens:
        if token not in operations and not token.isdigit():
            raise ValueError(f"неверный символ: {token}")
        if token in operations:
            if token != ")":
              while len(stack) != 0  and priority[stack[-1]] >= priority[token] and token != "(":
                  output.append(stack.pop())
              stack.append(token)
            else:
                while len(stack) != 0 and stack[-1] != "(":
                  output.append(stack.pop())
                if len(stack) == 0:
                    raise ValueError("Пересчитай скобки")
                stack.pop()
        else:  
            output.append(token)
    while len(stack) != 0 :
        s = stack.pop()
        if s == ")" or s == "(":
            raise ValueError("Пересчитай скобки")
        output.append(s)
    return output


def eval_postfix(postfix_tokens: list[str]) -> float:
    """
    Считает значение выражения в постфиксной записи.
    Здесь мы используем ОДИН стек чисел.

    Алгоритм:
      1. Идём слева направо по токенам.
      2. Если число — кладём в стек.
      3. Если оператор — достаём два последних числа из стека,
         применяем оператор и кладём результат обратно в стек.
      4. В конце в стеке должно остаться ровно одно число — это результат.

    🔹 Примеры:

    ["2", "3", "+"]
    Стек: [] → [2] → [2, 3] → [5]
    Результат = 5

    ["2", "3", "5", "*", "+"]
    Стек: [] → [2] → [2, 3] → [2, 3, 5]
          оператор *: [2, 15]
          оператор +: [17]
    Результат = 17

    ["10", "2", "-", "3", "+"]
    Стек: [] → [10] → [10, 2]
          оператор -: [8]
          → [8, 3]
          оператор +: [11]
    Результат = 11

    ["2", "3", "+", "4", "1", "-", "*"]
    ( (2+3) * (4-1) )
    Стек: [] → [2] → [2, 3]
          оператор +: [5]
          → [5, 4] → [5, 4, 1]
          оператор -: [5, 3]
          оператор *: [15]
    Результат = 15
    """
    stack_ans = []
    operations = ["+", "-", "*", "/", "^", "%"]
    for token in postfix_tokens:
        if token in operations:
            if len(stack_ans) < 2:
                raise ValueError("Нет необходимого кол-ва чисел")
            a, b = stack_ans[-2], stack_ans[-1]
            stack_ans.pop()
            stack_ans.pop()
            stack_ans.append(operation(a, b, token))

        else:
            stack_ans.append(int(token))
    return stack_ans[-1]
            
