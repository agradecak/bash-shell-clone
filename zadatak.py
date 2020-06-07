#   ________________________________________________________________________________
#   MODULI
import os
import time
import sys
import signal
import re

#   ________________________________________________________________________________
#   SIGNALI

#   ignorira signal 3 i ispisuje obavijest korisniku
def upravljacQUIT(broj_signala, stog):
    print('Signal broj 3 je ignoriran.')
    return

#   ispisuje obavijest i prekida izvodjenje programa
def upravljacTERM(broj_signala, stog):
    print('Pristigao je signal broj 15. Program se zavrsava.')
    sys.exit()
    return

signal.signal(signal.SIGINT, signal.SIG_DFL)
signal.signal(signal.SIGQUIT, upravljacQUIT)
signal.signal(signal.SIGTERM, upravljacTERM)

#   ________________________________________________________________________________
#   DEFINICIJE

#   ispisuje odzivni znak
def ispisi_odziv():
    #   da varijable budu globalne ili in-function defined?
    op_sustav = os.uname()[0]
    korisnik = os.getlogin()
    direktorij = os.getcwd()
    print('({}::{}){} $ '.format(korisnik, op_sustav, direktorij), end = '')

#   provjerava unos naredbi
def izvrsi(lista):
    #   funkcija radi za prepoznavanje nepoznatih naredbi ali
    #   if statements cekaju definicije svojih funkcija umjesto placeholdera pass
    if lista[0] == 'pwd': pwd(lista)
    elif lista[0] == 'ps': ps(lista)
    elif lista[0] == 'echo': echo(lista)
    elif lista[0] == 'kill': kill(lista)
    elif lista[0] == 'cd': cd(lista)
    elif lista[0] == 'ls': pass
    elif lista[0] == 'touch': pass
    elif lista[0] == 'rm': pass
    elif lista[0] == 'kvadrat': pass
    elif lista[0] == 'izlaz' or lista[0] == 'odjava':
        sys.exit()
    else:
        print('Neprepoznata naredba.')

#   ispisuje apsolutnu adresu trenutnog direktorija ili obavjestava o krivom unosu
def pwd(lista):
    if len(lista) == 1:
        print(os.getcwd())
    else:
        print('Naredba ne prima parametre ni argumente.')

#   ispisuje PID trenutnog procesa ili obavjestava o krivom unosu
def ps(lista):
    if len(lista) == 1:
	    print(os.getpid())
    else:
	    print('Nepostojeci parametar ili argument.')

#   ispisuje korisnicki string ili obavjestava o krivom unosu
def echo(lista):
    if len(lista) == 1:
        print("Naredba prima barem jedan argument.")
    else:
        for dat in lista[1:]:
            dat = dat.replace('"', '')
            print(dat, end=' ')
        print('')

#   obraduje signal ili obavjestava o krivom unosu
def kill(lista):
    if len(lista) == 1:
        print("Naredba prima tocno jedan parametar: naziv signala ili njegov redni broj.")
    else:
        signal = int(lista[1].strip('-'))
        os.kill(os.getpid(), signal)

def cd(lista):
    if len(lista) == 1:
        os.chdir(os.path.expanduser('~'))
    elif len(lista) == 2:
        param = lista[1][0:2]
        if param == '.':
            pass
        elif param == '..':
            roditelj = os.path.join(os.getcwd(), os.pardir)
            os.chdir(roditelj)
        elif param == './':
            try:
                odrediste = lista[1].strip('./')
                dublje = os.path.join(os.getcwd(), odrediste)
                os.chdir(dublje)
            except:
                print('Direktorij ne postoji.')
        elif lista[1][0:1] == '/':
            try:
                os.chdir(lista[1])
            except:
                print('Direktorij ne postoji.')
        else:
            print('Nepostojeci parametar.')
    else:
        print('Dopusten je unos samo jednog parametra.')

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

#   ________________________________________________________________________________
#   MAIN

#   ispis pozdravne poruke i trenutnog vremena
vrijeme = time.ctime()
print('Pozdrav! ({})'.format(vrijeme))

#   glavna petlja
while (True):
    unos = ''
    ispisi_odziv()
    unos = input()
    unos_split = unos.split()
    #   ako je lista prazna, nastavi nastavi
    if not unos_split:
        continue
    #   ako lista nije prazna, provjeri za i izvrsi naredbu
    else:
        izvrsi(unos_split)
