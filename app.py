import pygame
import pickle
import socket
import threading
import Queue

pygame.init()

display_width = 600
display_height = 600
window = pygame.display.set_mode((display_width,display_height))
window.fill((255,255,255))

clock = pygame.time.Clock()
exit = False

event_listened = Queue.Queue()
ipAddress = '127.0.0.1'
port = 5000
address = (ipAddress,port)
socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
player_name = None
mythread = None
stoptread = False

def chat_event_listener(useless,conn):
     while not stoptread:
        try:
            message = conn.recv(4096)
            message = pickle.loads(message)
            event_listened.put(message)   
        except:
            continue

def make_message(message_type,message_body,room_num=None):
    message = {}
    message["sender"] = player_name
    message["type"] = message_type
    message["body"] = message_body
    message["room_number"] = room_num
    return pickle.dumps(message)

def exitting_game(current_room_number=None):
    print("do something here, e.g closing connection")
    socket.send(make_message("exit","exit",room_num=current_room_number))
    pygame.quit()
    stoptread=True
    quit()

def game_start():
    print("halo")

def join_room():
    jroom = False
    backText = pygame.font.Font("assets/Pixel Emulator.otf",25)
    backSurface = backText.render("back<",False,(0,0,0))

    joinSurface = backText.render("Join",False,(0,0,0))
    joinSurface_x = display_width/2-joinSurface.get_width()/2
    joinSurface_y = display_height/2 - joinSurface.get_height()/2 + 50
    textText = pygame.font.Font("assets/Pixel Emulator.otf",55)
    text = ""
    text_len = len(text)
    numerics = ["1","2","3","4","5","6","7","8","9","0"]
    while not jroom:
        for event in pygame.event.get():
            if(event.type==pygame.QUIT):
                exitting_game()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    text = text[:-1]
                    text_len = len(text)
                elif(text_len<4 and event.unicode in numerics):
                    text += event.unicode
                    text_len = len(text)
        textSurface = textText.render(text,False,(0,0,0))            
        mouse = pygame.mouse.get_pos()
        clicked = pygame.mouse.get_pressed()
        window.fill((255,255,255)) 
        pygame.draw.rect(window,(0,0,0),(200,210,200,80),3)
        window.blit(textSurface,(215,215))
        window.blit(joinSurface,(joinSurface_x,joinSurface_y))

        if(mouse[0]>5 and mouse[0]<5+backSurface.get_width() and mouse[1]>0 and mouse[1]<backSurface.get_height()):
            backSurface = backText.render("back<",False,(61,73,91))
            if(clicked[0]):
                game_intro()
        elif(mouse[0]>joinSurface_x and mouse[0]<joinSurface_x+joinSurface.get_width() and mouse[1]>joinSurface_y and mouse[1]<joinSurface_y+joinSurface.get_height()):
            joinSurface = backText.render("Join",False,(61,73,91))
            if(clicked[0]):
                game_start()
        else:
            joinSurface = backText.render("Join",False,(0,0,0))
            backSurface = backText.render("back<",False,(0,0,0))
        window.blit(backSurface,(5,0))
        pygame.display.update()           

