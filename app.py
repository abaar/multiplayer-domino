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
    titleText = pygame.font.Font("assets/8-BIT WONDER.TTF",45)
    textSurface = titleText.render("Dominomino",False,(0,0,0))

    quickText = pygame.font.Font("assets/8-BIT WONDER.TTF",20)
    quickSurface = quickText.render("Quick Search", False , (0,0,0))
    quickSurface_x = (display_width/2)-(quickSurface.get_width()/2)
    quickSurface_y = int(display_height/1.5)

    cusRoomtext = pygame.font.Font("assets/8-BIT WONDER.TTF",19)
    cusRomSurface = cusRoomtext.render("custom room",False, (0,0,0))
    cusRomSurface_x = (display_width/2)-(cusRomSurface.get_width()/2)
    cusRomSurface_y = int(display_height/1.3) 

    # dominoPict1 = pygame.image.load("assets/just-domino.png")
    # dominoPict1 = pygame.transform.scale(dominoPict1,(128,128))

    dominoPict2 = pygame.image.load("assets/domino-inline.jpg")
    dominoPict2 = pygame.transform.scale(dominoPict2,(305,143))

    while not intro:
        for event in pygame.event.get():
            if (event.type==pygame.QUIT):
                exitting_game()
        window.fill((255,255,255))
        window.blit(dominoPict2,(display_width/2 - dominoPict2.get_width()/2 ,int(display_height/3.2)))
        window.blit(textSurface,((display_width/2)-(textSurface.get_width()/2), int(display_height/6.2) ))
        window.blit(quickSurface,(quickSurface_x, quickSurface_y ))
        window.blit(cusRomSurface,(cusRomSurface_x, cusRomSurface_y))
        # window.blit(dominoPict1,(0,0))

        mouse = pygame.mouse.get_pos()
        print(mouse[0])
        if ( (mouse[0]< quickSurface_x + quickSurface.get_width() and mouse[0] > quickSurface_x) and \
            (mouse[1]>quickSurface_y and (mouse[1]< quickSurface_y+quickSurface.get_height()) )):
            quickSurface = quickText.render("Quick Search", False , (61, 73, 91))
        elif ( (mouse[0]<cusRomSurface_x + cusRomSurface.get_width() and mouse[0] > cusRomSurface_x)  and \
            (mouse[1]>cusRomSurface_y and mouse[1] < cusRomSurface_y + cusRomSurface.get_height() )):
            cusRomSurface = cusRoomtext.render("Custom Room", False, (61, 73, 91))
        else:
            quickSurface = quickText.render("Quick Search", False , (0, 0, 0))
            cusRomSurface = cusRoomtext.render("Custom Room", False, (0, 0, 0))
        pygame.display.update()


game_intro()
                

while not exit:
    for event in pygame.event.get():
        if (event.type == pygame.QUIT):
            exit=True
    pygame.display.update()
    clock.tick(30)

exitting_game()