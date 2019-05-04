import pygame

pygame.init()

display_width = 600
display_height = 600
window = pygame.display.set_mode((display_width,display_height))
window.fill((255,255,255))

clock = pygame.time.Clock()
exit = False

def exitting_game():
    print("do something here, e.g closing connection")
    pygame.quit()
    quit()

def text_objects(what,obj):
    textImage = font.render(text, False, colours.BLACK)

def game_intro():
    intro = False

    while not intro:
        for event in pygame.event.get():
            if (event.type==pygame.QUIT):
                exitting_game()
        
        titleText = pygame.font.Font("assets/8-BIT WONDER.TTF",45)
        textSurface = titleText.render("Dominomino",False,(0,0,0))
        window.fill((255,255,255))
        window.blit(textSurface,((display_width/2)-(textSurface.get_width()/2), int(display_height/5) ))

        pygame.display.update()


game_intro()
                

while not exit:
    for event in pygame.event.get():
        if (event.type == pygame.QUIT):
            exit=True
    pygame.display.update()
    clock.tick(60)

exitting_game()