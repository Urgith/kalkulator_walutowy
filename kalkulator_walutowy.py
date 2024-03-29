from bs4 import BeautifulSoup
import urllib.request as url
# rozwiązanie problemu z BUTTON(...command)
from functools import partial

from tkinter import *
from tkinter.ttk import *

import sys


class Interfejs:

    def __init__(self):
        self.link = 'https://www.nbp.pl/Kursy/KursyA.html'
        self.nazwa = 'nowy.txt'
        self.root = Tk()

        self.zapis()
        self.odczyt()
        self.polozenie()
        self.name()
        self.zakoncz()
        self.napis_poczatek()
        self.napis_waluta_startowa()
        self.napis_waluta_koncowa()
        self.napis_koniec()
        self.oblicz()

        self.root.entry = Entry(self.root, width=15)
        self.root.entry.place(x=20, y=60, width=150, height=25)

        self.root.listbox = Combobox(
            self.root,
            values=self.odczyt()[1],
            width=10
        )
        self.root.listbox.place(x=200, y=60, width=100, height=25)
        self.root.listbox.current(0)

        self.root.listbox1 = Combobox(
            self.root,
            values=self.odczyt()[1], 
            width=10
        )
        self.root.listbox1.place(x=340, y=60, width=100, height=25)
        self.root.listbox1.current(0)

        self.root.entry1 = Entry(self.root, width=35)
        self.root.entry1.place(x=150, y=200, width=200, height=25)

        self.root.mainloop()

    def polozenie(self):
        ''' napis jako nazwa interfejsu, jego rozmiar, kolor '''
        self.root.title('Kalkulator walutowy')
        self.root.geometry('500x300+150+150')
        self.root.configure(background='blue')

    def name(self):
        ''' napis na agórze ekranu 'Kalkulator walutowy' '''
        self.root.label = Label(self.root, text='Kalkulator walutowy')\
                                                            .pack(side=TOP)

    def zakoncz(self):
        ''' przecisk wyłączający interfejs '''
        self.root.button = Button(self.root, text='Zakończ program',
                                    command=quit).pack(side=BOTTOM)

    def napis_poczatek(self):
        ''' napis nad polem do wpisywania kwoty początkowej '''
        self.root.label2 = Label(self.root, text='Kwota początkowa:')\
                                    .place(x=30, y=30, width=130, height=20)

    def kwota_poczatkowa(self):
        return self.root.entry.get()

    def napis_waluta_startowa(self):
        ''' napis nad polem wyboru waluty startowej '''
        self.root.label3 = Label(self.root, text='Waluta startowa:')\
                                    .place(x=190, y=30, width=115, height=20)

    def waluta_startowa(self):
        return self.root.listbox

    def napis_waluta_koncowa(self):
        ''' napis nad polem wyboru waluty końcowej '''
        self.label4 = Label(self.root, text='Waluta końcowa:')\
                                    .place(x=330, y=30, width=120, height=20)

    def waluta_koncowa(self):
        return self.root.listbox1

    def napis_koniec(self):
        ''' napis nad polem wyniku konwersji waluty '''
        self.label5 = Label(self.root, text='Tyle otrzymasz:')\
                                    .place(x=190, y=170, width=120, height=20)

    def kwota_koncowa(self):
        return self.root.entry1

    def oblicz(self):
        ''' przycisk włączający konwersję waluty '''
        self.root.button1 = Button(self.root, text='Oblicz', command=partial(
            self.ilosc_pieniedzy)).place(x=360, y=200, width=70, height=25)

    def zapis(self):
        ''' zapisujemy tabelę do pliku '''
        try:
            otwarta_strona = url.urlopen(self.link)
            html = otwarta_strona.read()
            soup = BeautifulSoup(html, 'html.parser')
            cala_strona = soup.get_text()
            start = cala_strona.index('Kurs średni')
            koniec = cala_strona.index('Powyższa')
            tabela = cala_strona[start + len('Kurs średni') + 3:(koniec - 6)]

            with open(self.nazwa, 'w') as file:
                file.write(tabela)

        except:
            print('Nie ma dostępu do internetu albo brak dostępu do strony')

    def odczyt(self):
        ''' odczytujemy tabelę z pliku do zmiennych '''
        try:
            sczytywanie = open(self.nazwa, 'r')
        except:
            print('Nie znaleziono odpowiedniego pliku')
            sys.exit(0)

        nazwa2, ilosc, symbol, cena, kurs = [], [], [], [], []
        for linijka in sczytywanie:
            if len(linijka) >= 2:
                if ',' in linijka:
                    cena.append(eval(linijka[0] + '.' + linijka[2:-1]))

                elif '10000' in linijka:
                    ilosc.append(10000)
                    symbol.append(linijka[-4:-1])

                elif '100' in linijka:
                    ilosc.append(100)
                    symbol.append(linijka[-4:-1])

                elif '1' in linijka:
                    ilosc.append(1)
                    symbol.append(linijka[-4:-1])

                else:
                    nazwa2.append(linijka[0:-1])

        sczytywanie.close()
        for i in range(len(cena)):
            kurs.append(cena[i] / ilosc[i])

        nazwa2.append('złotówka(Polska)')
        symbol.append('PLN')
        kurs.append(1)

        Dict = {}
        for i in range(len(symbol)):
            Dict[symbol[i]] = kurs[i]

        return Dict, symbol

    def ilosc_pieniedzy(self):
        ''' wyświetla wynik konwersji walut w odpowiednim okienku'''
        try:
            # CZARY MARY HOKUS POKUS
            self.kwota_koncowa().delete(0, END)
            a = self.odczyt()[0]
            b = self.waluta_startowa().get()
            c = self.waluta_koncowa().get()
            d = eval(self.kwota_poczatkowa())
            e = self.kwota_koncowa()

            f = a[b]
            g = a[c]
            calosc = str((d*f) / g) + ' ' + c
            e.insert(0, str(calosc))

        except:
            self.kwota_koncowa().delete(0, END)
            self.kwota_koncowa().insert(0, 'Błędne dane')


Interfejs()
