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

#   pokusaj naredbi
def pwd (unos):
    if unos == 'pwd': # ILI REG \pwd$
        print('({}::{}){} $ '.format(korisnik, op_sustav, direktorij), end = '')
    else
        print('Naredba neprima ni parametre ni argumente')

def echo (unos):
    if unos == 'echo':  # REG \echo$
        print('Naredba prima barem jedan argument')
    # regularni izraz ???
    else unos == 'echo' # REG \echo\s([a-z]+\s)|\"([a-z]+\s)"
        # ispis argumenta bez ""
        # x=re.search([a-z]+\s)
        print('x')

def kill (unos):
    if unos == 'kill':  # REG \kill$
        print('Naredba prima tocno jedan parametar: naziv signala ili njegov redni broj')
    if else unos == 'echo -15': # \echo\s\-[0-9]{1,2}|[A-Z]{1,}
        print('Pristigao je signal 15 . Program se zatvara')



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
