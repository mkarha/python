import pygame, random

class Kivi:

    def __init__(self, x, y):
        self.x = x #random.randint(0, (640-leveys))
        self.y = y #random.randint(0, (480-korkeus))
        self.nopeus_x = 0
        self.nopeus_y = 1


    def liikuta(self, kivi, robo, robo_x, robo_y):
        pisteet = 0
        self.y += self.nopeus_y
        self.x += self.nopeus_x
        if self.nopeus_y > 0 and self.y+kivi.get_height() >= 480 and self.x >=320:
            self.nopeus_y = 0     
            pisteet = -1
        elif self.nopeus_y > 0 and self.y+kivi.get_height() >= 480 and self.x < 320:
            self.nopeus_y = 0
            pisteet = -1
        elif self.y+kivi.get_height() > robo_y and (self.x >= robo_x and self.x < robo_x+robo.get_width() or 
        self.x+kivi.get_width() >= robo_x and self.x+kivi.get_width() < robo_x+robo.get_width()):
            self.x =  random.randint(0, (640-kivi.get_width()))
            self.y = 0-kivi.get_height()
            self.nopeus_x = 0
            self.nopeus_y = 1
            pisteet = 1
        return pisteet


    def aseta(self):
        return self

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

class Peli:

    def __init__(self):
        pygame.init()
        self.naytto = pygame.display.set_mode((640, 480))

        self.robo = pygame.image.load("robo.png")
        self.kivi = pygame.image.load("kivi.png")
        self.leveys = self.kivi.get_width()
        self.korkeus = self.kivi.get_height()
        self.sijainnit = []
        self.x = 320
        self.y = 480-self.robo.get_height()
        self.pisteita = 0

        self.oikealle = False
        self.vasemmalle = False


        self.kello = pygame.time.Clock()

    def pelaa(self):
        while True:
            for tapahtuma in pygame.event.get():
                if tapahtuma.type == pygame.KEYDOWN:
                    if tapahtuma.key == pygame.K_LEFT:
                        self.vasemmalle = True
                    if tapahtuma.key == pygame.K_RIGHT:
                        self.oikealle = True
                if tapahtuma.type == pygame.KEYUP:
                    if tapahtuma.key == pygame.K_LEFT:
                        self.vasemmalle = False
                    if tapahtuma.key == pygame.K_RIGHT:
                        self.oikealle = False
                if tapahtuma.type == pygame.QUIT:
                    exit()
            if self.oikealle and self.x+self.robo.get_width() < 640:
                self.x += 4
            if self.vasemmalle and self.x >= 0:
                self.x -= 4


            self.naytto.fill((0, 0, 0))

            fontti = pygame.font.SysFont("Arial", 24)
            teksti = fontti.render(f"Pisteet: {self.pisteita}", True, (255, 0, 0))
            self.naytto.blit(teksti, (640-teksti.get_width(), 0))
            i = 0
            if len(self.sijainnit) == 0:
                while i < 3:   
                    x_kivi = random.randint(0, 640-self.leveys)
                    y_kivi = random.randint(0, 480-self.korkeus)
                    sijainti = Kivi(x_kivi, y_kivi)
                    self.sijainnit.append(sijainti.aseta())            
                    i += 1
            i = 0 
            while i < 3:
                self.naytto.blit(self.kivi, (self.sijainnit[i].get_x(), self.sijainnit[i].get_y())) 
                piste = self.sijainnit[i].liikuta(self.kivi, self.robo, self.x, self.y)
                if piste < 0:
                    self.lopetus()
                else:
                    self.pisteita += piste
                    self.sijainnit[i] = self.sijainnit[i].aseta()
            
                i += 1

            self.naytto.blit(self.robo, (self.x, self.y))
            pygame.display.flip()
    
   
            self.kello.tick(60)

    def lopetus(self):
        while True:
            for tapahtuma in pygame.event.get():
                if tapahtuma.type == pygame.KEYDOWN:
                    if tapahtuma.key == pygame.K_n:
                        peli = Peli()
                        peli.pelaa()
                if tapahtuma.type == pygame.QUIT:
                    exit()
            self.naytto.fill((0, 0, 0))

            fontti = pygame.font.SysFont("Arial", 24)
            teksti = fontti.render(f"Peli loppui. Paina n, jos haluat pelata uudelleen.", True, (255, 0, 0))
            

            self.naytto.blit(teksti, (320-teksti.get_width()/2, 240))
            pygame.display.flip()

peli = Peli()
peli.pelaa()