# Apre e legge il file temporale dei collegamenti tra fermate
file_collegamenti = open("/Users/martaristori/Desktop/Anna/network_temporal_day.csv", "r")
fermate_con_servizi = {}  # Dizionario: ID fermata → lista dei servizi che la attraversano
riga = file_collegamenti.readline()  # salta intestazione

for riga in file_collegamenti:
    campi = riga.strip().split(",")  # separazione dei dati
    id_partenza = campi[0]
    id_arrivo = campi[1]
    servizio = campi[4]

    # Aggiunge il servizio alla fermata di partenza
    if id_partenza not in fermate_con_servizi:
        fermate_con_servizi[id_partenza] = [servizio]
    elif servizio not in fermate_con_servizi[id_partenza]:
        fermate_con_servizi[id_partenza].append(servizio)

    # Aggiunge il servizio alla fermata di arrivo
    if id_arrivo not in fermate_con_servizi:
        fermate_con_servizi[id_arrivo] = [servizio]
    elif servizio not in fermate_con_servizi[id_arrivo]:
        fermate_con_servizi[id_arrivo].append(servizio)

file_collegamenti.close()

# Calcola il numero di servizi diversi per ogni fermata
lista_id_fermate = list(fermate_con_servizi.keys())
lista_numero_servizi = [len(fermate_con_servizi[id]) for id in lista_id_fermate]

top_10_id = []  # ID delle fermate con più servizi
top_10_valori = []  # Numero di servizi corrispondente

while len(top_10_id) < 10:
    massimo = max(lista_numero_servizi)
    indice_massimo = lista_numero_servizi.index(massimo)
    id_top = lista_id_fermate[indice_massimo]

    top_10_id.append(id_top)
    top_10_valori.append(massimo)
    lista_numero_servizi[indice_massimo] = 0  # così non viene riusata

# Apre il file dei nodi per associare ID → nome fermata
file_nodi = open("/Users/martaristori/Desktop/Anna/network_nodes.csv", "r")
mappa_id_nome = {}
riga = file_nodi.readline()  # salta intestazione

for riga in file_nodi:
    campi = riga.strip().split(",")
    mappa_id_nome[campi[0]] = campi[3]

file_nodi.close()

# Costruisce la lista dei nomi delle fermate per gli ID trovati
nomi_fermate_top = [mappa_id_nome[id] for id in top_10_id]

# Stampa finale, ordinata e chiara
print("Quesito A")
print("Le 10 fermate attraversate da più servizi diversi sono:\n")
for i in range(10):
    print(str(i + 1) + "." + nomi_fermate_top[i], "con", top_10_valori[i], "servizi diversi")


def to_float_like(s):
    i = 0
    parte_intera = ""
    parte_decimale = ""
    punto = 0

    while i < len(s):
        c = s[i]
        if c == ".":
            punto = 1
        elif c >= "0" and c <= "9":
            if punto == 0:
                parte_intera = parte_intera + c
            else:
                parte_decimale = parte_decimale + c
        i = i + 1

    intero = 0
    j = 0
    while j < len(parte_intera):
        intero = intero * 10 + (ord(parte_intera[j]) - ord("0"))
        j = j + 1

    decimale = 0
    base = 1
    k = 0
    while k < len(parte_decimale):
        decimale = decimale * 10 + (ord(parte_decimale[k]) - ord("0"))
        base = base * 10
        k = k + 1

    return intero + decimale / base


# Leggi fermate da network_nodes.csv
fermate = {}  # ID -> (x, y)
nomi = {}  # ID -> nome

f = open("/Users/martaristori/Desktop/Anna/network_nodes.csv", "r")
riga = f.readline()

while riga != "":
    valori = riga.strip().split(",")
    if len(valori) >= 4:
        idf = valori[0]
        nome = valori[1]
        x_str = valori[2]
        y_str = valori[3]

        x = to_float_like(x_str)
        y = to_float_like(y_str)

        fermate[idf] = (x, y)
        nomi[idf] = nome

    riga = f.readline()

f.close()

# Inizializza il massimo
massimo = -1
id_partenza = ""
id_arrivo = ""
tempo_massimo = 0

f2 = open("/Users/martaristori/Desktop/Anna/network_temporal_day.csv", "r")
riga = f2.readline()

