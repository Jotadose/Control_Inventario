def input_int(prompt):
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Por favor, ingrese un número válido.")
