def celsius_to_fahrenheit(c):
    """Converte uma temperatura de Celsius para Fahrenheit."""
    return (c * 9 / 5) + 32


def km_to_miles(km):
    """Converte quilômetros para milhas."""
    return km * 0.621371


def kg_to_pounds(kg):
    """Converte quilogramas para libras."""
    return kg * 2.20462


def ler_numero(mensagem, permitir_negativo=True):
    """Lê um número do usuário, com validação."""
    while True:
        entrada = input(mensagem).strip().replace(",", ".")
        try:
            valor = float(entrada)
            if not permitir_negativo and valor < 0:
                print("Por favor, o número não pode ser negativo.")
                continue
            return valor
        except ValueError:
            print("Entrada inválida. Por favor, insira um número.")


def menu():
    """Exibe o menu de opções para o usuário."""
    print("\nMenu de Conversão de Unidades:")
    print("1. Celsius para Fahrenheit")
    print("2. Quilômetros para Milhas")
    print("3. Quilogramas para Libras")
    print("0. Sair")


if __name__ == "__main__":
    while True:
        menu()
        opcao = input("\nEscolha uma opção: ").strip()

        if opcao == "1":
            c = ler_numero("Digite a temperatura em Celsius: ", permitir_negativo=True)
            resultado = celsius_to_fahrenheit(c)
            print(f"Resultado: {resultado:.2f} °F")

        elif opcao == "2":
            km = ler_numero("Digite a distância em quilômetros: ", permitir_negativo=False)
            resultado = km_to_miles(km)
            print(f"Resultado: {resultado:.2f} milhas")

        elif opcao == "3":
            kg = ler_numero("Digite o peso em quilogramas: ", permitir_negativo=False)
            resultado = kg_to_pounds(kg)
            print(f"Resultado: {resultado:.2f} libras")

        elif opcao == "0":
            print("Saindo do programa, Obrigada!!.")
            break

        else:
            print("\nOpção inválida. Por favor, escolha uma opção válida.")