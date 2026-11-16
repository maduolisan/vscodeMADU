import pygame
import random
import sys

# Inicializa o Pygame
pygame.init()

# Configurações da tela
LARGURA, ALTURA = 800, 600
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Invasão Espacial: O Confronto Final")

# Cores (RGB)
PRETO = (10, 10, 15)
AZUL_CLARO = (52, 152, 219)
AZUL_BRILHANTE = (41, 128, 185)
VERMELHO = (231, 76, 60)
VERMELHO_ESCURO = (192, 57, 43)
AMARELO = (241, 196, 15)
BRANCO = (255, 255, 255)
CINZA_ESCURO = (44, 62, 80)
CINZA_CLARO = (127, 140, 141)
VERDE = (46, 204, 113)

# Fontes
fonte = pygame.font.SysFont("arial", 26, bold=True)
fonte_grande = pygame.font.SysFont("arial", 50, bold=True)
relogio = pygame.time.Clock()

def criar_inimigo():
    largura_ini = 45
    x = random.randint(0, LARGURA - largura_ini)
    y = random.randint(-150, -50)
    velocidade = random.randint(3, 5)
    return {"rect": pygame.Rect(x, y, largura_ini, largura_ini), "vel": velocidade, "tempo_tiro": random.randint(30, 90)}

def desenhar_nave_jogador(x, y):
    """Desenha uma nave poligonal detalhada e bonita."""
    # Asas
    pygame.draw.polygon(tela, AZUL_BRILHANTE, [(x, y + 40), (x - 15, y + 35), (x, y + 15)])
    pygame.draw.polygon(tela, AZUL_BRILHANTE, [(x + 50, y + 40), (x + 65, y + 35), (x + 50, y + 15)])
    # Corpo Principal
    pygame.draw.polygon(tela, AZUL_CLARO, [(x + 25, y - 10), (x, y + 40), (x + 50, y + 40)])
    # Cabine de Vidro
    pygame.draw.ellipse(tela, BRANCO, (x + 18, y + 10, 14, 20))
    # Propulsores (Fogo)
    if random.choice([True, False]):
        pygame.draw.polygon(tela, AMARELO, [(x + 15, y + 40), (x + 25, y + 55), (x + 35, y + 40)])

def desenhar_nave_inimiga(rect):
    """Desenha uma nave alienígena em formato de capsula de combate."""
    x, y = rect.x, rect.y
    # Asas laterais vermelhas
    pygame.draw.polygon(tela, VERMELHO_ESCURO, [(x, y), (x - 8, y + 20), (x + 10, y + 15)])
    pygame.draw.polygon(tela, VERMELHO_ESCURO, [(x + 45, y), (x + 53, y + 20), (x + 35, y + 15)])
    # Corpo central
    pygame.draw.rect(tela, VERMELHO, (x + 10, y, 25, 35), border_radius=5)
    # Núcleo de energia / visor
    pygame.draw.circle(tela, AMARELO, (x + 22, y + 15), 5)

