def calcular():
	try:
		numero1 = float(input("Digite o primeiro número: "))
		operacao = input("Digite a operação (+, -, *, /): ").strip()
		numero2 = float(input("Digite o segundo número: "))

		if operacao == "+":
			resultado = numero1 + numero2
		elif operacao == "-":
			resultado = numero1 - numero2
		elif operacao == "*":
			resultado = numero1 * numero2
		elif operacao == "/":
			if numero2 == 0:
				print("Erro: não é possível dividir por zero.")
				return
			resultado = numero1 / numero2
		else:
			print("Operação inválida.")
			return

		print("Resultado:", resultado)
	except ValueError:
		print("Digite números válidos.")


if __name__ == "__main__":
	calcular()

      