import os, csv
import pandas as pd

def aktualizujPlik(plik, zawartosc):
    with open(plik, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerows(zawartosc)

def stworzNowaSale():
    nowa_sala = []
    print("\n" + "-"*40)
    rzedy = int(input("Podaj ile rzędów ma miec sala: "))
    miejsca = int(input("Podaj ile miejsc ma byc w rzędzie: "))

    opcja = str(input("Czy sala ma być pusta? (tak/nie) - w przeciwnym wypadku miejsca bedzie trzeba samemu wypelnic: "))
    if opcja == "tak" or opcja == "nie":
        if opcja == "tak":
            nowa_sala = [[0 for _ in range(miejsca)] for _ in range(rzedy)]
        elif opcja == "nie":
            nowa_sala = [[0 for _ in range(miejsca)] for _ in range(rzedy)]
            print("Wolne - 0 | Zajete - 1")
            for i in range(rzedy):
                for j in range(miejsca):
                    wybor = int(input(f'Podaj wartosc {j+1} miejsca z rzedu {i+1}: '))
                    nowa_sala[i][j] = wybor
        print("\n" + "-"*40)
        print("Rozkład miejsc w twojej sali: ")
        for row in nowa_sala:
            print(row)
    else:
        print("Błędna opcja")

    aktualne_sale = zbierzInfoSale()
    nazwa_pliku = "sala.csv"
    nr = 1
    pewne = str(input(f"Czy na pewno chcesz stworzyc nową sale (tak/nie): "))
    komunikat = ""
    if pewne == "tak":
        if aktualne_sale == None:
            with open(nazwa_pliku, mode="w", newline="", encoding="utf-8") as plik:
                writer = csv.writer(plik)
                writer.writerows(nowa_sala)
            return True, komunikat
        else:
            sukces = False
            while sukces == False:
                nazwa_pliku = f"sala{str(nr)}.csv"
                if nazwa_pliku in aktualne_sale:
                    nr = nr + 1
                else: 
                    sukces = True
            
            if nazwa_pliku in aktualne_sale:
                komunikat = "Wystąpił bład przy tworzeniu sali"
                return False, komunikat
            else:
                with open(nazwa_pliku, mode="w", newline="", encoding="utf-8") as plik:
                    writer = csv.writer(plik)
                    writer.writerows(nowa_sala)
                return True, komunikat
    elif pewne == "nie":
        komunikat = "Zdecydowano sie nie tworzyc nowej sali"
        return False, komunikat
    else:
        komunikat = "Wpisano błędną opcje"
        return False, komunikat

def usunSale():
    sale = zbierzInfoSale()
    komunikat = ""
    if sale != None:
        sala = wybierzSale()
        if sala != None:
            if sala in sale:
                try:
                    os.remove(sala)
                    return True, komunikat
                except FileNotFoundError:
                    komunikat = "Nie znaleziono takiej sali!"
                    return False, komunikat
            else:
                komunikat = "Nie znaleziono takiej sali!"
                return False, komunikat
        else:
            komunikat = "Wybrano sale której nie ma"
            return False, komunikat
    else:
        komunikat = "Brak sali do wybrania"
        return False, komunikat
    
def zmianaMiejscSali():
    komunikat = ""
    sala_plik = wybierzSale()
    if sala_plik != None:
        sala = odczytPliku(sala_plik)
        wyswietlMiejsca(sala, plik=sala_plik)

        df = pd.read_csv(sala_plik, header=None)
        rzedy = df.shape[0]
        miejsca = df.shape[1]
        rzad = int(input(f"Podaj rzad z ktorego chcesz cos zmienic  (1-{rzedy}): "))-1
        miejsce = int(input(f"Podaj miejsce ktore chcesz zmienić (1-{miejsca}): "))-1
        try: 
            opcja = input("Podaj opcje (zwolnij/zajmij)")
            if opcja.lower() == "zwolnij":
                if sala[rzad][miejsce] == 0:
                    komunikat = "Miejsce ktore chcesz zmienic ma juz taka wartosc"
                    return False, komunikat
                else:
                    sala[rzad][miejsce] = 0
                    aktualizujPlik(sala_plik, sala)
                    return True, komunikat
            elif opcja.lower() == "zajmij":
                if sala[rzad][miejsce] == 1:
                    komunikat = "Miejsce ktore chcesz zwolnic ma juz taka wartosc"
                    return False, komunikat
                else:
                    sala[rzad][miejsce] = 1
                    aktualizujPlik(sala_plik, sala)
                    return True, komunikat
            else:
                komunikat = "Wybrano bledna opcje"
                return False, komunikat
        except IndexError:
            komunikat = "Wystąpił błąd"
            return False, komunikat
    else:
        komunikat = "Brak sal do wybrania"
        return False, komunikat

def zbierzInfoSale():
    sale_info = []

    for dirpath, _, filenames in os.walk("."):
        for file in filenames:
            if file.endswith(".csv"):
                sale_info.append(file)
    
    if len(sale_info) != 0:
        return sale_info
    else: 
        return None

def wybierzSale():
    sale = zbierzInfoSale()
    if sale != None:
        print("Sale do wybrania: ")
        for i in range(len(sale)):
            print(f"- sala {i+1}")

        try:
            wybrana = int(input(f"Wybierz sale (1-{len(sale)}): "))
            wybrana_wartosc = sale[wybrana-1]
            if wybrana_wartosc in sale:
                print(f"Wybrano sale {wybrana}")
                return wybrana_wartosc
            else:
                print("Nie ma takiej sali")
                return None
        except (ValueError, IndexError):
            print("Błędna wartość")
            return None
    else: 
        print("Brak sal do wybrania, sprawdź czy plik z roszerzeniem '.csv' jest utworzony!")

def odczytPliku(file):
    with open(file, mode='r', encoding='utf-8') as plik:
        reader = csv.reader(plik)
        miejsca = [list(map(int, row)) for row in reader]
    return miejsca

def wyswietlMiejsca(sala, plik=None):
    if plik is not None:
        wolne_miejsca = 0
        zajete_miejsca = 0
        df = pd.read_csv(plik, header=None)
        
        for i in range(df.shape[0]):
            for j in range(df.shape[1]):
                if sala[i][j] == 1:
                    zajete_miejsca = zajete_miejsca + 1
                elif sala[i][j] == 0:
                    wolne_miejsca = wolne_miejsca + 1
        print(f"Miejsca w sali (0-wolne/1-zajete) ({wolne_miejsca} wolnych, {zajete_miejsca} zajetych)")
    else:
        print("Miejsca w sali (0-wolne/1-zajete)")
    for row in sala:
        print(row)

def rezerwujMiejsce():
    sala = wybierzSale()
    miejsca = odczytPliku(sala)
    wyswietlMiejsca(miejsca, plik=sala)
    
    df = pd.read_csv(sala, header=None)
    rzad = int(input("Podaj rzad miejsca ktorego chcesz zarezerwowac: "))-1
    nr_miejsca = int(input("Podaj numer miejsca ktore chcesz zarezerwowac: "))-1

    if 0 <= rzad < df.shape[0] and 0 <= nr_miejsca < df.shape[1]:
        if miejsca[rzad][nr_miejsca] == 0:
            miejsca[rzad][nr_miejsca] = 1
            print(f"Zarezerwowano miejsce {nr_miejsca+1} w rzedzie {rzad+1}")
            
            with open(sala, mode='w', newline="", encoding="utf-8") as plik:
                writer = csv.writer(plik)
                writer.writerows(miejsca)
        else:
            print(f"Miejsce {nr_miejsca+1} w rzedzie {rzad+1} jest zajete")
    else:
        print("Podałeś błędne miejsca")

while True:
    print("Opcje: [w = więcej opcji] / [z = zakończ]")
    opcja = str(input("Wybierz opcje: "))

    if opcja == 'w':
        print("\n" + "-"*40)
        print("Opcje do wybrania:")
        print("- s (wyswietla sale do wybrania) ")
        print("- m (wyswietla miejsca na sali) ")
        print("- zm (zmien miejsce na sali) ")
        print("- r (rezerwacja miejsca) ")
        print("- n (stworz nowa sale) ")
        print("- u (usun sale) ")
        print("- z (zakoncz program) ")
        print("-"*40 + "\n")
        opcja2 = str(input("Wybierz opcje: "))
        match opcja2:
            case "s":
                sale = zbierzInfoSale()
                if sale != None:
                    print("")
                    print("------")
                    print("Sale do wybrania:")
                    for i in range(len(sale)):
                        print(f"- sala {i+1}")
                    print()
                else:
                    print("Brak sal do wybrania ;(")
            case "m": 
                sala = wybierzSale()
                if sala != None:
                    miejsca = odczytPliku(sala)
                    wyswietlMiejsca(miejsca, plik=sala)
            case "zm":
                sukces, komunikat = zmianaMiejscSali()
                if sukces: 
                    print("\n" + "-"*40)
                    print("Pomyślnie zmieniono wartosci")
                else:
                    print(f"Operacja nie powiodła sie, komunikat: {komunikat}")
            case "r":
                rezerwujMiejsce()
            case "n":
                sukces, komunikat = stworzNowaSale()
                if sukces:
                    print("\n" + "-"*40)
                    print("Pomyślnie utworzono nową sale")
                else:
                    print(f"Nie utworzono sali, komunikat: {komunikat}")
            case "u":
                sukces, komunikat = usunSale()
                if sukces:
                    print("\n" + "-"*40)
                    print("Pomyślnie usunięto sale")
                else:
                    print(f"Nie usunięto sali, komunikat: {komunikat}")
            case "z":
                print("Zakonczono program")
                break
            case _:
                print("Błędna opcja")

    elif opcja == 'z':
        print("Zakonczono program")
        break 
    else: 
        print("Wpisano nie prawidłową opcje")
