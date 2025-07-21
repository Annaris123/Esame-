import time

start_tot = time.time()
start = time.time()

print("Quesito A:")  # I 10 luoghi attraversati da più servizi diversi
print("")


def collegamenti(temporal_day):
    file = open(temporal_day, "r")  # Apre un file CSV in modalità lettura
    fermate_servizi = {}  # Chiave = ID della fermata
    # Valore = lista dei servizi che passano per quella fermata

    file.readline()  # Salta intestazione
    for riga in file:
        campi = riga.strip().split(",")  # Pulisce e divide la riga in una lista usando la virgola
        id_partenza = campi[0]  # ID fermata di partenza
        id_arrivo = campi[1]  # ID fermata di arrivo
        servizio = campi[4]  # tipo o nome del servizio

        # Aggiungi servizio alla fermata di partenza
        if id_partenza not in fermate_servizi:
            fermate_servizi[id_partenza] = [servizio]
        elif servizio not in fermate_servizi[id_partenza]:
            fermate_servizi[id_partenza].append(servizio)

        # Aggiungi servizio alla fermata di arrivo
        if id_arrivo not in fermate_servizi:
            fermate_servizi[id_arrivo] = [servizio]
        elif servizio not in fermate_servizi[id_arrivo]:
            fermate_servizi[id_arrivo].append(servizio)

    file.close()
    return fermate_servizi


def top_fermate(fermate_servizi, top_n=10):
    id_fermate = list(fermate_servizi.keys())
    numero_servizi = [len(fermate_servizi[id]) for id in id_fermate]

    top_fermate = []  # Lista vuota per salvare le top fermate
    top_servizi = []  # Lista vuota per salvare il numero di servizi

    while len(top_fermate) < top_n:
        massimo = max(numero_servizi)  # Trova il massimo numero di servizi nella lista
        indice_massimo = numero_servizi.index(massimo)
        id_top = id_fermate[indice_massimo]  # Ottiene l'indice relativo per trovare l'ID della fermata corrispondente

        # Aggiunge l'ID e il numero di servizi alle liste top_id e top_valori
        top_fermate.append(id_top)
        top_servizi.append(massimo)

        numero_servizi[indice_massimo] = 0  # Imposta quel valore a 0 per non riutilizzarlo nel prossimo ciclo

    return top_fermate, top_servizi  # Restituisce le due liste: ID delle fermate top e numero di servizi corrispondenti


def id_nome(nodes):
    file = open(nodes, "r")
    nome = {}

    file.readline()  # Salta intestazione
    for riga in file:
        campi = riga.strip().split(",")
        nome[campi[0]] = campi[3]

    file.close()
    return nome


def stampa_top_fermate(fermate_top, n_servizi_fermata, id_nome_fermata):
    print("Le 10 fermate attraversate da più servizi diversi sono:\n")
    for i in range(10):
        fid = fermate_top[i]
        servizi = n_servizi_fermata[i]
        nome = id_nome_fermata.get(fid, "Errore")
        print(str(i + 1) + ". " + nome + " con " + str(servizi) + " servizi diversi")


# Percorsi dei file
percorso_collegamenti = "/Users/martaristori/Desktop/Anna/network_temporal_day.csv"
percorso_nodi = "/Users/martaristori/Desktop/Anna/network_nodes.csv"

# Elaborazione
fermate_servizi = collegamenti(percorso_collegamenti)
fermate_top, n_servizi_fermata = top_fermate(fermate_servizi)
id_nome_fermata = id_nome(percorso_nodi)

# Output
stampa_top_fermate(fermate_top, n_servizi_fermata, id_nome_fermata)

print("")
print("Quesito B:")
print("")


def numero_float(s):
    cifre = {str(i): i for i in range(10)}
    intera, _, decimale = s.partition('.')

    intero = 0
    for c in intera:
        if c in cifre:
            intero = intero * 10 + cifre[c]

    dec = 0
    base = 1
    for c in decimale:
        if c in cifre:
            base *= 10
            dec += cifre[c] / base

    return intero + dec


