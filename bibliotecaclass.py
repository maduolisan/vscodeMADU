class biblioteca:
    def __init__(self, titulo, autor, isbn, disponivel=True):
        self.titulo = titulo
        self.autor = autor
        self.isbn = isbn
        self.disponivel = disponivel

    def emprestar(self):
        if self.disponivel:
            self.disponivel = False
            print(f"O livro '{self.titulo}' foi emprestado com sucesso.")
        else:
            print(f"O livro '{self.titulo}' não está disponível para empréstimo.")

    def devolver(self):
        if not self.disponivel:
            self.disponivel = True
            print(f"O livro '{self.titulo}' foi devolvido com sucesso.")
        else:
            print(f"O livro '{self.titulo}' não está emprestado.")

    def descricao(self):
        print(
            f"Título: {self.titulo}\n"
            f"Autor: {self.autor}\n"
            f"ISBN: {self.isbn}\n"
            f"Disponibilidade: {'Sim' if self.disponivel else 'Não'}"
        )


class usuario:
    def __init__(self, nome, matricula, livros_emprestados=None):
        self.nome = nome
        self.matricula = matricula
        self.limite = 1
        self.livros_emprestados = []

    def descricao(self):
        print(f"Nome: {self.nome}\nMatrícula: {self.matricula}")

    def pegar_livro(self, livro):
        if livro.disponivel:
            livro.emprestar()
            self.livros_emprestados.append(livro)
        else:
            print(f"O livro '{livro.titulo}' não está disponível para empréstimo.")

    def devolver_livro(self, livro):
        if livro in self.livros_emprestados:
            livro.devolver()
            self.livros_emprestados.remove(livro)
        else:
            print(f"O usuário não pegou o livro '{livro.titulo}' emprestado.")


class Aluno(usuario):
    def __init__(self, nome, matricula, curso, livros_emprestados=None):
        super().__init__(nome, matricula, livros_emprestados)
        self.curso = curso

    def descricao(self):
        super().descricao()
        print(f"Curso: {self.curso}")

    def pegar_livro(self, livro):
        if len(self.livros_emprestados) >= 2:
            print("O aluno pode pegar até 2 livros.")
            return

        super().pegar_livro(livro)


class Professor(usuario):
    def __init__(self, nome, matricula, disciplina, livros_emprestados=None):
        super().__init__(nome, matricula, livros_emprestados)
        self.disciplina = disciplina

    def descricao(self):
        super().descricao()
        print(f"Disciplina: {self.disciplina}")

    def pegar_livro(self, livro):
        if len(self.livros_emprestados) >= 5:
            print("O professor pode pegar até 5 livros.")
            return

        super().pegar_livro(livro)


if __name__ == "__main__":
    aluno = Aluno("Ana", "001", "Informática")
    professor = Professor("Carlos", "002", "Matemática")

    aluno.pegar_livro(biblioteca("Dom Casmurro", "Machado de Assis", "001"))
    aluno.pegar_livro(biblioteca("Iracema", "José de Alencar", "002"))

    terceiro_livro = biblioteca("O Cortiço", "Aluísio Azevedo", "003")
    aluno.pegar_livro(terceiro_livro)      
    professor.pegar_livro(terceiro_livro)  
