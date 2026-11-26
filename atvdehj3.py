class ErroBiblioteca(Exception):
    pass

def validar_campos(*campos):
    if any(not c.strip() for c in campos):
        raise ValueError("Todos os campos são obrigatórios.")

class Livro:
    def __init__(self, titulo, autor, isbn):
        validar_campos(titulo, autor, isbn)
        self.titulo, self.autor, self.isbn = titulo, autor, isbn
        self.disponivel = True

    def emprestar(self):
        if not self.disponivel:
            raise ErroBiblioteca(f"'{self.titulo}' já está emprestado.")
        self.disponivel = False

    def devolver(self):
        if self.disponivel:
            raise ErroBiblioteca(f"'{self.titulo}' já está disponível.")
        self.disponivel = True

    def __str__(self):
        status = "Disponível" if self.disponivel else "Emprestado"
        return f"[{self.isbn}] '{self.titulo}' - {self.autor} ({status})"

class Usuario:
    def __init__(self, nome, matricula):
        validar_campos(nome, matricula)
        self.nome, self.matricula = nome, matricula
        self.limite = 1
        self.livros = []

    def pegar_livro(self, livro):
        if len(self.livros) >= self.limite:
            raise ErroBiblioteca(f"Limite de {self.limite} livro(s) atingido para {self.nome}.")
        livro.emprestar()
        self.livros.append(livro)
        print(f"Sucesso: '{livro.titulo}' emprestado para {self.nome}.")

    def devolver_livro(self, livro):
        if livro not in self.livros:
            raise ErroBiblioteca(f"{self.nome} não está com o livro '{livro.titulo}'.")
        livro.devolver()
        self.livros.remove(livro)
        print(f"Sucesso: '{livro.titulo}' devolvido por {self.nome}.")

    def __str__(self):
        return f"{self.nome} (Mat: {self.matricula}) | Livros: {len(self.livros)}/{self.limite}"

class Aluno(Usuario):
    def __init__(self, nome, matricula, curso):
        super().__init__(nome, matricula)
        validar_campos(curso)
        self.curso, self.limite = curso, 2

    def __str__(self):
        return f"[Aluno] {super().__str__()} | Curso: {self.curso}"

class Professor(Usuario):
    def __init__(self, nome, matricula, disciplina):
        super().__init__(nome, matricula)
        validar_campos(disciplina)
        self.disciplina, self.limite = disciplina, 5

    def __str__(self):
        return f"[Professor] {super().__str__()} | Disciplina: {self.disciplina}"

class Biblioteca:
    def __init__(self):
        self.livros = {}
        self.usuarios = {}

    def adicionar_livro(self, livro):
        if livro.isbn in self.livros:
            raise ErroBiblioteca(f"ISBN {livro.isbn} já cadastrado.")
        self.livros[livro.isbn] = livro

    def adicionar_usuario(self, usuario):
        if usuario.matricula in self.usuarios:
            raise ErroBiblioteca(f"Matrícula {usuario.matricula} já cadastrada.")
        self.usuarios[usuario.matricula] = usuario

    def buscar(self, colecao, chave, nome_item):
        if chave not in colecao:
            raise ErroBiblioteca(f"{nome_item} '{chave}' não encontrado(a).")
        return colecao[chave]

def menu():
    bib = Biblioteca()
    for l in [("Dom Casmurro", "Machado de Assis", "001"), ("Iracema", "José de Alencar", "002")]:
        bib.adicionar_livro(Livro(*l))
    bib.adicionar_usuario(Aluno("Ana", "101", "Informática"))
    bib.adicionar_usuario(Professor("Carlos", "202", "Matemática"))

    opcoes = "\n1. Cadastrar Livro | 2. Cadastrar Usuário | 3. Emprestar\n4. Devolver | 5. Listar Livros | 6. Listar Usuários | 0. Sair\nOpção: "

    while (op := input(opcoes).strip()) != "0":
        try:
            if op == "1":
                bib.adicionar_livro(Livro(input("Título: "), input("Autor: "), input("ISBN: ")))
                print("Livro cadastrado!")
            elif op == "2":
                tipo = input("Tipo (1-Aluno / 2-Professor): ").strip()
                if tipo not in ("1", "2"):
                    raise ValueError("Tipo inválido.")
                nome, mat = input("Nome: "), input("Matrícula: ")
                user = Aluno(nome, mat, input("Curso: ")) if tipo == "1" else Professor(nome, mat, input("Disciplina: "))
                bib.adicionar_usuario(user)
                print("Usuário cadastrado!")
            elif op in ("3", "4"):
                user = bib.buscar(bib.usuarios, input("Matrícula: ").strip(), "Usuário")
                livro = bib.buscar(bib.livros, input("ISBN: ").strip(), "Livro")
                user.pegar_livro(livro) if op == "3" else user.devolver_livro(livro)
            elif op == "5":
                print("\n".join(map(str, bib.livros.values())) or "Acervo vazio.")
            elif op == "6":
                print("\n".join(map(str, bib.usuarios.values())) or "Nenhum usuário.")
            else:
                print("Opção inválida!")
        except (ErroBiblioteca, ValueError) as e:
            print(f"[ERRO]: {e}")

if __name__ == "__main__":
    menu()
