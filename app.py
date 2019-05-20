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
domino_tiles = {}
domino_tiles['00']=pygame.image.load("assets/domino-tiles/0-0-copy.png")
domino_tiles['01']=pygame.image.load("assets/domino-tiles/0-1.png")
domino_tiles['02']=pygame.image.load("assets/domino-tiles/0-2.png")
domino_tiles['03']=pygame.image.load("assets/domino-tiles/0-3.png")
domino_tiles['04']=pygame.image.load("assets/domino-tiles/0-4.png")
domino_tiles['05']=pygame.image.load("assets/domino-tiles/0-5.png")
domino_tiles['06']=pygame.image.load("assets/domino-tiles/0-6.png")
domino_tiles['11']=pygame.image.load("assets/domino-tiles/1-1.png")
domino_tiles['12']=pygame.image.load("assets/domino-tiles/1-2.png")
domino_tiles['13']=pygame.image.load("assets/domino-tiles/1-3.png")
domino_tiles['14']=pygame.image.load("assets/domino-tiles/1-4.png")
domino_tiles['15']=pygame.image.load("assets/domino-tiles/1-5.png")
domino_tiles['16']=pygame.image.load("assets/domino-tiles/1-6.png")
domino_tiles['22']=pygame.image.load("assets/domino-tiles/2-2.png")
domino_tiles['23']=pygame.image.load("assets/domino-tiles/2-3.png")
domino_tiles['24']=pygame.image.load("assets/domino-tiles/2-4.png")
domino_tiles['25']=pygame.image.load("assets/domino-tiles/2-5.png")
domino_tiles['26']=pygame.image.load("assets/domino-tiles/2-6.png")
domino_tiles['33']=pygame.image.load("assets/domino-tiles/3-3.png")
domino_tiles['34']=pygame.image.load("assets/domino-tiles/3-4.png")
domino_tiles['35']=pygame.image.load("assets/domino-tiles/3-5.png")
domino_tiles['36']=pygame.image.load("assets/domino-tiles/3-6.png")
domino_tiles['44']=pygame.image.load("assets/domino-tiles/4-4.png")
domino_tiles['45']=pygame.image.load("assets/domino-tiles/4-5.png")
domino_tiles['46']=pygame.image.load("assets/domino-tiles/4-6.png")
domino_tiles['55']=pygame.image.load("assets/domino-tiles/5-5.png")
domino_tiles['56']=pygame.image.load("assets/domino-tiles/5-6.png")
domino_tiles['66']=pygame.image.load("assets/domino-tiles/6-6.png")

domino_tiles_tails={}
domino_tiles_tails["0"]=pygame.image.load("assets/domino-tiles/0.png")
domino_tiles_tails["1"]=pygame.image.load("assets/domino-tiles/1.png")
domino_tiles_tails["2"]=pygame.image.load("assets/domino-tiles/2.png")
domino_tiles_tails["3"]=pygame.image.load("assets/domino-tiles/3.png")
domino_tiles_tails["4"]=pygame.image.load("assets/domino-tiles/4.png")
domino_tiles_tails["5"]=pygame.image.load("assets/domino-tiles/5.png")
domino_tiles_tails["6"]=pygame.image.load("assets/domino-tiles/6.png")

def chat_event_listener(useless,conn):
     while not stoptread:
        try:
            message = conn.recv(4096)
            message = pickle.loads(message)
            event_listened.put(message)   
        except:
            continue

def make_message(message_type,message_body,room_num=None,notes=None):
    message = {}
    message["sender"] = player_name
    message["type"] = message_type
    message["body"] = message_body
    message["note"] = notes
    message["room_number"] = room_num
    return pickle.dumps(message)

def exitting_game(current_room_number=None):
    print("do something here, e.g closing connection")
    socket.send(make_message("exit","exit",room_num=current_room_number))
    pygame.quit()
    stoptread=True
    quit()

def transformImg(obj,scale,rotate=None):
    if(rotate!=None):
        return pygame.transform.rotate(pygame.transform.scale(obj,scale),90)
    return pygame.transform.scale(obj,scale)

