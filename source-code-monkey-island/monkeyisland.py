# Monkey Island
import pgzrun
import random

with open('data.txt') as d:
    script = d.readlines()

pauseCount = 0
stopped = False
currentScriptLine = 0
sceneBackground = "title"
sceneForeground = ""
currentScene = ""
currentText = ""
currentCharacter = 0
characters = [0,0,0]
mycolours = [(100,240,255),(200,200,200),(240,100,100)]
frame = 0
talkRandom = 0
optionText = ["","",""]
optionAction = ["","",""]

def draw():
    screen.blit(sceneBackground,(0,0))
    for c in characters:
        if c != 0:
            if (frame/(5+talkRandom))%10 < 5 and c.talking == True:
                c.image = c.imagename + "talk"
            else: c.image = c.imagename
            c.draw()
    if sceneForeground != "": screen.blit(sceneForeground,(0,0))
    cc = characters[currentCharacter]
    if currentText != "": screen.draw.text(currentText, center = (cc.x,cc.y-100), owidth=0.5, ocolor=(0,0,0), color=mycolours[currentCharacter] , fontsize=30)
    for o in range(0, 3): screen.draw.text(optionText[o], center = (400,450+(o*40)), color=(255,255,255) , fontsize=30)
    
def update():
    global pauseCount, frame, talkRandom, currentText
    while pauseCount == 0 and stopped == False:
        processScriptLine()
    if pauseCount > 0: pauseCount -= 1
    if pauseCount == 0: currentText = ""
    if pauseCount < 15 and characters[currentCharacter] != 0:
        characters[currentCharacter].talking = False
    frame += 1
    if frame%30 == 0: talkRandom = random.randint(0, 2)

def processScriptLine():
    global script, currentScriptLine, pauseCount, stopped, sceneBackground, currentScene, sceneForeground, currentText, currentCharacter
    sl = script[currentScriptLine].split(":")
    if sl[0] == "Background": sceneBackground = sl[1].strip('\n')
    if sl[0] == "Foreground": sceneForeground = sl[1].strip('\n')
    elif sl[0] == "Pause": pauseCount = int(sl[1].strip('\n'))*30
    elif sl[0] == "Scene": currentScene = sl[1].strip('\n')
    elif sl[0] == "Character":
        cl = sl[2].split(",")
        setCharacter(int(sl[1]),cl[0],int(cl[1]),int(cl[2]))
    elif sl[0] == "Speech":
        currentCharacter = int(sl[1])
        currentText = sl[2].strip('\n')
        characters[currentCharacter].talking = True
    elif sl[0] == "SetOption":
        optionAction[int(sl[1])] = sl[2]
        optionText[int(sl[1])] = sl[3]
    elif sl[0] == "Stop": stopped = True
    currentScriptLine += 1
    
def setScene(scene):
    global optionText, optionAction, sceneForeground, currentScriptLine, stopped, currentText, currentCharacter, characters
    optionText = ["","",""]
    optionAction = ["","",""]
    currentText = ""
    currentCharacter = 0
    characters = [0,0,0]
    sceneForeground = ""
    line = 0
    for s in script:
        if s.strip('\n') == "Scene:"+scene:
            currentScriptLine = line
            stopped = False
        line += 1

def on_mouse_down(pos):
    for o in range(0, 3):
        if pos[1] > 450+(o*40)-15 and pos[1] < 450+(o*40)+15 and optionAction[o] != "":
            setScene(optionAction[o])
    
def setCharacter(cnum,cname,cx,cy):
    characters[cnum] = Actor(cname, center=(cx, cy))
    characters[cnum].imagename = cname
    characters[cnum].talking = False
            
pgzrun.go()
