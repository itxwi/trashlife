import pygame
import random
import math


#have friction
#have it snap to 0

pygame.init()

boarder = [600,400]

screen = pygame.display.set_mode((boarder[0],boarder[1]))
clock = pygame.time.Clock()

#ymc color scheme
#each value corrosponds to how much it is attracted or repeled from the other im ymc, it is from [-1,1]
"""
nature settings i like:
{'y': {'attraction': [0.49, 0.43, -0.22], 'color': [255, 255, 0]}, 'm': {'attraction': [0.92, 0.24, 0.4], 'color': [255, 0, 255]}, 'c': {'attraction': [0.11, 0.04, -0.29], 'color': [0, 255, 255]}}

removes all but 2 color types and forms a nucleus with cross

nature = {
    'y' : {
        'attraction': [-1,-1,0],
        'color': [255,255,0]
    },
    'm' : {
        'attraction': [-1,0,0],
        'color': [255,0,255]
    },
    'c' : {
        'attraction': [1,-.2,0],
        'color': [0,255,255],
    }
}
forms a nucleus in the wrong settings

nature = {
    'y' : {
        'attraction': [0,0,0],
        'color': [255,255,0]
    },
    'm' : {
        'attraction': [0,0,0],
        'color': [255,0,255]
    },
    'c' : {
        'attraction': [0,0,0],
        'color': [0,255,255],
    }
}
lifeless

"""

naturemap = {
    'tonum': {
        'y':0,
        'm':1,
        'c':2
    },
    'tocol': {
        0:'y',
        1:'m',
        2:'c'
    }
}

nature = {
    'y' : {
        'attraction': [-1,0,0],
        'color': [255,255,0]
    },
    'm' : {
        'attraction': [0,0,0],
        'color': [255,0,255]
    },
    'c' : {
        'attraction': [0,0,0],
        'color': [0,255,255],
    }
}

repelradius = 3
attractionradius = 350
attr=100
friction = .9
termvel=3
repelforce = 1
snapvel = .01
showarrows = False
arrowfactor = 15
selfattract = True

def dist(p1,p2):
    return ((p1[0]-p2[0])**2+(p1[1]-p2[1])**2)**.5

def dir(p1,p2):
    return math.degrees(math.atan2(p2[1]-p1[1],p2[0]-p1[0]))

def inbounds(p1):
    return True if 0<=p1[0]<=boarder[0] and 0<=p1[1]<=boarder[1] else False

class Arrrow:
    def __init__(self,p1,p2,col,wid=1):
        self.length = dist(p1,p2)
        self.p1 = p1
        self.p2 = p2
        self.col = col
        self.wid = wid
    
    def draw(self):
        pygame.draw.line(screen,self.col,self.p1,self.p2,self.wid)

