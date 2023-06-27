import pygame

pygame.init()

font = pygame.font.Font("freesansbold.ttf", 20)
fonts=pygame.font.Font("freesansbold.ttf", 32)
screen = pygame.display.set_mode([900, 950])

def draw_misc():
    background_image = pygame.image.load("assets/extraimage/hii.jpg")
    screen.blit(background_image, (-450, 0))

    rect_surface = pygame.Surface((760, 260), pygame.SRCALPHA)
    rect_alpha = 128
    rect_color = (100, 100, 100, rect_alpha)
    pygame.draw.rect(rect_surface, rect_color, rect_surface.get_rect(), 0, 10)
    screen.blit(rect_surface, (70, 220))

    start_game_text = fonts.render('"Pac Man is back!"', True, 'red')
    screen.blit(start_game_text, (200, 300))
    start_game_text = fonts.render('"Now you are Two!"', True, 'white')
    screen.blit(start_game_text, (300, 350))

    start_game_text = font.render('Space Bar to Start', True, 'white')
    screen.blit(start_game_text, (350, 450))

def start():
    run = True
    while run:
        draw_misc()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    run = False
                    break

        pygame.display.flip()

    pygame.quit()
start()