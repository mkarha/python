# TEE PELI TÄHÄN

import pygame, random, math

# Hahmo-luokka, jonka muut hahmot perivät
class Hahmo( object ):

    def __init__(self, x, y):
        self.x = x
        self.y = y 

    # Palauttaa Hahmo-olion
    def aseta(self):
        return self

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    # Tarkastaa osuuko robo-kuvake hamon kuvakkeeseen. 
    # Korkeussuunnassa helpottamassa hirviöiden välissä liikkumista +/-10, 
    # jotta vaaditaan kunnon osuma, eli reunan hipaisu ei riitä
    # Sama käytössä kolikoilla. Oven kohdalla huomioitu funktiota kutsuttaessa.
    def osuma(self, hahmo, robo, robo_x, robo_y):
        if (self.y >= robo_y+10 and self.y < robo_y+robo.get_height()-10 or 
        self.y+hahmo.get_height() >= robo_y+10 and self.y+hahmo.get_height() < robo_y+robo.get_height()-10):
            if (self.x >= robo_x and self.x < robo_x+robo.get_width() or 
            self.x+hahmo.get_width() >= robo_x and self.x+hahmo.get_width() < robo_x+robo.get_width()):
                return True
        else:
            return False

class Hirvio( Hahmo ):

    def __init__(self, x, y, nopeus):   
        self.nopeus = nopeus
        Hahmo.__init__(self, x, y)

    # Vaakasuuntaisesti liikkuvien hirviöiden toiminta
    # Lisätään x-suuntaista liikettä nopeuden verran vuorossa. 
    # Mikäli vastaan tulee seinä, käännytään ympäri vaihtamalla nopeus negatiiviseksi. suhteessa sen hetkiseen nopeuteen.
    # Tarkistetaan onko ruudussa robottia "osuma"-metodilla "Hahmo"-luokasta
    def liikuta(self, hirvio, robo, robo_x, robo_y):
        jatka = 0
        self.x += self.nopeus
        if self.nopeus > 0 and self.x+hirvio.get_width() >= 640:
            self.nopeus = -self.nopeus   
        elif self.nopeus < 0 and self.x <= 0 :
            self.nopeus = -self.nopeus
        elif self.osuma(hirvio, robo, robo_x, robo_y) == True:
            jatka = -1
        return jatka


    # Pystysuuntainen liike
    # Lisätään y-suuntaista liikettä nopeuden verran vuorossa. 
    # Mikäli vastaan tulee seinä, käännytään ympäri vaihtamalla nopeus negatiiviseksi. suhteessa sen hetkiseen nopeuteen.
    # Tarkistetaan onko ruudussa robottia "osuma"-metodilla "Hahmo"-luokasta
    def pystyliike(self, hirvio, robo, robo_x, robo_y):
        jatka = 0
        self.y += self.nopeus
        if self.nopeus > 0 and self.y+hirvio.get_height() >= 480:
            self.nopeus = -self.nopeus   
        elif self.nopeus < 0 and self.y <= 0 :
            self.nopeus = -self.nopeus
        elif self.osuma(hirvio, robo, robo_x, robo_y) == True:
            jatka = -1
        return jatka

    # Keskipistettä kiertävän hirviön toiminta
    # Pääohjelmassa kulma kasvaa 0.01, joka kieroksella.
    # Asetetaan hirviö uuteen pisteeseen, joka kierroksella.
    # Tarkistetaan onko ruudussa robottia "osuma"-metodilla "Hahmo"-luokasta
    def kierra(self, hirvio, kulma, robo, robo_x, robo_y):
        jatka = 0
        self.y = 240+math.sin(kulma)*150-hirvio.get_height()/2
        self.x = 320+math.cos(kulma)*150-hirvio.get_width()/2
        if self.osuma(hirvio, robo, robo_x, robo_y) == True:
                jatka = -1
        return jatka

    # Pelaajaa seuraavan hirviön toiminta
    # Mikäli hirviön sijainnin piste (joko x tai y) on suurempi kuin robotin,
    # piennennetään hirviös pisteen suuruutta. Mikäli pienempi, kasvatetaan
    # Tarkistetaan onko ruudussa robottia "osuma"-metodilla "Hahmo"-luokasta
    def seuraa(self, hirvio, robo, robo_x, robo_y):
        jatka = 0
        if robo_x > self.x:
            self.x += 1
        if robo_x < self.x:
            self.x -= 1
        if robo_y > self.y:
            self.y += 1
        if robo_y < self.y:
            self.y -= 1
        if self.osuma(hirvio, robo, robo_x, robo_y) == True:
            jatka = -1
        return jatka  

