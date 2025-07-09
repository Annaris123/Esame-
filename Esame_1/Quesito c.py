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
