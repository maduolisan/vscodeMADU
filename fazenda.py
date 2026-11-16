import pygame
import sys
import random

# Inicializa o Pygame
pygame.init()

# Configurações da Janela
LARGURA, ALTURA = 1000, 650
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Vale da Colheita - Minha Fazenda")

# Definição de Cores (RGB)
PRETO = (10, 10, 12)
BRANCO = (240, 240, 240)
CINZA_PAINEL = (44, 53, 57)
CINZA_CLARO = (150, 152, 154)
TERRA_ARADA = (110, 74, 46)
VERDE_BROTO = (46, 204, 113)
AMARELO = (241, 196, 15)
VERDE = (39, 174, 96)

# Paleta de Estações
COR_PRIMAVERA = (39, 174, 96)   # Verde vivo
COR_VERAO = (219, 176, 68)      # Tom amarelado/seco
COR_OUTONO = (186, 94, 35)      # Tons alaranjados
COR_INVERNO = (200, 214, 229)   # Tons azulados/neve

# Fontes
fonte_p = pygame.font.SysFont("arial", 18, bold=True)
fonte_m = pygame.font.SysFont("arial", 24, bold=True)
fonte_g = pygame.font.SysFont("arial", 45, bold=True)
relogio = pygame.time.Clock()

# Dados das Plantas (Nome: [Tempo para crescer em frames, Cor do fruto, Preço Semente, Preço Venda, Tipo])
PROPRIEDADES_PLANTAS = {
    "Trigo": {"ciclo": 180, "cor": (241, 196, 15), "compra": 5, "venda": 12, "tipo": "Planta"},
    "Tomate": {"ciclo": 300, "cor": (231, 76, 60), "compra": 10, "venda": 25, "tipo": "Vegetal"},
    "Morango": {"ciclo": 420, "cor": (255, 107, 107), "compra": 15, "venda": 45, "tipo": "Fruta"}
}

