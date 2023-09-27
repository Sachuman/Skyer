# cse30
# pa5
#file = skyland.py
# skyland.py - a two-level platform video game
# author: Sachin Jain
# date: 9 June, 2023

from tkinter import *
import tkinter.font as font
from random import random, randint # optional
from math import sin, cos, pi, radians# optional
#from pygame import mixer # do not use it in the submitted version

WIDTH, HEIGHT = 600, 400 # global variables (constants) go here
CLOCK_RATE = 15
START_X, START_Y = 20, 350
END_X, END_Y = 400, 350

class Skyland:

    def __init__(self, canvas):

        self.canvas = canvas
        self.canvas.bind_all('<KeyPress-space>', self.pause)
        self.canvas.bind_all('<KeyPress-Alt_L>', self.restart)
        self.paused = False
        self.land = Land(canvas)
        self.AI1 = AI_jelly(canvas, 100, 40)
        self.AI2 = AI_jelly(canvas, 500, 105)
        self.AI3 = AI_jelly(canvas, 300, 205)
        self.AI11 = AI(canvas, 55, 220)
        self.AI22 = AI(canvas, 500, 125)
        self.trophy = Trophy(canvas)
        self.avatar = Avatar(canvas)
        self.text = canvas.create_text(150, 370, text='Score ?  Time ? ',
                                       font=font.Font(family='Helveca', size=15, weight='bold'))
        self.time = 0
        self.score = 0
        #self.play_music() # do not include it in the submitted version
        self.update()


    def restart(self, event=None):

        self.avatar.replace()
        self.trophy.replace()
        self.canvas.bind_all('<KeyPress-space>', self.pause)
        self.time = 0
        self.score = 0
        self.paused = False
        self.canvas.delete(self.text)
        self.text = canvas.create_text(150, 370, text='Score ?  Time ? ',
                                       font=font.Font(family='Helveca', size=15, weight='bold'))


      #  self.sound.stop() # do not use sounds in the submitted version
      #  self.sound.play()


    def pause(self, event=None):
        self.paused = not self.paused



    def update(self):
        if not self.paused:
            self.time += 1
            minute = self.time//60
            second = self.time%60

            time_text = f'Score: {self.score} Time: {minute:02d}:{second:02d}'
            if self.avatar.find_trophy(self.trophy.get_trophy()):
                self.score += 1
            self.canvas.itemconfig(self.text, text=time_text)
            self.avatar.update(self.land, self.trophy)
            self.AI1.update()
            self.AI2.update()
            self.AI3.update()
            self.AI11.update(5, 200, True)
            self.AI22.update(5, 100, True)


            self.land.update(self.land.w, 550, 300)



        self.canvas.after(CLOCK_RATE, self.update)
        avatar_coords = self.canvas.coords(self.avatar.head)
        if self.AI1.check_collision(avatar_coords):
            self.paused = True
            self.canvas.delete(self.text)
            self.canvas.unbind_all('<KeyPress-space>')
            self.text = canvas.create_text(150, 370, text='              YOU DIED! PRESS ALT_L TO RESTART ',
                                           font=font.Font(family='Helveca', size=15, weight='bold'))
        if self.AI2.check_collision(avatar_coords):
            self.paused = True
            self.canvas.delete(self.text)
            self.canvas.unbind_all('<KeyPress-space>')
            self.text = canvas.create_text(150, 370, text='              YOU DIED! PRESS ALT_L TO RESTART ',
                                           font=font.Font(family='Helveca', size=15, weight='bold'))
        if self.AI3.check_collision(avatar_coords):
            self.paused = True
            self.canvas.delete(self.text)
            self.canvas.unbind_all('<KeyPress-space>')
            self.text = canvas.create_text(150, 370, text='              YOU DIED! PRESS ALT_L TO RESTART ',
                                           font=font.Font(family='Helveca', size=15, weight='bold'))

        if self.AI11.check_collision(avatar_coords):
            self.paused = True
            self.canvas.delete(self.text)
            self.canvas.unbind_all('<KeyPress-space>')
            self.text = canvas.create_text(150, 370, text='              YOU DIED! PRESS ALT_L TO RESTART ',
                                           font=font.Font(family='Helveca', size=15, weight='bold'))
        if self.AI22.check_collision(avatar_coords):
            self.paused = True
            self.canvas.delete(self.text)
            self.canvas.unbind_all('<KeyPress-space>')
            self.text = canvas.create_text(150, 370, text='              YOU DIED! PRESS ALT_L TO RESTART ',
                                           font=font.Font(family='Helveca', size=15, weight='bold'))
        if self.score == 6:
            self.paused = True
            self.canvas.delete(self.text)
            self.canvas.unbind_all('<KeyPress-space>')
            self.text = canvas.create_text(150, 370, text='              YOU WIN !!! PRESS ALT_L to restart',
                                           font=font.Font(family='Helveca', size=15, weight='bold'))
  # def play_music(self): # optional, do not use it in the submitted version
    #    if not mixer.get_init():
    #        mixer.init()
    #    self.sound = mixer.Sound('./sound1.mp3')
    #    self.sound.play()

