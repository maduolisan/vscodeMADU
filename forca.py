import random
import os

def limpar_tela():
    """Limpa o terminal para manter o jogo organizado."""
    os.system('cls' if os.name == 'nt' else 'clear')

def desenhar_forca(erros):
    """Retorna o desenho da forca baseado no número de erros."""
    estagios = [
        """
           +---+

           |   |
               |
               |
               |
               |
         =========
        """,
        """
           +---+

           |   |
           O   |
               |
               |
               |
         =========
        """,
        """
           +---+

           |   |
           O   |

           |   |
               |
               |
         =========
        """,
        """
           +---+

           |   |
           O   |
          /|   |
               |
               |
         =========
        """,
        """
           +---+

           |   |
           O   |
          /|\\  |
               |
               |
         =========
        """,
        """
           +---+

           |   |
           O   |
          /|\\  |
          /    |
               |
         =========
        """,
        """
           +---+

           |   |
           O   |
          /|\\  |
          / \\  |
               |
         =========
        """
    ]
    return estagios[erros]

def jogar():
    # Lista de palavras para o jogo (Tema: Tecnologia/Programação)
    palavras = ["PYTHON", "COMPUTADOR", "INTERNET", "PROGRAMA", "CODIGO", "SOFTWARE", "BANCO", "TECLADO"]
    palavra_secreta = random.choice(palavras)
    
    letras_descobertas = ["_" for _ in palavra_secreta]
    letras_tentadas = []
    erros = 0
    max_erros = 6

    while erros < max_erros:
        limpar_tela()
        print("========= JOGO DA FORCA =========")
        print(desenhar_forca(erros))
        print(f"Palavra: {' '.join(letras_descobertas)}")
        print(f"Letras tentadas: {', '.join(letras_tentadas)}")
        print(f"Tentativas restantes: {max_erros - erros}")
        print("=================================")

        # Verifica se o jogador ganhou
        if "_" not in letras_descobertas:
            print(f"\n🎉 Parabéns! Você salvou o programador! A palavra era: {palavra_secreta}\n")
            return

        # Captura e valida o palpite do usuário
        palpite = input("Digite uma letra: ").strip().upper()

        if len(palpite) != 1 or not palpite.isalpha():
            input("Por favor, digite apenas uma única letra. Pressione Enter para continuar...")
            continue

        if palpite in letras_tentadas:
            input("Você já tentou essa letra! Pressione Enter para continuar...")
            continue

        letras_tentadas.append(palpite)

        # Verifica se acertou ou errou
        if palpite in palavra_secreta:
            for i, letra in enumerate(palavra_secreta):
                if letra == palpite:
                    letras_descobertas[i] = palpite
        else:
            erros += 1

    # Se sair do loop é porque esgotou as tentativas
    limpar_tela()
    print(desenhar_forca(erros))
    print(f"💀 Game Over! O programador foi enforcado.")
    print(f"A palavra correta era: {palavra_secreta}\n")

# Executa o jogo
if __name__ == "__main__":
    jogar()
