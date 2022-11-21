import turtle, math, time, random
import turtle as tur


turtle.setup(600,600)
wireframeGame = turtle.Screen()
wireframeGame.tracer(0,0)
wireframeGame.bgcolor('black')
canvas = wireframeGame.getcanvas()


# -------turtles------------
artist = turtle.Turtle()
artist.hideturtle()
artist.turtlesize(0.2,0.2)
artist.speed(0)
artist.shape('circle')
artist.color('white')
artist.penup()


pointer = turtle.Turtle()
pointer.hideturtle()
pointer.turtlesize(2,2)
pointer.shape('square')
pointer.pensize(1)
pointer.penup()
pointer.speed(0)
pointer.color('black')
pointer.pencolor('white')


stars = turtle.Turtle()
stars.hideturtle()
stars.penup()
stars.speed(0)
stars.color('white')
stars.shape('circle')
stars.turtlesize(0.1,0.1)


bullet = turtle.Turtle()
bullet.hideturtle()
bullet.penup()
bullet.speed(0)
bullet.color('white')


scoreboard = turtle.Turtle()
scoreboard.hideturtle()
scoreboard.penup()
scoreboard.setpos(275,265)
scoreboard.color('white')
scoreboard.write(0, align='right', font=('impact', 15, 'normal'))


boom = turtle.Turtle() #draws ship-explosion animation
boom.hideturtle()
boom.penup()
boom.color('white')
boom.speed(0)


#--------------------starting conditions---------------------
constellation = [] #star coords
ships = []
shipIndex = -1
shipState = False
shipExplode = [0,(0,0)] # [whether a ship-explosion animation is playing and what stage its in, its coords]
shipXDist = [0,0,0] #[index of point, index of point, max dist between two ship points' x coords; used for hit detection]
shipYDist = [0,0] #btw i'm using the words "points" and "vertices" interchangeably here
xMod = 0
yMod = 0
bulletPos = []
screenZ = -10 #the viewing screen's z coordinate
shootFlag = False
shipLeave = 0 #counts up ship vertices that have went offscreen- once they all have, it disappears
camera = [[0,0,0],[5,-10,5]] #[coords],[rotation]
score = 0
for i in range(0,101):
   stars.setpos(random.randint(-300,300), random.randint(-300,300))
   stars.stamp()
   constellation.append([stars.xcor(), stars.ycor()])


#------------------functions----------------------
def drawLine(list,turtle, point1,point2):
   if list[point1] == 'n/a' or list[point2] == 'n/a':
       return
   elif abs(list[point1][0] - list[point2][0]) >= 600 or abs(list[point1][1] - list[point2][1]) >= 600:
       return
   else:
       turtle.penup()
       turtle.setpos(list[point1][0],list[point1][1])
       #artist.stamp()
       turtle.pendown()
       turtle.setpos(list[point2][0],list[point2][1])
       #artist.stamp()
       turtle.penup()




def leave():
   wireframeGame.bye()


def threeDee(turtle, list, index):
   global shipState
   turtle.clear()
   cx = math.cos(math.radians(camera[1][0]))
   sx = math.sin(math.radians(camera[1][0]))
   cy = math.cos(math.radians(camera[1][1]))
   sy = math.sin(math.radians(camera[1][1]))
   cz = math.cos(math.radians(camera[1][2]))
   sz = math.sin(math.radians(camera[1][2]))
   if list[index][2] > screenZ:
       return 'n/a'
   else:
       d1 = cy * (sz * (list[index][1] - camera[0][1]) + cz * (list[index][0] - camera[0][0])) - (
                   sy * (list[index][2] - camera[0][2]))
       d2 = sx * (cy * (list[index][2] - camera[0][2]) + sy * (
                   sz * (list[index][1] - camera[0][1]) + cz * (list[index][0] - camera[0][0]))) + cx * (
                        cz * (list[index][1] - camera[0][1]) - sz * (list[index][0] - camera[0][0]))
       d3 = cx * (cy * (list[index][2] - camera[0][2]) + sy * (
                   sz * (list[index][1] - camera[0][1]) + cz * (list[index][0] - camera[0][0]))) - sx * (
                        cz * (list[index][1] - camera[0][1]) - sz * (list[index][0] - camera[0][0]))
       bx = (-10 / d3) * d1 * 10
       by = (-10 / d3) * d2 * 10
       #artist.setpos(bx, by)
       #artist.write(i,font=('arial',13,'normal'))
       return [bx, by]






