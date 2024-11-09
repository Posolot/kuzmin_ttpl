def prefix_to_infix(stroke):
    tokens = stroke.split()
    stack = []
    for i in tokens.__reversed__():
        if i.isdigit():
            stack.append(i)
        elif i in "+-/*":
            if len(stack) < 2:
                return f"Нехватка операндов для оператора {i} в выражении ({stroke})"
            first_numb = stack.pop()
            second_numb = stack.pop()
            stack.append(f"({first_numb} {i} {second_numb})")
    if len(stack) != 1:
        return f"Некорректное количество операндов или операторов в выражении ({stroke})"
    return stack.pop()