def mycard(objs,height, types="potrait"):
    if(types=="potrait"):
        card_len = len(objs)
        width_total = card_len*56
        center = display_width/2 - width_total/2
        for obj in objs:
            window.blit(transformImg(obj,(55,120)),(center,height))
            center = center + 56
    else:
        card_len = len(objs)
        width_total = card_len*56
        center = display_width/2 - width_total/2
        for obj in objs:
            window.blit(transformImg(obj,(55,120),rotate=90),(height,center-75))
            center = center + 56



# def boardcard(obj):
#     return pygame.transform.scale(obj,(35,65))

def game_start():
    on_game=False

    p1cards=[domino_tiles['00'],domino_tiles['03'],domino_tiles['02']]
    p2cards=[domino_tiles['00'],domino_tiles['00'],domino_tiles['00'],domino_tiles['00']]
    p3cards=[domino_tiles['00'],domino_tiles['00']]
    p4cards=[domino_tiles['00'],domino_tiles['00'],domino_tiles['00'],domino_tiles['00']]

    headtailText = pygame.font.Font("assets/Pixel Emulator.otf",35)
    headSurface = headtailText.render("HEAD",False,(0,0,0))
    tailSurface = headtailText.render("TAIL",False,(0,0,0))
    drawSurface = headtailText.render("DRAW CARD",False,(0,0,0))

    while not on_game:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exitting_game()
        
        window.fill((255,255,255))

        mycard(p1cards,460)
        mycard(p2cards,-70)
        mycard(p3cards,-70,types="landscape")
        mycard(p4cards,550,types="landscape")

        window.blit(headSurface,(display_width/2-headSurface.get_width()/2-100,150))
        window.blit(transformImg(domino_tiles_tails['0'],(100,100)),(display_width/2-headSurface.get_width()/2-99,195))
        window.blit(tailSurface,(display_width/2-tailSurface.get_width()/2+100,150))
        window.blit(transformImg(domino_tiles_tails['0'],(100,100)),(display_width/2-tailSurface.get_width()/2+99,195))

        window.blit(drawSurface,(display_width/2-drawSurface.get_width()/2 , 350))

        pygame.display.update()

def failed_join_room():
    failedn=False

    okText = pygame.font.Font("assets/Pixel Emulator.otf",45)
    okSurface = okText.render("OK",False,(0,0,0))
    okSurface_x = display_width/2 - okSurface.get_width()/2
    okSurface_y = display_height/2 - okSurface.get_height()/2 + 35

    notifText = pygame.font.Font("assets/Pixel Emulator.otf",35)
    notifSurface = notifText.render("Sorry, request rejected",False,(0,0,0))
    notifSurface_x = display_width/2 - notifSurface.get_width()/2
    notifSurface_y = display_height/2 - notifSurface.get_height()/2 - 100

    notifSurface2 = notifText.render("try again later",False,(0,0,0))
    notifSurface2_x = display_width/2 - notifSurface2.get_width()/2
    notifSurface2_y = display_height/2 - notifSurface2.get_height()/2 - 50
    while not failedn:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exitting_game()
            elif event.type == pygame.MOUSEBUTTONUP and event.button==1:
                if(mouse[0]>okSurface_x and mouse[0]<okSurface_x+okSurface.get_width() and mouse[1]>okSurface_y and mouse[1]<okSurface_y+okSurface.get_height()):
                    join_room()
                    failedn=True
        
        mouse = pygame.mouse.get_pos()
        window.fill((255,255,255))
        window.blit(notifSurface,(notifSurface_x,notifSurface_y))
        window.blit(notifSurface2,(notifSurface2_x,notifSurface2_y))
        window.blit(okSurface,(okSurface_x,okSurface_y))

        if(mouse[0]>okSurface_x and mouse[0]<okSurface_x+okSurface.get_width() and mouse[1]>okSurface_y and mouse[1]<okSurface_y+okSurface.get_height()):
            okSurface = okText.render("OK",False,(61,73,91))
        else:
            okSurface = okText.render("ok",False,(0,0,0))

        pygame.display.update()   

