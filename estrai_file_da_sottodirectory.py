import os
import sys
import shutil
import datetime
import webbrowser
import argparse
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk

MAX_INPUT_SIZE_BYTES = 10 * 1024 ** 3

parser = argparse.ArgumentParser(
    description="Estrae i file dalle sottodirectory della cartella selezionata."
)
parser.add_argument(
    "cartella",
    nargs="?",
    help="Percorso della cartella principale contenente le sottodirectory.",
)
args = parser.parse_args()

def resource_path(relative_path):
    base_path = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

root = tk.Tk()
root.title("Estrai file da sottodirectory - Giuseppe Cautiero ")
root.minsize(500, 500)
root.geometry("500x500")
root.resizable(0, 0)
root.configure(bg="#cce6ff")
root.iconbitmap(resource_path("images/app_logo.ico"))
desktopIcon = tk.PhotoImage(file=resource_path("images/app_logo.png"))
root.iconphoto(True, desktopIcon)

## Titolo principale
mainLabel = tk.Label(root,
    text="Selezionare la cartella principale contenente le sottodirectory.",
    font=("Segoe UI", 12, "bold"),
    bg="#cce6ff",
    width=80,
    height=2)
mainLabel.pack(pady=(30, 10))

## Credits
creditsLabel = tk.Label(root,
    text="Giuseppe Cautiero - Github: giuseeee88",
    font=("Segoe UI", 10, "bold"),
    bg="#cce6ff",
    width=50,
    height=2,
    cursor="hand2")
creditsLabel.bind("<Button-1>", lambda e: apriProfilo("https://github.com/giuseeee88"))

def apriProfilo(url):
    webbrowser.open_new(url)

## Box di upload cartelle
canvas_width = 340
canvas_height = 300
mainCanvas = tk.Canvas(root,
    width=canvas_width,
    height=canvas_height,
    bg="#cce6ff",
    highlightthickness=0,
    cursor="hand2")
mainCanvas.place(relx=0.5, rely=0.52, anchor="center")
mainCanvas.bind("<Button-1>", lambda event: selezionaCartella(mainLabel, mainCanvas))
creditsLabel.place(relx=0.5, rely=0.97, anchor="s")

def poly_oval(x, y, width, height, resolution=32):
    points = [x, y,
              x+width, y,
              x+width, y+height,
              x, y+height,
              x, y]

    return mainCanvas.create_polygon(points, fill='#f00', smooth=True, splinesteps=resolution)


def poly_roundrect(x, y, width, height, radius, resolution=32):
    radius = min(radius, width / 2, height / 2)
    points = [
        x + radius, y,
        x + width - radius, y,
        x + width, y,
        x + width, y + radius,
        x + width, y + height - radius,
        x + width, y + height,
        x + width - radius, y + height,
        x + radius, y + height,
        x, y + height,
        x, y + height - radius,
        x, y + radius,
        x, y,
        x + radius, y,
    ]

    rect = mainCanvas.create_polygon(
        points,
        fill='#ffffff',
        outline='#8a8a8a',
        width=2,
        smooth=True,
        splinesteps=resolution,
    )

    return rect


poly_roundrect(10, 10, canvas_width - 20, canvas_height - 20, 20, 64)

## Immagine box di upload
image = Image.open(resource_path("images/upload.png"))
image = image.resize((canvas_width - 80, canvas_height - 90), Image.Resampling.LANCZOS)
mainImage = ImageTk.PhotoImage(image)
mainCanvas.create_image(canvas_width / 2, canvas_height / 2, image=mainImage)

## LOGICA
def validaCartella(path, listaCartelle):
    if not path:
        return False, "Percorso vuoto."

    percorso_assoluto = os.path.abspath(path)

    if len(listaCartelle) != 0:
        for cartella in listaCartelle:
            if cartella["percorso"] == percorso_assoluto:
                return False, "Cartella esistente."

    if not os.path.exists(percorso_assoluto):
        return False, f"Il percorso non esiste: {percorso_assoluto}"

    if not os.path.isdir(percorso_assoluto):
        return False, f"Il percorso non è una cartella: {percorso_assoluto}"

    return True, {
        "nome": os.path.basename(percorso_assoluto),
        "percorso": percorso_assoluto,
        "numero_file": len(os.listdir(percorso_assoluto)),
        "esiste": True,
    }

def nascondiSchermataIniziale(mainLabel, mainCanvas, creditsLabel):
    mainLabel.pack_forget()
    mainCanvas.place_forget()
    creditsLabel.place_forget()

