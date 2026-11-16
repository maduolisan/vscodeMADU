import pygame
import random
import sys

# Inicializa o Pygame
pygame.init()

# Configurações da tela
LARGURA, ALTURA = 800, 600
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Invasão Espacial")

# Cores (RGB)
PRETO = (10, 10, 15)
AZUL_CLARO = (52, 152, 219)
VERMELHO = (231, 76, 60)
AMARELO = (241, 196, 15)
BRANCO = (255, 255, 255)

# Configurações da Nave do Jogador
jogador_largura, jogador_altura = 50, 40
jogador_x = LARGURA // 2 - jogador_largura // 2
jogador_y = ALTURA - 70
jogador_velocidade = 8
vidas = 3

# Configurações dos Tiros
tiro_largura, tiro_altura = 5, 15
tiro_velocidade = 10
lista_tiros = []

# Configurações dos Inimigos
inimigo_largura, inimigo_altura = 45, 45
lista_inimigos = []

def criar_inimigo():
    x = random.randint(0, LARGURA - inimigo_largura)
    y = random.randint(-150, -50)
    velocidade = random.randint(3, 7)
    return {"rect": pygame.Rect(x, y, inimigo_largura, inimigo_altura), "vel": velocidade}

# Criar inimigos iniciais
for _ in range(6):
    lista_inimigos.append(criar_inimigo())

# Pontuação e Relógio
pontos = 0
relogio = pygame.time.Clock()
fonte = pygame.font.SysFont("arial", 26, bold=True)
fonte_game_over = pygame.font.SysFont("arial", 50, bold=True)

# Loop Principal do Jogo
jogando = True
while jogando:
    tela.fill(PRETO)
    
    # 1. Captura de Eventos
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            
        elif evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_SPACE:
                # Cria um tiro saindo do centro da nave do jogador
                tiro_x = jogador_x + jogador_largura // 2 - tiro_largura // 2
                tiro_y = jogador_y
                lista_tiros.append(pygame.Rect(tiro_x, tiro_y, tiro_largura, tiro_altura))

    # 2. Movimentação do Jogador
    teclas = pygame.key.get_pressed()
    if teclas[pygame.K_LEFT] and jogador_x > 0:
        jogador_x -= jogador_velocidade
    if teclas[pygame.K_RIGHT] and jogador_x < LARGURA - jogador_largura:
        jogador_x += jogador_velocidade
    if teclas[pygame.K_UP] and jogador_y > 300: # Limita para não subir demais
        jogador_y -= jogador_velocidade
    if teclas[pygame.K_DOWN] and jogador_y < ALTURA - jogador_altura - 10:
        jogador_y += jogador_velocidade

    # 3. Movimentação dos Tiros
    for tiro in lista_tiros[:]:
        tiro.y -= tiro_velocidade
        if tiro.y < 0:
            lista_tiros.remove(tiro)

    # 4. Movimentação dos Inimigos
    for inimigo in lista_inimigos:
        inimigo["rect"].y += inimigo["vel"]
        
        # Se o inimigo passar direto pela tela, reseta ele no topo e o jogador perde 1 vida
        if inimigo["rect"].y > ALTURA:
            inimigo["rect"].x = random.randint(0, LARGURA - inimigo_largura)
            inimigo["rect"].y = random.randint(-100, -40)
            inimigo["vel"] = random.randint(3, 7)
            vidas -= 1

    # 5. Detecção de Colisões
    rect_jogador = pygame.Rect(jogador_x, jogador_y, jogador_largura, jogador_altura)
    
    for inimigo in lista_inimigos[:]:
        # Colisão: Tiro acertou Inimigo
        for tiro in lista_tiros[:]:
            if inimigo["rect"].colliderect(tiro):
                if tiro in lista_tiros:
                    lista_tiros.remove(tiro)
                # Reseta o inimigo destruído
                inimigo["rect"].x = random.randint(0, LARGURA - inimigo_largura)
                inimigo["rect"].y = random.randint(-150, -50)
                inimigo["vel"] = random.randint(3, 7)
                pontos += 10
                break
        
        # Colisão: Inimigo bateu na Nave do Jogador
        if inimigo["rect"].colliderect(rect_jogador):
            inimigo["rect"].x = random.randint(0, LARGURA - inimigo_largura)
            inimigo["rect"].y = random.randint(-150, -50)
            vidas -= 1

    # 6. Condição de Game Over
    if vidas <= 0:
        jogando = False

    # 7. Desenhar Elementos na Tela
    # Desenha o Jogador (Triângulo/Nave estilizada usando retângulos)
    pygame.draw.rect(tela, AZUL_CLARO, (jogador_x, jogador_y, jogador_largura, jogador_altura), border_radius=5)
    pygame.draw.rect(tela, BRANCO, (jogador_x + 15, jogador_y - 10, 20, 10)) # Bico da nave
    
    # Desenha os Tiros
    for tiro in lista_tiros:
        pygame.draw.rect(tela, AMARELO, tiro)
        
    # Desenha os Inimigos
    for inimigo in lista_inimigos:
        pygame.draw.rect(tela, VERMELHO, inimigo["rect"], border_radius=3)

    # Desenha a Interface (Pontos e Vidas)
    texto_pontos = fonte.render(f"Pontos: {pontos}", True, BRANCO)
    texto_vidas = fonte.render(f"Vidas: {'❤️ ' * vidas}", True, VERMELHO)
    tela.blit(texto_pontos, (10, 10))
    tela.blit(texto_vidas, (LARGURA - 150, 10))

    pygame.display.flip()
    relogio.tick(60)

# Tela de Game Over fora do loop principal
while True:
    tela.fill(PRETO)
    texto_game_over = fonte_game_over.render("GAME OVER", True, VERMELHO)
    texto_final = fonte.render(f"Pontuação Final: {pontos}", True, BRANCO)
    texto_sair = fonte.render("Feche a janela para sair", True, BRANCO)
    
    tela.blit(texto_game_over, (LARGURA // 2 - 140, ALTURA // 2 - 60))
    tela.blit(texto_final, (LARGURA // 2 - 100, ALTURA // 2 + 10))
    tela.blit(texto_sair, (LARGURA // 2 - 120, ALTURA // 2 + 60))
    
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            
    pygame.display.flip()
