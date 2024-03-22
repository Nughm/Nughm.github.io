import asyncio
import pygame
from sys import exit
pygame.init()
Width, height = 1280, 720
screen = pygame.display.set_mode((Width, height))
# pygame.scrap.init()
icon = pygame.image.load("favicon.png")
pygame.display.set_icon(icon)
pygame.display.set_caption("Fetch Decode Execute GCSE LMC simulator")
screen.fill("White")
clock = pygame.time.Clock()



async def main():
    global Width, height
    count_down = -100
    #dot class
    class dot:
        def __init__(self, col):
            self.color = col
            self.phase = 0
            self.iphase = 0
            self.target = 0
            self.x = -10
            self.y = -10
            self.speed = 2
            self.value = ""

        def reset(self):
            self.color, self.phase, self.target, self.x, self.y, self.value = "Red", 0, None, -10, -10, ""
        def update(self):
            temp = base_font.render(str(self.value), True, "Black")
            temp_rect = temp.get_rect(center=(self.x, self.y))
            if len(str(self.value)) == 3:
                pygame.draw.ellipse(screen, self.color, temp_rect, 50)
            else:
                pygame.draw.circle(screen, self.color, temp_rect.center, 10)
            screen.blit(temp, temp_rect)

        def setcoord(self, ex, why):
            self.x, self.y = ex, why

        def py(self, val):
            self.y += self.speed
            if self.y >= val:
                self.y, self.iphase = val, self.iphase + 1

        def px(self, val):
            self.x += self.speed
            if self.x >= val:
                self.x = val
                self.iphase += 1

        def my(self, val):
            self.y -= self.speed
            if self.y <= val:
                self.y = val
                self.iphase += 1

        def mx(self, val):
            self.x -= self.speed
            if self.x <= val:
                self.x = val
                self.iphase += 1

        def travelmem(self): #starting from the variables, travels to memory and back
            if self.iphase == -1:
                self.py(490)
            elif self.iphase == 0:
                self.px(565)
            elif self.iphase == 1:
                self.py(675)
            elif self.iphase == 2:
                self.px(655)
            elif self.iphase == 3:
                self.my((self.target//10)*60+50)
            elif self.iphase == 4:
                self.px((self.target%10)*60+710)
            elif self.iphase == 5:
                self.mx(655)
            elif self.iphase == 6:
                self.py(675)
            elif self.iphase == 7:
                self.mx(565)
            elif self.iphase == 8:
                self.my(375)
            elif self.iphase == 9:
                self.mx(430)
            elif self.iphase == 10:
                self.my(325)
                if self.iphase == 11: self.iphase = 100
            elif self.iphase == 11:
                self.mx(430)
                if self.iphase == 12: self.iphase = 100

        def travelALU(self): #After travelmem iphase1, travel to ALU and back (to PC)
            if self.iphase == 0:
                self.py(630)
            elif self.iphase == 1:
                self.px(472)
            elif self.iphase == 2:
                self.my(270)
            elif self.iphase == 3:
                self.mx(430)
                if self.iphase == 4: self.iphase = 100

    def scrollout(lis, off, val, rect, font):#Handles all scrolling
        if lis:
            if len(lis) > 10:
                for i in range(len(lis)-10):
                    lis.pop(0)
            for i in range(len(lis)):
                temp = font.render(f"  {str(lis[i])}", True, "Black")
                screen.blit(temp, (rect.left, rect.top+i*val+off))
            return lis
        else: return []

    def blitmem(memory):
        for i in range(100):
            temp = Bigger_font.render(memory[i], True, "Black")
            temp_rect = temp.get_rect(center=((i % 10 * 60 + 710), (i // 10) * 60 + 50))
            pygame.draw.rect(screen, "Gray", temp_rect)
            screen.blit(temp, temp_rect)
        return memory

    def updateCPU(PrC, InR, AdrR, AcC):
        templis = [PrC, InR, AdrR, AcC]
        for i in range(4):
            temp = Biggest_font.render(str(templis[i]), True, "Black")
            temp_rect = temp.get_rect(center = (430, i*50+270))
            pygame.draw.rect(screen, "White", temp_rect)
            screen.blit(temp, temp_rect)

    def addLis(lis, offset):
        if lis:
            count = 0
            for i in lis:
                if len(str(count)) == 1: count = str(0) + str(count)
                temp = Base_font.render(f"{count} {i}", False, "Black")
                screen.blit(temp, (275, ((int(count))*12)-offset))
                count  = int(count)
                count += 1
            return lis
        else:
            return []
    def convstring(lis):
        temp = ""
        for i in lis:
            temp += i
        return temp

    def disp(lis, offset):
        if lis:
            y = 0 - offset
            for i in range(len(lis)):
                temp = base_font.render(convstring(lis[i]), False, "Black")
                if i*15 >= offset:
                    screen.blit(temp, (0, (i*15 - offset)+50))
            return lis
        return lis
    def check(lis): #checking if it is valid
        AIn = ["HLT", "ADD", "SUB", "STA", "STO", "LDA", "BRA", "BRZ", "BRP", "INP", "OUT", "OTC", "DAT"]
        Sing = ["HLT", "INP", "OUT", "OTC"]
        labels = []
        labelsloc = []
        if lis == []: return ("Empty input", False)
        for i in range(len(lis)):
            tlis = lis[i].split(" ")
            if tlis[0].upper() not in AIn:
                if tlis[0] not in labels: #Adds labels
                    labels.append(tlis[0])
                    labelsloc.append(str(i))
                lis[i] = lis[i][len(tlis[0])+1:]

            tlis = lis[i].split(" ")
            if tlis[0].upper() not in AIn: #False if the action is not valid
                return (f"Invalid action \n or no action \n in line {i+1}", False)
        for i in range(len(labelsloc)):
            if len(str(labelsloc[i])) == 1:
                labelsloc[i] = "0" + labelsloc[i]
        for i in range(len(lis)): #Adding 0 to those that require a label but are blank (Assumed)
            tlis = lis[i].split(" ")
            if len(tlis) == 1:
                if tlis[0].upper() not in Sing:
                    lis[i] += " 0"
                    tlis.append("0")
            elif tlis[0].upper() in Sing:
                lis[i] = lis[i][:len(tlis[0])]
                tlis.pop(1)
            if tlis[0].upper() not in Sing and tlis[1].isnumeric() is False:
                if tlis[1] not in labels:
                    return (f"Label '{tlis[1]}' \n is \n not defined.", False)
                else:
                    lis[i] = lis[i][:len(tlis[0])]+f" {labelsloc[labels.index(tlis[1])]}"
            if tlis[0].upper() not in Sing and tlis[1].isnumeric() and len(tlis[1]) == 1:
                tlis[1] = "0"+tlis[1]
                lis[i] = f"{tlis[0]} {tlis[1]}"

        for i in range(len(lis)):
            lis[i] = lis[i].upper()

        return(lis, True)

    def convass(test):
        memory = ['000' for i in range(100)]
        WordToNum = {'HLT' : '000','ADD' : '1','SUB' : '2','STA' : '3','STO' : '3', 'LDA' : '5','BRA' : '6','BRZ' : '7','BRP' : '8','INP' : '901','OUT' : '902','OTC' : '922','DAT' : ''}
        for i in range(len(test)):
            temp = test[i].split(" ")
            if len(temp) == 1:
                memory[i] = WordToNum[test[i]]
            elif temp[0] == 'DAT' and len(temp[1]) == 2:
                memory[i] = '0' + temp[1]
            elif len(temp) == 2:
                memory[i] = WordToNum[temp[0]] + temp[1]
        return memory

    # def export(file):
    #     exportstring = ""
    #     if file:
    #         for i in range(len(file)):
    #             for e in range(len(file[i])):
    #                 exportstring += file[i][e]
    #             exportstring += "%"
    #         pygame.scrap.put_text(exportstring)
    #         return True
    #     else:
    #         return False



    #Fonts
    base_font = pygame.font.Font("sfx/CourierPrime-Regular.ttf", 20)
    Base_font = pygame.font.Font("sfx/Pixeltype.ttf", 25)
    Small_font = pygame.font.Font("sfx/Pixeltype.ttf", 20)
    Bigger_font = pygame.font.Font("sfx/Pixeltype.ttf", 35)
    Biggest_font = pygame.font.Font("sfx/Pixeltype.ttf", 50)

    #CPU surface
    cpu_surf = pygame.image.load("sfx/CPU.png").convert_alpha()
    cpu_surf_rect = cpu_surf.get_rect(topleft=(395, 250))

    #Wire surface
    wire_surf = pygame.image.load("sfx/wire.png").convert_alpha()
    wire_surf_rect = wire_surf.get_rect(topright = (690, 35))

    #memory grid
    grid_surf = pygame.image.load("sfx/grid.png").convert_alpha()
    grid_surf_rect = grid_surf.get_rect(topright = (Width, 0))

    #output surface
    output_surf = pygame.Surface((100, 200))
    output_surf.fill("#CBC3E3")
    output_surf_rect = output_surf.get_rect(bottomleft = (cpu_surf_rect.left, cpu_surf_rect.top - 50))
    output = []
    outoffset = 0

    #input
    input_surf = pygame.Surface((100, 50))
    input_surf.fill("Cyan")
    input_surf_rect = input_surf.get_rect(midleft = (output_surf_rect.midright))
    inp = []

    #Text vars
    memory = ["000" for i in range(100)]
    PC, IR, ADR, ACC = 0, 0, 0, 0

    #Changable vars
    done = True
    step = 2
    typing = False
    TempPC = PC
    pause = False
    # wait = False
    phase2 = False
    phase1 = True
    # wskip = False
    skip = False
    delay = 0
    delay1 = 0
    Run = False

    #List of dialougue
    dialouge = ["The Program Counter has the memory address of\nthe instruction to be executed next.", "The address is copied to the MAR from the Program Counter", "" ]

    #Instantiate dots
    dot1 = dot("Red")
    dot2 = dot("Red")
    
    #phase1 items:
    #DisplayTyped
    Instructions = []
    dispt_surface = pygame.Surface((100, 800))
    dispt_surface.fill("Green")
    dispt_surface_rect = dispt_surface.get_rect(midtop = (325, 0))
    offset1 = 0 #Amount scrolled

    #Display entry
    entry_surf = pygame.surface.Surface((250, 600))
    entry_surf_rect = entry_surf.get_rect(topleft = (0, 50))
    entry_surf.fill("Green")
    guide = base_font.render("|", False, "Orange")
    guide_rect = guide.get_rect(center = (0,0))
    screen.fill("White")
    entry = [[]]
    x = 0
    y = 0
    clicked = False
    offset = 0
    Temp2 = [[]]
    #submit
    submit_surf = base_font.render("SUBMIT", True, "Black")
    submit_surf_rect = submit_surf.get_rect(bottomleft = (0, height))
    clear_surf = base_font.render("CLEAR", True, "Black")
    clear_surf_rect = clear_surf.get_rect(bottomleft = (submit_surf_rect.right, height))
    #run
    run_surf = base_font.render("RUN CODE", True, "Black")
    run_surf_rect = run_surf.get_rect(bottomleft = (clear_surf_rect.right, height))
    #reset
    reset_surf = base_font.render("RESET", True, "Black")
    reset_surf_rect = reset_surf.get_rect(bottomleft = (submit_surf_rect.topleft))

    #no animation
    noanim_surf = base_font.render("Hyper", True, "Black")
    noanim_surf_rect = reset_surf.get_rect(midleft = (reset_surf_rect.midright))

    #speed up down
    spddown_surf = base_font.render("<<", True, "Black")
    speed_surf = base_font.render("SPEED", True, "Black")
    spdup_surf = base_font.render(">>", True, "Black")

    spddown_surf_rect = spddown_surf.get_rect(bottomleft = (reset_surf_rect.topleft))
    speed_surf_rect = speed_surf.get_rect(midleft = (spddown_surf_rect.midright))
    spdup_surf_rect = speed_surf.get_rect(midleft = (speed_surf_rect.midright))
    #wait
    # wait_surf = base_font.render("WAIT", True, "Black")
    # wait_surf_rect = wait_surf.get_rect(midleft = (noanim_surf_rect.midright))
    #pause
    pause_surf = base_font.render("PAUSE", True, "Black")
    pause_surf_rect = pause_surf.get_rect(midleft = (spdup_surf_rect.midright))
    pause_color = "Green"
    Allowed = ['0', '9', '8', '7', '6', '5', '4', '3', '2', '1', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
    #define the person images
    panim_1 = pygame.image.load('sfx/person/p1.png').convert_alpha()
    panim_2 = pygame.image.load('sfx/person/p2.png').convert_alpha()
    panim_3 = pygame.image.load('sfx/person/p3.png').convert_alpha()
    panim_4 = pygame.image.load('sfx/person/p4.png').convert_alpha()
    panim_5 = pygame.image.load('sfx/person/p5.png').convert_alpha()
    panim_6 = pygame.image.load('sfx/person/p6.png').convert_alpha()
    panim_7 = pygame.image.load('sfx/person/p7.png').convert_alpha()
    panim_8 = pygame.image.load('sfx/person/p8.png').convert_alpha()
    panim_9 = pygame.image.load('sfx/person/p9.png').convert_alpha()
    panim_10 = pygame.image.load('sfx/person/p10.png').convert_alpha()

    panim = [panim_1, panim_2, panim_3, panim_4, panim_5, panim_6, panim_7, panim_8, panim_9, panim_10]
    for i in panim:
        temp = pygame.transform.scale(i, (128,128))
        i = temp
    panim_index = 0
    panim_surface = panim_1
    gone = False

    #export button

    # animation for person talking
    def personanimation(panim_index, panim_surface, panim):
        panim_index += 0.24
        if panim_index > 9: panim_index = 0
        panim_surface = panim[int(panim_index)]
        return (panim_index, panim_surface, panim)

    #blitting phase2 stuff
    screen.fill("White")
    screen.blit(output_surf, output_surf_rect)
    screen.blit(input_surf, input_surf_rect)
    screen.blit(grid_surf, grid_surf_rect)
    screen.blit(wire_surf, wire_surf_rect)
    screen.blit(cpu_surf, cpu_surf_rect)
    pygame.draw.line(screen, "Gray", (430,output_surf_rect.bottom), (430,cpu_surf_rect.top), 30)
    pygame.draw.line(screen, "Gray", (input_surf_rect.midbottom), (input_surf_rect.midbottom[0], cpu_surf_rect.top), 30)
    memory = blitmem(memory)
    updateCPU(PC,IR, ADR, ACC)
    while True:
        while phase1:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:

                    # export(entry)
                    pygame.quit()
                    exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if submit_surf_rect.collidepoint(pygame.mouse.get_pos()):
                        Temp2 = []
                        for i in entry:
                            Temp2.append(convstring(i))
                        poplis = []
                        i = 0
                        for i in range(len(Temp2)):
                            Temp2[i] = Temp2[i].strip()
                            if Temp2[i] == "":
                                poplis.append(i)
                        poplis = poplis[::-1]
                        for i in poplis:
                            Temp2.pop(i)
                            entry.pop(i)
                        Temp2 = check(Temp2)
                        if Temp2[1] is True:
                            Run = True
                            Instructions = Temp2[0]
                        else:
                            Run = False
                            Instructions = [Temp2[0]]
                    x, y = (pygame.mouse.get_pos())
                    if entry_surf_rect.collidepoint(x, y):
                        clicked = True
                        x = round(((x - 1) / 12) + 0.01)
                        y = round((y + offset) / 15 + 0.01) - 4
                        if entry == []:
                            entry = [[]]
                        if y >= len(entry): y = len(entry) - 1
                        if x > len(entry[y]): x = len(entry[y])
                    elif clear_surf_rect.collidepoint(x, y):
                        Run = False
                        entry = [[]]
                    elif run_surf_rect.collidepoint(x, y):
                        if Run is True:
                            memory = convass(Instructions)
                            phase1, phase2 = False, True
                            PC, IR, ADR, ACC = 0, 0, 0, 0
                            done = True
                            step = 2
                            typing = False
                            TempPC = PC
                            pause = False
                            # wait = False
                            # wskip = False
                            skip = False
                            delay = 0
                            delay1 = 0
                            inp =[]
                            output = []
                    else:
                        clicked = False


                if event.type == pygame.MOUSEWHEEL:
                    if dispt_surface_rect.collidepoint(pygame.mouse.get_pos()):
                        if offset1 < ((len(Instructions)) * 10) and event.y > 0:
                            offset1 += 10
                        elif event.y < 0 and offset1 > 0:
                            offset1 += -10
                    if entry_surf_rect.collidepoint(pygame.mouse.get_pos()) and False is True:
                        if offset <= ((len(entry))* 15) and event.y > 0:
                            offset += 15
                        elif event.y < 0  and offset > 0:
                            offset += -15

                if event.type == pygame.KEYDOWN:
                    if clicked == True:
                        if event.key == pygame.K_BACKSPACE:
                            if x == 0 and y != 0 and len(entry[y]) == 0:
                                x = len(entry[y-1])
                                entry[y-1] += entry[y]
                                y -= 1
                                entry.pop(y+1)
                            elif x != 0:
                                entry[y].pop(x-1)
                                x -= 1

                        elif event.key == pygame.K_RETURN:
                            if len(entry) < 40:
                                entry.insert(y + 1, entry[y][x:])
                                entry[y] = entry[y][:x]
                                y += 1
                                x = 0

                        elif y != 0 and event.key == pygame.K_UP:
                            if x > len(entry[y-1]): x = len(entry[y-1])
                            y -= 1

                        elif y < len(entry)-1 and event.key == pygame.K_DOWN:
                            if x > len(entry[y+1]): x = len(entry[y+1])
                            y += 1

                        elif event.key == pygame.K_RIGHT and (x,y) != (len(entry[len(entry)-1]), len(entry)-1):
                            if x == len(entry[y]):
                                x = 0
                                y += 1
                            else:
                                x += 1

                        elif event.key == pygame.K_LEFT and (x, y) != (0, 0):
                            if x == 0:
                                x = len(entry[y-1])
                                y -= 1
                            else:
                                x -= 1

                        elif x < 19:
                            if event.key == pygame.K_SPACE or event.unicode.lower() in Allowed:
                                entry[y].insert(x, event.unicode)
                                x += 1
            #output = scrollout(output, outoffset, 20, output_surf_rect, Bigger_font)
            screen.blit(entry_surf, entry_surf_rect)
            entry = disp(entry, offset)
            if clicked == True and y * 15 >= offset:
                guide_rect.center = (x * 12, (y * 15 - offset) + 60)
                screen.blit(guide, guide_rect)
            screen.blit(dispt_surface, dispt_surface_rect)
            pygame.draw.rect(screen, "Green", submit_surf_rect)
            screen.blit(submit_surf, (submit_surf_rect))
            pygame.draw.rect(screen, "Red", clear_surf_rect)
            screen.blit(clear_surf, (clear_surf_rect))
            pygame.draw.rect(screen, "Cyan", run_surf_rect)
            screen.blit(run_surf, (run_surf_rect))
            pygame.draw.rect(screen, "Red", reset_surf_rect)
            screen.blit(reset_surf, reset_surf_rect)
            pygame.draw.rect(screen, "Cyan", noanim_surf_rect)
            screen.blit(noanim_surf, noanim_surf_rect)
            pygame.draw.rect(screen, "#fed8b1", spddown_surf_rect)
            screen.blit(spddown_surf, spddown_surf_rect)
            pygame.draw.rect(screen, "orange", speed_surf_rect)
            screen.blit(speed_surf, speed_surf_rect)
            pygame.draw.rect(screen, "#fed8b1", spdup_surf_rect)
            screen.blit(spdup_surf, spdup_surf_rect)
            pygame.draw.rect(screen, pause_color, pause_surf_rect)
            screen.blit(pause_surf, pause_surf_rect)
            # pygame.draw.rect(screen, "Orange", wait_surf_rect)
            # screen.blit(wait_surf, wait_surf_rect)
            Instructions = addLis(Instructions, offset1)
            (panim_index, panim_surface, panim) = personanimation(panim_index, panim_surface, panim)
            panim_surface_rect = panim_surface.get_rect(topleft=(675, 600))
            screen.blit(panim_1 , panim_surface_rect)
            pygame.display.update()
            await asyncio.sleep(0)  # Very important, and keep it 0

            if not count_down:
                return

            count_down = count_down - 1
            clock.tick(60)

        while phase2:
            while typing is False:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit()
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        if spdup_surf_rect.collidepoint(pygame.mouse.get_pos()):
                            if dot1.speed < 50:
                                dot1.speed += 2
                                dot2.speed += 2
                                step += 2
                        elif spddown_surf_rect.collidepoint(pygame.mouse.get_pos()):
                            if dot1.speed != 2:
                                dot1.speed -= 2
                                dot2.speed -= 2
                                step -= 2
                        elif pause_surf_rect.collidepoint(pygame.mouse.get_pos()):
                            if pause is False:
                                pause = True
                                pause_color = "red"
                            else:
                                pause = False
                                pause_color = "Green"
                        # elif wait_surf_rect.collidepoint(pygame.mouse.get_pos()):
                        #     if wait is False:
                        #         wait = True
                        #     elif wait is True:
                        #         if pause is True: pause = False
                        #         wait = False
                        # elif noanim_surf_rect.collidepoint(pygame.mouse.get_pos()):
                        #     if wskip is False:
                        #         wskip = True
                        #     elif wskip is True:
                        #         wskip, skip = False, False
                    elif event.type == pygame.MOUSEWHEEL:
                        if output_surf_rect.collidepoint(pygame.mouse.get_pos()):
                            if event.y < 0 and outoffset > (len(output) - 1) * -10:
                                outoffset -= 20
                            elif event.y > 0 and outoffset < 0:
                                outoffset += 20
                if 0 > PC > 99 or abs(ACC) >= 1000:
                    phase1, phase2 = True, False
                    break
                if skip is True and pause is False:
                    IR = memory[PC][0]
                    ADR = memory[PC][1:]
                    PC += 1
                    if IR == '0':
                        phase1, phase2 = True, False
                        break
                    elif IR == "1":
                        ACC += int(memory[int(ADR)])
                    elif IR == "2":
                        ACC -= int(memory[int(ADR)])
                    elif IR == "3":
                        memory[int(ADR)] = (3 - len(str(ADR))) * "0" + str(ACC)
                    elif IR == "5":
                        ACC = int(memory[int(ADR)])
                    elif IR == "6":
                        PC = int(ADR)
                    elif IR == "7":
                        if ACC == 0:
                            PC = int(ADR)
                    elif IR == "8":
                        if ACC >= 0:
                            PC = int(ADR)
                    elif IR == "9":
                        if ADR == "01":
                            if typing is False:
                                typing = True
                            else:
                                ACC = int(dot1.value)
                        elif ADR == "02":
                            output.append(str(ACC))
                        elif ADR == "22":
                            if ACC > 0:
                                output.append(chr(ACC))
                        else:
                            phase1, phase2 = True, False
                    else:
                        phase1, phase2 = True, False

                elif done is True and pause is False and delay >= delay1: #Fetch cycle
                    if dot1.phase == 0:
                        TempPC = PC
                        dot1.setcoord(420, 270)
                        dot2.setcoord(420, 270)
                        dot1.value, dot2.value = str(PC), str(PC)
                        dot1.phase, dot2.phase = (1, 1)
                    elif dot1.phase == 1:
                        dot1.iphase, dot2.iphase = -1, -1
                        dot1.travelmem()
                        dot2.travelmem()
                        if dot1.iphase == 0:
                            dot1.phase, dot2.phase = 2, 2
                            dot1.target = TempPC
                    elif dot1.phase == 2:
                        dot1.travelmem()
                        if dot1.iphase == 5:
                            dot1.value = memory[TempPC]
                            dot1.color = "Cyan"
                        elif dot1.iphase == 10:
                            ADR = int(memory[TempPC][1:])
                        elif dot1.iphase == 100:
                            IR = int(memory[TempPC][:1])
                            dot1.setcoord(-10, -10)
                        dot2.travelALU()
                        if dot2.iphase == 1 and dot2.x >= 460:
                            dot2.value = str(PC + 1)
                            dot2.color = "Cyan"
                        elif dot2.iphase == 2:
                            dot2.value = str(PC + 1)
                            dot2.color = "Cyan"
                        elif dot2.iphase == 100:
                            PC = int(dot2.value)
                            dot2.setcoord(-10, -10)
                        if dot2.iphase == 100 and dot1.iphase == 100:
                            dot1.reset()
                            dot2.reset()
                            # if wait is True:
                            #     pause = True
                            delay = pygame.time.get_ticks()
                            delay1 = delay + 250
                            done = False
                elif pause is False and done is False and delay >= delay1:
                    if IR == 1 or IR == 2 or IR  == 5: #ADD, SUB, LDA
                        if dot1.phase == 0:
                            dot1.phase = 1
                            dot1.setcoord(430, 370)
                            dot1.target = ADR
                            dot1.iphase = -1
                            dot1.value = str(ADR)
                        dot1.travelmem()
                        if dot1.iphase == 5:
                            dot1.value = memory[ADR]
                            dot1.color = "Cyan"
                        elif dot1.iphase == 8 and dot1.y <= 420:
                            dot1.iphase = 11
                        elif dot1.iphase == 9:
                            dot.iphase = 11
                        elif dot1.iphase == 100:
                            if IR == 1: ACC += int(dot1.value)
                            elif IR == 2: ACC -= int(dot1.value)
                            else: ACC = int(dot1.value)
                            dot1.reset()
                            done = True
                    elif IR == 3: #STA
                        if dot1.phase == 0:
                            dot1.setcoord(430, 370)
                            dot2.setcoord(430, 420)
                            dot1.phase, dot2.phase = 1, 1
                            dot1.target, dot2.target = ADR, ADR
                            dot1.value, dot2.value = str(ADR), str(ACC)
                            dot1.iphase, dot2.iphase = -1, -1
                            dot2.color = "Cyan"
                        dot1.travelmem()
                        dot2.travelmem()
                        if dot2.iphase == 5:
                            dot2.iphase = 100
                        if dot1.iphase == 5:
                            memory[ADR] = "0"*(3-len(dot2.value))+(dot2.value)
                            dot1.reset()
                            dot2.reset()
                            done = True
                    elif IR == 6 or IR == 7 or IR == 8:
                        if dot1.phase == 0:
                            if IR == 7:
                                if ACC == 0:
                                    dot1.phase, dot1.value, dot1.iphase = 1, str(ADR), 0
                                    dot1.setcoord(430, 370)
                                else:
                                    dot1.reset()
                                    done = True
                            elif IR == 8:
                                if ACC >= 0:
                                    dot1.phase, dot1.value, dot1.iphase = 1, str(ADR), 0
                                    dot1.setcoord(430, 370)
                                else:
                                    dot1.reset()
                                    done = True
                            else:
                                dot1.phase, dot1.value, dot1.iphase = 1, str(ADR), 0
                                dot1.setcoord(430, 370)
                        elif dot1.phase == 1:
                            dot1.my(270)
                            if dot1.iphase > 0:
                                PC = int(dot1.value)
                                dot1.reset()
                                done = True
                    elif IR == 9:
                        if ADR == 22 or ADR == 2:
                            if dot1.phase == 0:
                                dot1.value, dot1.phase, dot1.iphase = str(ACC), 1, 0
                                dot1.my(output_surf_rect.bottom)
                                dot1.setcoord(430, 420)
                            dot1.my(output_surf_rect.bottom)
                            if dot1.iphase == 1:
                                if ADR == 22:
                                    if ACC != 0:
                                        output.append(chr(int(dot1.value)))
                                elif ADR == 2:
                                    output.append(dot1.value)
                                dot1.reset()
                                done = True
                        elif ADR == 1:
                            if dot1.phase == 0:
                                dot1.value, dot1.phase, dot1.iphase = str(ACC), 1, 0
                                dot1.setcoord(430, 420)
                            elif dot1.iphase == 0:
                                dot1.my(270)
                            elif dot1.iphase == 1:
                                dot1.px(input_surf_rect.midbottom[0])
                            elif dot1.iphase == 2:
                                dot1.my(input_surf_rect.midbottom[1])
                            elif dot1.iphase == 3:
                                typing = True
                                dot1.setcoord(-10, -10)
                            elif dot1.iphase == 4:
                                if dot1.phase == 1:
                                    dot1.phase = 2
                                    dot1.setcoord(input_surf_rect.midbottom[0], input_surf_rect.midbottom[1])
                                elif dot1.phase == 2:
                                    dot1.py(270)
                            elif dot1.iphase == 5:
                                dot1.mx(430)
                            elif dot1.iphase == 6:
                                dot1.py(420)
                                if dot1.iphase == 7:
                                    dot1.iphase, ACC, done = 100, int(dot1.value), True
                                    dot1.reset()
                        else:
                            phase1, phase2 = True, False
                            break
                    if done is True and dot1.x == -10:
                        delay = pygame.time.get_ticks()
                        delay1 =  delay+250
                        # if wait is True: pause = True
                        # if wskip is True: skip = True
                    elif IR == 0 or IR == 4:
                        phase1, phase2 = True, False
                        break


                screen.fill("White")
                screen.blit(output_surf, output_surf_rect)
                screen.blit(input_surf, input_surf_rect)
                screen.blit(grid_surf, grid_surf_rect)
                screen.blit(wire_surf, wire_surf_rect)
                screen.blit(cpu_surf, cpu_surf_rect)
                pygame.draw.line(screen, "Gray", (430,output_surf_rect.bottom), (430,cpu_surf_rect.top), 30)
                pygame.draw.line(screen, "Gray", (input_surf_rect.midbottom), (input_surf_rect.midbottom[0], cpu_surf_rect.top), 30)
                memory = blitmem(memory)
                updateCPU(PC, IR, ADR, ACC)
                output = scrollout(output, outoffset, 20, output_surf_rect, Bigger_font)
                dot1.update()
                dot2.update()
                screen.blit(entry_surf, entry_surf_rect)
                screen.blit(dispt_surface, dispt_surface_rect)
                pygame.draw.rect(screen, "Green", submit_surf_rect)
                screen.blit(submit_surf, (submit_surf_rect))
                pygame.draw.rect(screen, "Red", clear_surf_rect)
                screen.blit(clear_surf, (clear_surf_rect))
                pygame.draw.rect(screen, "Cyan", run_surf_rect)
                screen.blit(run_surf, (run_surf_rect))
                pygame.draw.rect(screen, "Red", reset_surf_rect)
                screen.blit(reset_surf, reset_surf_rect)
                pygame.draw.rect(screen, "Cyan", noanim_surf_rect)
                screen.blit(noanim_surf, noanim_surf_rect)
                pygame.draw.rect(screen, "#fed8b1", spddown_surf_rect)
                screen.blit(spddown_surf, spddown_surf_rect)
                pygame.draw.rect(screen, "orange", speed_surf_rect)
                screen.blit(speed_surf, speed_surf_rect)
                pygame.draw.rect(screen, "#fed8b1", spdup_surf_rect)
                screen.blit(spdup_surf, spdup_surf_rect)
                pygame.draw.rect(screen, pause_color, pause_surf_rect)
                screen.blit(pause_surf, pause_surf_rect)
                # pygame.draw.rect(screen, "Orange", wait_surf_rect)
                # screen.blit(wait_surf, wait_surf_rect)
                Instructions = addLis(Instructions, offset1)
                (panim_index, panim_surface, panim)= personanimation(panim_index, panim_surface, panim)
                panim_surface_rect = panim_surface.get_rect(topleft=(675, 600))
                screen.blit(panim_surface, panim_surface_rect)
                pygame.display.update()
                await asyncio.sleep(0)  # Very important, and keep it 0

                if not count_down:
                    return

                count_down = count_down - 1
                delay = pygame.time.get_ticks()
                clock.tick(60)
            while typing is True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit()
                    elif event.type == pygame.KEYDOWN:
                        if event.unicode.isnumeric() and len(inp) < 3:
                            inp.append(event.unicode)
                        elif event.key == pygame.K_BACKSPACE and len(inp) > 0:
                            inp.pop(-1)
                        elif event.key == pygame.K_RETURN and inp:
                            dot1.value, typing, dot1.iphase = str(convstring(inp)), False, 4
                            inp = []
                        # elif event.key == pygame.K_RSHIFT:
                            # if wskip is False: wskip = True
                            # else: wksip, skip = False, False
                screen.blit(input_surf, input_surf_rect)
                screen.blit(Biggest_font.render(convstring(inp), True, "Black"), (input_surf_rect.topleft))
                pygame.display.update()
                await asyncio.sleep(0)  # Very important, and keep it 0

                if not count_down:
                    return

                count_down = count_down - 1
                clock.tick(60)

asyncio.run(main())