def leggi_fermate(nodes):
    fermate = {}  # ID -> (x, y)
    nomi = {}  # ID -> nome

    file = open(nodes, "r")
    riga = file.readline()

    while riga != "":
        estrai = riga.strip().split(",")
        if len(estrai) >= 4:
            id = estrai[0]
            nome = estrai[3]
            latitudine = estrai[1]
            longitudine = estrai[2]

            lat = numero_float(latitudine)
            lon = numero_float(longitudine)

            fermate[id] = (lat, lon)
            nomi[id] = nome

        riga = file.readline()

    file.close()
    return fermate, nomi


def leggi_tempi(temporal_day, fermate):
    massimo = -1
    id_partenza = ""
    id_arrivo = ""
    tempo_massimo = 0
    distanza_massima = 0

    file = open(temporal_day, "r")
    riga = (file.readline())

    while riga != "":
        estrai = riga.strip().split(",")
        if len(estrai) >= 4:
            from_stop = estrai[0]
            to_stop = estrai[1]
            dep_time = estrai[2]
            arr_time = estrai[3]

            dep = numero_float(dep_time)
            arr = numero_float(arr_time)
            tempo = arr - dep

            if from_stop in fermate and to_stop in fermate and tempo > 0:
                x1, y1 = fermate[from_stop]
                x2, y2 = fermate[to_stop]

                dx = x2 - x1
                dy = y2 - y1

                distanza = (dx * dx + dy * dy) ** 0.5
                rapporto = distanza / tempo

                if rapporto > massimo:
                    massimo = rapporto
                    id_partenza = from_stop
                    id_arrivo = to_stop
                    tempo_massimo = tempo
                    distanza_massima = distanza

        riga = file.readline()

    file.close()
    return id_partenza, id_arrivo, tempo_massimo, distanza_massima, massimo


def main():
    percorso_fermate = "/Users/martaristori/Desktop/Anna/network_nodes.csv"
    percorso_tempi = "/Users/martaristori/Desktop/Anna/network_temporal_day.csv"

    fermate, nomi = leggi_fermate(percorso_fermate)
    id_partenza, id_arrivo, tempo, distanza, rapporto = leggi_tempi(percorso_tempi, fermate)

    print("Coppia di fermate consecutive con il rapporto distanza/tempo più alto:")
    print("Da", id_partenza, "a", id_arrivo)


# Esegui
main()

print("")
print("Quesito C:")
print("")


# Riutilizzo la funzione numero_float creata nell'esercizio precedente
def leggi_fermate(percorso_file):
    fermate = {}
    file = open(percorso_file, 'r')
    righe = file.readlines()
    file.close()

    if len(righe) == 0:
        print("Errore")
        return fermate

    intestazione = righe[0].strip()
    separatore = ';'
    conta_virgole = 0
    conta_punto_e_virgola = 0

    indice = 0
    while indice < len(intestazione):
        carattere = intestazione[indice]
        if carattere == ',':
            conta_virgole = conta_virgole + 1
        if carattere == ';':
            conta_punto_e_virgola = conta_punto_e_virgola + 1
        indice = indice + 1

    if conta_virgole > conta_punto_e_virgola:
        separatore = ','

    riga_corrente = 1
    while riga_corrente < len(righe):
        riga = righe[riga_corrente].strip()
        colonne = riga.split(separatore)

        if len(colonne) >= 4:
            id_fermata = colonne[0].strip()
            lat = colonne[1].strip()
            lon = colonne[2].strip()
            nome = colonne[3].strip()

            # Controlla validità latitudine
            indice_carattere = 0
            lat_valida = 1
            while indice_carattere < len(lat):
                c = lat[indice_carattere]
                if c != '.' and c != '-' and (c < '0' or c > '9'):
                    lat_valida = 0
                indice_carattere = indice_carattere + 1

            # Controlla validità longitudine
            indice_carattere = 0
            lon_valida = 1
            while indice_carattere < len(lon):
                c = lon[indice_carattere]
                if c != '.' and c != '-' and (c < '0' or c > '9'):
                    lon_valida = 0
                indice_carattere = indice_carattere + 1

            if lat_valida == 1 and lon_valida == 1:
                latitudine = numero_float(lat)
                longitudine = numero_float(lon)
                fermate[id_fermata] = (latitudine, longitudine, nome)

        riga_corrente = riga_corrente + 1

    return fermate


