#   ___MODULI___
import os
import time
import sys


#   ___DEFINICIJE___

#   ispisuje odzivni znak
def ispisi_odziv():
    #   da varijable budu globalne ili in-function defined?
    op_sustav = os.uname()[0]
    korisnik = os.getlogin()
    direktorij = os.getcwd()
    print('({}::{}){} $ '.format(korisnik, op_sustav, direktorij), end = '')

#   provjerava unos naredbi
def provjeri_unos(lista):
    #   funkcija radi za prepoznavanje nepoznatih naredbi ali
    #   if statements cekaju definicije svojih funkcija umjesto placeholdera pass
    if lista[0] == 'pwd': pwd(lista)
    elif lista[0] == 'ps': pass
    elif lista[0] == 'echo': pass
    elif lista[0] == 'kill': pass
    elif lista[0] == 'cd': pass
    elif lista[0] == 'ls': pass
    elif lista[0] == 'touch': pass
    elif lista[0] == 'rm': pass
    elif lista[0] == 'kvadrat': pass
    elif lista[0] == 'izlaz' or lista[0] == 'odjava':
        sys.exit()
    else:
        print('Neprepoznata naredba.')

def pwd (lista):
    if len(lista) == 1:
        print(os.getcwd())
    else:
        print('Naredba ne prima parametre ni argumente.')
def ps (lista):
    if len(lista) == 1:
	print(os.getpid())
    else:
	print('Ne postojeci parametar ili argument.')
""" 
#   pokusaj naredbi


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

"""


#   ___MAIN___

#   ispis pozdravne poruke i trenutnog vremena
vrijeme = time.ctime()
print('Pozdrav! ({})'.format(vrijeme))

#   glavna petlja
while (True):
    unos = ''
    ispisi_odziv()
    unos = input()
    unos_split = unos.split()
    provjeri_unos(unos_split)