class Land:

    def __init__(self, canvas):

        self.canvas = canvas

        # sky
        self.canvas.create_rectangle( 0, 0, WIDTH, START_Y-100,
                                 fill='cyan4')
        # valley
        self.canvas.create_rectangle( 0, START_Y-120, WIDTH, START_Y,
                                 fill='cyan2')
        self.platforms = []

        self.make_hill( 50, 230, 250, 230, height=100, delta=3)
        self.make_hill(150, 300, 350, 300, height=100, delta=3)
        self.make_hill(250, 250, 450, 250, height=100, delta=3)
        self.make_hill(350, 300, 550, 300, height=100, delta=3)

        self.ground = self.cases(0, 0, START_X-10, HEIGHT-45)
        self.left = self.cases(END_X+190, 0, WIDTH, HEIGHT-45)
        self.right = self.cases(0, 350 , WIDTH+10, 355)
        self.third = self.cases(325, 150, 330, 335)
        self.yo = self.cases(240, HEIGHT-150, 330, HEIGHT-45)
        self.yo1 =self.cases(325, HEIGHT-80, 450, HEIGHT-45)

        self.w = self.cases(360, 100, 410, 106)
        self.ww = self.cases(160, 100, 210, 106)

        self.first = self.cases(325, 250, 420, 290)
        self.second = self.cases(100, 250, 105, 355)
        self.fourth = self.cases(0, HEIGHT/2-50, 150, HEIGHT/2-46 )
        self.fifth = self.cases(0, HEIGHT/2+46, 50, HEIGHT/2+50)
        self.sixth =  self.cases(WIDTH-100, HEIGHT/2-50, WIDTH, HEIGHT/2-46)
        self.webs(75, 100)
        self.webs(300, 190)
        self.webs(500, 190)
        self.din = 1.25
        self.sped = -0.5
        self.platforms.append(self.w)
        self.platforms.append(self.ground)
        self.platforms.append(self.left)
        self.platforms.append(self.right)
        self.platforms.append(self.first)
        self.platforms.append(self.yo)
        self.platforms.append(self.yo1)
        self.platforms.append(self.second)
        self.platforms.append(self.third)
        self.platforms.append(self.fourth)
        self.platforms.append(self.fifth)
        self.platforms.append(self.sixth)
        self.platforms.append(self.ww)
        startsy = 330
        endsy = 360

        for i in range(0, 6):
            start_y = 150 + (i * 10)
            end_y = start_y + 32
            self.canvas.create_line(startsy, start_y, endsy, end_y, fill='green', width=5)
        startsy = 324
        endsy = 294

        for i in range(0, 6):
            start_y = 150 + (i * 10)
            end_y = start_y + 32
            self.canvas.create_line(startsy, start_y, endsy, end_y, fill='green', width=5)

        start_x = 99
        end_x = 69

        for i in range(0, 6):
            start_y = 250 + (i * 10)
            end_y = start_y + 32

            self.canvas.create_line(start_x, start_y, end_x, end_y, fill='green', width=5)
        start_x = 105
        end_x = 135

        for i in range(0, 6):
            start_y = 250 + (i * 10)
            end_y = start_y + 32
            self.canvas.create_line(start_x, start_y, end_x, end_y, fill='green', width=5)

        self.canvas.create_arc(10, 50, 300, -30, start=180, extent=60, outline='green', width=10, style="arc")
        self.canvas.create_arc(10, 80, 300, 0, start=180, extent=65, outline='green', width=10, style="arc")
        self.canvas.create_arc(10, 110, 300, 30, start=180, extent=72, outline='green', width=10, style="arc")
        self.canvas.create_arc(10, 140, 300, 60, start=180, extent=78, outline='green', width=10, style="arc")

        self.canvas.create_arc(520, 40, 605, -30, start=-30, extent=-120, outline='green', width=10, style="arc")
        self.canvas.create_arc(490, 70, 610, 0, start=-30, extent=-120, outline='green', width=10, style="arc")
        self.canvas.create_arc(460, 100, 610, 30, start=-30, extent=-120, outline='green', width=10, style="arc")
        self.canvas.create_arc(430, 130, 610, 60, start=-30, extent=-120, outline='green', width=10, style="arc")

        self.canvas.create_arc(23, 235, 43, 245, start=180, extent=180, outline='brown', width=10, style="arc")
        self.canvas.create_arc(310, 150, 330, 160, start=180, extent=180, outline='brown', width=10, style="arc")
        self.canvas.create_arc(560, 140, 580, 150, start=180, extent=180, outline='brown', width=10, style="arc")


        cloud1 = self.make_cloud(100, 120)
        cloud2 = self.make_cloud(300, 50)
        cloud3 = self.make_cloud(480, 100)
        self.clouds = [cloud1, cloud2, cloud3]


    def make_hill(self, x1, y1, x2, y2, height=100, delta=3):
        midpoint = (x1 + x2) / 2
        hill = self.canvas.create_polygon(x1, y1, midpoint, y1 - height, x2+delta, y1, fill='white')
        return hill

    def make_cloud(self, x, y):
        cloud = self.canvas.create_oval(x, y, x + 75, y + 40, fill='grey', outline='black')
        return cloud

    def cases(self, x1, y1, x2, y2):
        platforms = self.canvas.create_rectangle(x1, y1, x2, y2, fill = 'light green', outline = 'black')
        return platforms

    def get_obstacles(self):
        return self.platforms

    def webs(self, x, y):
        octalist = []
        shushush = 45
        sachasch = 8
        wooh = 75
        for i in range(sachasch):
            angle = radians(i * shushush)
            joji = x + wooh * cos(angle)
            factors = y + wooh * sin(angle)
            octalist.append((joji, factors))
            self.canvas.create_line(x, y, joji, factors, fill='ivory2', width=3)

        for i in range(sachasch - 8):
            firstx, secondy = octalist[i]
            joji, factors = octalist[(i + 1) % sachasch]
            self.canvas.create_line(firstx, secondy, joji, factors, fill='ivory2', width=3)
        for j in range(6):
            wooh -= 20
            andri = []

            for i in range(sachasch):
                angle = radians(i * shushush)
                joji = x + wooh * cos(angle)
                factors = y + wooh * sin(angle)
                andri.append((joji, factors))
                self.canvas.create_line(x, y, joji, factors, fill='ivory2', width=3)

            for i in range(sachasch):
                firstx, secondy = andri[i]
                joji, factors = andri[(i + 1) % sachasch]
                self.canvas.create_line(firstx, secondy, joji, factors, fill='ivory2', width=3)

    def update(self, z, X, Y):
        coordsofmovingrec = self.canvas.coords(z)
        x1, y1, x2, y2 = coordsofmovingrec

        maxkijai = X
        minkijai = Y


        if x2 >= maxkijai and self.din == 1.25 and self.sped == -0.5:
            self.din = -1.25
            self.sped = 0.5
        elif x1 <= minkijai and self.din == -1.25 and self.sped == 0.5:
            self.din = 1.25
            self.sped = -0.5

        self.canvas.move(self.w,  self.din, self.sped)

