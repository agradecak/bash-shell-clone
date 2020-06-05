#   import koristenih modula
import os
import time

#   ispis pozdravne poruke i trenutnog vremena
vrijeme = time.ctime()
print('Pozdrav! ({})'.format(vrijeme))

#   definicija funkcije ispisa odzivnog znaka
def ispisi_odziv():
    #   da varijable budu globalne ili in-function defined?
    op_sustav = os.uname()[0]
    korisnik = os.getlogin()
    direktorij = os.getcwd()
    print('{}@{}:{}$ '.format(op_sustav, korisnik, direktorij))
    
ispisi_odziv()