def kicked_notif():
    kickedn=False

    okText = pygame.font.Font("assets/Pixel Emulator.otf",45)
    okSurface = okText.render("OK",False,(0,0,0))
    okSurface_x = display_width/2 - okSurface.get_width()/2
    okSurface_y = display_height/2 - okSurface.get_height()/2 + 35

    notifText = pygame.font.Font("assets/Pixel Emulator.otf",35)
    notifSurface = notifText.render("You've been kicked",False,(0,0,0))
    notifSurface_x = display_width/2 - notifSurface.get_width()/2
    notifSurface_y = display_height/2 - notifSurface.get_height()/2 - 100

    notifSurface2 = notifText.render("from the room",False,(0,0,0))
    notifSurface2_x = display_width/2 - notifSurface2.get_width()/2
    notifSurface2_y = display_height/2 - notifSurface2.get_height()/2 - 50
    while not kickedn:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exitting_game()
            elif event.type == pygame.MOUSEBUTTONUP and event.button==1:
                if(mouse[0]>okSurface_x and mouse[0]<okSurface_x+okSurface.get_width() and mouse[1]>okSurface_y and mouse[1]<okSurface_y+okSurface.get_height()):
                    game_intro()
                    kickedn=True
        
        mouse = pygame.mouse.get_pos()
        window.fill((255,255,255))
        window.blit(notifSurface,(notifSurface_x,notifSurface_y))
        window.blit(notifSurface2,(notifSurface2_x,notifSurface2_y))
        window.blit(okSurface,(okSurface_x,okSurface_y))

        if(mouse[0]>okSurface_x and mouse[0]<okSurface_x+okSurface.get_width() and mouse[1]>okSurface_y and mouse[1]<okSurface_y+okSurface.get_height()):
            okSurface = okText.render("OK",False,(61,73,91))
        else:
            okSurface = okText.render("ok",False,(0,0,0))

        pygame.display.update()

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
        while(not event_listened.empty()):
            message = event_listened.get()
            if(message['response']=="join_custom_room_succeed"):
                custom_room(room_number=message['room_number'],player=message['note'],participants=message['body'])
            elif(message['response']=="join_custom_room_failed"):
                failed_join_room()
        
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
            elif event.type == pygame.MOUSEBUTTONUP and event.button==1:
                if(mouse[0]>5 and mouse[0]<5+backSurface.get_width() and mouse[1]>0 and mouse[1]<backSurface.get_height()):
                    game_intro()
                elif(mouse[0]>joinSurface_x and mouse[0]<joinSurface_x+joinSurface.get_width() and mouse[1]>joinSurface_y and mouse[1]<joinSurface_y+joinSurface.get_height()):
                    message = make_message("cmd","join_custom_room "+text)
                    socket.send(message)
        
        textSurface = textText.render(text,False,(0,0,0))            
        mouse = pygame.mouse.get_pos()
        clicked = pygame.mouse.get_pressed()
        window.fill((255,255,255)) 
        pygame.draw.rect(window,(0,0,0),(200,210,200,80),3)
        window.blit(textSurface,(215,215))
        window.blit(joinSurface,(joinSurface_x,joinSurface_y))

        if(mouse[0]>5 and mouse[0]<5+backSurface.get_width() and mouse[1]>0 and mouse[1]<backSurface.get_height()):
            backSurface = backText.render("back<",False,(61,73,91))
        elif(mouse[0]>joinSurface_x and mouse[0]<joinSurface_x+joinSurface.get_width() and mouse[1]>joinSurface_y and mouse[1]<joinSurface_y+joinSurface.get_height()):
            joinSurface = backText.render("Join",False,(61,73,91))
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
            print(message)
            if(message['response']=="quick_room_joined"):
                quick_loading(current_total_players=str(message['body']),room_number=message['room_number'])
            elif(message['response']=="create_custom_room_succeed"):
                custom_room(room_number=message['room_number'],player="1",participants=message['body'])

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
                    message=make_message("cmd","create_custom_room")
                    socket.send(message)
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

