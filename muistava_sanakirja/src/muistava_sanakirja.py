def muistava_sanakirja():
    while True:
        print("1 - Lisää sana, 2 - Hae sanaa, 3 - Poistu")
        valinta = int(input("Valinta: " ))

        if valinta == 3:
            print("Moi!")
            break
        elif valinta == 1:
            suomi = input("Anna sana suomeksi: ")
            engl = input("Anna sana englanniksi: ")
            pari = suomi + " - " + engl + "\n"
            with open("sanakirja.txt", "a") as tiedosto:
                tiedosto.write(pari)
                print("Sanapari lisätty")
        elif valinta == 2:
            haettava = input("Anna sana: ")
            with open("sanakirja.txt") as tiedosto:
                for rivi in tiedosto:
                    if rivi.find(haettava) >= 0:
                        rivi = rivi.replace("\n", "")
                        print(rivi)


muistava_sanakirja()