def desenhar_boss(x, y, largura, altura):
    """Desenha uma nave-mãe massiva e intimidadora."""
    # Casco principal
    pygame.draw.polygon(tela, CINZA_ESCURO, [(x, y), (x + largura, y), (x + largura - 40, y + altura), (x + 40, y + altura)])
    # Placas de blindagem vermelhas nas pontas
    pygame.draw.polygon(tela, VERMELHO, [(x, y), (x + 40, y), (x + 50, y + 30)])
    pygame.draw.polygon(tela, VERMELHO, [(x + largura, y), (x + largura - 40, y), (x + largura - 50, y + 30)])
    # Canhões inferiores
    pygame.draw.rect(tela, CINZA_CLARO, (x + largura // 4 - 5, y + altura, 10, 15))
    pygame.draw.rect(tela, CINZA_CLARO, (x + (largura * 3) // 4 - 5, y + altura, 10, 15))
    # Luzes de comando centrais
    for i in range(5):
        pygame.draw.circle(tela, VERMELHO if random.randint(0, 1) == 0 else AMARELO, (x + 45 + (i * 28), y + 20), 4)

def rodar_jogo():
    jogador_largura, jogador_altura = 50, 40
    jogador_x = LARGURA // 2 - jogador_largura // 2
    jogador_y = ALTURA - 70
    jogador_velocidade = 8
    vidas = 3
    pontos = 0
    
    tiro_largura, tiro_altura = 6, 18
    tiro_velocidade = 12
    lista_tiros = []
    tiros_inimigos = []
    
    estrelas = [[random.randint(0, LARGURA), random.randint(0, ALTURA), random.randint(2, 6)] for _ in range(40)]
    lista_inimigos = [criar_inimigo() for _ in range(5)]
    
    boss_ativo = False
    boss_x = LARGURA // 2 - 100
    boss_y = -100
    boss_largura, boss_altura = 200, 60
    boss_vida_max = 30
    boss_vida = boss_vida_max
    boss_velocidade = 4
    boss_direcao = 1

    jogando = True
    resultado = "DERROTA"

    while jogando:
        tela.fill(PRETO)
        
        # 1. Estrelas de Fundo
        for estrela in estrelas:
            estrela[1] += estrela[2]
            if estrela[1] > ALTURA:
                estrela[1] = 0
                estrela[0] = random.randint(0, LARGURA)
            pygame.draw.circle(tela, (150, 150, 150), (estrela[0], estrela[1]), 2)

        # 2. Captura de Eventos
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    tiro_x = jogador_x + jogador_largura // 2 - tiro_largura // 2
                    lista_tiros.append(pygame.Rect(tiro_x, jogador_y, tiro_largura, tiro_altura))

        # 3. Controles do Jogador
        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_LEFT] and jogador_x > 15: jogador_x -= jogador_velocidade
        if teclas[pygame.K_RIGHT] and jogador_x < LARGURA - jogador_largura - 15: jogador_x += jogador_velocidade
        if teclas[pygame.K_UP] and jogador_y > 350: jogador_y -= jogador_velocidade
        if teclas[pygame.K_DOWN] and jogador_y < ALTURA - jogador_altura - 10: jogador_y += jogador_velocidade

        # Ativação do Boss
        if pontos >= 100 and not boss_ativo and boss_vida > 0:
            boss_ativo = True
            lista_inimigos.clear()

        # 4. Movimentação dos Tiros do Jogador
        for tiro in lista_tiros[:]:
            tiro.y -= tiro_velocidade
            if tiro.y < 0: lista_tiros.remove(tiro)

        # 5. Inimigos Comuns
        if not boss_ativo:
            for inimigo in lista_inimigos:
                inimigo["rect"].y += inimigo["vel"]
                inimigo["tempo_tiro"] -= 1
                
                if inimigo["tempo_tiro"] <= 0:
                    tiros_inimigos.append(pygame.Rect(inimigo["rect"].centerx - 3, inimigo["rect"].bottom, 6, 14))
                    inimigo["tempo_tiro"] = random.randint(60, 120)

                # CORREÇÃO AQUI: Se passar da tela, reaparece no topo sem tirar vida do jogador
                if inimigo["rect"].y > ALTURA:
                    inimigo["rect"].x = random.randint(0, LARGURA - 45)
                    inimigo["rect"].y = random.randint(-100, -40)
        # 6. Lógica do Chefe (Boss)
        else:
            if boss_y < 60:
                boss_y += 2
            else:
                boss_x += boss_velocidade * boss_direcao
                if boss_x <= 20 or boss_x >= LARGURA - boss_largura - 20:
                    boss_direcao *= -1
                
                if random.randint(1, 18) == 1:
                    tiros_inimigos.append(pygame.Rect(boss_x + boss_largura // 4, boss_y + boss_altura, 6, 16))
                    tiros_inimigos.append(pygame.Rect(boss_x + (boss_largura * 3) // 4, boss_y + boss_altura, 6, 16))

        # 7. Movimentação dos Tiros Inimigos
        for t_ini in tiros_inimigos[:]:
            t_ini.y += 6
            if t_ini.y > ALTURA: tiros_inimigos.remove(t_ini)

        # 8. Colisões
        rect_jogador = pygame.Rect(jogador_x, jogador_y, jogador_largura, jogador_altura)
        
        # Colisão com Tiros Inimigos
        for t_ini in tiros_inimigos[:]:
            if t_ini.colliderect(rect_jogador):
                tiros_inimigos.remove(t_ini)
                vidas -= 1

        if not boss_ativo:
            for inimigo in lista_inimigos[:]:
                for tiro in lista_tiros[:]:
                    if inimigo["rect"].colliderect(tiro):
                        if tiro in lista_tiros: lista_tiros.remove(tiro)
                        inimigo["rect"].x = random.randint(0, LARGURA - 45)
                        inimigo["rect"].y = random.randint(-150, -50)
                        pontos += 10
                        break
                # Colisão direta entre naves (Jogador bate na nave inimiga)
                if inimigo["rect"].colliderect(rect_jogador):
                    inimigo["rect"].x = random.randint(0, LARGURA - 45)
                    inimigo["rect"].y = random.randint(-150, -50)
                    vidas -= 1
        else:
            rect_boss = pygame.Rect(boss_x, boss_y, boss_largura, boss_altura)
            for tiro in lista_tiros[:]:
                if rect_boss.colliderect(tiro):
                    lista_tiros.remove(tiro)
                    boss_vida -= 1
                    if boss_vida <= 0:
                        resultado = "VITÓRIA"
                        jogando = False

        if vidas <= 0:
            jogando = False

        # 9. Desenhar Elementos na Tela
        desenhar_nave_jogador(jogador_x, jogador_y)
        
        for tiro in lista_tiros: pygame.draw.rect(tela, VERDE, tiro, border_radius=2)
        for t_ini in tiros_inimigos: pygame.draw.rect(tela, AMARELO, t_ini, border_radius=2)
            
        if not boss_ativo:
            for inimigo in lista_inimigos: desenhar_nave_inimiga(inimigo["rect"])
        else:
            desenhar_boss(boss_x, boss_y, boss_largura, boss_altura)
            largura_barra = int((boss_vida / boss_vida_max) * boss_largura)
            pygame.draw.rect(tela, CINZA_ESCURO, (boss_x, boss_y - 25, boss_largura, 8))
            pygame.draw.rect(tela, VERDE, (boss_x, boss_y - 25, largura_barra, 8))

        # Interface
        tela.blit(fonte.render(f"Pontos: {pontos}", True, BRANCO), (10, 10))
        tela.blit(fonte.render(f"Vidas: {'❤️ ' * max(0, vidas)}", True, VERMELHO), (LARGURA - 170, 10))

        pygame.display.flip()
        relogio.tick(60)
        
    return resultado, pontos

# Loop de Estados do Jogo
while True:
    resultado, pontos_finais = rodar_jogo()
    
    esperando_input = True
    while esperando_input:
        tela.fill(PRETO)
        
        if resultado == "VITÓRIA":
            texto_fim = fonte_grande.render("VITÓRIA! O ESPAÇO ESTÁ SALVO!", True, VERDE)
        else:
            texto_fim = fonte_grande.render("GAME OVER", True, VERMELHO)
            
        texto_final = fonte.render(f"Pontuação Final: {pontos_finais}", True, BRANCO)
        texto_reiniciar = fonte.render("Pressione [R] para Jogar Novamente", True, AMARELO)
        texto_sair = fonte.render("Pressione [ESC] para Sair", True, CINZA_CLARO)
        tela.blit(texto_fim, (LARGURA // 2 - texto_fim.get_width() // 2, ALTURA // 2 - 80))
        tela.blit(texto_final, (LARGURA // 2 - texto_final.get_width() // 2, ALTURA // 2 - 10))
        tela.blit(texto_reiniciar, (LARGURA // 2 - texto_reiniciar.get_width() // 2, ALTURA // 2 + 50))
        tela.blit(texto_sair, (LARGURA // 2 - texto_sair.get_width() // 2, ALTURA // 2 + 90))
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_r:
                    esperando_input = False
            elif evento.key == pygame.K_ESCAPE:
                pygame.quit()
    sys.exit()
    pygame.display.flip()
    relogio.tick(15)
