import os, csv
import pandas as pd
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

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


#strefa tkinter

def pokazSale(parent, title): 
    nowe = tk.Toplevel(parent)
    nowe.title(title)
    nowe.geometry("600x400")

    label = tk.Label(nowe, text=f"To jest {title}")
    label.pack(pady=20)



def przyciskiSalMain(parent):
    sale = zbierzInfoSale()
    for i in range(len(sale)):
        button_sala = ttk.Button(parent, text=f"Sala {i+1}", command=lambda i=i: wykazSali(i))
        button_sala.pack(pady=5, padx=5)

def wykazSali(i):
    nowe = tk.Toplevel(frame1)
    nowe.title(f"Sala {i+1}")
    nowe.geometry("600x400")
    nowe.resizable(False, False) 

    frame_main = tk.Frame(nowe)
    frame_main.pack(fill="x", pady=10)

    label_sala = tk.Label(frame_main, text=f"Wykaz miejsc na sali {i+1}", font=("Arial", 15))
    label_sala.pack(pady=20)


    frame_miejsca = tk.Frame(nowe)
    frame_miejsca.pack(pady=20)

    sale = zbierzInfoSale()
    sala = sale[i]
    df = pd.read_csv(sala, header=None)
    rzedy = df.shape[0]
    miejsca = df.shape[1]
    
    wolne = "seatw.png"
    zajete = "seatz.png"

    miejsca_img = []  
    for r in range(rzedy):
        for c in range(miejsca):
            status = df.iloc[r, c]
            img = wolne if status == 0 else zajete
            image = Image.open(img)
            image = image.resize((20, 20))  
            photo = ImageTk.PhotoImage(image)
            miejsca_img.append(photo) 
            
            miejsce_label = tk.Label(frame_miejsca, image=photo)
            miejsce_label.grid(row=r, column=c, padx=2, pady=2)


    frame_info = tk.Frame(nowe)
    frame_info.pack(pady=20)
    imgsw = Image.open(wolne)
    imgsz = Image.open(zajete)
    imgsw = imgsw.resize((40,40))
    imgsz = imgsz.resize((40,40))

    photo1 = ImageTk.PhotoImage(imgsw)
    photo2 = ImageTk.PhotoImage(imgsz)

    label_info1 = tk.Label(frame_info, image=photo1)
    label_info2 = tk.Label(frame_info, text="- Wolne")
    label_info3 = tk.Label(frame_info, image=photo2)
    label_info4 = tk.Label(frame_info, text="- Zajęte")

    label_info1.grid(row=0, column=0, padx=0, pady=5)
    label_info2.grid(row=0, column=1, padx=0, pady=5)
    label_info3.grid(row=0, column=2, padx=0, pady=5)
    label_info4.grid(row=0, column=3, padx=0, pady=5)


    frame_miejsca.image_references = miejsca_img
    frame_info.image_references = [photo1, photo2]

root = tk.Tk()
root.title("Sala kinowa")
root.geometry("1000x600")

tabs = ttk.Notebook(root)
tabs.pack(fill="both", expand=True)

frame1 = ttk.Frame(tabs)
tabs.add(frame1, text="Wykaz sal")

label1 = tk.Label(frame1, text="Wybierz sale by pokazać miejsca", font=("Arial", 20))
label1.pack(pady=20, padx=20)

przyciskiSalMain(frame1)

frame2 = ttk.Frame(root)
tabs.add(frame2, text="Rezerwacja miejsca")


root.mainloop()