class Particle:
    def __init__(self,pos,rad,col, wid=1, vel=[0,0]):
        #essential
        self.pos = pos
        self.rad = rad
        self.wid = wid
        self.vel = vel
        
        self.col = nature[col]['color']
        self.realcol = col

    def draw(self):
        pygame.draw.circle(screen,self.col,self.pos,self.rad,self.wid)
        if not inbounds(self.pos):
            parts.remove(self)

    def update(self):

        # old conservation of matter
        # self.pos = [
        #     self.pos[0]+self.vel[0] if inbounds([self.pos[0]+self.vel[0],0]) else self.pos[0]-self.vel[0],
        #     self.pos[1]+self.vel[1] if inbounds([0,self.pos[1]+self.vel[1]]) else self.pos[1]-self.vel[1]
        # ]
        
        self.pos = [
            self.pos[0]+self.vel[0],
            self.pos[1]+self.vel[1]
        ]
        
        #friction
        self.vel=[
            self.vel[0]*friction,
            self.vel[1]*friction

        ]

        # part applies forces to self

        for part in parts:
            if part!=self:
                partdist = dist(part.pos,self.pos)
                #default repulsion
                if partdist<=repelradius:
                    #-1 to 0 based on distance
                    #inverse square
                    force = -partdist/(repelradius) * repelforce if partdist>0 else -1
                    

                    #technically right way of doing this but i dont like it
                    # force = -1 if partdist==0 else -repelradius/(partdist**2) * repelforce
                    # print(force)

                    direction = math.radians(dir(self.pos,part.pos)) + random.uniform(-1,1)
                    
                    self.vel=[
                        ( self.vel[0] + force * math.cos(direction) ) if abs( self.vel[0] + force * math.cos(direction) ) <= termvel else termvel * math.cos(direction),
                        ( self.vel[1] + force * math.sin(direction) ) if abs( self.vel[1] + force * math.sin(direction) ) <= termvel else termvel * math.sin(direction)
                    ]
                    # arrow management
                    if showarrows:
                        #print(force,direction)
                        finalpos = [
                        self.pos[0]+force*arrowfactor**2*math.cos(direction),
                        self.pos[1]+force*arrowfactor**2*math.sin(direction)
                        ]

                        Arrrow(self.pos,finalpos,[255,0,0]).draw()

                #repulsion or attraction
                if repelradius<=partdist<=attractionradius:
                    #inverse sqaure from 0 to 1
                    force = (partdist/(attractionradius**2)) * nature[str(self.realcol)]['attraction'][naturemap['tonum'][str(part.realcol)]] * attr #changing 1 to 2 -> inverse sqaure

                    #force = nature[str(self.realcol)]['attraction'][naturemap['tonum'][str(part.realcol)]] * attr if partdist==0 else (attractionradius/(partdist**2)) * nature[str(self.realcol)]['attraction'][naturemap['tonum'][str(part.realcol)]] * attr

                    #self direction
                    direction = math.radians(dir(part.pos,self.pos))

                    self.vel=[
                        ( self.vel[0] + force * math.cos(direction) ) if abs( self.vel[0] + force * math.cos(direction) ) <= termvel else termvel * math.cos(direction),
                        ( self.vel[1] + force * math.sin(direction) ) if abs( self.vel[1] + force * math.sin(direction) ) <= termvel else termvel * math.sin(direction)
                    ]
                
                    # arrow management
                    if showarrows:
                        #print(force,direction)
                        finalpos = [
                        self.pos[0]+force*arrowfactor*math.cos(direction),
                        self.pos[1]+force*arrowfactor*math.sin(direction)
                        ]

                        Arrrow(self.pos,finalpos,[255,0,0]).draw()
                
        #snapping
        if abs(self.vel[0])<snapvel:
            self.vel[0]=0
        if abs(self.vel[1])<snapvel:
            self.vel[1]=0

parts = []

def fillMap(num_part, weight = [1,1,1]):
    #weight is ymc
    for part in range(num_part):
        placement = [random.randint(0,boarder[0]),random.randint(0,boarder[1])]
        val = random.uniform(0,1)
        yellow = weight[0]/sum(weight)
        magenta = weight[1]/sum(weight)
        if val<yellow:
            parts.append(Particle(placement,2,'y'))
        elif yellow<=val<yellow+magenta:
            parts.append(Particle(placement,2,'m'))
        elif yellow+magenta<=val:
            parts.append(Particle(placement,2,'c'))

def setNature(numcolors):
    for i,color in enumerate(nature):
        nature[color]['attraction'] = [round(random.uniform(-1,1),2) for i in range(numcolors)]
        if selfattract:
            nature[color]['attraction'][i]=0


#fillMap(150)
#setNature(3)
print(nature)

colState = 0
forcestates = [False,False]

while True:
    screen.fill([0,0,0])
    mousePos = pygame.mouse.get_pos()
    mouseState = pygame.mouse.get_pressed()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_r:
                colState+=1
                colState=colState%(len(nature)+1)
                print(colState)

            if event.key == pygame.K_q:
                forcestates[0]=not forcestates[0]
            
            if event.key == pygame.K_f:
                 parts.append(Particle(mousePos,2,naturemap['tocol'][random.randint(0,2)])) if colState>=len(list(nature.keys())) else parts.append(Particle(mousePos,2,naturemap['tocol'][colState]))
 
            if event.key == pygame.K_e:
                forcestates[1]=not forcestates[1]


    for part in parts:
        part.update()
        part.draw()

    if mouseState[0]:
        parts.append(Particle(mousePos,2,naturemap['tocol'][random.randint(0,2)])) if colState>=len(list(nature.keys())) else parts.append(Particle(mousePos,2,naturemap['tocol'][colState]))

    pygame.display.flip()
    clock.tick(120)

