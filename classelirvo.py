class Livro:
	def __init__(self, titulo, autor, paginas, disponiveis=True):
		self.titulo = titulo
		self.autor = autor
		self.paginas = paginas
		self.disponiveis = disponiveis

	def descricao(self):
		print(
			f"Título: {self.titulo}\n"
			f"Autor: {self.autor}\n"
			f"Páginas: {self.paginas}\n"
			f"Disponibilidade: {'Sim' if self.disponiveis else 'Não'}"
		)

	def emprestar(self):
		if self.disponiveis:
			self.disponiveis = False
			print(f"O livro '{self.titulo}' foi emprestado com sucesso.")
		else:
			print(f"O livro '{self.titulo}' não está disponível para empréstimo.")

	def devolver(self):
		if not self.disponiveis:
			self.disponiveis = True
			print(f"O livro '{self.titulo}' foi devolvido com sucesso.")
		else:
			print(f"O livro '{self.titulo}' não está emprestado.")


livro1 = Livro("1984", "George Orwell", 328)
livro2 = Livro("O Senhor dos Anéis", "J.R.R. Tolkien", 1216, disponiveis=False)

print("Descrição do Livro 1:")
livro1.descricao()
print("\nDescrição do Livro 2:")
livro2.descricao()

livro1.emprestar()
livro2.emprestar()
