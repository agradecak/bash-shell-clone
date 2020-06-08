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
    elif lista[0] == 'date': date(lista)
    elif lista[0] == 'ls': ls(lista)
    elif lista[0] == 'touch': touch(lista)
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
            dat = dat.replace("'", '')
            print(dat, end=' ')
        print('')

#   obraduje signal ili obavjestava o krivom unosu
def kill(lista):
    if len(lista) == 1:
        print("Naredba prima tocno jedan parametar: naziv signala ili njegov redni broj.")
    else:
        signal = int(lista[1].strip('-'))
        os.kill(os.getpid(), signal)
#   mjenja direktorij ovisno o koristenom parametru
def cd(lista):
    #   izvrsava se ako nema parametara
    if len(lista) == 1:
        os.chdir(os.path.expanduser('~'))
    #   izvrsava se ako ima jedan parametar
    elif len(lista) == 2:
        #   slice prva dva karaktera u parametru, za provjeru sta se koristi
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
    #   izvrsava se ako ima previse parametara
    else:
        print('Dopusten je unos samo jednog parametra.')

def date(lista):
    if len(lista) == 1:
        print(time.strftime("%H<>%M<>%S %A %d./%m./%Y", time.localtime()))
    elif len(lista) == 2 and lista[1] == '-w':
        print(time.strftime("%H<>%M<>%S %a %d./%m./%Y", time.localtime()))
    else:
        print("Naredba prima najvise jedan parametar (-w).")

def ls(lista):
    if len(lista) == 1:
        sadrzaj = os.scandir()
        for dat in sadrzaj:
            #   ako datoteka nije sakrivena (pocinje sa '.'), ispisi podatke
            if not dat.name[0] == '.':
                print(dat.name)
    elif len(lista) == 2 and lista[1] == '-l':
        sadrzaj = os.scandir()
        print('{: <20}{: >10}{: >10}{: >10}{: >10}{: >10}'.format('Name', 'Mode' , 'Nlinks', 'UID', 'GID', 'Size'))
        print('-' * 70)
        for dat in sadrzaj:
            if not dat.name[0] == '.':
                info = dat.stat()
                print('{: <20}{: >10}{: >10}{: >10}{: >10}{: >10}'.format(dat.name, info.st_mode, info.st_nlink, info.st_uid, info.st_gid, info.st_size))
    elif len(lista) == 2 and lista[1][0:2] == './':
        try:
            odrediste = lista[1].strip('./')
            dublje = os.path.join(os.getcwd(), odrediste)
            sadrzaj = os.scandir(dublje)
            for dat in sadrzaj:
                #   ako datoteka nije sakrivena (pocinje sa '.'), ispisi podatke
                if not dat.name[0] == '.':
                    print(dat.name)
        except:
            print('Direktorij ne postoji.')
    elif len(lista) == 3 and lista[1] == '-l' and lista[2][0:2] == './':
        try:
            odrediste = lista[2].strip('./')
            dublje = os.path.join(os.getcwd(), odrediste)
            sadrzaj = os.scandir(dublje)
            print('{: <20}{: >10}{: >10}{: >10}{: >10}{: >10}'.format('Name', 'Mode' , 'Nlinks', 'UID', 'GID', 'Size'))
            print('-' * 70)
            for dat in sadrzaj:
                if not dat.name[0] == '.':
                    info = dat.stat()
                    print('{: <20}{: >10}{: >10}{: >10}{: >10}{: >10}'.format(dat.name, info.st_mode, info.st_nlink, info.st_uid, info.st_gid, info.st_size))
        except:
            print('Direktorij ne postoji.')
    else:
        print('Naredba prima najvise jedan parametar (-l) i jedan argument (rel. adresu).')

def touch(lista):
    put = lista[1]
    if os.path.isfile(put):
        print('Datoteka vec postoji.')
    else:
        try:
            open(put, 'w').close()
        except:
            print('Direktorij ne postoji.')

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
    #   ako je lista prazna, nastavi (kako se nebi pristupalo indeksima kojih nema)
    if not unos_split:
        continue
    #   ako lista nije prazna, provjeri za i izvrsi naredbu
    else:
        izvrsi(unos_split)
