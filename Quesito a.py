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

top_10_id = []     # ID delle fermate con più servizi
top_10_valori = [] # Numero di servizi corrispondente

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
print("Le 10 fermate attraversate da più servizi diversi sono:\n")
for i in range(10):
    print(str(i+1) + "." + nomi_fermate_top[i], "con", top_10_valori[i], "servizi diversi")