def leggi_viaggi_bus(percorso_file):
    viaggi = {}

    file = open(percorso_file, 'r')
    righe = file.readlines()
    file.close()

    if len(righe) == 0:
        print("Errore")
        return viaggi

    intestazione = righe[0].strip()
    separatore = ';'
    conta_virgole = 0
    conta_punto_e_virgola = 0

    i = 0
    while i < len(intestazione):
        carattere = intestazione[i]
        if carattere == ',':
            conta_virgole = conta_virgole + 1
        elif carattere == ';':
            conta_punto_e_virgola = conta_punto_e_virgola + 1
        i = i + 1

    if conta_virgole > conta_punto_e_virgola:
        separatore = ','

    # Mappa colonne
    colonne = {}
    nomi_colonne = intestazione.split(separatore)
    posizione = 0
    while posizione < len(nomi_colonne):
        nome = nomi_colonne[posizione].strip()
        colonne[nome] = posizione
        posizione = posizione + 1

    indice_riga = 1
    while indice_riga < len(righe):
        riga = righe[indice_riga].strip()
        parti = riga.split(separatore)

        if len(parti) >= len(colonne):
            tipo_mezzo = parti[colonne['route_type']].strip()
            if tipo_mezzo == '3':
                id_viaggio = parti[colonne['trip_I']]
                da_fermata = parti[colonne['from_stop_I']]
                a_fermata = parti[colonne['to_stop_I']]
                numero_seq = parti[colonne['seq']].strip()

                numero = True
                j = 0
                while j < len(numero_seq):
                    c = numero_seq[j]
                    if c < '0' or c > '9':
                        numero = False
                    j = j + 1

                if numero == True:
                    numero_seq_intero = int(numero_seq)

                    # se non esiste ancora la lista, la crea
                    if id_viaggio in viaggi:
                        viaggi[id_viaggio].append((numero_seq_intero, da_fermata, a_fermata))
                    else:
                        viaggi[id_viaggio] = [(numero_seq_intero, da_fermata, a_fermata)]

        indice_riga = indice_riga + 1

    return viaggi


def calcola_distanze(viaggi, fermate):
    distanze_per_viaggio = {}

    for id_viaggio in viaggi:
        connessioni = viaggi[id_viaggio]

        # Ordina le connessioni in base al numero sequenziale
        indice_conn = 0
        while indice_conn < len(connessioni) - 1:
            indice_prossimo = indice_conn + 1
            while indice_prossimo < len(connessioni):
                if connessioni[indice_conn][0] > connessioni[indice_prossimo][0]:
                    temp = connessioni[indice_conn]
                    connessioni[indice_conn] = connessioni[indice_prossimo]
                    connessioni[indice_prossimo] = temp
                indice_prossimo = indice_prossimo + 1
            indice_conn = indice_conn + 1

        distanza_totale = 0.0

        indice = 0
        while indice < len(connessioni):
            da_fermata = connessioni[indice][1]
            a_fermata = connessioni[indice][2]

            if da_fermata in fermate and a_fermata in fermate:
                lat1 = fermate[da_fermata][0]
                lon1 = fermate[da_fermata][1]
                lat2 = fermate[a_fermata][0]
                lon2 = fermate[a_fermata][1]

                delta_lat = lat2 - lat1
                delta_lon = lon2 - lon1
                distanza = ((delta_lat * delta_lat) + (delta_lon * delta_lon)) ** 0.5
                distanza_totale = distanza_totale + distanza

            indice = indice + 1

        distanze_per_viaggio[id_viaggio] = distanza_totale

    return distanze_per_viaggio


def trova_massimo(distanze):
    massimo_valore = -1.0
    id_massimo = ''

    for id_viaggio in distanze:
        valore = distanze[id_viaggio]
        if valore > massimo_valore:
            massimo_valore = valore
            id_massimo = id_viaggio

    return id_massimo


