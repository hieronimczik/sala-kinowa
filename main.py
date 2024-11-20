import os, csv
import pandas as pd

def zbierzInfoSale():
    sale_info = []

    for dirpath, _, filenames in os.walk('.'):
        for file in filenames:
            if file.endswith('.csv'):
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
        except ValueError:
            print("Błędna wartość")
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
    
    rzad = int(input("Podaj rzad miejsca ktorego chcesz zarezerwowac: "))-1
    nr_miejsca = int(input("Podaj numer miejsca ktore chcesz zarezerwowac: "))-1

    if miejsca[rzad][nr_miejsca] == 0:
        miejsca[rzad][nr_miejsca] = 1
        print(f"Zarezerwowano miejsce {nr_miejsca+1} w rzedzie {rzad+1}")
        
        with open(sala, mode='w', newline="", encoding="utf-8") as plik:
            writer = csv.writer(plik)
            writer.writerows(miejsca)
    else:
        print(f"Miejsce {nr_miejsca+1} w rzedzie {rzad+1} jest zajete")

while True:
    print("Opcje: [w = więcej opcji] / [z = zakończ]")
    opcja = str(input("Wybierz opcje: "))

    if opcja == 'w':
        print("Opcje do wybrania:")
        print("- s (wyswietla sale do wybrania) ")
        print("- m (wyswietla miejsca na sali) ")
        print("- r (rezerwacja miejsca) ")
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
                miejsca = odczytPliku(sala)
                wyswietlMiejsca(miejsca, plik=sala)
            case "r":
                rezerwujMiejsce()
            case _:
                print("Błędna opcja")

    elif opcja == 'z':
        print("Zakonczono program")
        break 
    else: 
        print("Wpisano nie prawidłową opcje")