class Trophy:

    def __init__(self, canvas):

        self.canvas = canvas
        purple_egg = self.canvas.create_oval(12, 140, 32, 150, fill='orchid')
        pink_egg = self.canvas.create_oval(565, 15, 585, 25, fill='pink')
        red_egg = self.canvas.create_oval(310, 150, 330, 160, fill='red')
        blue_egg = self.canvas.create_oval(22, 235, 42, 245, fill='blue')
        yellow_egg = self.canvas.create_oval(330, 308, 350, 318, fill='yellow')
        green_egg = self.canvas.create_oval(560, 140, 580, 150, fill='green')

        self.trophies = [purple_egg, pink_egg, red_egg, blue_egg, yellow_egg, green_egg]

    def get_trophy(self):
        return self.trophies

    def replace(self):
        for i in self.trophies:
          self.canvas.delete(i)

        purple_egg = self.canvas.create_oval(12, 140, 32, 150, fill='orchid')
        pink_egg = self.canvas.create_oval(565, 15, 585, 25, fill='pink')
        red_egg = self.canvas.create_oval(310, 150, 330, 160, fill='red')
        blue_egg = self.canvas.create_oval(22, 235, 42, 245, fill='blue')
        yellow_egg = self.canvas.create_oval(330, 308, 350, 318, fill='yellow')
        green_egg = self.canvas.create_oval(560, 140, 580, 150, fill='green')

        self.trophies = [purple_egg, pink_egg, red_egg, blue_egg, yellow_egg, green_egg]