def quick_loading(current_total_players=None,room_number=None):
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
    playerSurface = playerText.render(current_total_players+"/4", False, (0,0,0))
    playerSurface_x = (display_width/2) - (playerSurface.get_width()/2)

    while not qload:
        if(not event_listened.empty()):
            message = event_listened.get()
            if(message['response']=="qroom_update_players"):
                current_total_players=message['body']
                playerSurface = playerText.render(current_total_players+"/4", False, (0,0,0))     
            elif(message['response']=="quit_succeed"):
                game_intro()
            elif(message['response']=="game_ready"):
                print("letsplay")                     
        for event in pygame.event.get():
            if(event.type==pygame.QUIT):
                exitting_game(current_room_number=room_number)
            elif(event.type==pygame.MOUSEBUTTONUP and event.button==1):
                if(mouse[0]>5 and mouse[0]<5+backSurface.get_width() and mouse[1]>0 and mouse[1]<backSurface.get_height()):
                    message=make_message("cmd","quit",room_num=room_number)
                    socket.send(message)
        mouse = pygame.mouse.get_pos()
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
    quickSurface_y = int(display_height/1.6)

    cusRoomtext = pygame.font.Font("assets/Pixel Emulator.otf",19)
    cusRomSurface = cusRoomtext.render("custom room",False, (0,0,0))
    cusRomSurface_x = (display_width/2)-(cusRomSurface.get_width()/2)
    cusRomSurface_y = int(display_height/1.4) 

    dominoPict2 = pygame.image.load("assets/domino-inline.jpg")
    dominoPict2 = pygame.transform.scale(dominoPict2,(305,143))

    joinRom = pygame.font.Font("assets/Pixel Emulator.otf",19)
    joinRomSurface = joinRom.render("Join A room",False,(0,0,0))
    joinRomSurface_x = (display_width/2) - (joinRomSurface.get_width()/2)
    joinRomSurface_y = int(display_height/1.25)
    while not intro:
        if(not event_listened.empty()):
            message = event_listened.get()
            if(message['response']=="quick_room_joined"):
                quick_loading(current_total_players=str(message['body']),room_number=message['room_number'])

        for event in pygame.event.get():
            if (event.type==pygame.QUIT):
                exitting_game()
            elif(event.type==pygame.MOUSEBUTTONUP and event.button == 1):
                if ( (mouse[0]< quickSurface_x + quickSurface.get_width() and mouse[0] > quickSurface_x) and \
                    (mouse[1]>quickSurface_y and (mouse[1]< quickSurface_y+quickSurface.get_height()) )):
                    message=make_message("cmd","quick_room")
                    socket.send(message)
                elif ( (mouse[0]<cusRomSurface_x + cusRomSurface.get_width() and mouse[0] > cusRomSurface_x)  and \
                    (mouse[1]>cusRomSurface_y and mouse[1] < cusRomSurface_y + cusRomSurface.get_height() )):
                    intro = custom_room()
                elif ( mouse[0]<joinRomSurface_x + joinRomSurface.get_width() and mouse[0]>joinRomSurface_x and \
                    mouse[1]<joinRomSurface_y+joinRomSurface.get_height() and mouse[1]>joinRomSurface_y):
                    intro = join_room()

        window.fill((255,255,255))
        window.blit(dominoPict2,(display_width/2 - dominoPict2.get_width()/2 ,int(display_height/3.5)))
        window.blit(textSurface,((display_width/2)-(textSurface.get_width()/2), int(display_height/6.2) ))
        window.blit(quickSurface,(quickSurface_x, quickSurface_y ))
        window.blit(cusRomSurface,(cusRomSurface_x, cusRomSurface_y))
        window.blit(joinRomSurface,(joinRomSurface_x,int(display_height/1.25)))

        mouse = pygame.mouse.get_pos()
        clicked = pygame.mouse.get_pressed()
        if ( (mouse[0]< quickSurface_x + quickSurface.get_width() and mouse[0] > quickSurface_x) and \
            (mouse[1]>quickSurface_y and (mouse[1]< quickSurface_y+quickSurface.get_height()) )):
            quickSurface = quickText.render("Quick Search", False , (61, 73, 91))
        elif ( (mouse[0]<cusRomSurface_x + cusRomSurface.get_width() and mouse[0] > cusRomSurface_x)  and \
            (mouse[1]>cusRomSurface_y and mouse[1] < cusRomSurface_y + cusRomSurface.get_height() )):
            cusRomSurface = cusRoomtext.render("Custom Room", False, (61, 73, 91))
        elif ( mouse[0]<joinRomSurface_x + joinRomSurface.get_width() and mouse[0]>joinRomSurface_x and \
            mouse[1]<joinRomSurface_y+joinRomSurface.get_height() and mouse[1]>joinRomSurface_y):
            joinRomSurface = joinRom.render("Join a Room",False,(61,83,91))
        else:
            joinRomSurface = joinRom.render("Join a Room",False,(0,0,0))
            quickSurface = quickText.render("Quick Search", False , (0, 0, 0))
            cusRomSurface = cusRoomtext.render("Custom Room", False, (0, 0, 0))
        pygame.display.update()


