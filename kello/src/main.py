import pygame, datetime, math

pygame.init()
naytto = pygame.display.set_mode((640, 480))
naytto.fill((0, 0, 0))
kello = pygame.time.Clock()

#(r, g, b), (alkupiste x, alkupiste y, leveys, korkeus)
#pygame.draw.rect(naytto, (0, 255, 0), (0, 0, 640, 480))
#(r, g, b), (keskipiste x, keskipiste y), halkaisija 
#pygame.draw.circle(naytto, (255, 0, 0), (320, 240), 200)
#(r, g, b), (alkupiste x, alkupiste y), (loppupiste x, loppupiste y) paksuus
#pygame.draw.line(naytto, (0, 0, 255), (320, 240), (300, 160), 2)

kulma_s = 0




while True:
    for tapahtuma in pygame.event.get():
        if tapahtuma.type == pygame.QUIT:
            exit()

    current_time = datetime.datetime.now()  
    t_sijainti= current_time.hour 
    m_sijainti = current_time.minute    
    s_sijainti = current_time.second 

    kulma_t = (t_sijainti*5-15)*(2*math.pi/60)
    kulma_m = (m_sijainti-15)*(2*math.pi/60)
    kulma_s = (s_sijainti-15)*(2*math.pi/60)

    #(r, g, b), (alkupiste x, alkupiste y, leveys, korkeus)
    pygame.draw.rect(naytto, (120, 40, 100), (0, 0, 640, 480))
    #(r, g, b), (keskipiste x, keskipiste y), halkaisija 
    pygame.draw.circle(naytto, (200, 200, 200), (320, 240), 200)
    pygame.draw.circle(naytto, (0, 0 , 0), (320, 240), 200, 4)
    pygame.draw.circle(naytto, (0, 0, 0), (320, 240), 10)
    #(r, g, b), (alkupiste x, alkupiste y), (loppupiste x, loppupiste y) paksuus
    pygame.draw.line(naytto, (0, 0, 100), (320, 240), (320+math.cos(kulma_t)*100, 240+math.sin(kulma_t)*100), 2)
    pygame.draw.line(naytto, (0, 0, 100), (320, 240), (320+math.cos(kulma_m)*140, 240+math.sin(kulma_m)*140), 2)
    pygame.draw.line(naytto, (0, 0, 100), (320, 240), (320+math.cos(kulma_s)*180, 240+math.sin(kulma_s)*180), 2)

    pygame.display.flip()

    kello.tick(60)