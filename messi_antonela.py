import pygame
import sys
import random

############################################################
##### Este juego fue creado por Sandreke (@sandreke99) #####
############################################################

# Inicializar Pygame
pygame.init()

# Configuración de la pantalla
width, height = 700, 650  
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("TK GAME🎮")

# Cargar imágenes y escalarlas
player_image = pygame.image.load("imgs/messi.png")
player_image = pygame.transform.scale(player_image, (60, 60))

bullet_image = pygame.image.load("imgs/corazón.png")
bullet_image = pygame.transform.scale(bullet_image, (50, 50))   

enemy_image = pygame.image.load("imgs/antonela.png")
enemy_image = pygame.transform.scale(enemy_image, (60, 60))

background_image = pygame.image.load("imgs/fondo_amor.jpg")
background_image = pygame.transform.scale(background_image,
                                          (width, height))

# Jugador
player_rect = player_image.get_rect()
player_rect.topleft = (width // 2 - player_rect.width // 2,
                       height - player_rect.height - 10)
player_speed = 15

# Bala
bullet_rect = bullet_image.get_rect()
bullet_speed = 10
bullets = []

# Enemigo
enemy_rect = enemy_image.get_rect()
enemy_speed = 5
enemies = []

# Puntaje
score = 0
winning_score = 3

# Reloj
clock = pygame.time.Clock()

# Mantener registro de teclas presionadas
keys_pressed = {'left': False, 'right': False}

# Función para mostrar la pantalla de bienvenida
def show_welcome_screen():
    welcome_font = pygame.font.Font(None, 74)
    welcome_text = welcome_font.render("Bienvenido!", True, (255, 255, 255))
    play_font = pygame.font.Font(None, 50)
    play_text = play_font.render("Ingresa la clave secreta", True, (255, 255, 255))
    secret_key = "amor"
    user_input = ""

    while True: 
        screen.blit(background_image, (0, 0))
        screen.blit(welcome_text, (width // 2 - welcome_text.get_width() // 2, height // 3))
        screen.blit(play_text, (width // 2 - play_text.get_width() // 2, height // 2))

        input_font = pygame.font.Font(None, 50)
        hidden_input = '*' * len(user_input)
        input_text = input_font.render(hidden_input, True, (255, 255, 255))
        screen.blit(input_text, (width // 2 - input_text.get_width() // 2, height // 2 + 50))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if user_input == secret_key:
                        return
                    else:
                        user_input = ""
                elif event.key == pygame.K_BACKSPACE:
                    user_input = user_input[:-1]
                else:
                    user_input += event.unicode

        pygame.display.flip()
        clock.tick(30)

# Función para mostrar la pantalla de victoria
def show_winning_screen():
    winning_font = pygame.font.Font(None, 74)
    winning_text = winning_font.render("¡Ganaste!", True, (255, 255, 255))
    play_again_font = pygame.font.Font(None, 50)
    play_again_text = play_again_font.render("Presiona R para reiniciar", True, (255, 255, 255))

    while True:
        screen.blit(background_image, (0, 0))
        screen.blit(winning_text, (width // 2 - winning_text.get_width() // 2, height // 3))
        screen.blit(play_again_text, (width // 2 - play_again_text.get_width() // 2, height // 2))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                return

        pygame.display.flip()
        clock.tick(30)

# Mostrar la pantalla de bienvenida antes de iniciar el juego
show_welcome_screen()

# Bucle principal del juego
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Manejar movimientos del jugador
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                keys_pressed['left'] = True
            elif event.key == pygame.K_RIGHT:
                keys_pressed['right'] = True
            elif event.key == pygame.K_SPACE:
                bullet_rect = bullet_image.get_rect()
                bullet = {
                    'rect': pygame.Rect(
                        player_rect.x +
                        player_rect.width//2 -
                        bullet_rect.width//2,
                        player_rect.y,
                        bullet_rect.width,
                        bullet_rect.height 
                    ),
                    'image': bullet_image
                }
                bullets.append(bullet)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                keys_pressed['left'] = False
            elif event.key == pygame.K_RIGHT:
                keys_pressed['right'] = False

    # Actualizar posición del jugador
    if keys_pressed['left'] and player_rect.left > 0:
        player_rect.x -= player_speed
    if keys_pressed['right'] and player_rect.right < width:
        player_rect.x += player_speed

    # Actualizar posición de las balas
    for bullet in bullets:
        bullet['rect'].y -= bullet_speed

    # Generar enemigos aleatorios
    if random.randint(0, 100) < 5:
        enemy_rect = enemy_image.get_rect()
        enemy_rect.x = random.randint(0,
                                    width - enemy_rect.width)
        enemies.append(enemy_rect.copy())

    # Actualizar posición de los enemigos
    for enemy in enemies:
        enemy.y += enemy_speed

    # Colisiones entre balas y enemigos
    for bullet in bullets:
        for enemy in enemies:
            if enemy.colliderect(bullet['rect']):
                bullets.remove(bullet)
                enemies.remove(enemy)
                score += 1
                if score >= winning_score:
                    show_winning_screen()
                    score = 0
                    bullets.clear()
                    enemies.clear()
                    show_welcome_screen()

    # Colisiones entre jugador y enemigos
    for enemy in enemies:
        if player_rect.colliderect(enemy):
            pygame.quit()
            sys.exit()

    # Limpiar la pantalla con el fondo
    screen.blit(background_image, (0, 0))

    # Dibujar al jugador
    screen.blit(player_image, player_rect)

    # Dibujar las balas
    for bullet in bullets:
        screen.blit(bullet['image'], bullet['rect'].topleft)

    # Dibujar los enemigos
    for enemy in enemies:
        screen.blit(enemy_image, enemy)

    # Dibujar el puntaje
    score_font = pygame.font.Font(None, 36)
    score_text = score_font.render(f"Puntaje: {score}", True, (255, 255, 255))
    screen.blit(score_text, (10, 10))

    # Actualizar la pantalla
    pygame.display.flip()

    # Establecer límite de FPS
    clock.tick(30)
