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

"""
while True:
    print("Opcje: [r = rezerwuj] / [w = wyjdz]")
    opcja = str(input("Wybierz opcje: "))

    if opcja == 'r':
        
        break
    elif opcja == 'w':
        print("Zakonczono program")
        break 
    else: 
        print("Wpisano nie prawidłową opcje")
"""