def estrai_fermate(connessioni, fermate):
    # Ordinamento manuale per sequenza
    i = 0
    while i < len(connessioni) - 1:
        j = i + 1
        while j < len(connessioni):
            if connessioni[i][0] > connessioni[j][0]:
                temp = connessioni[i]
                connessioni[i] = connessioni[j]
                connessioni[j] = temp
            j = j + 1
        i = i + 1

    fermate_visitate = []
    nomi_fermate = []

    indice = 0
    while indice < len(connessioni):
        da_fermata = connessioni[indice][1]
        a_fermata = connessioni[indice][2]

        for f in [da_fermata, a_fermata]:
            esiste = False
            k = 0
            while k < len(fermate_visitate):
                if fermate_visitate[k] == f:
                    esiste = True
                k = k + 1

            if f in fermate and esiste == False:
                posizione = len(nomi_fermate)
                nomi_fermate.insert(posizione, fermate[f][2])
                posizione2 = len(fermate_visitate)
                fermate_visitate.insert(posizione2, f)

        indice = indice + 1

    return nomi_fermate


def main():
    fermate = leggi_fermate('/Users/martaristori/Desktop/Anna/network_nodes.csv')
    viaggi = leggi_viaggi_bus('/Users/martaristori/Desktop/Anna/network_temporal_day.csv')
    distanze = calcola_distanze(viaggi, fermate)
    id_massimo = trova_massimo(distanze)

    if id_massimo == '':
        print("Errore")
        return

    fermate_ordinate = estrai_fermate(viaggi[id_massimo], fermate)

    print("Bus che si è mosso di più in termini di distanze percorse:", id_massimo)
    print("")
    print("Fermate attraversate:")

    indice = 0
    while indice < len(fermate_ordinate):
        numero = indice + 1
        print(str(numero) + ". " + fermate_ordinate[indice])
        indice = indice + 1


main()

end = time.time()

print("")
print("Quesito D:")
print("")


def n_fermate(percorso, separatore, nome):
    # Conta il numero di fermate uniche presenti nel file CSV.
    fermate = set()

    file = open(percorso, "r")
    righe = file.readlines()
    file.close()

    intestazione = righe[0].strip().split(separatore)
    indice_partenza = intestazione.index("from_stop_I")
    indice_arrivo = intestazione.index("to_stop_I")

    for riga in righe[1:]:
        estrai = riga.strip().split(separatore)
        if len(estrai) > max(indice_partenza, indice_arrivo):
            partenza = estrai[indice_partenza]
            arrivo = estrai[indice_arrivo]
            fermate.add(partenza)
            fermate.add(arrivo)

    print("Numero di fermate uniche in " + nome + ": " + str(len(fermate)))


def n_collegamenti(percorso, separatore, nome):
    # Conta il numero di collegamenti diretti unici tra fermate.

    collegamenti = set()

    file = open(percorso, "r")
    righe = file.readlines()
    file.close()

    intestazione = righe[0].strip().split(separatore)
    indice_partenza = intestazione.index("from_stop_I")
    indice_arrivo = intestazione.index("to_stop_I")

    for riga in righe[1:]:
        valori = riga.strip().split(separatore)
        if len(valori) > max(indice_partenza, indice_arrivo):
            partenza = valori[indice_partenza]
            arrivo = valori[indice_arrivo]
            collegamenti.add((partenza, arrivo))

    print("Numero di collegamenti diretti in " + nome + ": " + str(len(collegamenti)))


# Percorsi dei file CSV

network_temporal_day = "/Users/martaristori/Desktop/Anna/network_temporal_day.csv"

network_temporal_week = "/Users/martaristori/Desktop/Anna/network_temporal_week.csv"

# Tempo per network_temporal_day
start_day = time.time()
n_fermate(network_temporal_day, ",", "network_temporal_day")
n_collegamenti(network_temporal_day, ",", "network_temporal_day")
end_day = time.time()

print("")

# Tempo per network_temporal_week
start_week = time.time()
n_fermate(network_temporal_week, ";", "network_temporal_week")
n_collegamenti(network_temporal_week, ";", "network_temporal_week")
end_week = time.time()

end_tot = time.time()
print("")
print("Tempo risposte A, B, C: ", end - start)
print("Tempi risposta D:", (end_day - start_day), "e", (end_week - start_week))
print("Totale: ", end_tot - start_tot)
