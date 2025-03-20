import cv2 as cv
import numpy as np


def zmanjsaj_sliko(slika, sirina, visina):
    return cv.resize(slika, (sirina, visina))
    


def obdelaj_sliko_s_skatlami(slika, sirina_skatle, visina_skatle, barva_koze) -> list:
    '''Sprehodi se skozi sliko v velikosti škatle (sirina_skatle x visina_skatle) in izračunaj število pikslov kože v vsaki škatli.
    Škatle se ne smejo prekrivati!
    Vrne seznam škatel, s številom pikslov kože.
    Primer: Če je v sliki 25 škatel, kjer je v vsaki vrstici 5 škatel, naj bo seznam oblike
      [[1,0,0,1,1],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[1,0,0,0,1]].
      V tem primeru je v prvi škatli 1 piksel kože, v drugi 0, v tretji 0, v četrti 1 in v peti 1.'''
    spodnja_meja = np.array(barva_koze[0], dtype=np.uint8)
    zgornja_meja = np.array(barva_koze[1], dtype=np.uint8)

    # Preverimo dimenzije slike
    visina, sirina, _ = slika.shape

    skatle = []

    for y in range(0, visina - visina_skatle, visina_skatle):
        vrstica_skatel = []
        for x in range(0, sirina - sirina_skatle, sirina_skatle):

            podslika = slika[y:y + visina_skatle, x:x + sirina_skatle]

            maska = cv.inRange(podslika, spodnja_meja, zgornja_meja)

            stevilo_pikslov_koze = np.sum(maska > 0)
            vrstica_skatel.append(stevilo_pikslov_koze)

        skatle.append(vrstica_skatel)

    return skatle


def prestej_piklse_z_barvo_koze(slika, barva_koze) -> int:
    '''Prestej število pikslov z barvo kože v škatli.'''
    pass


def doloci_barvo_koze(slika, levo_zgoraj, desno_spodaj) -> tuple:
    '''Ta funkcija se kliče zgolj 1x na prvi sliki iz kamere.
    Vrne barvo kože v območju ki ga definira oklepajoča škatla (levo_zgoraj, desno_spodaj).
      Način izračuna je prepuščen vaši domišljiji.'''
    pass


if __name__ == '__main__':
    # Pripravi kamero

    # Zajami prvo sliko iz kamere

    # Izračunamo barvo kože na prvi sliki

    # Zajemaj slike iz kamere in jih obdeluj

    # Označi območja (škatle), kjer se nahaja obraz (kako je prepuščeno vaši domišljiji)
    # Vprašanje 1: Kako iz števila pikslov iz vsake škatle določiti celotno območje obraza (Floodfill)?
    # Vprašanje 2: Kako prešteti število ljudi?

    # Kako velikost prebirne škatle vpliva na hitrost algoritma in točnost detekcije? Poigrajte se s parametroma velikost_skatle
    # in ne pozabite, da ni nujno da je škatla kvadratna.
    pass