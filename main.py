import os, csv
import pandas as pd

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
    sukces = False
    nr = 1
    while sukces == False:
        nazwa_pliku = f"sala{str(nr)}.csv"
        if nazwa_pliku in aktualne_sale:
            nr = nr + 1
        else: 
            sukces = True
    
    pewne = str(input(f"Czy na pewno chcesz stworzyc nową sale (sala {nr}) (tak/nie): "))
    komunikat = ""
    if pewne == "tak":
        if nazwa_pliku in aktualne_sale:
            komunikat = "Wystąpił bład przy tworzeniu sali"
            return False, komunikat
        else:
            with open(nazwa_pliku, mode="w", newline="", encoding="utf-8") as plik:
                writer = csv.writer(plik)
                writer.writerows(nowa_sala)
            return True, komunikat
    elif pewne == "nie":
        komunikat = "Zdecydowano sie nie tworzyc sali"
        return False, komunikat
    else:
        komunikat = "Wybrano błędna wartość"
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
        print("- r (rezerwacja miejsca) ")
        print("- n (stworz nowa sale) ")
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
            case "r":
                rezerwujMiejsce()
            case "n":
                sukces, komunikat = stworzNowaSale()
                if sukces:
                    print("\n" + "-"*40)
                    print("Pomyślnie utworzono nową sale")
                else:
                    print(f"Nie utworzono sali, komunikat: {komunikat}")
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
