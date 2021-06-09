from pygame.constants import USEREVENT
from functions import Disk_BF, CLU_BF, TRON_BF, score
import pygame
import sys

PageTitle = "Final Boss" # Titulo da pagina
screen_size = (800,800)
###########################
# # # # # # RGB # # # # # # 
###########################

BLACK = (0,0,0)
BLUE_MIDNIGHT = (0,0,30)
BLUE = (12,12,100)
BLUE_ICE = (0,255,251)
YELLOW_GOLD = (255,215,0)
WHITE = (255,255,255)

pygame.init() # inicia o pygame
surface =  pygame.display.set_mode(screen_size) #tamanho tela
pygame.display.set_caption(PageTitle) # titulo tela


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

############################
# Rotina principal do game #
############################
clock = pygame.time.Clock() #Fps
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

print(score_b,score_y)