def mostraSchermataIniziale(mainLabel, mainCanvas, creditsLabel):
    mainLabel.pack(pady=(30, 10))
    mainCanvas.place(relx=0.5, rely=0.52, anchor="center")
    creditsLabel.place(relx=0.5, rely=0.97, anchor="s")

def mostraSchermataPreUpload(cartelleValide):
    preUploadLabel = tk.Label(root,
        text="Queste sono le sottodirectory che hai selezionato.",
        font=("Segoe UI", 12, "bold"),
        bg="#cce6ff",
        width=80,
        height=2)
    preUploadLabel.pack(pady=(30, 10))

    preUploadcontainer = tk.Frame(root, bg="#cce6ff")
    preUploadcontainer.pack(pady=(10, 0), padx=20, fill="both", expand=True)

    preUploadcanvas = tk.Canvas(preUploadcontainer, height=260, bg="#cce6ff", highlightthickness=0, bd=0)
    
    preUploadscrollbar = tk.Scrollbar(preUploadcontainer, width=15, orient="vertical", command=preUploadcanvas.yview, 
        troughcolor="#dfefff", activebackground="#8bb8e8", bg="#bad8f7")
    preUploadcanvas.configure(yscrollcommand=preUploadscrollbar.set)

    preUploadscrollbar.pack(side="right", fill="y", padx=(0, 6))
    preUploadcanvas.pack(side="left", fill="both", expand=True, padx=(0, 4))

    tabella = tk.Frame(preUploadcanvas, bg="#cce6ff")
    frame_id = preUploadcanvas.create_window((0, 0), window=tabella, anchor="nw")

    intestazioni = ["Indice", "Nome", "Percorso", "Files"]
    for col, intestazione in enumerate(intestazioni):
        label = tk.Label(tabella, text=intestazione, font=("Segoe UI", 9, "bold"), 
            bg="#cce6ff", borderwidth=1, relief="solid")
        label.grid(row=0, column=col, sticky="nsew", padx=1, pady=1)

    for i, cartella in enumerate(cartelleValide, start=1):
        nomeCartella = str(cartella['nome'])
        percorsoCartella = str(cartella['percorso'])
        numeroFileCartella = str(cartella['numero_file'])

        if len(nomeCartella) > 20:
            nomeCartella = nomeCartella[:20] + "..."

        if len(percorsoCartella) > 40:
            percorsoCartella = percorsoCartella[:40] + "..."

        tk.Label(tabella, text=i, font=("Segoe UI", 8), bg="#cce6ff", borderwidth=1, relief="solid").grid(row=i, column=0, sticky="nsew", padx=1, pady=1)
        tk.Label(tabella, text=nomeCartella, font=("Segoe UI", 8), bg="#cce6ff", borderwidth=1, relief="solid").grid(row=i, column=1, sticky="nsew", padx=1, pady=1)
        tk.Label(tabella, text=percorsoCartella, font=("Segoe UI", 8), bg="#cce6ff", borderwidth=1, relief="solid", wraplength=260).grid(row=i, column=2, sticky="nsew", padx=1, pady=1)
        tk.Label(tabella, text=numeroFileCartella, font=("Segoe UI", 8), bg="#cce6ff", borderwidth=1, relief="solid").grid(row=i, column=3, sticky="nsew", padx=1, pady=1)

    tabella.update_idletasks()
    preUploadcanvas.config(scrollregion=preUploadcanvas.bbox("all"))

    tabella.grid_columnconfigure(0, weight=0, minsize=20)
    tabella.grid_columnconfigure(1, weight=2, minsize=120)
    tabella.grid_columnconfigure(2, weight=3, minsize=200)
    tabella.grid_columnconfigure(3, weight=0, minsize=35)

    def _on_frame_configure(event):
        preUploadcanvas.configure(scrollregion=preUploadcanvas.bbox("all"))

    def _on_preUploadcanvas_configure(event):
        preUploadcanvas.itemconfig(frame_id, width=event.width)

    tabella.bind("<Configure>", _on_frame_configure)
    preUploadcanvas.bind("<Configure>", _on_preUploadcanvas_configure)

    preUploadButton = tk.Button(root, width=20, height=2, text="Estrai file", command=lambda: estraiFile(cartelleValide, componentiPreUpload, mainLabel, mainCanvas), bg="#0177fe", fg="white", font=("Segoe UI", 11, "bold"), relief="flat", bd=0, highlightthickness=0)
    componentiPreUpload = [preUploadLabel, preUploadcontainer, preUploadscrollbar, preUploadcanvas, preUploadButton]
    preUploadButton.pack(pady=50)
    preUploadButton.config(borderwidth=0, highlightbackground="#0177fe", highlightcolor="#0177fe")

