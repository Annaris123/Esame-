# Risposta alla domanda A
def leggi_dati_network_nodes(network_nodes):
    luogo_servizi = {}  # crea un dizionario vuoto

    network_nodes = open('/Users/martaristori/Desktop/Anna/network_nodes.csv', 'r')  # Apri il file
    file = network_nodes.readlines()  # Leggi tutte le righe in una lista di stringhe
    network_nodes.close()  # Chiudi il file

    for riga in file[1:]:  # Salta la prima riga
        campi = riga.strip().split(',')  # strip -> Rimuove \n e split -> gli divide una lista
        servizio = campi[0]
        luogo = campi[3]

        if luogo not in luogo_servizi:  # Se il luogo non è ancora nel dizionario, lo aggiungiamo
            luogo_servizi[luogo] = [servizio]
        elif servizio not in luogo_servizi[luogo]:  # Se il luogo esiste già, ma il servizio no, lo aggiungiamo
            luogo_servizi[luogo].append(servizio)

    return luogo_servizi  # restituiamo il dizionario completo


def trova_top_luoghi(luogo_servizi, n=10):
    """
    Restituisce i primi n luoghi con il maggior numero di servizi diversi
    """
    lista = []  # crea una lista che conterrà delle coppie
    for luogo in luogo_servizi:
        conta = len(luogo_servizi[luogo])  # Conta quanti servizi diversi passano in luogo
        lista.append((luogo, conta))  # Aggiunge la coppia alla lista

    def prendi_secondo_elemento(tupla):
        return tupla[1] #serve per ordinare correttamente

    lista.sort(key=prendi_secondo_elemento, reverse=True) #Ordina la lista di coppie in base al numero di servizi
    return lista[:n]


def stampa_risultato(top_luoghi):
    print("I 10 luoghi attraversati da più servizi diversi:\n")
    for luogo, luogo_servizi in top_luoghi:
        print("Luogo:", luogo, ", Servizi diversi:", luogo_servizi)


# Esegui il tutto
dati = leggi_dati_network_nodes("network_nodes.csv")
top10 = trova_top_luoghi(dati)
stampa_risultato(top10)