def tela_customizacao():
    """Interface de customização do personagem antes do jogo começar."""
    nome = "Fazendeiro"
    genero_index = 0
    generos = ["Masculino", "Feminino", "Não-Binário"]
    
    cores_roupa = [(231, 76, 60), (52, 152, 219), (155, 89, 182), (241, 196, 15), (230, 126, 34)]
    cor_index = 0
    
    escrevendo = False
    configurando = True
    
    while configurando:
        tela.fill((30, 39, 46))
        
        # Título
        txt_titulo = fonte_g.render("Crie seu Fazendeiro", True, BRANCO)
        tela.blit(txt_titulo, (LARGURA // 2 - txt_titulo.get_width() // 2, 50))
        
        # Caixas de Opções
        box_nome = pygame.Rect(350, 180, 300, 40)
        box_genero = pygame.Rect(350, 260, 300, 40)
        box_cor = pygame.Rect(350, 340, 300, 40)
        btn_jogar = pygame.Rect(400, 460, 200, 50)
        
        pygame.draw.rect(tela, (57, 72, 85) if not escrevendo else (75, 101, 129), box_nome, border_radius=5)
        pygame.draw.rect(tela, (57, 72, 85), box_genero, border_radius=5)
        pygame.draw.rect(tela, (57, 72, 85), box_cor, border_radius=5)
        pygame.draw.rect(tela, (46, 204, 113), btn_jogar, border_radius=8)
        
        # Textos das opções
        tela.blit(fonte_m.render(f"Nome: {nome}", True, BRANCO), (360, 188))
        tela.blit(fonte_m.render(f"Gênero: {generos[genero_index]}", True, BRANCO), (360, 268))
        tela.blit(fonte_m.render("Mudar Cor da Roupa", True, BRANCO), (360, 348))
        
        # Amostra da Cor selecionada
        pygame.draw.circle(tela, cores_roupa[cor_index], (680, 360), 15)
        
        txt_jogar = fonte_m.render("Começar Fazenda", True, PRETO)
        tela.blit(txt_jogar, (btn_jogar.centerx - txt_jogar.get_width() // 2, btn_jogar.centery - txt_jogar.get_height() // 2))
        
        # Pequena dica na tela
        tela.blit(fonte_p.render("*Clique na caixa de texto do Nome para digitar", True, CINZA_CLARO), (350, 225))
        
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            if evento.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if box_nome.collidepoint(pos):
                    escrevendo = True
                else:
                    escrevendo = False
                    
                if box_genero.collidepoint(pos):
                    genero_index = (genero_index + 1) % len(generos)
                if box_cor.collidepoint(pos):
                    cor_index = (cor_index + 1) % len(cores_roupa)
                if btn_jogar.collidepoint(pos):
                    configurando = False
                    
            if evento.type == pygame.KEYDOWN and escrevendo:
                if evento.key == pygame.K_BACKSPACE:
                    nome = nome[:-1]
                elif len(nome) < 14 and (evento.unicode.isalnum() or evento.key == pygame.K_SPACE):
                    nome += evento.unicode
                    
        pygame.display.flip()
        relogio.tick(30)
        
    return nome, generos[genero_index], cores_roupa[cor_index]

def rodar_fazenda():
    # Carrega customizações do Menu
    nome_player, genero_player, cor_roupa = tela_customizacao()
    
    # Status iniciais do jogador
    ouro = 50
    inventario_sementes = {"Trigo": 5, "Tomate": 3, "Morango": 2}
    semente_selecionada = "Trigo"
    
    # Posição do Fazendeiro
    player_x, player_y = 350, 300
    player_vel = 4
    
    # Configurações do Terreno de Cultivo
    lotes_terra = []
    tamanho_lote = 60
    for linha in range(4):
        for coluna in range(6):
            rx = 150 + (coluna * (tamanho_lote + 15))
            ry = 150 + (linha * (tamanho_lote + 15))
            lotes_terra.append({
                "rect": pygame.Rect(rx, ry, tamanho_lote, tamanho_lote),
                "status": "vazio", "tipo": None, "progresso": 0
            })
            
    # Variáveis de Estações do Ano
    estacoes = ["Primavera", "Verão", "Outono", "Inverno"]
    estacao_atual_idx = 0
    tempo_estacao = 0

    jogando = True
    while jogando:
        tempo_estacao += 1
        if tempo_estacao >= 1800: # 30 segundos por estação
            estacao_atual_idx = (estacao_atual_idx + 1) % 4
            tempo_estacao = 0
            
        # Define a cor de fundo com base na estação atual
        if estacoes[estacao_atual_idx] == "Primavera": cor_grama = COR_PRIMAVERA
        elif estacoes[estacao_atual_idx] == "Verão": cor_grama = COR_VERAO
        elif estacoes[estacao_atual_idx] == "Outono": cor_grama = COR_OUTONO
        else: cor_grama = COR_INVERNO
        
        tela.fill(cor_grama)
        
        # 1. Eventos do Jogo
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_1: semente_selecionada = "Trigo"
                if evento.key == pygame.K_2: semente_selecionada = "Tomate"
                if evento.key == pygame.K_3: semente_selecionada = "Morango"
                
                if evento.key == pygame.K_e:
                    player_rect = pygame.Rect(player_x, player_y, 30, 45)
                    for lote in lotes_terra:
                        if lote["rect"].colliderect(player_rect):
                            if lote["status"] == "vazio" and inventario_sementes[semente_selecionada] > 0:
                                inventario_sementes[semente_selecionada] -= 1
                                lote["status"] = "plantado"
                                lote["tipo"] = semente_selecionada
                                lote["progresso"] = 0
                            elif lote["status"] == "pronto":
                                valor_venda = PROPRIEDADES_PLANTAS[lote["tipo"]]["venda"]
                                ouro += valor_venda
                                lote["status"] = "vazio"
                                lote["tipo"] = None
                                lote["progresso"] = 0
                                
                if evento.key == pygame.K_p:
                    custo = PROPRIEDADES_PLANTAS[semente_selecionada]["compra"]
                    if ouro >= custo:
                        ouro -= custo
                        inventario_sementes[semente_selecionada] += 1

        # 2. Movimentação do Fazendeiro
        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_LEFT] or teclas[pygame.K_a]: player_x -= player_vel
        if teclas[pygame.K_RIGHT] or teclas[pygame.K_d]: player_x += player_vel
        if teclas[pygame.K_UP] or teclas[pygame.K_w]: player_y -= player_vel
        if teclas[pygame.K_DOWN] or teclas[pygame.K_s]: player_y += player_vel
        
        player_x = max(10, min(player_x, 710))
        player_y = max(10, min(player_y, ALTURA - 55))

        # 3. Atualizar crescimento
        for lote in lotes_terra:
            if lote["status"] == "plantado":
                fator_estacao = 0.5 if estacoes[estacao_atual_idx] == "Inverno" else 1.0
                lote["progresso"] += fator_estacao
                
                ciclo_necessario = PROPRIEDADES_PLANTAS[lote["tipo"]]["ciclo"]
                if lote["progresso"] >= ciclo_necessario:
                    lote["status"] = "pronto"

        # 4. Renderizar Lotes
        for lote in lotes_terra:
            pygame.draw.rect(tela, TERRA_ARADA, lote["rect"], border_radius=4)
            
            if lote["status"] == "plantado":
                ciclo = PROPRIEDADES_PLANTAS[lote["tipo"]]["ciclo"]
                raio_crescimento = int((lote["progresso"] / ciclo) * 12) + 2
                pygame.draw.circle(tela, VERDE_BROTO, lote["rect"].center, max(2, min(raio_crescimento, 14)))
                
            elif lote["status"] == "pronto":
                cor_fruta = PROPRIEDADES_PLANTAS[lote["tipo"]]["cor"]
                pygame.draw.circle(tela, cor_fruta, lote["rect"].center, 15)
                pygame.draw.rect(tela, (39, 174, 96), (lote["rect"].centerx - 4, lote["rect"].centery - 18, 8, 6))

        # 5. Desenhar Personagem
        pygame.draw.rect(tela, cor_roupa, (player_x, player_y + 15, 30, 30), border_radius=4)
        pygame.draw.ellipse(tela, (255, 219, 172), (player_x + 3, player_y - 3, 24, 22))
        pygame.draw.ellipse(tela, (243, 198, 119), (player_x - 5, player_y - 5, 40, 10))
        pygame.draw.ellipse(tela, (213, 168, 89), (player_x + 5, player_y - 12, 20, 12))

        # 6. Painel Lateral (HUD)

        # 6. Painel Lateral (HUD)
        painel_x = 760
        painel_largura = 240

        pygame.draw.rect(
            tela,
            CINZA_PAINEL,
            (painel_x, 0, painel_largura, ALTURA)
        )

        # Título do painel
        titulo_hud = fonte_m.render("MINHA FAZENDA", True, BRANCO)
        tela.blit(titulo_hud, (painel_x + 15, 20))

        pygame.draw.line(
            tela, CINZA_CLARO,
            (painel_x + 10, 60),
            (990, 60), 2
        )

        # Informações do jogador
        tela.blit(
            fonte_p.render(f"Fazendeiro: {nome_player}", True, BRANCO),
            (painel_x + 15, 80)
        )

        tela.blit(
            fonte_p.render(f"Gênero: {genero_player}", True, CINZA_CLARO),
            (painel_x + 15, 110)
        )

        # Ouro
        pygame.draw.rect(
            tela, (80, 65, 20),
            (painel_x + 10, 150, 210, 45),
            border_radius=8
        )

        tela.blit(
            fonte_m.render(f"Ouro: {ouro}", True, AMARELO),
            (painel_x + 20, 158)
        )

        # Estação
        tela.blit(
            fonte_m.render("Estação:", True, BRANCO),
            (painel_x + 15, 215)
        )

        tela.blit(
            fonte_p.render(
                estacoes[estacao_atual_idx],
                True,
                BRANCO
            ),
            (painel_x + 15, 250)
        )

        # Inventário
        tela.blit(
            fonte_m.render("SEMENTES", True, BRANCO),
            (painel_x + 15, 295)
        )

        y_inv = 335

        for i, planta in enumerate(["Trigo", "Tomate", "Morango"]):
            cor = (
                AMARELO if planta == semente_selecionada
                else BRANCO
            )

            tela.blit(
                fonte_p.render(
                    f"[{i + 1}] {planta}: {inventario_sementes[planta]}",
                    True,
                    cor
                ),
                (painel_x + 15, y_inv)
            )

            y_inv += 30

        # Planta selecionada
        pygame.draw.line(
            tela, CINZA_CLARO,
            (painel_x + 10, 440),
            (990, 440), 2
        )

        tela.blit(
            fonte_p.render("Selecionada:", True, CINZA_CLARO),
            (painel_x + 15, 455)
        )

        tela.blit(
            fonte_m.render(semente_selecionada, True, VERDE_BROTO),
            (painel_x + 15, 480)
        )

        # Controles
        tela.blit(
            fonte_m.render("CONTROLES", True, BRANCO),
            (painel_x + 15, 530)
        )

        controles = [
            "WASD / Setas: Mover",
            "1, 2, 3: Selecionar",
            "E: Plantar / Colher",
            "P: Comprar sementes"
        ]

        for i, texto in enumerate(controles):
            tela.blit(
                fonte_p.render(texto, True, CINZA_CLARO),
                (painel_x + 15, 565 + i * 22)
            )

        # 7. Atualizar a tela
        pygame.display.flip()

        # Controlar FPS
        relogio.tick(60)


# Iniciar o jogo
if __name__ == "__main__":
    rodar_fazenda()

