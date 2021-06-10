"""
Programa do mini-game_state de Motos
Autor: Enricco Gemha
Data: 18/05/2021
"""

import random
import sys
import pygame
from functions import yellowLightCicle, blueLightCicle, tutorial_screen, score, Disk, Player, Disk_BF, CLU_BF, TRON_BF


# Algumas variáveis essenciais para a aplicação
screen_size = (800,800) # Largura e altura da tela
pygame.init()  # inicializa as rotinas do PyGame
clock = pygame.time.Clock()


# Define o código RGB das cores utilizadas
BLACK = (0,0,0)
BLUE_MIDNIGHT = (0,0,30)
BLUE = (12,12,100)
BLUE_ICE = (0,255,251)
YELLOW_GOLD = (255,215,0)
WHITE = (255,255,255)

b_score = 0
y_score = 0

time = clock.tick(60) # segura a taxa de quadros em 60 por segundo
pygame.display.set_caption("TRON vs CLU") # título da surface do jogo
surface = pygame.display.set_mode(screen_size) # cria a tela do jogo com tamanho personalizado

initial_screen = True
i=0
while initial_screen:
    if i % 2 == 0:  # gera um efeito de letreiro piscante "aleatório"
        surface.blit(pygame.image.load('SOLID GAME SCREEN/game_front_page.jpeg'),(0,0))
    else:
        surface.blit(pygame.image.load('SOLID GAME SCREEN/game_insert_coin.png'),(0,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            pygame.quit()
            sys.exit()
        if event.type==pygame.KEYDOWN:
            initial_screen = False
    pygame.display.update()
    i+=1

choose_screen = True
while choose_screen:
    surface.blit(pygame.image.load('SOLID GAME SCREEN/selection_screen.jpeg'),(0,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            pygame.quit()
            sys.exit()
        if event.type==pygame.KEYDOWN:
            if event.key == pygame.K_1:
                game_access = "fastest_disc"
                choose_screen = False
            if event.key == pygame.K_2:
                game_access = "disc_wars"
                choose_screen = False
            if event.key == pygame.K_3:
                game_access = "lightcicle_run"
                choose_screen = False
    pygame.display.update()

# Rotinas de aúdio
pygame.mixer.music.load('AUDIO/DerezzedSong.ogg')
pygame.mixer.music.set_volume(0.04)
pygame.mixer.music.play(-1)


while game_access == "disc_wars":
    screen_size = (800,800) # Largura e altura da tela
    page_title = "Disc Wars" # Define o nome desta página
    surface = pygame.display.set_mode(screen_size) # cria a tela do jogo com tamanho personalizado
    pygame.display.set_caption(page_title) # título da janela do jogo

    # variável que declara o clock do jogo
    clock = pygame.time.Clock()

    # cria sprite dos Paddles
    sprites = pygame.sprite.Group()
    yellow = Player(sprites, "yellow")
    blue = Player(sprites, "blue")

    # Variáveis para regular processos
    b_disk_alive = False
    y_disk_alive = False
    pressed_blue = False
    pressed_yellow = False
    y_score = 0
    b_score = 0
    angle_index = 0
    sub_angle_index = 0
    v=0.2
    angle_list_1 = [(v,-v), (v,-v/2), (v,0), (v,v/2), (v,v)]
    angle_list_2 = [(-v,-v), (-v,-v/2), (-v,0), (-v,v/2), (-v,v)]


    while True:
        time = clock.tick(60) # segura a taxa de quadros em 60 por segundo
        surface.blit(pygame.image.load('SPRITES_BOSS/wallpaper_disc_wars.png').convert_alpha(), (0,0))
        pygame.draw.line(surface, BLUE_ICE, (400,60), (400,800), 5)
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type in (pygame.KEYDOWN, pygame.KEYUP):
                blue.game_controls(event)
                yellow.game_controls(event)
                if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_e and not pressed_blue and b_disk_alive != True:
                            pressed_blue = True
                        elif event.key == pygame.K_e and pressed_blue == True and b_disk_alive != True:
                            rect_b = blue.rect.midright
                            b_disk = Disk(sprites, 'blue', rect_b, angle_index)
                            b_disk_alive = True
                            pressed_blue = False
                        if event.key == pygame.K_RETURN and not pressed_yellow and y_disk_alive != True:
                            pressed_yellow = True
                        
                        elif event.key == pygame.K_RETURN and pressed_yellow == True and y_disk_alive != True:
                            rect_y = yellow.rect.midleft
                            y_disk = Disk(sprites, 'yellow', rect_y, angle_index)
                            y_disk_alive = True
                            pressed_yellow = False

                            
        if pressed_blue == True and b_disk_alive != True:
            v_15 = [int(angle_list_1[angle_index][0]*200), int(angle_list_1[angle_index][1]*200)]
            end_pos = ((list(blue.rect.center)[0] + v_15[0]),(list(blue.rect.center)[1] + v_15[1]))
            pygame.draw.line(surface, WHITE, blue.rect.center, end_pos, 5)

        if pressed_yellow == True and y_disk_alive != True:
            v_15_ = [int(angle_list_2[angle_index][0]*200), int(angle_list_2[angle_index][1]*200)]
            end_pos1 = ((list(yellow.rect.center)[0] + v_15_[0]),(list(yellow.rect.center)[1] + v_15_[1]))
            pygame.draw.line(surface, WHITE, yellow.rect.center, end_pos1, 5)

        sub_angle_index += 1
        if sub_angle_index == 12:
            sub_angle_index = 0
            angle_index += 1
        if angle_index > 4:
            angle_index = 0

        blue.update()
        yellow.update()

        if y_disk_alive == True:
            y_disk.update(time)
            if pygame.sprite.collide_mask(yellow,y_disk) != None:
                y_disk.kill()
                y_disk_alive = False    
            if pygame.sprite.collide_mask(blue,y_disk) != None:
                y_score += 1
                blue.kill()
                blue = Player(sprites, "blue")
        if b_disk_alive == True:
            b_disk.update(time)
            if pygame.sprite.collide_mask(blue,b_disk) != None:
                b_disk.kill()
                b_disk_alive = False
            if pygame.sprite.collide_mask(yellow,b_disk) != None:
                b_score += 1
                yellow.kill()
                yellow = Player(sprites, "yellow")

        sprites.draw(surface)
        score(y_score, b_score, surface)
        pygame.display.update()



# Breve tutorial de instruções deste modo de jogo
tutorial_screen(surface)

while game_access == "lightcicle_run":
    screen_size = (800,800) # Largura e altura da tela
    page_title = "Lightcicle Chase" # Define o nome desta página
    surface = pygame.display.set_mode(screen_size) # cria a tela do jogo com tamanho personalizado
    pygame.display.set_caption(page_title) # título da janela do jogo

    # variável que declara o clock do jogo
    clock = pygame.time.Clock()
    
    # cria sprite das Motos
    sprites = pygame.sprite.Group()
    yellow = yellowLightCicle(sprites)
    blue = blueLightCicle(sprites)

    # Variáveis para regular processos
    stop_sound = True
    game_state = "RUNNING"
    game = True

    # Início do Loop da corrida de moto
    while game:
        time = clock.tick(60) # segura a taxa de quadros em 60 por segundo
        # Adquire todos os eventos e os testa para casos desejados
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE): # quebra o loop
                    pygame.quit()
                    sys.exit()
            if event.type == pygame.KEYDOWN: 
                
                if event.key == pygame.K_LEFT:
                    blue.update_direction("LEFT")
                elif event.key == pygame.K_RIGHT:
                    blue.update_direction("RIGHT")
                elif event.key == pygame.K_DOWN:
                    blue.update_direction("UP")
                elif event.key == pygame.K_UP:
                    blue.update_direction("DOWN")
                elif event.key == pygame.K_SPACE:
                    blue.slow_down()
                
                elif event.key == pygame.K_a:
                    yellow.update_direction("LEFT")
                elif event.key == pygame.K_d:
                    yellow.update_direction("RIGHT")
                elif event.key == pygame.K_s:
                    yellow.update_direction("UP")
                elif event.key == pygame.K_w:
                    yellow.update_direction("DOWN")
                elif event.key == pygame.K_RETURN:
                    yellow.slow_down()

                elif event.key == pygame.K_p:
                    if game_state != "PAUSED":
                        pygame.mixer.music.pause()
                        surface.blit(pygame.image.load('SOLID GAME SCREEN/pause_menu_screen.jpeg').convert_alpha(),(0,0))
                        game_state = "PAUSED"
                    else:
                        pygame.mixer.music.unpause()
                        game_state = "RUNNING"

        if game_state == "PAUSED":
            pygame.display.flip()
            continue

        # Desenha o Background
        surface.fill(BLUE)
        thickness = 10
        distance = screen_size[0]/8 # espaço entre cada quadrado
        i = 0
        while i < 9:
            pygame.draw.line(surface, BLUE_MIDNIGHT, (0,(i*distance)), (screen_size[0],(i*distance)), thickness) # Desenha linha horizontal
            pygame.draw.line(surface, BLUE_MIDNIGHT, ((i*distance),0), ((i*distance),screen_size[0]), thickness) # Desenha linha vertical
            i+=1

        # Desenha o rastro, que cessa quando há uma explosão
        if yellow.explode == False and blue.explode == False:
            i = 0
            if len(blue.trace) >= 2:
                while i < len(blue.trace):
                    pygame.draw.circle(surface, BLUE_ICE, blue.trace[i], 6)
                    i+=1
            i = 0
            if len(yellow.trace) >= 2:
                while i < len(yellow.trace):
                    pygame.draw.circle(surface, YELLOW_GOLD, yellow.trace[i], 6)
                    i+=1
                
        sprites.draw(surface) # desenha as sprites

        # Atualiza a posição da moto e rastro
        yellow.update(time)
        blue.update(time)

        # Verifica se houve colisão
        if yellow.explode:
            b_score += 1
            game = False
        if blue.explode:
            y_score += 1
            game = False
        for t in blue.trace:
            if yellow.rect.collidepoint(t):
                derezzed_visual = pygame.image.load('SPRITES/VFX DEREZZED EXPLOSION.png').convert_alpha()
                derezzed_visual = pygame.transform.scale(derezzed_visual, (80, 80))
                surface.blit(derezzed_visual, yellow.rect.center)
                yellow.kill()
                b_score += 1
                game = False
                break
        for t in yellow.trace:
            if blue.rect.collidepoint(t):
                derezzed_visual = pygame.image.load('SPRITES/VFX DEREZZED EXPLOSION.png').convert_alpha()
                derezzed_visual = pygame.transform.scale(derezzed_visual, (80, 80))
                surface.blit(derezzed_visual, blue.rect.center)
                blue.kill()
                y_score += 1
                game = False
                break
        if pygame.sprite.collide_mask(blue,yellow) != None:
            yellow.kill()
            blue.kill()
            game = False

        if (b_score == False or y_score == False) and stop_sound == True:
            derezzed_sound = pygame.mixer.Sound('AUDIO/DerezzedFX.ogg')
            derezzed_sound.set_volume(0.08)
            derezzed_sound.play()
            stop_sound = False

        score(y_score, b_score, surface)

        pygame.display.update() # atualiza o display
    
    while game_access == "fastest_disc":
        PageTitle = "The Fastest Disc in the Grid" # Titulo da pagina
        screen_size = (800,800)
        surface = pygame.display.set_mode(screen_size) # cria a tela do jogo com tamanho personalizado
        pygame.display.set_caption(PageTitle) # título da janela do jogo


        sprites = pygame.sprite.Group()
        ydisks = pygame.sprite.Group()
        clu = CLU_BF(sprites)
        tron = TRON_BF(sprites)
        can_y_launch = True
        can_b_launch = True
        disk_y_n = 0
        disk_b_n = 0
        tron_died = False
        clu_died = False
        score_y = 0
        score_b = 0

        ADD_YDISK = pygame.USEREVENT + 1
        pygame.time.set_timer(ADD_YDISK, 1000)
        ADD_BDISK = pygame.USEREVENT
        pygame.time.set_timer(ADD_BDISK, 3000)


        clock = pygame.time.Clock()

        while True:    #True
            Time = clock.tick(60) # segura a taxa de quadros em 60 por segundo
            # Adquire todos os eventos e os testa para casos desejados
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE): # quebra o loop
                        pygame.quit()
                        sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_s:
                        tron.duck()
                    if event.key == pygame.K_w:
                        tron.jump()
                    if event.key == pygame.K_d and can_b_launch:
                        can_b_launch = False
                        disk_b = Disk_BF(sprites, "blue", (170,568))
                        disk_b_n += 1
                    if event.key == pygame.K_i and can_y_launch:
                        can_y_launch = False
                        disk_y = Disk_BF(sprites, "yellow", (580,538))
                        ydisks.add(disk_y)
                        disk_y_n += 1
                    if event.key == pygame.K_k and can_y_launch:
                        can_y_launch = False
                        disk_y = Disk_BF(sprites, "yellow", (580,568))
                        ydisks.add(disk_y)
                        disk_y_n += 1
                    if event.key == pygame.K_m and can_y_launch:
                        can_y_launch = False
                        disk_y = Disk_BF(sprites, "yellow", (580,598))
                        ydisks.add(disk_y)
                        disk_y_n += 1
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_s:
                        tron.stand()
                if event.type == ADD_BDISK:
                    can_b_launch = True
                if event.type == ADD_YDISK:
                    can_y_launch = True

            surface.blit(pygame.image.load('SPRITES_BOSS/wallpaper_boss_fight.jpg').convert_alpha(), (0,0))

            score(score_y, score_b, surface)
            tron.update(Time)
            sprites.draw(surface)
            
            if disk_b_n != 0 and disk_y_n != 0: # Se a contagem for 0, não faz sentido verificar a colisãom
                if pygame.sprite.collide_mask(disk_b,disk_y) != None:
                    disk_b.kill()
                    disk_b_n -= 1
                    disk_y.kill()
                    disk_y_n -= 1

            if disk_y_n != 0:
                ydisks.update(Time)
                if disk_y.rect.x == 0:
                    disk_y.kill()
                    disk_y_n -= 1
                for disky in ydisks.sprites():
                    if pygame.sprite.collide_mask(tron,disky) != None:
                        tron.kill()
                        tron_died = True
            if disk_b_n != 0:
                disk_b.update(Time)
                if disk_b.rect.x == 800:
                    disk_b.kill()
                    disk_b_n -= 1
                if pygame.sprite.collide_mask(clu,disk_b) != None:
                    print(pygame.sprite.collide_mask(clu,disk_b))
                    clu.kill()
                    clu_died = True

            if clu_died:
                score_b += 1
                break
            if tron_died:
                score_y += 1
                break

            pygame.display.update()