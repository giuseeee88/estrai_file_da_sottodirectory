# Estrazione file da sottodirectory
Questo progetto è nato con lo scopo di risolvere il problema dell'estrazione dei file dalle sottodirectory di una cartella Windows. Ad esempio, se ho una directory con centinaia di sottodirectory al suo interno e mi servono i file all'interno delle varie sottodirectory è un procedimento molto lungo quello di aprire ciascuna sottodirectory e recuperare i file all'interno per inserirli in un'unica cartella. Questo programma nasce proprio per risolvere questo problema, infatti, consente all'utente di selezionare la cartella desiderata e di inserire i file delle varie sottodirectory in un'unica cartella sul desktop. Al momento funziona solo con le directory di Windows

Librerie utilizzate:
- Tkinter (per la creazione della GUI)

La dimensione complessiva della cartella selezionata, incluse le sue sottocartelle,
non può superare 10 GiB. Il limite evita di avviare l'analisi o l'estrazione di
cartelle molto grandi, come alcune directory di sistema.