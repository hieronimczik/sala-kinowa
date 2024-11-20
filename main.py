import os, csv

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
        miejsca = list(reader)
    return miejsca

def wyswietlMiejsca(sala):
    print("Miejsca w sali (0-wolne, 1-zajete)")
    for row in sala:
        print(row)

def rezerwujMiejsce():
    sala = wybierzSale()
    miejsca = odczytPliku(sala)
    print(miejsca[0][0])
    wyswietlMiejsca(miejsca)
    
    rzad = int(input("Podaj rzad miejsca ktorego chcesz zarezerwowac: "))
    nr_miejsca = int(input("Podaj numer miejsca ktore chcesz zarezerwowac: "))
    for _ in range(len(miejsca)):
        for _ in range(len(miejsca)):
            if miejsca[rzad-1][nr_miejsca-1] == 0:
                miejsca[rzad-1][nr_miejsca-1] = 1
                print(f"Zarezerwowales {nr_miejsca} miejsce w rzedzie {rzad}")
                break
            else: 
                print(f"Miejsce {nr_miejsca} w rzedzie {rzad} jest juz zajete!")
                break


    with open(sala, mode='w', newline="", encoding="utf-8") as plik:
        writer = csv.writer(plik)
        writer.writerows(miejsca)
    

    




















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
                print("sdas")
            case "r":
                rezerwujMiejsce()
            case _:
                print("Błędna opcja")

    elif opcja == 'z':
        print("Zakonczono program")
        break 
    else: 
        print("Wpisano nie prawidłową opcje")