def custom_room():
    lobi = False
    backText = pygame.font.Font("assets/Pixel Emulator.otf",25)
    backSurface = backText.render("back<",False,(0,0,0))

    idText = pygame.font.Font("assets/Pixel Emulator.otf",25)
    idSurface = idText.render("Room ID : 12345",False,(0,0,0))

    startText = pygame.font.Font("assets/Pixel Emulator.otf",25)
    startSurface = startText.render("Start",False,(0,0,0))

    you1 = pygame.font.Font("assets/Pixel Emulator.otf",20)
    youSurface = you1.render("You",False,(0,0,0))
    p1Img = pygame.image.load("assets/player1.jpg")
    
    player2Text = pygame.font.Font("assets/Pixel Emulator.otf",17)
    player2Surface = player2Text.render("Player 2",False,(0,0,0))
    player2ready = player2Text.render("Ready",False,(0,0,0))
    p2Img = pygame.image.load("assets/player2.jpg")

    player1Text = pygame.font.Font("assets/Pixel Emulator.otf",17)
    player1Surface = player1Text.render("Player 1",False,(0,0,0))
    player1ready = player1Text.render("Ready",False,(0,0,0))
    p4Img = pygame.image.load("assets/player4.jpg")

    player3Text = pygame.font.Font("assets/Pixel Emulator.otf",17)
    player3Surface = player3Text.render("Player 3",False,(0,0,0))
    player3ready = player3Text.render("Ready",False,(0,0,0))
    p3Img = pygame.image.load("assets/player3.jpg")
    while not lobi:
        for event in pygame.event.get():
            if(event.type==pygame.QUIT):
                exitting_game()
        window.fill((255,255,255))
        window.blit(backSurface,(5,0))

        window.blit(player1Surface,(102,125))
        pygame.draw.rect(window,(0,0,0),(110,150,80,100),3)
        window.blit(player1ready,(118,250))
        window.blit(p4Img,(118,155))

        window.blit(idSurface,(display_width/2-idSurface.get_width()/2,80))
        window.blit(player2Surface,(252,125))
        pygame.draw.rect(window,(0,0,0),(260,150,80,100),3)

        window.blit(player3Surface,(402,125))
        pygame.draw.rect(window,(0,0,0),(410,150,80,100),3)
        window.blit(player3ready,(418,250))
        window.blit(p3Img,(418,155))

        window.blit(p1Img,(268,355))
        window.blit(youSurface,(277,325))
        pygame.draw.rect(window,(0,0,0),(260,350,80,100),3)
        window.blit(startSurface,(258,455))

        mouse = pygame.mouse.get_pos()
        clicked = pygame.mouse.get_pressed()
        if(mouse[0]>5 and mouse[0]<5+backSurface.get_width() and mouse[1]>0 and mouse[1]<backSurface.get_height()):
            backSurface = backText.render("back<",False,(61,73,91))
            if(clicked[0]):
                game_intro()
        elif(mouse[0]>258 and mouse[0]<258+startSurface.get_width() and mouse[1]>455 and mouse[1]<455+startSurface.get_height()):
            startSurface = startText.render("Start",False,(61,73,91))
        else:
            startSurface = startText.render("Start",False,(0,0,0))
            backSurface = backText.render("back<",False,(0,0,0))
        pygame.display.update()       
    
                
if __name__ == '__main__':
    socket.connect(address)
    message = socket.recv(4096)
    message = pickle.loads(message)
    if message["sender"] == "admin" and message.get("player_name",False) != False:
        player_name = message["player_name"]  
    mythread=threading.Thread(target=chat_event_listener,args=(address,socket))
    mythread.start()  

    game_intro()