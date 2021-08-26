def syote():
    sisalto = input("Syötä sanasta haettava sisältö: ")
    print(hae_sanat(sisalto))

def hae_sanat(hakusana: str):
    sanat = []
    if "." in hakusana:
        sanat = pisteet_kirjaimiksi(hakusana)
    else: 
        sanat = etsi(hakusana)
        
            
    return sanat

def etsi(hakusana):
    sanat = []
    with open("sanat.txt") as tiedosto:
        for rivi in tiedosto:
            rivi = rivi.replace("\n", "")
            verrokki = str(rivi)
            if hakusana[0] == "*" and hakusana[len(hakusana)-1] == "*":
                etsi = hakusana[1:len(hakusana)-1]
                if etsi in verrokki:
                    sanat.append(verrokki)
            elif hakusana[0] == "*":
                etsi = hakusana[1:]
                i = verrokki.find(etsi)
                if i >= 0 and len(verrokki) == i+len(etsi):
                    sanat.append(verrokki)
            elif hakusana[len(hakusana)-1] == "*":
                etsi = hakusana[:len(hakusana)-1]
                i = verrokki.find(etsi)
                if i == 0:
                    sanat.append(verrokki)
            elif verrokki == hakusana:
                sanat.append(verrokki)
    return sanat

def etsi_pituus(pituus):
    sanat = []
    with open("sanat.txt") as tiedosto:
        for rivi in tiedosto:
            rivi = rivi.replace("\n", "")
            verrokki = str(rivi)
            if len(verrokki) == pituus:
                sanat.append(verrokki)
    return sanat



def pisteet_kirjaimiksi(hakusana):
    kirjaimet = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]
    i = 0
    j = 0
    pisteiden_maara = 0
    sanalista = [hakusana]
    palautettavat = []
    listan_koko = 26
    mahdolliset = etsi_pituus(len(hakusana))
    
    indeksit = []
    while i < len(hakusana):
        if hakusana[i] != ".":
            indeksit.append(i)
        i += 1
    
    for sana in mahdolliset:
        i = 0
        on_sama = False
        while i < len(indeksit):
            if sana[indeksit[i]]  == hakusana[indeksit[i]]:
                on_sama = True
            else:
                on_sama = False
                i += 1
                break
            i += 1
        if on_sama == True:
            palautettavat.append(sana)


       #palautettavat.append(sana)       
        
    print(f"sanalista {sanalista}")
    sanalista = palautettavat
    print(f"palautettavat {palautettavat}")
    return sanalista

syote()
#if __name__ == "__main__":  

 #   print(hae_sanat("*aa*"))