class Kolikko( Hahmo ):

    def __init__(self, x, y):
        self.nopeus_x = 0
        self.nopeus_y = 1
        Hahmo.__init__(self, x, y)

    def liikuta(self, kolikko, robo, robo_x, robo_y):
        pisteet = 0
        self.y += self.nopeus_y
        self.x += self.nopeus_x
        if self.nopeus_y > 0 and self.y+kolikko.get_height() >= 480:
            self.nopeus_y = 0     
            pisteet = -1
        # Kun pelaaja tavoittaa kolikon, luodaan uusi kolikko ja lisätään pistemäärää yhdellä
        elif self.osuma(kolikko, robo, robo_x, robo_y) == True:
                self.x =  random.randint(0, (640-kolikko.get_width()))
                self.y = 0-kolikko.get_height()
                self.nopeus_x = 0
                self.nopeus_y = 1
                pisteet = 1
        return pisteet

class Ovi( Hahmo ):

    # "Ovi"-luokassa vain alustetaan olio. Mut metodit "Hahmo"-luokasta
    def __init__(self, x, y):
        Hahmo.__init__(self, x, y)

class Peli:

    def __init__(self):
        pygame.init()
        self.naytto = pygame.display.set_mode((640, 480))
        self.robo = pygame.image.load("robo.png")
        self.kolikko = pygame.image.load("kolikko.png")
        self.hirvio = pygame.image.load("hirvio.png")
        self.ovi = pygame.image.load("ovi.png")
        self.sijainnit_kolikko = []
        self.sijainnit_hirvio = []
        self.x = 320
        self.y = 480-self.robo.get_height()
        self.pisteita = 0
        self.kulma = 0
        self.oikealle = False
        self.vasemmalle = False
        self.alas = False
        self.ylos = False        
        self.kello = pygame.time.Clock()
        self.loppu = False

    def ohjeet(self):
        while True:
            for tapahtuma in pygame.event.get():
                if tapahtuma.type == pygame.KEYDOWN:
                    if tapahtuma.key == pygame.K_SPACE:
                        peli = Peli()
                        peli.pelaa()
                if tapahtuma.type == pygame.QUIT:
                    exit()
            self.naytto.fill((0, 0, 0))
            ohjeet = []
            ohjeet.append("Tervetuloa Kolikkokaaos-peliin.")
            ohjeet.append("Pelin tarkoituksena on kerätä robotilla tippuvia kolikoita,")
            ohjeet.append("samalla haamuja väistellen.")
            ohjeet.append("Mikäli kolikko ehtii maahan tai haamu osuu robottiin, peli päättyy.")
            ohjeet.append("Robottia ohjataan nuolinäppäimillä ylös, alas tai sivuille.")
            ohjeet.append("Sivureunoilla on teleporttiovet, joiden kautta voi liikkua puolelta toiselle.")
            ohjeet.append("Lisää haamuja ilmestyy 25 pisteen välein.")
            ohjeet.append("Pelaamaan pääset painamalla välilyöntiä.")
            ohjeet.append("")
            ohjeet.append("Onnea peliin!")
            fontti = pygame.font.SysFont("Arial", 24)
            i = 0
            n = 0
            # Käydään "ohjeet"-taulukon alkiot läpi tulostaen ne ruudulle
            while i < len(ohjeet):
                ohjeteksti = fontti.render(f"{ohjeet[i]}", True, (255, 0, 0))
                self.naytto.blit(ohjeteksti, (320-ohjeteksti.get_width()/2, (n+1)*ohjeteksti.get_height()))
                i += 1
                n = i+1
            pygame.display.flip()

    def pelaa(self):
        while True:
            ovi1 = Ovi(0-0.7*self.ovi.get_width(), 240-self.ovi.get_height()/2)
            ovi2 = Ovi(640-0.3*self.ovi.get_width(), 240-self.ovi.get_height()/2)

            # Määritellään robotin liikuttamiseen tarvittavat komennot
            for tapahtuma in pygame.event.get():
                if tapahtuma.type == pygame.KEYDOWN:
                    if tapahtuma.key == pygame.K_LEFT:
                        self.vasemmalle = True
                    if tapahtuma.key == pygame.K_RIGHT:
                        self.oikealle = True
                    if tapahtuma.key == pygame.K_DOWN:
                        self.alas = True
                    if tapahtuma.key == pygame.K_UP:
                        self.ylos = True
                if tapahtuma.type == pygame.KEYUP:
                    if tapahtuma.key == pygame.K_LEFT:
                        self.vasemmalle = False
                    if tapahtuma.key == pygame.K_RIGHT:
                        self.oikealle = False
                    if tapahtuma.key == pygame.K_DOWN:
                        self.alas = False
                    if tapahtuma.key == pygame.K_UP:
                        self.ylos = False
                if tapahtuma.type == pygame.QUIT:
                    exit()
            if self.oikealle and self.x+self.robo.get_width() < 640:
                self.x += 4
            if self.vasemmalle and self.x >= 0: 
                self.x -= 4
            if self.alas and self.y+self.robo.get_height() < 480:
                self.y += 4
            if self.ylos and self.y >= 0:
                self.y -= 4

            self.naytto.fill((120, 40, 100))

            # Pisteet ruudun oikeaan ylänurkkaan
            fontti = pygame.font.SysFont("Arial", 24)
            teksti = fontti.render(f"Pisteet: {self.pisteita}", True, (255, 0, 0))
            self.naytto.blit(teksti, (640-teksti.get_width(), 0))

            self.naytto.blit(self.ovi, (ovi1.get_x(), ovi1.get_y()))
            self.naytto.blit(self.ovi, (ovi2.get_x(), ovi2.get_y()))

            # Määritellään kolme satunnaista kolikon tiputuspaikkaa
            # Korkeus vähintään ruudun puolesta välistä 
            i = 0
            if len(self.sijainnit_kolikko) == 0:
                while i < 3:   
                    x_kolikko = random.randint(0, 640-self.kolikko.get_width())
                    y_kolikko = random.randint(0, 240-self.kolikko.get_height())
                    sijainti_kolikko = Kolikko(x_kolikko, y_kolikko)
                    self.sijainnit_kolikko.append(sijainti_kolikko.aseta())            
                    i += 1

            # Määritellään hirviöiden paikat
            i = 0 
            # Kolme vaakasuunnassa liikkuvaa hirviötä
            if len(self.sijainnit_hirvio) == 0:
                while i < 3:   
                    x_hirvio = random.randint(0, 640-self.hirvio.get_width())
                    y_hirvio = (240*i)-self.robo.get_height()*(1/2)*i
                    if y_hirvio == 480-self.robo.get_height():
                        while x_hirvio > 200 and x_hirvio < 440-self.hirvio.get_height():
                            x_hirvio = random.randint(0, 640-self.hirvio.get_width())
                    sijainti_hirvio = Hirvio(x_hirvio, y_hirvio, 3-i)
                    self.sijainnit_hirvio.append(sijainti_hirvio.aseta())            
                    i += 1
                # Ruudun keskiosaa kiertävä hirviö
                sijainti_hirvio = Hirvio(320+math.cos(self.kulma)*150-self.hirvio.get_width()/2, 240+math.sin(self.kulma)*150-self.hirvio.get_height()/2, 0) 
                self.sijainnit_hirvio.append(sijainti_hirvio.aseta()) 
                
                # Pystysuunnassal iikkuva hirviö
                sijainti_hirvio = Hirvio(320-self.hirvio.get_width()/2, 0, 2)
                self.sijainnit_hirvio.append(sijainti_hirvio.aseta())   

                # Pelaajaa seuraava hirviö
                sijainti_hirvio =  Hirvio(random.randint(0, 640-self.hirvio.get_width()), random.randint(0, 480-self.hirvio.get_height()), 2)                
                self.sijainnit_hirvio.append(sijainti_hirvio.aseta()) 

            i = 0 

            # Määritellään teleporttien toiminta
            # Y-koordinaattia kasvatetaan kymmenellä, jotta ovi toimii reunoja myöten,
            # selitys "Hahmo"-luokoan "osuma"-metodin yhteydessä
            if ovi1.osuma(self.ovi, self.robo, self.x, self.y-10) or ovi1.osuma(self.ovi, self.robo, self.x, self.y+10):
                self.x = 620-self.robo.get_width()
            elif ovi2.osuma(self.ovi, self.robo, self.x, self.y-10) or ovi2.osuma(self.ovi, self.robo, self.x, self.y+10):
                self.x = 20

            # Käydään läpi osuuko pelaaja joko kolikoihin tai vaakasuuntaan liikkuviin hirviöihin tai osuuko kolikko maahan
            while i < 3:
                self.naytto.blit(self.kolikko, (self.sijainnit_kolikko[i].get_x(), self.sijainnit_kolikko[i].get_y())) 
                self.naytto.blit(self.hirvio, (self.sijainnit_hirvio[i].get_x(), self.sijainnit_hirvio[i].get_y()))
                piste_kolikko = self.sijainnit_kolikko[i].liikuta(self.kolikko, self.robo, self.x, self.y)
                piste_hirvio = self.sijainnit_hirvio[i].liikuta(self.hirvio, self.robo, self.x, self.y)
                if piste_kolikko < 0 or piste_hirvio < 0:
                    self.loppu = True
                    #self.lopetus(self.pisteita)
                else:
                    self.pisteita += piste_kolikko
                    self.sijainnit_kolikko[i] = self.sijainnit_kolikko[i].aseta()
                    self.sijainnit_hirvio[i] = self.sijainnit_hirvio[i].aseta()            
                i += 1
            # 25 pisteen kohdalla otetaan ruudulle keskustaa kiertävä hirviö. Hirviö ei vielä voi vahingoittaa pelaajaa.
            # 26 pisteen kohdalla pelaaja ei voi enää osua uuteen hirviöön
            if self.pisteita >= 25:
                self.naytto.blit(self.hirvio, (self.sijainnit_hirvio[3].get_x(), self.sijainnit_hirvio[3].get_y()))
                piste_hirvio = self.sijainnit_hirvio[3].kierra(self.hirvio, self.kulma, self.robo, self.x, self.y)
            if self.pisteita > 25:
                if piste_hirvio < 0:
                    #self.lopetus(self.pisteita)
                    self.loppu = True
            # 50 pisteen kohdalla otetaan ruudulle ruudun keskellä pystysuuntaisesti liikkuva hirviö. 
            # Hirviö ei vielä voi vahingoittaa pelaajaa.
            # 51 pisteen kohdalla pelaaja ei voi enää osua uuteen hirviöön
            if self.pisteita >= 50:
                self.naytto.blit(self.hirvio, (self.sijainnit_hirvio[4].get_x(), self.sijainnit_hirvio[4].get_y()))
                piste_hirvio = self.sijainnit_hirvio[4].pystyliike(self.hirvio, self.robo, self.x, self.y)
            if self.pisteita > 50:                
                if piste_hirvio < 0:
                    #self.lopetus(self.pisteita)
                    self.loppu = True
            # 75 pisteen kohdalla otetaan ruudulle pelaajaa seuraava hirviö. Hirviö ei vielä voi vahingoittaa pelaajaa.
            # 76 pisteen kohdalla pelaaja ei voi enää osua uuteen hirviöön
            if self.pisteita >= 75:
                self.naytto.blit(self.hirvio, (self.sijainnit_hirvio[5].get_x(), self.sijainnit_hirvio[5].get_y()))
                piste_hirvio = self.sijainnit_hirvio[5].seuraa(self.hirvio, self.robo, self.x, self.y)
            if self.pisteita > 75:                
                if piste_hirvio < 0:
                    #self.lopetus(self.pisteita)
                    self.loppu = True

            if self.loppu == True:
                self.lopetus(self.pisteita)

            self.naytto.blit(self.robo, (self.x, self.y))
            pygame.display.flip()

            self.kulma += 0.01
            self.kello.tick(60)

    def lopetus(self, tulos):
        while True:
            for tapahtuma in pygame.event.get():
                if tapahtuma.type == pygame.KEYDOWN:
                    if tapahtuma.key == pygame.K_n or tapahtuma.key == pygame.K_SPACE:
                        peli = Peli()
                        peli.pelaa()
                    if tapahtuma.key == pygame.K_ESCAPE:
                        exit()
                if tapahtuma.type == pygame.QUIT:
                    exit()

            fontti = pygame.font.SysFont("Arial", 24)
            pisteet = fontti.render(f"Peli loppui. Tuloksesi oli {tulos} pistettä.", True, (255, 0, 0))
            teksti = fontti.render(f"Paina n tai välilyönti, jos haluat pelata uudelleen.", True, (255, 0, 0))
            
            self.naytto.blit(pisteet, (320-pisteet.get_width()/2, 240-pisteet.get_height()))
            self.naytto.blit(teksti, (320-teksti.get_width()/2, 240))
            pygame.display.flip()

peli = Peli()
peli.ohjeet()