class AI_jelly:

    def __init__(self, canvas, x, y):

        self.canvas = canvas

        self.thread = self.canvas.create_line(x+10, 0, x+10, y+5,
                                          fill='ivory2', width=3)
        self.spider = self.make_spider(x, y)
        self.x, self.y = 0, 0.5

        self.movingleft = True


    def make_spider(self, x, y):

        color1 = 'black'
        body = canvas.create_oval(5, 5, 35, 20, fill=color1)  # Body of the crab
        leg1 = canvas.create_line(5, 20, 5, 40, fill=color1, width=4)  # First leg
        leg2 = canvas.create_line(15, 20, 15, 40, fill=color1, width=4)  # Second leg
        leg3 = canvas.create_line(25, 20, 25, 40, fill=color1, width=4)  # Third leg
        leg4 = canvas.create_line(35, 20, 35, 40, fill=color1, width=4)  # Fourth leg
        claw1 = canvas.create_polygon(0, 20, 10, 20, 10, 10, fill=color1)  # First claw
        claw2 = canvas.create_polygon(30, 20, 40, 20, 30, 10, fill=color1)  # Second claw

        crab = [body, leg1, leg2, leg3, leg4, claw1, claw2]

        for part in crab:
            self.canvas.move(part, x, y)

        return crab

    def update(self):
        spider_head_pos = self.canvas.coords(self.spider[0])
        spider_head_x = spider_head_pos[0]
        spider_head_y = spider_head_pos[1]
        new_x = spider_head_x + self.x  # Update the x-coordinate
        canvas_width = self.canvas.winfo_width()
        if new_x >= canvas_width - 100:
            self.x = -1.75
        elif new_x <= 0:
            self.x = 1.75
        move_x = new_x - spider_head_x
        for part in self.spider:
            self.canvas.move(part, move_x, 0)

    def check_collision(self, bodyparts):
        for part in self.spider:
            coords_part = self.canvas.coords(part)
            if (
                    bodyparts[0] < coords_part[
                2] and  # Check if left side of bodypart is to the left of the right side of the part
                    bodyparts[2] > coords_part[
                0] and  # Check if right side of bodypart is to the right of the left side of the part
                    bodyparts[1] < coords_part[
                3] and  # Check if top side of bodypart is above the bottom side of the part
                    bodyparts[3] > coords_part[1]  # Check if bottom side of bodypart is below the top side of the part
            ):
                return True
        return False


class AI:

    def __init__(self, canvas, x, y):

        self.canvas = canvas

        self.thread = self.canvas.create_line(x+10, 0, x+10, y+5,
                                          fill='ivory2', width=3)
        self.spider = self.make_spider(x, y)
        self.x, self.y = 0, 0.5

        self.uptown = True


    def make_spider(self, x, y):

        color1 = 'black'
        head = canvas.create_oval(5, 5, 15, 13, fill=color1)
        torso = canvas.create_oval(0, 10, 20, 40, fill=color1)
        legs = [canvas.create_line(-5-i*5, 10*i+5, 5, 10*i+15,
                fill=color1, width=4) for i in range(2) ] + \
               [canvas.create_line(15, 10*i+15, 25+i*5, 10*i+5,
                fill=color1, width=4) for i in range(2) ] + \
               [canvas.create_line(-10+i*5, 10*i+35, 5, 10*i+25,
                fill=color1, width=4) for i in range(2) ] + \
               [canvas.create_line(15, 10*i+25, 30-i*5, 10*i+35,
                fill=color1, width=4) for i in range(2) ]

        spider = [head, torso] + legs
        for part in spider:
            self.canvas.move(part, x, y)
        return spider



    def update(self, X, Y, eatable):
        tallspider = self.canvas.coords(self.spider[0])[1]
        if tallspider <= X:
            self.uptown = False
        elif tallspider >= Y:
            self.uptown = True

        if not self.uptown:
            self.y = 1.75
        else:
            self.y = -1.75

        for part in self.spider:
            self.canvas.move(part, self.x, self.y)

    def check_collision(self, bodyparts):
        coords101 = self.canvas.coords(self.spider[1])
        if bodyparts[0] < coords101[2] and bodyparts[2] > coords101[0] and bodyparts[1] < coords101[3] and bodyparts[3] > coords101[1]:
            return True
        return False