def shoot(bulletCoords):
   laser3d = []
   laser2d = []
   for z in (-20,-10):
       for y in (-3,3):
           for x in (-3,3):
               laser3d.append([bulletCoords[0] + x, bulletCoords[1] + y,bulletCoords[2] + z])
   for j in range(len(laser3d)):
       laser2d.append(threeDee(bullet,laser3d, j))
   drawLine(laser2d,bullet, 0, 1)
   drawLine(laser2d,bullet, 1, 3)
   drawLine(laser2d,bullet, 2, 0)
   drawLine(laser2d,bullet, 3, 2)
   drawLine(laser2d,bullet, 0, 4)
   drawLine(laser2d,bullet, 4, 6)
   drawLine(laser2d,bullet, 5, 7)
   drawLine(laser2d,bullet, 6, 7)
   drawLine(laser2d,bullet, 1, 5)
   drawLine(laser2d,bullet, 2, 6)
   drawLine(laser2d,bullet, 3, 7)
   drawLine(laser2d,bullet, 7, 5)
   drawLine(laser2d,bullet, 4, 5)
   #artist.clear()


def alienShip(centrPoint):
   global shipLeave, shipState, shipXDist, shipYDist
   #time.sleep(0.00005)
   shipLeave = 0
   shipXDist = [0,0,0]
   shipYDist = [0,0]
   ufo3d = []
   radius = 10
   for i in (0, 1, 2, 3):
       ufo3d.append([(math.cos(math.radians(i * 90 + centrPoint[4])) * radius) + centrPoint[0] + centrPoint[3], centrPoint[1],
                             (math.sin(math.radians(i * 90 + centrPoint[4])) * radius) + centrPoint[2]]) #making a square rotated by centrPoint[4] degrees
   ufo3d.append([centrPoint[0] + centrPoint[3], centrPoint[1] + radius * 1.5, centrPoint[2]])
   ufo2d = []
   for i in range(len(ufo3d)):
       point = threeDee(artist, ufo3d, i)
       ufo2d.append(point)
       if abs(point[0]) > 300 or abs(point[1]) > 300:
           shipLeave += 1
   shipYDist = [ufo2d[0][1], ufo2d[4][1]]
   #print(ufo2d)
   for i in (1,2,3):
       if abs(ufo2d[i][0] - ufo2d[i - 1][0]) > shipXDist[2]:
           shipXDist = [ufo2d[i][0], ufo2d[i - 1][0], ufo2d[i][0] - ufo2d[i - 1][0]]
   if shipLeave == 5:
       shipState = False
   drawLine(ufo2d,artist, 0, 1)
   drawLine(ufo2d,artist, 1, 2)
   drawLine(ufo2d,artist, 2, 3)
   drawLine(ufo2d,artist, 3, 0)
   drawLine(ufo2d,artist, 0, 4)
   drawLine(ufo2d,artist, 1, 4)
   drawLine(ufo2d,artist, 2, 4)
   drawLine(ufo2d,artist, 3, 4)
   #print(ufo2d)
   #wireframeGame.update()


def cameraSpin(xMod, yMod): #one of these should always be 0
   stars.clear()
   for i in range(len(constellation)):
       if abs(constellation[i][0] + xMod) > 300 or abs(constellation[i][1] + yMod) > 300:
           if xMod == 0:
               constellation[i] = [constellation[i][0], -constellation[i][1]]
           else:
               constellation[i] = [-constellation[i][0], constellation[i][1]]
       else:
           constellation[i] = [constellation[i][0] + xMod, constellation[i][1] + yMod]
       stars.setpos(constellation[i][0], constellation[i][1])
       stars.stamp()
   #wireframeGame.update()




