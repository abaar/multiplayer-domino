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

def quick_loading():
    dominoPict2 = pygame.image.load("assets/domino-inline.jpg")
    dominoPict2 = pygame.transform.scale(dominoPict2,(305,143))

    qload = False
    # pygame
    loadingText = pygame.font.Font("assets/Pixel Emulator.otf",35)
    loadingSurface = loadingText.render("loading",False, (0,0,0))
    loadingSurface_x = (display_width/2) - (loadingSurface.get_width()/2)
    dots=0

    backText = pygame.font.Font("assets/Pixel Emulator.otf",25)
    backSurface = backText.render("back<",False,(0,0,0))

    playerText = pygame.font.Font("assets/Pixel Emulator.otf",20)
    playerSurface = playerText.render("2/4", False, (0,0,0))
    playerSurface_x = (display_width/2) - (playerSurface.get_width()/2)
    
    player_berubah = 0
    
    while not qload:
        for event in pygame.event.get():
            if(event.type==pygame.QUIT):
                exitting_game()

        mouse = pygame.mouse.get_pos()

        if(player_berubah):
            #do something when player changed here
            playerSurface = playerText.render("1/4", False, (0,0,0))          

        if(pygame.time.get_ticks()%500==0):
            if(dots==3):
                dots=0
                ltext = "loading"
            else:
                dots+=1
                if(dots==1):
                    ltext = "loading."
                elif(dots==2):
                    ltext = "loading.."
                elif(dots==3):
                    ltext = "loading..."

            loadingSurface = loadingText.render(ltext,False, (0,0,0))

        window.fill((255,255,255)) 
        window.blit(dominoPict2,(display_width/2 - dominoPict2.get_width()/2 ,int(display_height/3.5)))
        window.blit(loadingSurface,(loadingSurface_x,int(display_height/1.9)))
        window.blit(playerSurface,(playerSurface_x,int(display_height/1.7)))
        window.blit(backSurface,(5,0))
        if(mouse[0]>5 and mouse[0]<5+backSurface.get_width() and mouse[1]>0 and mouse[1]<backSurface.get_height()):
            backSurface = backText.render("back<",False,(61,73,91))
        else:
            backSurface = backText.render("back<",False,(0,0,0))
        pygame.display.update()

def game_intro():
    intro = False
    titleText = pygame.font.Font("assets/Pixel Emulator.otf",45)
    textSurface = titleText.render("Dominomino",False,(0,0,0))

    quickText = pygame.font.Font("assets/Pixel Emulator.otf",20)
    quickSurface = quickText.render("Quick Search", False , (0,0,0))
    quickSurface_x = (display_width/2)-(quickSurface.get_width()/2)
    quickSurface_y = int(display_height/1.5)

    cusRoomtext = pygame.font.Font("assets/Pixel Emulator.otf",19)
    cusRomSurface = cusRoomtext.render("custom room",False, (0,0,0))
    cusRomSurface_x = (display_width/2)-(cusRomSurface.get_width()/2)
    cusRomSurface_y = int(display_height/1.3) 

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


quick_loading()
                

while not exit:
    for event in pygame.event.get():
        if (event.type == pygame.QUIT):
            exit=True
    pygame.display.update()
    clock.tick(30)

exitting_game()