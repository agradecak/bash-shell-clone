#   ___MODULI___
import os
import time


#   ___DEFINICIJE___

#   definicija funkcije ispisa odzivnog znaka
def ispisi_odziv():
    #   da varijable budu globalne ili in-function defined?
    op_sustav = os.uname()[0]
    korisnik = os.getlogin()
    direktorij = os.getcwd()
    print('({}::{}){} $ '.format(korisnik, op_sustav, direktorij), end = '')

#   vraca korisnicki unos (string)
def korisn_unos():
    unos = input()
    return unos

#   provjerava zavrsetak programa
def je_izlaz(unos):
    if unos == 'izlaz' or unos == 'odjava':
        return 1


#   ___MAIN___

#   ispis pozdravne poruke i trenutnog vremena
vrijeme = time.ctime()
print('Pozdrav! ({})'.format(vrijeme))

#   glavna petlja
while (True):
    unos = ''
    ispisi_odziv()
    unos = korisn_unos()

    #   provjera izlaza iz programa
    if je_izlaz(unos):
        break
