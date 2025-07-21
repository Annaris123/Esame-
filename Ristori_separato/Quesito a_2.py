print("Quesito A:")
print("")


def collegamenti(temporal_day):
    file = open(temporal_day, "r")
    fermate_servizi = {}

    file.readline()  # Salta intestazione
    for riga in file:
        campi = riga.strip().split(",")
        id_partenza = campi[0]
        id_arrivo = campi[1]
        servizio = campi[4]

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