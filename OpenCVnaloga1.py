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
    spodnja_meja = np.array(barva_koze[0], dtype=np.uint8)
    zgornja_meja = np.array(barva_koze[1], dtype=np.uint8)

    maska = cv.inRange(slika, spodnja_meja, zgornja_meja)

    stevilo_pikslov_koze = np.sum(maska > 0)

    return stevilo_pikslov_koze
    pass


def doloci_barvo_koze(slika, levo_zgoraj, desno_spodaj) -> tuple:
    '''Določimo meje barve kože na podlagi izbranega območja v sliki.'''

    izrez = slika[levo_zgoraj[1]:desno_spodaj[1], levo_zgoraj[0]:desno_spodaj[0]]
    povprecje_bgr = np.mean(izrez, axis=(0, 1))

    spodnja_meja = np.maximum(povprecje_bgr - 20, 0)
    zgornja_meja = np.minimum(povprecje_bgr + 20, 255)

    return (spodnja_meja.astype(np.uint8), zgornja_meja.astype(np.uint8))


if __name__ == '__main__':
    cap = cv.VideoCapture(0)  # Kamera 0 je običajno privzeta kamera
    if not cap.isOpened():
        print("Napaka pri odpiranju kamere.")
        exit()

    # Nastavitev velikosti slike
    sirina, visina = 320, 240
    cap.set(3, sirina)
    cap.set(4, visina)

    # Zajemi prvo sliko iz kamere
    ret, slika = cap.read()
    if not ret:
        print("Napaka pri zajemu prve slike.")
        exit()

    # Določimo območje za barvo kože (izberite primerno območje na prvi sliki)
    levo_zgoraj = (50, 50)
    desno_spodaj = (150, 150)

    # Izračunamo barvo kože na prvi sliki
    barva_koze = doloci_barvo_koze(slika, levo_zgoraj, desno_spodaj)

    # Zajemaj slike iz kamere in jih obdeluj
    while True:
        ret, slika = cap.read()
        if not ret:
            break

        # Preprosta obdelava slike
        skatle = obdelaj_sliko_s_skatlami(slika, 60, 80, barva_koze)

        # Označi območja (škatle), kjer se nahaja obraz
        for (x, y, w, h) in skatle:
            cv.rectangle(slika, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # Prikaz rezultatov
        cv.putText(slika, "Press 'q' to exit", (10, 30), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        cv.imshow("Detekcija obraza", slika)

        # Pritisnite 'q' za izhod
        if cv.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv.destroyAllWindows()