#!/usr/bin/env python
"""
    Copyright (C) 2011  Smart Viking (smartestviking@gmail.com)

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import sys, pygame, random, getpass, os.path, time
from pygame.locals import *
from string import ascii_lowercase

#Developer notes to other developers (Format is: From - To - Message)
    #Robert Maehl - Smartviking - Please name your variables better.
    #Robert Maehl - Smartviking - We need to make it so the resources get reused instead of drawn with each game.
    #Robert Maehl - ALL - I recommend using scite for editing from now on (sudo apt-get install scite)
    #Robert Maehl - ALL - You can change scite's spacing and tabs using Ctrl + Shift + I
    #Robert Maehl - ALL - While in Debug Mode hold both left and right arrows to make the guy bounce.
    #SmartViking - Robert Maehl - It's better to add an additional condition to an if statement than to indent 100 lines of code.

version = "1.5" #Version Control
debug = "" #Debug Control
skipvid = False #Video Control

for argument in sys.argv:
    if argument == "--novideo":
        skipvid = True
    if argument == "--version" or argument == "-v":
        print "Crazy China Pong version "+version
        if argument == sys.argv[-1]:
            sys.exit()
        else:
            pass
    if argument == "--credits":
        print "Crazy China Pong "+version+" Credits:\n\n"+\
            " " +"#"*40+"\n"+\
            " # Coding            : SmartViking"+" "*6+"#"+"\n"+" #"+" "*21+"Staticsafe"+" "*7+"#"+"\n"+" #"+" "*21+"Robert Maehl"+" "*5+"#"+"\n"+\
            " #"+"-"*38+"#\n"+\
            " # All Music         : Kris Occhipinti  #\n"+\
            " #"+"-"*38+"#\n"+\
            " # Artwork           : SmartViking      #\n"+\
            " "+"#"*40
        if argument == sys.argv[-1]:
            sys.exit()
        else:
            pass
    if argument == "--debug" or argument == "-d":
        open('.debug', 'w').close()
        debug = " - Debug Mode"
    if argument == "--bug" or argument == "-b":
        if os.path.exists(".debug") == True:
            os.remove('.debug')
        if argument == sys.argv[-1]:
                sys.exit()
        else:
            pass
pygame.mixer.pre_init()
pygame.init()

pygame.display.set_icon(pygame.image.load("data/icon.png"))
pygame.display.set_caption('Crazy China Pong - '+version+debug)
pygame.mixer.init()

def music(song):
    if song == 10:
        impatient = pygame.mixer.music.load("data/music/impatient.ogg")
        pygame.mixer.music.play()
        pygame.mixer.music.set_volume(0.4)
    elif song == 20:
        oil = pygame.mixer.music.load("data/music/oil.ogg")
        pygame.mixer.music.play()
        pygame.mixer.music.set_volume(0.4)
    elif song == 30:
        breath = pygame.mixer.music.load("data/music/breath.ogg")
        pygame.mixer.music.play()
        pygame.mixer.music.set_volume(0.7)

def nextsong(song):
    song += 10
    if song > 30:
        song = 10
    music(song)
    return song

def highscore(player,score): #Score Output
    with open('.score', 'a') as f:
        f.write(player+","+str(int(score))+"\n")
    f.close()

def mpause(musicp):
    if musicp:
        pygame.mixer.music.unpause()
        return 0
    else:
        pygame.mixer.music.pause()
        return 1

whichsong = random.choice(range(10,40,10))
music(whichsong)

def main(startup=0,songnumber=10):

    musicpause = 0
    clock = pygame.time.Clock() #FPS Clock Method used for Main()
    size = width, height = 600,400
    screen = pygame.display.set_mode(size)
    debug = os.path.exists(".debug")

    font = pygame.font.Font("data/FreeMonoBold.ttf", 12)
    endscorefont = pygame.font.Font("data/FreeMonoBold.ttf", 30)
    bonusfont = pygame.font.Font("data/FreeMonoBold.ttf", 17)

    #Image Importation
    gun = pygame.image.load("data/gun.png").convert()
    bg = pygame.image.load("data/bg.png").convert()
    guy = pygame.image.load("data/guy.png")
    guy2 = pygame.image.load("data/guy2.png")
    finished = pygame.image.load("data/finished.png")
    bonus = pygame.image.load("data/bonus_score.png")
    badbonus = pygame.image.load("data/bad_score.png")
    bgfreeze = pygame.image.load("data/bgfreeze.png")
    freezeball = pygame.image.load("data/freeze.png")
    bgimg = bg
    if startup == 2: #Start Screen
        write = 1
        Name = getpass.getuser()
        numb = ["1","2","3","4","5","6","7","8","9","0"]
        upper = 0
        remove = 0
        while write:
            keystate = pygame.key.get_pressed()
            pygame.key.set_repeat(1000, 100)
            if keystate[K_LSHIFT]:
                upper = 1
            elif keystate[K_CAPSLOCK]:
                upper = 1
            else:
                upper = 0
            if keystate[K_BACKSPACE]:
                Name = Name[:-1]

            for event in pygame.event.get():
                if event.type == pygame.QUIT or event.type == KEYDOWN and event.key == K_ESCAPE:
                    sys.exit()
                if event.type == KEYDOWN:
                    if str(pygame.key.name(event.key)) in (list(ascii_lowercase) + numb):
                        if upper:
                            Name += str(pygame.key.name(event.key)).upper()
                        else:
                            Name += str(pygame.key.name(event.key))
                        if Name.count("") == 25:
                            Name = Name[:-1]
                if event.type == KEYDOWN and event.key == K_RETURN:
                    if Name == "": Name = getpass.getuser()
                    write = 0
            screen.blit(bgimg,(0,0))
            nameview = endscorefont.render(Name, True, (44,44,44))
            namerequest = endscorefont.render("Enter your name...", True, (213, 98, 0))
            screen.blit(nameview,(40,150))
            screen.blit(namerequest,(40,120))
            pygame.display.update()
            clock.tick(20)
    else:
        Name = startup                
    score = 0

    #Intro Video
    if startup == 2 and not skipvid:
        #Intro Video Variables
        vgunh = -100
        video = 1
        videocycle = 0
        vbonusw = 650
        vbbonusw = 650
        goodw = 700
        badw = 700
        vguyw = 650
        vguyh = 450
        vballh = -50
        coldw = 450
        coldh = -40
        vfarmer = guy
        enterh = -20
        enterstay = 0
        skipped = 0
        while video:
            videocycle += 1
            for event in pygame.event.get():
                if event.type == pygame.QUIT or event.type == KEYDOWN and event.key == K_ESCAPE:
                    sys.exit()
                if event.type == KEYDOWN and event.key == K_s:
                    musicpause = mpause(musicpause)
                if event.type == KEYDOWN and event.key == K_n or not pygame.mixer.music.get_busy():
                    songnumber = nextsong(songnumber)
                if event.type == KEYDOWN and event.key == K_RETURN or event.type == KEYDOWN and event.key == K_SPACE:
                    video = 0
            screen.blit(bgimg,(0,0))
            if 250 > videocycle > 10:
                enternoaw = bonusfont.render("Press enter to skip", True, (255, 255, 255))
                screen.blit(enternoaw,(100,enterh))
                if enterh < 10 and not skipped:
                    enterh += 2
                else:
                    skipped = 1
                    enterstay += 1
                    if enterstay > 100:
                        enterh -= 1
            if videocycle < 400:
                vgunh += 1.2
            if videocycle < 125:
                vbonusw -= 5
                vprize = bonusfont.render("113", True, (255, 255, 255))
                good = endscorefont.render("This is good.", True, (44,44,99))
                screen.blit(good, (goodw,140))
                screen.blit(bonus,(vbonusw,100))
                screen.blit(vprize,(vbonusw+4,100))
                if videocycle < 80:
                    goodw -= 7
                elif videocycle > 80:
                    goodw += 10
                else:
                    time.sleep(1.5)
            if 300 > videocycle > 130:
                vbbonusw -= 6
                vbadprize = bonusfont.render("-42", True, (255, 255, 255))
                bad = endscorefont.render("This is bad.", True, (222,54,19))
                screen.blit(bad, (badw,230))
                screen.blit(badbonus,(vbbonusw,180))
                screen.blit(vbadprize,(vbbonusw+4,180))
                if videocycle < 200:
                    badw -= 8
                elif videocycle > 200:
                    badw += 10
                else:
                    time.sleep(1.5)
                if 235 > videocycle > 200:
                    vgunh -= 4
                if 260 > videocycle > 235:
                    vgunh -= 1.2
            if videocycle > 230:
                if videocycle > 280:
                    vballh += 0.7
                if 360 > videocycle > 230:
                    coldw -= 3
                    coldh += 0.7
                cold = endscorefont.render("This is very good (and cold).", True, (255,224,219))
                screen.blit(cold, (coldw,coldh))

                if videocycle < 585:
                    screen.blit(freezeball, (440,vballh))
                if 650 > videocycle > 600:
                    coldw += 12
            if videocycle > 250:
                if videocycle < 458:
                    vguyh -= 0.9
                    vguyw -= 3
                else:
                    if videocycle == 458:
                        vfarmer = guy2
                    vguyh -= 0.7
                    vguyw += 3
                    if videocycle > 580 and vgunh > 125:
                        vgunh -= 1
                        if int(vgunh) <= 125:
                            textloop = 1
                            introtext1 = endscorefont.render("Do not let the Chinese rice", True, (0,50,0))
                            introtext2 = endscorefont.render("farmer escape to the western", True, (0,50,0))
                            introtext3 = endscorefont.render("world.", True, (0,50,0))
                            introtext4 = endscorefont.render("Stop him by controlling", True, (0,50,0))
                            introtext5 = endscorefont.render("the block... thing with the", True, (0,50,0))
                            introtext6 = endscorefont.render("arrow keys or the mouse.", True, (0,50,0))
                            introtext7 = endscorefont.render("You win if you have fun.", True, (0,50,0))
                            introtext8 = endscorefont.render("Good luck!", True, (0,50,0))
                            while textloop:
                                for event in pygame.event.get():
                                    if event.type == pygame.QUIT or event.type == KEYDOWN and event.key == K_ESCAPE:
                                        sys.exit()
                                    if event.type == KEYDOWN and event.key == K_RETURN or event.type == KEYDOWN and event.key == K_SPACE:
                                        video = 0
                                        textloop = 0
                                    if event.type == KEYDOWN and event.key == K_s:
                                        musicpause = mpause(musicpause)
                                    if event.type == KEYDOWN and event.key == K_n or not pygame.mixer.music.get_busy():
                                        songnumber = nextsong(songnumber)
                                screen.blit(bgimg,(0,0))
                                screen.blit(introtext1,(70,60))
                                screen.blit(introtext2,(70,90))
                                screen.blit(introtext3,(70,120))
                                screen.blit(introtext4,(70,170))
                                screen.blit(introtext5,(70,200))
                                screen.blit(introtext6,(70,230))
                                screen.blit(introtext7,(70,290))
                                screen.blit(introtext8,(340,340))
                                screen.blit(gun,(30,vgunh))
                                pygame.display.update()
                                clock.tick(10)
                screen.blit(vfarmer, (vguyw,vguyh))
            screen.blit(gun,(30,vgunh))
            pygame.display.update()
            clock.tick(50)
    farmer = guy2 #Farmer Image Direction
    gunh = 125 #Gun height
    guyh = 200 #Farmer height
    guyw = 280 #Farmer width
    east = 1 #Farmer Direction Variable

    guydirs = 0.2 #+/- Value guyh per loop
    guyspeed = 4
    if debug == True:
        guyspeed = 0
    gunspeed = 8
    scorespeed = 0.04 #Score

    badbonusw = 650
    bonusw = 650
    bonusactive = 0
    bonuspoints = 0
    badbonusactive = 0
    gamespeed = 90

    balls = 0
    ballw = 0
    ballh = -50
    freeze = 0
    freezecycle = 0
    mouse = 0
    gunmov = 0
    while 1:
        previousgh = gunh
        if not pygame.mouse.get_rel()[1] == 0:
            gunh = (pygame.mouse.get_pos()[1]-250)*1.2+210
            mouse = 151
        if mouse > 0:
            mouse -= 1
        score += scorespeed
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == KEYDOWN and event.key == K_ESCAPE:
                sys.exit()
            if event.type == KEYDOWN and event.key == K_s:
                musicpause = mpause(musicpause)
            if event.type == KEYDOWN and event.key == K_n or not pygame.mixer.music.get_busy():
                songnumber = nextsong(songnumber)
        keystate = pygame.key.get_pressed()

        #Controls
        if debug == True:
            if keystate[115]:
                gunh += gunspeed
            if keystate[119]:
                gunh -= gunspeed
            if keystate[pygame.K_UP]:
                guyh = guyh - 4
            if keystate[pygame.K_DOWN]:
                guyh = guyh + 4
            #Vertical Limiting
            if not 374 > guyh > -14:
                guyh = guyh-(8*(guyh/guyh))
        else:
            if keystate[pygame.K_UP]:
                if gunmov > 0:
                    gunmov = 0
                gunmov -= gunspeed/3.0

            if keystate[pygame.K_DOWN]:
                if gunmov < 0:
                    gunmov = 0
                gunmov += gunspeed/3.0


            if -0.2 < gunmov < 0.2:
                gunmov = 0

            elif gunmov > 0:
                gunmov -= 0.15
                if not keystate[pygame.K_DOWN]:
                    gunmov -= 0.5
            elif gunmov < 0:
                if not keystate[pygame.K_UP]:
                    gunmov += 0.5
                gunmov += 0.15

            if gunmov > 7:
                gunmov = 7
            if gunmov < -7:
                gunmov = -7

            if not 300 > gunh > 0 and not mouse:
                if gunh > 300:
                    gunh -= 5
                else:
                    gunh += 5

            gunh += gunmov
    
            #Vertical Bounce
            if not 370 > guyh > -10:
                guydirs = guydirs - (guydirs*2)
            guyh = guyh + guydirs

        #Horizontal Bounce
        if east:
            farmer = guy2
            if debug == True:
                if keystate[pygame.K_RIGHT]:
                    guyw = guyw + 4
            else:
                guyw += guyspeed
            if guyw > 560:
                east = 0
        else:
            farmer = guy
            if debug == True:
                if keystate[pygame.K_LEFT]:
                    guyw = guyw - 4
            else:
                guyw -= guyspeed
            if guyw < 31 and guyh > gunh-40 and guyh < gunh+100:
                east = 1
                guydirs = guydirs- (gunh-(guyh+20)+50)/50.0
                if previousgh > gunh:
                    guydirs -= 0.6
                elif previousgh < gunh:
                    guydirs += 0.6

        #Pause Screen
        if guyw < 0:
            writefile = 1
            while 1:
                #Pause screen rendering
                screen.blit(bgimg,(0,0))
                screen.blit(finished,(0,0))
                text = endscorefont.render(" "*4+"Your final score was: "+str(int(score))+" "*40, True, (255, 255, 255), (213, 98, 0))
                screen.blit(farmer,(guyw,guyh))
                screen.blit(gun,(30,gunh))
                screen.blit(text,(0,369))
                pygame.display.update()
                if writefile:
                    highscore(Name,score)
                    writefile = 0
                clock.tick(10) #FPS and Resource limiting
                for event in pygame.event.get():
                    if event.type == KEYDOWN and event.key == K_SPACE:
                        main(Name)
                    if event.type == pygame.QUIT or event.type == KEYDOWN and event.key == K_ESCAPE:
                        sys.exit()
                    if event.type == KEYDOWN and event.key == K_s:
                        musicpause = mpause(musicpause)
                    if event.type == KEYDOWN and event.key == K_n or not pygame.mixer.music.get_busy():
                        songnumber = nextsong(songnumber)
                    if event.type == KEYDOWN and event.key == K_h:
                        f = open(".score")
                        playerscore = {}
                        for line in f:
                            player,score = line.split(",")
                            playerscore[int(score)] = player
                        f.close

                        screen.blit(bgimg,(0,0))
                        screen.blit(farmer,(guyw,guyh))
                        screen.blit(gun,(30,gunh))
                        stopten= 0
                        heightheight = 60
                        for i in sorted(playerscore.keys(), reverse=True):
                            stopten += 1
                            textplayers = endscorefont.render(playerscore[i], True, (44,44,44))
                            screen.blit(textplayers,(50,heightheight))
                            textscore = endscorefont.render(str(i), True, (44,44,44))
                            r = textscore.get_rect(center=(100,100))
                            r.right = 550
                            r.y = heightheight
                            screen.blit(textscore,r)
                            heightheight += 30
                            if stopten == 10:
                                break
                        leaderboards = endscorefont.render("Highscores", True, (213,98,0))
                        screen.blit(leaderboards,(200,25))
                        enterpress = font.render("Press Enter...", True, (44,44,44))
                        screen.blit(enterpress,(250,10))
                        screen.blit(text,(0,369))

                        pygame.display.update()
                        pause = 1
                        while pause:
                            for event in pygame.event.get():
                                if event.type == pygame.QUIT or event.type == KEYDOWN and event.key == K_ESCAPE:
                                    sys.exit()
                                if event.type == KEYDOWN and event.key == K_RETURN or event.type == KEYDOWN and event.key == K_h:
                                    pause = 0
                                if event.type == KEYDOWN and event.key == K_s:
                                    musicpause = mpause(musicpause)
                                if event.type == KEYDOWN and event.key == K_n or not pygame.mixer.music.get_busy():
                                    songnumber = nextsong(songnumber)

                                    
        #Freeze ball
        randomball = random.randint(1,1000)
        if not balls and not freeze and randomball == 399:
            ballw = random.choice(range(100,550,50))
            balls = 1
        #Bonus
        randombonus = random.randint(1,1000)
        if not bonusactive and randombonus == 99:
            bonush = random.choice(range(10,390,10))
            bonusactive = 1
        #Bad bonus
        randombadbonus = random.randint(1,2000)
        if not badbonusactive and randombadbonus == 199:
            badbonush = random.choice(range(5,385,10))
            badbonusactive = 1
        #Rendering
        screen.blit(bgimg,(0,0))
        text = font.render(" Score: "+str(int(score))+"  "+"Speed: "+str(int(guyspeed))+" ", True, (255, 255, 255), (213, 98, 0))
        screen.blit(text, (50,10))

        if balls:
            screen.blit(freezeball,(ballw,ballh))
            ballh += 1
            if ballw < guyw+40 and ballw+40 > guyw and ballh+40 > guyh and ballh < guyh+40:
                ballh = -50
                freeze = 1
                balls = 0
            if ballh > 405:
                ballh = -50
                balls = 0

        #Bonus Calculations
        if bonusactive:
            if bonusw == 650:
                prize = random.randint(100,180)

            bonusamount = bonusfont.render(str(prize), True, (255, 255, 255))
            screen.blit(bonus,(bonusw,bonush))
            screen.blit(bonusamount,(bonusw+4,bonush))

            bonusw -= 2
            if 5 < bonusw < 30 and bonush+20 > gunh and bonush < gunh+100:
                score += prize
                bonuspoints += prize
                bonusactive = 0
                bonusw = 650
            if bonusw < -50:
                bonusactive = 0
                bonusw = 650

        if badbonusactive:
            if badbonusw == 650:
                badprize = random.randint(-99,-30)

            badprizeamount = bonusfont.render(str(badprize), True, (255, 255, 255))
            screen.blit(badbonus,(badbonusw+1,badbonush-1))
            screen.blit(badprizeamount,(badbonusw+5,badbonush))

            badbonusw -= 3
            if 5 < badbonusw < 30 and badbonush+20 > gunh and badbonush < gunh+100:
                score += badprize
                bonuspoints += badprize
                badbonusactive = 0
                badbonusw = 650
            if badbonusw < -50:
                badbonusactive = 0
                badbonusw = 650

        screen.blit(farmer,(guyw,guyh))
        screen.blit(gun,(30,gunh))

        if freeze:
            gunspeed = 10
            score += 0.5
            bonuspoints += 0.5
            gamespeed = 70
            bgimg = bgfreeze
            freezecycle += 1
            if freezecycle > 600:
                freeze = 0
                gamespeed = 90
                freezecycle = 0
                gunspeed = 8
                bgimg = bg

        #The score algorithm
        if score < 0:
            score = 0
        if debug == False:
            guyspeed += 0.001
            scorespeed = 0.02*(guyspeed)

        else:
            guyspeed = 0
            scorespeed = 0.15  

        #Update Screen
        pygame.display.update()
        clock.tick(gamespeed)

if __name__ == "__main__": main(2,whichsong)