def custom_room(room_number=None,player=None,participants=[]):
    lobi = False
    backText = pygame.font.Font("assets/Pixel Emulator.otf",25)
    backSurface = backText.render("back<",False,(0,0,0))

    idText = pygame.font.Font("assets/Pixel Emulator.otf",25)
    idSurface = idText.render("Room ID : " + str(room_number),False,(0,0,0))

    startText = pygame.font.Font("assets/Pixel Emulator.otf",25)
    startSurface = startText.render("Start",False,(0,0,0))

    TendangText = pygame.font.Font("assets/Pixel Emulator.otf",17)
    Tendang2Surface = TendangText.render("KICK",False,(0,0,0))
    Tendang3Surface = TendangText.render("KICK",False,(0,0,0))
    Tendang4Surface = TendangText.render("KICK",False,(0,0,0))
    
    if player=="1":
        player1Text = pygame.font.Font("assets/Pixel Emulator.otf",20)
        player1Surface = player1Text.render("You",False,(0,0,0))
    else:
        player1Text = pygame.font.Font("assets/Pixel Emulator.otf",17)
        player1Surface = player1Text.render("R-Master",False,(0,0,0))    
    p1Img = pygame.image.load("assets/player1.jpg")
    
    if player=="2":
        player2Text = pygame.font.Font("assets/Pixel Emulator.otf",20)
        player2Surface = player2Text.render("You",False,(0,0,0))        
    else:
        player2Text = pygame.font.Font("assets/Pixel Emulator.otf",17)
        player2Surface = player2Text.render("Player 2",False,(0,0,0))
    p2Img = pygame.image.load("assets/player2.jpg")

    if player=="4":
        player4Text = pygame.font.Font("assets/Pixel Emulator.otf",20)
        player4Surface = player4Text.render("You",False,(0,0,0))        
    else:
        player4Text = pygame.font.Font("assets/Pixel Emulator.otf",17)
        player4Surface = player4Text.render("Player 4",False,(0,0,0))
    p4Img = pygame.image.load("assets/player4.jpg")

    if player=="3":
        player3Text = pygame.font.Font("assets/Pixel Emulator.otf",20)
        player3Surface = player3Text.render("You",False,(0,0,0))
    else:
        player3Text = pygame.font.Font("assets/Pixel Emulator.otf",17)
        player3Surface = player3Text.render("Player 3",False,(0,0,0))
    p3Img = pygame.image.load("assets/player3.jpg")


    while not lobi:
        if(not event_listened.empty()):
            message = event_listened.get()
            print(message)
            if(message['response']=="update_custom_room"):
                participants=message['body']
            elif(message['response']=="quit_cusroom_succeed"):
                game_intro()
            elif(message['response']=="been_kicked"):
                kicked_notif()

        for event in pygame.event.get():
            if(event.type==pygame.QUIT):
                exitting_game()
            elif(event.type==pygame.MOUSEBUTTONUP and event.button==1):
                if(mouse[0]>5 and mouse[0]<5+backSurface.get_width() and mouse[1]>0 and mouse[1]<backSurface.get_height()):
                    if player=="1" and participants.count("0")==3:
                        message=make_message("cmd","quit_cusroom",room_num=room_number,notes="im-last")
                        socket.send(message)
                    elif player!="1":
                        message=make_message("cmd","quit_cusroom",room_num=room_number)
                        socket.send(message)

                elif(player=="1" and participants[3]=="1" and mouse[0]>124 and mouse[0]<124+Tendang4Surface.get_width() and mouse[1]>250 and mouse[1]<250+Tendang4Surface.get_height()):
                    message=make_message("cmd","kick 4",room_num=room_number)
                    # print(message)
                    socket.send(message)
                elif(player=="1" and participants[2]=="1" and mouse[0]>424 and mouse[0]<424+Tendang3Surface.get_width() and mouse[1]>250 and mouse[1]<250+Tendang3Surface.get_height()):
                    message=make_message("cmd","kick 3",room_num=room_number)
                    # print(message)
                    socket.send(message)
                elif(player=="1" and participants[1]=="1" and mouse[0]>274 and mouse[0]<274+Tendang2Surface.get_width() and mouse[1]>250 and mouse[1]<250+Tendang2Surface.get_height()):
                    message=make_message("cmd","kick 2",room_num=room_number)
                    # print(message)
                    socket.send(message)
                elif(player=="1" and mouse[0]>258 and mouse[0]<258+startSurface.get_width() and mouse[1]>455 and mouse[1]<455+startSurface.get_height()):
                    if(not "0" in participants):
                        print("starting game")
        window.fill((255,255,255))
        
        if(participants.count("0")==3 and player=="1"):
            window.blit(backSurface,(5,0))
        elif(player!="1"):
            window.blit(backSurface,(5,0))


        if(participants[3]=="1"):
            window.blit(p4Img,(118,155))
        if(player=="4"):
            window.blit(player4Surface,(137,125))
        else:
            window.blit(player4Surface,(102,125))
        pygame.draw.rect(window,(0,0,0),(110,150,80,100),3)

        window.blit(idSurface,(display_width/2-idSurface.get_width()/2,80))

        if(participants[1]=="1"):
            window.blit(p2Img,(268,155))
        if(player=="2"):
            window.blit(player2Surface,(277,125))
        else:
            window.blit(player2Surface,(252,125))
        pygame.draw.rect(window,(0,0,0),(260,150,80,100),3)

        if(participants[2]=="1"):
            window.blit(p3Img,(418,155))
        if(player=="3"):
            window.blit(player3Surface,(427,125))
        else:
            window.blit(player3Surface,(402,125))
        pygame.draw.rect(window,(0,0,0),(410,150,80,100),3)

        if(participants[0]=="1"):
            window.blit(p1Img,(268,355))
        if(player=="1"):
            window.blit(player1Surface,(277,325))
            if(not "0" in participants):
                window.blit(startSurface,(258,455))
            if(participants[3]=="1"):
                window.blit(Tendang4Surface,(124,250))
            if(participants[1]=="1"):
                window.blit(Tendang2Surface,(274,250))
            if(participants[2]=="1"):
                window.blit(Tendang3Surface,(424,250))
        else:
            window.blit(player1Surface,(252,325))
        pygame.draw.rect(window,(0,0,0),(260,350,80,100),3)
        

        mouse = pygame.mouse.get_pos()
        if(mouse[0]>5 and mouse[0]<5+backSurface.get_width() and mouse[1]>0 and mouse[1]<backSurface.get_height()):
            backSurface = backText.render("back<",False,(61,73,91))
        elif(mouse[0]>258 and mouse[0]<258+startSurface.get_width() and mouse[1]>455 and mouse[1]<455+startSurface.get_height()):
            startSurface = startText.render("Start",False,(61,73,91))
        elif(mouse[0]>124 and mouse[0]<124+Tendang4Surface.get_width() and mouse[1]>250 and mouse[1]<250+Tendang4Surface.get_height()):
            Tendang4Surface = TendangText.render("KICK",False,(61,73,91))
        elif(mouse[0]>424 and mouse[0]<424+Tendang3Surface.get_width() and mouse[1]>250 and mouse[1]<250+Tendang3Surface.get_height()):
            Tendang3Surface = TendangText.render("KICK",False,(61,73,91))
        elif(mouse[0]>274 and mouse[0]<274+Tendang2Surface.get_width() and mouse[1]>250 and mouse[1]<250+Tendang2Surface.get_height()):
            Tendang2Surface = TendangText.render("KICK",False,(61,73,91))
        else:
            startSurface = startText.render("Start",False,(0,0,0))
            backSurface = backText.render("back<",False,(0,0,0))
            Tendang2Surface = TendangText.render("KICK",False,(0,0,0))
            Tendang3Surface = TendangText.render("KICK",False,(0,0,0))
            Tendang4Surface = TendangText.render("KICK",False,(0,0,0))   

        pygame.display.update()       
    
                
if __name__ == '__main__':
    socket.connect(address)
    message = socket.recv(4096)
    message = pickle.loads(message)
    if message["sender"] == "admin" and message.get("player_name",False) != False:
        player_name = message["player_name"]  
    mythread=threading.Thread(target=chat_event_listener,args=(address,socket))
    mythread.start()  

    # game_intro()
    game_start()
    # custom_room()
    # kicked_notif()
    # failed_join_room()