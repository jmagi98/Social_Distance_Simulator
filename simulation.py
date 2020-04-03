import pygame
import math
pygame.init()
import random
import time
# amount of people in sim
pygame.font.init()
myfont = pygame.font.SysFont('Comic Sans MS', 24)
numInfected = input("How many initially infected? > ")
WIDTH = 500
HEIGHT = 500
people = 100
personList = []
socialistanceNum = input("What percentage of population is socially distancing? (ex input: 50): > ")
socialistanceNum = int(socialistanceNum) / 100
notAbiding = round((1 - socialistanceNum) * people)
infectedColor = (252, 3, 3)
recoveredColor = (3, 252, 248)
infectedList = []
recoveredList = []

class Person():
    def __init__(self, position, direction, speed, color):
        self.position = position
        self.direction = direction
        self.speed = speed
        self.color = color
        self.infected = False
        self.days = 0
        self.recovered = False
        x, y = self.position
        self.rect = pygame.rect.Rect((x, y, 5, 5))
        self.notAbiding = False
    def update(self, others):
        dx, dy = self.direction
        x, y = self.position
        self.rect.move_ip((dx * self.speed),(dy * self.speed))
        if self.rect.right >= WIDTH or self.rect.left <= 0:
            self.direction = -dx, dy
        if self.rect.bottom >= HEIGHT or self.rect.top <= 0:
            self.direction = dx, -dy
        for i in others:
            if i.rect.colliderect(self.rect):
                if i.rect != self.rect:
                    self.direction = -dx, -dy

    def draw(self, pos):
        pygame.draw.rect(pos, self.color, self.rect)
    def recover(self):
        self.infected = False
        self.color = recoveredColor
        self.recovered = True

def setInitialPos(screen):
    moving = 0
    for i in range(people):
        xpos = random.randint(0, 500)
        ypos = random.randint(0, 500)
        randonNum = random.random()
        angle = 360 * randonNum
        directiony = .5 * math.sin(angle)
        directionx = .5 * math.cos(angle)
        person = Person((xpos, ypos), (directionx, directiony), 3, (0, 0, 128))
        # Ensure no overlap on start, which would cause a buggy no-movement between dots
        for i in personList:
            if i.rect.colliderect(person.rect):
                person.position = (random.randint(0, 500), random.randint(0, 500))
        if moving < notAbiding:
            person.notAbiding = True
            moving += 1
        personList.append(person)
        person.draw(screen)

def runSim(screen):
    for i in range(int(numInfected)):
        personList[i].infected = True
        personList[i].color = infectedColor
    days = 1
    counter = 0
    while days <= 30:
        counter += 1
        if counter == 100:
            for i in infectedList:
                i.days += 1
                if i.days == 14:
                    infectedList.remove(i)
                    i.recover()
                    recoveredList.append(i)
            days += 1
            counter = 0


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((255, 255, 255))
        for i, v in enumerate(personList):
            if v.notAbiding:
                v.update(personList)
            for p in personList:
                if p != v:
                    if v.rect.colliderect(p.rect):
                        if(p.infected and not v.recovered):
                            v.infected = True
                            v.color = infectedColor
                            if v not in infectedList:
                                infectedList.append(v)
            v.draw(screen)
        infectedText = "Number Infected: " + str(len(infectedList))
        recoveredText = "Number Recovered: " + str(len(recoveredList))
        daysText = "Days: " + str(days)

        textsurfacedays = myfont.render(daysText, False, (128,128,128))
        screen.blit(textsurfacedays, (0, 0))
        textsurfaceinfected = myfont.render(infectedText, False, (128,128,128))
        screen.blit(textsurfaceinfected, (0, 15))
        textsurfacerecovered = myfont.render(recoveredText, False, (128,128,128))
        screen.blit(textsurfacerecovered, (0, 30))
        pygame.display.flip()
        time.sleep(0.01)
    pygame.quit()

def main():

    screen = pygame.display.set_mode([WIDTH, HEIGHT])
    setInitialPos(screen)
    runSim(screen)


if __name__ == '__main__':
    main()