def calcolaDimensioneCartella(path, limite_bytes):
    dimensione = 0
    cartelle_da_visitare = [path]

    while cartelle_da_visitare:
        cartella_corrente = cartelle_da_visitare.pop()
        with os.scandir(cartella_corrente) as elementi:
            for elemento in elementi:
                if elemento.is_symlink():
                    continue
                if elemento.is_dir(follow_symlinks=False):
                    cartelle_da_visitare.append(elemento.path)
                    continue
                if elemento.is_file(follow_symlinks=False):
                    dimensione += elemento.stat(follow_symlinks=False).st_size
                    if dimensione > limite_bytes:
                        return dimensione

    return dimensione

def formattaDimensione(dimensione_bytes):
    unita = ("B", "KiB", "MiB", "GiB", "TiB")
    dimensione = float(dimensione_bytes)
    indice = 0

    while dimensione >= 1024 and indice < len(unita) - 1:
        dimensione /= 1024
        indice += 1

    return f"{dimensione:.2f} {unita[indice]}"

def nascondiSchermataPreUpload(componentiPreUpload):
    componentiPreUpload[0].pack_forget()
    componentiPreUpload[1].pack_forget()
    componentiPreUpload[2].pack_forget()
    componentiPreUpload[3].pack_forget()
    componentiPreUpload[4].pack_forget()

def selezionaCartella(mainLabel, mainCanvas, percorso_cli=None):
    parent_dir = percorso_cli or filedialog.askdirectory(
        initialdir="/",
        title="Selezionare la cartella principale che contiene le varie sottodirectory"
    )

    if not parent_dir:
        return

    parent_dir = os.path.abspath(parent_dir)
    if not os.path.isdir(parent_dir):
        print(f"Il percorso della cartella selezionata non è valido: {parent_dir}")
        return

    try:
        dimensione_cartella = calcolaDimensioneCartella(parent_dir, MAX_INPUT_SIZE_BYTES)
    except PermissionError:
        mostraPopupEstrazione(
            False,
            "Impossibile verificare la dimensione: una o più sottocartelle "
            "non sono accessibili. Seleziona una cartella per cui hai "
            "permessi di lettura.",
        )
        return
    except OSError as errore:
        mostraPopupEstrazione(False, f"Impossibile verificare la dimensione della cartella: {errore}")
        return

    if dimensione_cartella > MAX_INPUT_SIZE_BYTES:
        mostraPopupEstrazione(
            False,
            "La cartella è troppo grande: "
            f"{formattaDimensione(dimensione_cartella)} rilevati, "
            f"limite {formattaDimensione(MAX_INPUT_SIZE_BYTES)}.",
        )
        return

    sottocartelle_paths = [
        os.path.join(parent_dir, nome) 
        for nome in os.listdir(parent_dir) 
        if os.path.isdir(os.path.join(parent_dir, nome))
    ]

    if not sottocartelle_paths:
        mostraPopupEstrazione(False, "Nessuna sottodirectory trovata nella cartella selezionata.")
        return

    win_selezione = tk.Toplevel(root)
    win_selezione.title("Seleziona Cartelle Multiple")
    win_selezione.geometry("400x450")
    win_selezione.resizable(0, 0)
    win_selezione.configure(bg="#cce6ff")
    win_selezione.transient(root)
    win_selezione.grab_set()

    lbl_istruzioni = tk.Label(win_selezione, text="Seleziona le sottodirectory (Ctrl/Shift per scelte multiple):", 
                              font=("Segoe UI", 10, "bold"), bg="#cce6ff")
    lbl_istruzioni.pack(pady=15, padx=10)

    frame_listbox = tk.Frame(win_selezione, bg="#cce6ff")
    frame_listbox.pack(padx=20, pady=5, fill="both", expand=True)

    scrollbar = tk.Scrollbar(frame_listbox)
    scrollbar.pack(side="right", fill="y")

    listbox = tk.Listbox(frame_listbox, selectmode=tk.EXTENDED, yscrollcommand=scrollbar.set, 
                         font=("Segoe UI", 10), selectbackground="#0177fe", activestyle="none")
    listbox.pack(side="left", fill="both", expand=True)
    scrollbar.config(command=listbox.yview)

    for path in sottocartelle_paths:
        listbox.insert(tk.END, os.path.basename(path))

    def conferma_selezione():
        indici_selezionati = listbox.curselection()
        cartelle_valide = []

        for i in indici_selezionati:
            percorso_scelto = sottocartelle_paths[i]
            valido, risultato = validaCartella(percorso_scelto, cartelle_valide)
            if valido:
                cartelle_valide.append(risultato)
                print(f"Cartella valida aggiunta: {risultato['percorso']}")
            else:
                print(f"Cartella non valida: {risultato}")

        win_selezione.destroy()

        if cartelle_valide:
            nascondiSchermataIniziale(mainLabel, mainCanvas, creditsLabel)
            mostraSchermataPreUpload(cartelle_valide)
        else:
            print("Nessuna cartella valida selezionata.")

    btn_conferma = tk.Button(win_selezione, text="Conferma Selezione", command=conferma_selezione,
                             bg="#0177fe", fg="white", font=("Segoe UI", 11, "bold"), relief="flat")
    btn_conferma.pack(pady=20, ipadx=10, ipady=5)

