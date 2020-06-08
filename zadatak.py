#   ________________________________________________________________________________
#   MODULI
import os
import time
import sys
import signal
import threading



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

#   signali koji su usmjereni na specijalno definirane upravljace
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
def izvrsi(naredba_lista):
    #   funkcija radi za prepoznavanje naredbi
    #   funkcijama se proslijedjuje korisnicki unos u obliku liste (naredba, parametar, argument...)
    if naredba_lista[0] == 'pwd': pwd(naredba_lista)
    elif naredba_lista[0] == 'ps': ps(naredba_lista)
    elif naredba_lista[0] == 'echo': echo(naredba_lista)
    elif naredba_lista[0] == 'kill': kill(naredba_lista)
    elif naredba_lista[0] == 'cd': cd(naredba_lista)
    elif naredba_lista[0] == 'date': date(naredba_lista)
    elif naredba_lista[0] == 'ls': ls(naredba_lista)
    elif naredba_lista[0] == 'touch': touch(naredba_lista)
    elif naredba_lista[0] == 'rm': rm(naredba_lista)
    elif naredba_lista[0] == 'kvadrat': kvadrat(naredba_lista)
    elif naredba_lista[0] == 'izlaz' or naredba_lista[0] == 'odjava':
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
        #   radi se slice prva dva karaktera u parametru, za provjeru sta se koristi
        param = lista[1][0:2]
        if param == '.':
            pass
        elif param == '..':
            roditelj = os.path.join(os.getcwd(), os.pardir)
            os.chdir(roditelj)
        #   ako naredba ne uspjeva, ispisuje se obavijest o pogresci
        elif param == './':
            try:
                odrediste = lista[1].strip('./')
                dublje = os.path.join(os.getcwd(), odrediste)
                os.chdir(dublje)
            except:
                print('Nepostojeca adresa.')
        elif lista[1][0:1] == '/':
            try:
                os.chdir(lista[1])
            except:
                print('Nepostojeca adresa.')
        else:
            print('Nepostojeci parametar.')
    #   izvrsava se ako ima previse parametara
    else:
        print('Dopusten je unos samo jednog parametra.')

#   ispisuje posebno formatirano vrijeme, u kratkom ili dugom obliku dana u tjednu
def date(lista):
    if len(lista) == 1:
        print(time.strftime("%H<>%M<>%S %A %d./%m./%Y", time.localtime()))
    elif len(lista) == 2 and lista[1] == '-w':
        print(time.strftime("%H<>%M<>%S %a %d./%m./%Y", time.localtime()))
    else:
        print("Naredba prima najvise jedan parametar (-w).")

#   ispisuje sadrzaj direktorija, ovisno o adresi na koju pokazujemo
def ls(lista):
    #   izvrsava se ukoliko nije zadan ni argument ni parametar
    if len(lista) == 1:
        sadrzaj = os.scandir()
        for dat in sadrzaj:
            #   ako datoteka nije sakrivena (pocinje sa '.'), ispisi podatke
            if not dat.name[0] == '.':
                print(dat.name)
    #   izvrsava se ukoliko je zadan samo argument -l, za dugi ispis trenutnog direktorija
    elif len(lista) == 2 and lista[1] == '-l':
        sadrzaj = os.scandir()
        #   ispis i formatiranje naziva podataka (sirina i poravnanje)
        print('{: <20}{: >10}{: >10}{: >10}{: >10}{: >10}'.format('Name', 'Mode' , 'Nlinks', 'UID', 'GID', 'Size'))
        print('-' * 70)
        for dat in sadrzaj:
            if not dat.name[0] == '.':
                info = dat.stat()
                #   (limitacija) ispis je uredan samo za datoteke duljine do 20 karaktera
                print('{: <20}{: >10}{: >10}{: >10}{: >10}{: >10}'.format(dat.name, info.st_mode, info.st_nlink, info.st_uid, info.st_gid, info.st_size))
    #   izvrsava se ukoliko je zadana relativna adresa direktorija
    elif len(lista) == 2 and lista[1][0:2] == './':
        #   ispituje se valjanost pristupa direktoriju
        try:
            odrediste = lista[1].strip('./')
            dublje = os.path.join(os.getcwd(), odrediste)
            sadrzaj = os.scandir(dublje)
            for dat in sadrzaj:
                #   ako datoteka nije sakrivena (pocinje sa '.'), ispisi podatke
                if not dat.name[0] == '.':
                    print(dat.name)
        #   inace baca obavijest o krivom pristupu
        except:
            print('Nepostojeca adresa.')
    #   izvrsava se ukoliko je zadan dugi ispis direktorija na relativnoj adresi
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
            print('Nepostojeca adresa.')
    #   ispisuje pogresku ukoliko je uneseno previse argumenata, ili krivih
    else:
        print('Naredba prima najvise jedan parametar (-l) i jedan argument (rel. adresu).')

#   stvara datoteku na adresi ukoliko ona vec ne postoji
def touch(lista):
    odrediste = lista[1]
    if os.path.isfile(odrediste):
        print('Datoteka vec postoji.')
    else:
        #   ako pristup ne uspijeva
        try:
            open(odrediste, 'w').close()
        #   ispisuje se pogreska
        except:
            print('Nepostojeca adresa.')

#   brise datoteku na adresi ukoliko ona tamo postoji
def rm(lista):
    odrediste = lista[1]
    if os.path.isfile(odrediste):
        os.remove(odrediste)
    #   ispisuje pogresku ako je pristup datoteci nevaljan
    else:
        print('Datoteka ne postoji.')

#   ________________________________________________________________________________
#   NITI

broj = 33330330330320320320
lokot = threading.Lock()
barijera = threading.Barrier(4)

#   neki opis
def oduzmi_kvad(pocetak, kraj):
    lokot.acquire()
    global broj
    medjuvrijed = open('/home/andrija/result.txt', 'a')
    for i in range(pocetak, kraj):
        broj -= i*i
        medjuvrijed.write(str(broj))
        medjuvrijed.write('\n')
    medjuvrijed.close()
    lokot.release()
    id_niti = barijera.wait()
    if id_niti == 1:
        print("Nit {} spava".format(id_niti))
        time.sleep(2)
        print("Nit {} je zavrsila spavat.".format(id_niti))
    print('Nit {} je zavrsila sa radom.'.format(id_niti))


#   neki opis
def kvadrat(lista):
    open('/home/andrija/result.txt', 'w').close()
    nit1.start()
    nit2.start()
    nit3.start()
    nit4.start()
    nit1.join()
    nit2.join()
    nit3.join()
    nit4.join()

nit1 = threading.Thread(target=oduzmi_kvad, args=(1, 24000))
nit2 = threading.Thread(target=oduzmi_kvad, args=(24000, 48000))
nit3 = threading.Thread(target=oduzmi_kvad, args=(48000, 72000))
nit4 = threading.Thread(target=oduzmi_kvad, args=(72000, 95960))


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
    #   ako je lista prazna, nastavi (kako se ne bi pristupalo indeksima kojih nema)
    if not unos_split:
        continue
    #   ako lista nije prazna, provjeri postoji li definicija i izvrsi naredbu
    else:
        izvrsi(unos_split)
