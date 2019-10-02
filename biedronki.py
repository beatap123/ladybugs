import os
import random
import pygame

pygame.init()

szer = 600
wys = 600
screen = pygame.display.set_mode((szer, wys))


def napisz(text, x, y, rozmiar):
    cz = pygame.font.SysFont("Cambria", rozmiar)
    rend = cz.render(text, 1, (255, 0, 0))
    screen.blit(rend, (x, y))


copokazuje = "menu"


class Bramka():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.wysokosc = 20
        self.szerokosc = 580
        self.kolor = (255, 69, 0)
        self.ksztalt = pygame.Rect(self.x, self.y, self.szerokosc, self.wysokosc)

    def rysuj(self):
        pygame.draw.rect(screen, self.kolor, self.ksztalt, 0)


class Przeszkoda():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.wysokosc = 64
        self.szerokosc = 64
        self.ksztalt = pygame.Rect(self.x, self.y, self.szerokosc, self.wysokosc)
        self.grafika = pygame.image.load(os.path.join("biedronka.png"))

    def rysuj(self):
        screen.blit(self.grafika, (self.x, self.y))

    def ruch(self, v):
        self.y = self.y + v
        self.ksztalt = pygame.Rect(self.x, self.y, self.szerokosc, self.wysokosc)

    def kolizja(self, player):
        if self.ksztalt.colliderect(player):
            return True
        else:
            return False


class Pajak():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.wysokosc = 32
        self.szerokosc = 32
        self.ksztalt = pygame.Rect(self.x, self.y, self.szerokosc, self.wysokosc)
        self.grafika = pygame.image.load(os.path.join("pajak.png"))

    def rysuj(self):
        screen.blit(self.grafika, (self.x, self.y))

    def ruch1(self, v):
        self.y = self.y - v
        self.ksztalt = pygame.Rect(self.x, self.y, self.szerokosc, self.wysokosc)

    def ruch2(self, v):
        self.x = self.x - v
        self.ksztalt = pygame.Rect(self.x, self.y, self.szerokosc, self.wysokosc)


przeszkody = []
for i in range(1):
    przeszkody.append(Przeszkoda((random.randint(0, 550)), (random.randint(0, 550))))

gracz = Pajak(250, 500)
dy = 2

pole = Bramka(10, 0)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                gracz.ruch2(4 * dy)
            if event.key == pygame.K_RIGHT:
                gracz.ruch2(4 * (-dy))
            if event.key == pygame.K_UP:
                gracz.ruch1(10)
            if event.key == pygame.K_SPACE:
                if copokazuje != "rozgrywka":
                    gracz = Pajak(250, 500)
                    dy = 2
                    copokazuje = "rozgrywka"
    screen.fill((0, 0, 0))
    if copokazuje == "menu":
        napisz("ZEMSTA BIEDRONKI", 150, 300, 35)
        napisz("Naciśnij spację, żeby rozpocząć!", 100, 350, 30)
        logo = pygame.image.load(os.path.join("newlogo.png"))
        screen.blit(logo, (150, 190))
    elif copokazuje == "rozgrywka":
        pole.rysuj()
        for p in przeszkody:
            p.ruch(5)
            p.rysuj()
            if p.kolizja(gracz.ksztalt):
                copokazuje = "koniec"
        for p in przeszkody:
            if p.y >= -p.wysokosc:
                przeszkody.remove(p)
                pygame.time.wait(700)
                przeszkody.append(Przeszkoda((random.randint(0, 550)), (random.randint(0, 550))))
        gracz.ruch1(2)
        gracz.rysuj()
        if gracz.ksztalt.colliderect(pole.ksztalt):
            copokazuje = "wygrana"
    elif copokazuje == "wygrana":
        napisz("WYGRANA!", 200, 250, 35)
        logo = pygame.image.load(os.path.join("wygrana.png"))
        screen.blit(logo, (150, 190))
    elif copokazuje == "koniec":
        napisz("TO KONIEC!", 180, 250, 35)
        napisz("Naciśnij spację, żeby spróbować jeszcze raz!", 25, 320, 30)
        logo = pygame.image.load(os.path.join("koniec.png"))
        screen.blit(logo, (150, 190))

    pygame.display.update()