def mostraPopupEstrazione(isEstratto, msgEstrazione):
    popupStatoEstrazione = tk.Toplevel(root)
    popupStatoEstrazione.title("Stato estrazione")
    popupStatoEstrazione.geometry("320x220")
    popupStatoEstrazione.resizable(0, 0)
    popupStatoEstrazione.configure(bg="#cce6ff")
    popupStatoEstrazione.transient(root)
    popupStatoEstrazione.grab_set()

    if isEstratto:
        msg = "L'estrazione è avvenuta con successo."
        color = "#32d548"
        icona = "✓"
    else:
        msg = msgEstrazione
        color = "#d53232"
        icona = "!"

    frame_popup = tk.Frame(popupStatoEstrazione, bg="#cce6ff", padx=20, pady=20)
    frame_popup.pack(fill="both", expand=True)

    label_icona = tk.Label(frame_popup, text=icona, font=("Segoe UI", 30, "bold"), fg=color, bg="#cce6ff")
    label_icona.pack(pady=(0, 10))

    labelStato = tk.Label(frame_popup, text=msg, font=("Segoe UI", 10, "bold"), bg="#cce6ff", fg="#1f1f1f", justify="center", wraplength=260)
    labelStato.pack(pady=(0, 15))

def estraiFile(cartelleValide, componentiPreUpload, mainLabel, mainCanvas):
    isEstratto = False
    msgEstrazione = ""
    
    nascondiSchermataPreUpload(componentiPreUpload)

    dataEstrazioneFiles = str(datetime.datetime.now()).replace(":", "").replace(" ", "")
    nomeDirectoryOutput = "output-" + dataEstrazioneFiles
    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
    path_output = os.path.join(desktop_path, nomeDirectoryOutput)

    if len(cartelleValide) > 0 and len(cartelleValide) < 1000:
        try:
            os.mkdir(path_output)
            print(f"La directory '{path_output}' è stata creata correttamente.")
            count = 0

            def estrai_elementi(percorso_cartella):
                nonlocal count

                for elemento in os.listdir(percorso_cartella):
                    sorgente = os.path.join(percorso_cartella, elemento)

                    if os.path.isdir(sorgente):
                        estrai_elementi(sorgente)
                        continue

                    nome_base, estensione = os.path.splitext(elemento)
                    nuovo_nome = f"{nome_base}_{count + 1}{estensione}"
                    destinazione = os.path.join(path_output, nuovo_nome)
                    shutil.copy2(sorgente, destinazione)
                    count += 1

            for cartella in cartelleValide:
                estrai_elementi(cartella['percorso'])

            isEstratto = True
        
        except FileExistsError:
            msgEstrazione = f"La directory '{path_output}' già esiste."
        except PermissionError:
            msgEstrazione = f"Permesso negato: non è stato possibile creare '{path_output}'."
        except Exception as e:
            msgEstrazione = f"Errore nella creazione della cartella di output: {e}"
    elif len(cartelleValide) > 1000:
        msgEstrazione = "La cartella selezionata ha troppe sottodirectory (più di 1000)."
    else:
        msgEstrazione = "La cartella selezionata non ha sottodirectory"

    mostraSchermataIniziale(mainLabel, mainCanvas, creditsLabel)
    mostraPopupEstrazione(isEstratto, msgEstrazione)
    
if args.cartella:
    percorso_input = args.cartella.strip('"')
    root.after(100, lambda: selezionaCartella(mainLabel, mainCanvas, percorso_input))

root.mainloop()