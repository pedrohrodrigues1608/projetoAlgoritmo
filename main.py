from padaria import Padaria


if __name__ == "__main__":
    padaria = Padaria()

    print("--- Cadastrando produtos ---")
    padaria.cadastrar_produto("Pão Francês", 0.85, 100, "Panificação")
    padaria.cadastrar_produto("Pão de Queijo", 3.50, 40, "Salgados")
    padaria.cadastrar_produto("Bolo de Chocolate", 32.00, 4, "Confeitaria")

    for prod in padaria.get_produtos():
        print(prod)

    print("\n--- Testando regras de negocio (RN01 a RN04) ---")
    padaria.cadastrar_produto("pão francês", 1.00, 10)  # RN02 nome repetido
    padaria.cadastrar_produto("Sonho", 0, 10)           # RN03 preco invalido
    padaria.cadastrar_produto("Torta", 20.00, -5)       # RN04 estoque negativo

    print("\n--- Busca por codigo ---")
    achado = padaria.buscar_por_codigo(2)
    print("Codigo 2:", achado)

    print("\n--- Busca por nome ---")
    busca = padaria.buscar_por_nome("pão")
    for p in busca:
        print(p)
