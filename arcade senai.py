import mysql.connector
from mysql.connector import Error

def conectar():
    """Estabelece conexão com o banco MySQL local."""
    try:
        conexao = mysql.connector.connect(
            host="localhost",
            user="root",        # Altere para o seu usuário do MySQL
            password="",        # Altere para a sua senha do MySQL
            database="arcade senai"
        )
        return conexao
    except Error as e:
        print(f"\n[ERRO] Falha ao conectar ao banco de dados: {e}")
        return None

def registrar_jogador(nome, escola):
    """Cadastra o jogador ou retorna o ID se já existir."""
    conexao = conectar()
    if not conexao:
        return None

    try:
        cursor = conexao.cursor()
        query = "INSERT INTO jogadores (nome, escola) VALUES (%s, %s)"
        cursor.execute(query, (nome, escola))
        conexao.commit()
        id_jogador = cursor.lastrowid
        return id_jogador
    except Error as e:
        print(f"\n[ERRO] Falha ao cadastrar jogador: {e}")
        return None
    finally:
        conexao.close()

def salvar_pontuacao(id_jogador, nome_jogo, pontos):
    """Salva a pontuação da partida no banco de dados."""
    conexao = conectar()
    if not conexao:
        return

    try:
        cursor = conexao.cursor()
        # Busca o id do jogo pelo nome
        cursor.execute("SELECT id_jogo FROM jogos WHERE nome_jogo = %s", (nome_jogo,))
        resultado = cursor.fetchone()
        
        if resultado:
            id_jogo = resultado[0]
            query = "INSERT INTO pontuacoes (id_jogador, id_jogo, pontos) VALUES (%s, %s, %s)"
            cursor.execute(query, (id_jogador, id_jogo, pontos))
            conexao.commit()
            print("\n✅ Pontuação salva com sucesso no ranking!")
        else:
            print(f"\n[ERRO] Jogo '{nome_jogo}' não cadastrado no banco.")
    except Error as e:
        print(f"\n[ERRO] Falha ao salvar pontuação: {e}")
    finally:
        conexao.close()

def exibir_ranking(nome_jogo):
    """Consulta e exibe os 10 melhores resultados de um jogo específico."""
    conexao = conectar()
    if not conexao:
        return

    try:
        cursor = conexao.cursor()
        query = """
            SELECT 
                RANK() OVER (ORDER BY p.pontos DESC) AS posicao,
                j.nome AS jogador,
                j.escola,
                p.pontos
            FROM pontuacoes p
            JOIN jogadores j ON p.id_jogador = j.id_jogador
            JOIN jogos g ON p.id_jogo = g.id_jogo
            WHERE g.nome_jogo = %s
            ORDER BY p.pontos DESC
            LIMIT 10;
        """
        cursor.execute(query, (nome_jogo,))
        resultados = cursor.fetchall()

        print(f"\n=== RANKING TOP 10 - {nome_jogo.upper()} ===")
        if not resultados:
            print("Nenhuma pontuação registrada ainda.")
        else:
            print(f"{'POS':<5} | {'JOGADOR':<20} | {'ESCOLA':<20} | {'PONTOS':<8}")
            print("-" * 60)
            for pos, nome, escola, pontos in resultados:
                print(f"{pos:<5} | {nome:<20} | {escola:<20} | {pontos:<8}")
        print("=" * 60)
    except Error as e:
        print(f"\n[ERRO] Falha ao carregar ranking: {e}")
    finally:
        conexao.close()