def pointerDraw(x,y):
   pointer.setpos(x - 8, y + 20)
   pointer.pendown()
   pointer.setpos(x - 10, y + 20)
   pointer.setpos(x - 20, y + 20)
   pointer.setpos(-300,300)
   pointer.setpos(x - 20, y + 20)
   pointer.setpos(x - 20, y - 20)
   pointer.setpos(-300,-300)
   pointer.setpos(x - 20, y - 20)
   pointer.setpos(x - 8, y - 20)
   pointer.penup()
   pointer.setpos(x + 8, y - 20)
   pointer.pendown()
   pointer.setpos(x + 20, y - 20)
   pointer.setpos(300,-300)
   pointer.setpos(x + 20, y - 20)
   pointer.setpos(x + 20, y + 20)
   pointer.setpos(300,300)
   pointer.setpos(x + 20, y + 20)
   pointer.setpos(x + 8, y + 20)
   pointer.penup()
   pointer.setpos(x, y)


def startShoot(x,y):
   global shootFlag, bulletPos
   shootFlag = True
   bulletPos = [x,y, -10]


wireframeGame.listen()
#wireframeGame.onkeypress(up, 'Up')
#wireframeGame.onkeypress(down, 'Down')
#wireframeGame.onkeypress(left, 'Left')
#wireframeGame.onkeypress(right, 'Right')
wireframeGame.onclick(startShoot)
wireframeGame.onkey(leave, 'x')
#wireframeGame.onkey(alienShip, 'o')
pointerDraw(pointer.xcor(), pointer.ycor())
wireframeGame.update()




while True:
   if shootFlag:
       shootFlag = False
   if bulletPos != []:
       if bulletPos[2] > -200:
           shoot(bulletPos)
           bulletPos[2] -= 10
           if shipXDist[0] <= bulletPos[0] <= shipXDist[1] or shipXDist[0] >= bulletPos[0] >= shipXDist[1]:
               if shipYDist[0] >= bulletPos[1] >= shipYDist[1] or shipYDist[0] <= bulletPos[1] <= shipYDist[1]:
                   shipState = False
                   shipExplode = [10, (shipXDist[0], shipYDist[0] - 50)]
                   score += 150
                   scoreboard.clear()
                   scoreboard.write(score, align='right', font=('impact', 15, 'normal'))
                   if score == 6900: # a little treat for the dedicated gamers who get this far :)
                       scoreboard.setpos(210, 265)
                       scoreboard.write('nice!', align='right', font=('impact', 15, 'normal'))
                       scoreboard.setpos(275,265)
       else:
           bullet.clear()
           bulletPos = []
   x = canvas.winfo_pointerx() - 860 #convert to turtle-style coords (i.e 0,0 in the centre of the screen
   y = canvas.winfo_pointery() - 505 #(cont.) instead of in the top left corner)
   pointer.setpos(x,-y)
   if pointer.ycor() >= 275:
       cameraSpin(0,-1)
       if yMod < 1:
           yMod += -0.05
   elif pointer.ycor() <= -275:
       cameraSpin(0,1)
       if yMod > -1:
           yMod += 0.05
   elif pointer.xcor() <= -275:
       cameraSpin(1,0)
       if xMod < 1:
           xMod += 0.05
   elif pointer.xcor() >= 275:
       cameraSpin(-1,0)
       if xMod > -1:
           xMod += -0.05
   else:
       xMod = 0
       yMod = 0
       pointer.clear()
       pointerDraw(x,-y)
   if shipExplode[0] != 0:
       boom.clear()
       boom.setpos(shipExplode[1])
       boom.pendown()
       boom.circle(shipExplode[0])
       boom.penup()
       shipExplode[0] += 1
       if shipExplode[0] > 50:
           shipExplode[0] = 0
           boom.clear()
   if not shipState:
       ships.append([-100, random.randint(-250, 100), random.randint(-50, -25), 0, 0]) #x,y,z,x movement across screen, spin
       shipIndex += 1
       shipState = True
       xMod = 0
       yMod = 0
   alienShip(ships[shipIndex])
   ships[shipIndex][0] += xMod
   ships[shipIndex][1] += yMod
   ships[shipIndex][3] += 2
   ships[shipIndex][4] += 1.5
   wireframeGame.update()






wireframeGame.mainloop()