class Avatar:

    def __init__(self, canvas):

        color1 = 'lime'
        color2 = 'sandybrown'

        self.canvas = canvas
        self.head = self.canvas.create_oval(0, 0, 10, 10, fill=color2)
        self.torso = self.canvas.create_rectangle(0, 10, 10, 20,
                                                  fill=color1)
        self.canvas.move(self.head, START_X, START_Y-20)
        self.canvas.move(self.torso, START_X, START_Y-20)
        self.canvas.bind_all('<KeyPress- Left>', self.move)
        self.canvas.bind_all('<KeyPress- Right>', self.move)
        self.canvas.bind_all('<KeyPress- Up>', self.move)
        self.canvas.bind_all('<KeyPress- Down>', self.move)
        self.is_jumping, self.falling = False, False
        self.gravity = 0.12

        self.x = 0
        self.y = 0

    def update(self, land, trophy):
        x1, y1, x2, y2 = self.canvas.coords(self.head)
        self.hit_object(land)

        if x1 + self.x < 0 or x2 + self.x > WIDTH:
            self.x = 0

        if y1 + self.y < 0 or y2 + self.y > HEIGHT-60:
            self.y = 0

        if self.is_jumping:
            if self.y >= 0:
                self.is_jumping = False
                self.y = 1.25

                return
        if self.y > 0:
            self.falling = True

        else:
            self.falling = False

        if self.falling:
            self.y = 1.25
        else:
             self.y += self.gravity
             if y2 + self.y >= HEIGHT-60:
                self.y = 0
        self.canvas.move(self.head, self.x, self.y)
        self.canvas.move(self.torso, self.x, self.y)

    def move(self, event=None):
        x1, y1, x2, y2 = self.canvas.coords(self.head)

        if event.keysym == 'Left' and x1 > 0:
            self.x = -1.25
        elif event.keysym == 'Right' and x2 < WIDTH:
            self.x = 1.25
        elif event.keysym == 'Up' and y1 > 0:
            self.y = -3
            self.is_jumping = True
        elif event.keysym == 'Down' and y2 < HEIGHT:
            self.y = 3
            self.falling = True

    def hit_object(self, obj):
        coordsofthetorso = self.canvas.coords(self.torso)
        x, y, xx, yy = coordsofthetorso
        obstacles = obj.get_obstacles()
        for obstacle in obstacles:
            ox1, oy1, ox2, oy2 = self.canvas.coords(obstacle)

            if xx >= ox1 and x <= ox2 and yy >= oy1 and y <= oy2:
                if x < ox1:
                    self.canvas.move(self.torso, -(xx - ox1), 0)
                    self.canvas.move(self.head, -(xx - ox1), 0)
                elif xx > ox2:
                    self.canvas.move(self.torso, ox2 - x, 0)
                    self.canvas.move(self.head, ox2 - x, 0)
                if y < oy1:
                    self.canvas.move(self.torso, 0, -(yy - oy1))
                    self.canvas.move(self.head, 0, -(yy - oy1))
                elif yy > oy2:
                    self.canvas.move(self.torso, 0, oy2 - y)
                    self.canvas.move(self.head, 0, oy2 - y)

    def replace(self):
        self.canvas.delete(self.head)
        self.canvas.delete(self.torso)
        color1 = 'lime'
        color2 = 'sandybrown'
        self.canvas = canvas
        self.head = self.canvas.create_oval(0, 0, 10, 10, fill=color2)
        self.torso = self.canvas.create_rectangle(0, 10, 10, 20, fill=color1)
        self.canvas.move(self.head, START_X, START_Y - 20)
        self.canvas.move(self.torso, START_X, START_Y - 20)
        self.canvas.bind_all('<KeyPress-Left>', self.move)
        self.canvas.bind_all('<KeyPress-Right>', self.move)
        self.canvas.bind_all('<KeyPress-Up>', self.move)
        self.canvas.bind_all('<KeyPress-Down>', self.move)
        self.is_jumping, self.falling = False, False
        self.jump_speed = 0
        self.gravity = 0.15

        self.x = 0
        self.y = 0

    def find_trophy(self, trophy):
        bodyparts2 = self.canvas.coords(self.torso)
        for jiji in trophy:
            eggies = self.canvas.coords(jiji)
            if len(bodyparts2) >= 4 and len(eggies) >= 4:
                if bodyparts2[0] < eggies[2] and bodyparts2[2] > eggies[0] and bodyparts2[1] < eggies[3] and bodyparts2[3] > eggies[1]:
                    self.canvas.delete(jiji)
                    return True
        return False

if __name__ == '__main__':

    tk = Tk()
    tk.title('Skyland')
    canvas = Canvas(tk, width=WIDTH, height=HEIGHT)
    canvas.pack()
    game = Skyland(canvas)
    mainloop()
