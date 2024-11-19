def wybierzSale():
    

while True:
    print("Opcje: [r = rezerwuj] / [w = wyjdz]")
    opcja = str(input("Wybierz opcje: "))

    if opcja == 'r':
        print("pzdr")
        break
    elif opcja == 'w':
        print("Zakonczono program")
        break 
    else: 
        print("Wpisano nie prawidłową opcje")