while riga != "":
    valori = riga.strip().split(",")
    if len(valori) >= 4:
        id1 = valori[0]
        id2 = valori[1]
        t1_str = valori[2]
        t2_str = valori[3]

        t1 = to_float_like(t1_str)
        t2 = to_float_like(t2_str)

        tempo = t2 - t1

        if id1 in fermate and id2 in fermate and tempo > 0:
            x1, y1 = fermate[id1]
            x2, y2 = fermate[id2]

            dx = x2 - x1
            dy = y2 - y1

            distanza = (dx * dx + dy * dy) ** 0.5

            rapporto = distanza / tempo

            if rapporto > massimo:
                massimo = rapporto
                id_partenza = id1
                id_arrivo = id2
                tempo_massimo = tempo
                distanza_massima = distanza

    riga = f2.readline()

f2.close()

# Stampa finale
print("")
print("Quesito B")
print("Coppia di fermate consecutive con il rapporto distanza/tempo più alto:")
print("Da ", id_partenza, " a ", id_arrivo)

def leggi_file(percorso):
    with open(percorso, "r") as f:
        return f.readlines()[1:]  # salta intestazione

def carica_fermate(righe):
    diz = {}
    for riga in righe:
        riga = riga.strip()
        if riga != "":
            campi = riga.split(",")
            if len(campi) >= 4:
                id_fermata = campi[0].strip()
                x_str = campi[1].replace(".", "").replace(",", "")
                y_str = campi[2].replace(".", "").replace(",", "")
                x = int(x_str[:6]) if x_str.isdigit() else 0
                y = int(y_str[:6]) if y_str.isdigit() else 0
                nome = campi[3].strip()
                diz[id_fermata] = (nome, x, y)
    return diz

def distanza(p1, p2):
    dx = p1[0] - p2[0]
    dy = p1[1] - p2[1]
    return (dx * dx + dy * dy) ** 0.5

def carica_percorsi(righe):
    percorsi = {}
    dati = []
    for riga in righe:
        campi = riga.strip().split(",")
        if len(campi) >= 8:
            from_stop = campi[0]
            to_stop = campi[1]
            trip = campi[5]
            seq = campi[6]
            route = campi[7]
            try:
                dati.append((int(route), int(trip), int(seq), from_stop, to_stop))
            except:
                continue

    # Ordina per bus, poi per trip, poi per seq
    def ordina_dati(dati):
        for i in range(1, len(dati)):
            corrente = dati[i]
            j = i - 1
            while j >= 0 and (dati[j][0], dati[j][1], dati[j][2]) > (corrente[0], corrente[1], corrente[2]):
                dati[j + 1] = dati[j]
                j -= 1
            dati[j + 1] = corrente

    for r in dati:
        bus = str(r[0])
        from_stop = r[3]
        to_stop = r[4]
        if bus not in percorsi:
            percorsi[bus] = []
        if len(percorsi[bus]) == 0 or percorsi[bus][-1] != from_stop:
            percorsi[bus].append(from_stop)
        if percorsi[bus][-1] != to_stop:
            percorsi[bus].append(to_stop)
    return percorsi


def calcola_distanze(percorsi, fermate):
    distanze = {}
    for bus, percorso in percorsi.items():
        somma = 0
        for j in range(len(percorso) - 1):
            f1, f2 = percorso[j], percorso[j + 1]
            if f1 in fermate and f2 in fermate:
                p1 = fermate[f1][1:]
                p2 = fermate[f2][1:]
                somma += distanza(p1, p2)
        distanze[bus] = somma
    return distanze

def trova_bus_max(distanze):
    massimo = None
    valore_massimo = float('-inf')
    for k in distanze:
        valore = distanze[k]
        if valore > valore_massimo:
            valore_massimo = valore
            massimo = k
    return massimo


def stampa_percorso(bus, percorsi, fermate, distanze):
    print("")
    print("Quesito C")
    print("Bus che ha percorso più distanza:", bus)
    print("Distanza totale:", round(distanze[bus], 2))
    print("Fermate attraversate (in ordine):")
    percorso = percorsi[bus]
    for id_fermata in percorso:
        if id_fermata in fermate:
            nome_fermata = fermate[id_fermata][0]
        else:
            nome_fermata = "Fermata sconosciuta (", id_fermata, ")"
        print("- ", nome_fermata)

def main():
    righe_fermate = leggi_file("/Users/martaristori/Desktop/Anna/network_nodes.csv")
    righe_percorsi = leggi_file("/Users/martaristori/Desktop/Anna/network_temporal_day.csv")

    fermate = carica_fermate(righe_fermate)
    percorsi = carica_percorsi(righe_percorsi)
    distanze = calcola_distanze(percorsi, fermate)
    bus = trova_bus_max(distanze)
    stampa_percorso(bus, percorsi, fermate, distanze)

main()