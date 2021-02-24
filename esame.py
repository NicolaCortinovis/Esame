# Esame del 24/02/2021 del corso di Laboratorio di Programmazione insegnato dal docente Stefano Alberto Russo
# by Nicola Cortinovis

# importo la funzione floor da math
from math import floor

# Eccezione specifica per l'esame
class ExamException(Exception):
    pass

# Classe che legge un file csv dato un nome, la classe ha un metodo che salva il contenuto  delle righe del file csv in liste che a loro volta verranno inserite in una lista di liste, effettivamente una lista di liste degli elementi contenuti in una riga del file csv (distinguiamo gli elementi nel csv tramite le ",")

class CSVTimeSeriesFile:

    # Costruttore di un oggetto della classe, riceve in input da tastiera il nome del file csv da aprire
    def __init__(self,name):
        self.name = name
    
    # Funzione della classe che crea e ritorna la lista di liste menzionata sopra
    def get_data(self):

        # Provo ad aprire un file csv avente nome self.name, se non ci riesco alzo eccezione
        try:
            file_esaminato = open(self.name,'r')
        except:
            raise ExamException('Errore, il file csv con nome "{}" non si puo\' aprire / non e\' stato trovato'.format(self.name))
        
        # Creo una lista di liste vuota, sara' quella che ritorno a fine funzione
        lista_di_liste = []

        # Ciclo su tutte le righe del csv
        for line in file_esaminato:
            
            # Se la riga e' vuota, la skippo
            if not line.strip():
                continue
            
            # Se nella riga non e' presente una virgola allora non ci sono almeno 2 valori e quindi la skippo
            if not ',' in line:
                continue

            # Usando come separatore la virgola (",") , "seziono" il contenuto della riga e lo salvo in una lista
            contenuto_riga = line.split(',')
            
            # Se non e' la riga d'intestazione
            if contenuto_riga[0] != "epoch":

                # Creo 2 variabili d'appoggio
                epoch = contenuto_riga[0]
                temp = contenuto_riga[1]
                
                # epoch e' un intero? se lo e' convertilo ad int
                if(epoch.isnumeric()):
                    epoch = int(epoch)
                # se non e' un intero
                else:
                    # prova a vedere se e' convertibile a float ed in caso arrotondalo
                    try:
                        epoch = float(epoch)
                        epoch = round(epoch)
                    # altrimenti skippalo
                    except:
                        continue
                        #raise ExamException('Errore, il parametro "{}" deve essere della tipologia dati interi'.format(epoch)) 

                # se ho salvato nella lista delle liste contententi [epoch,temp] almeno una lista e quindi almeno un'epoch
                if(len(lista_di_liste) > 0):
                    # controlliamo che l'epoch che sto analizzando sia maggiore di quella precedente (l'ultima che ho salvato)
                    if(epoch > lista_di_liste[-1][0]):
                        pass   
                    else:
                        raise ExamException('Errore, l\'epoch "{}" non e\' maggiore dell\' epoch precedente "{}"'.format(epoch,lista_di_liste[-1][0]))

                # Check se temp e' un intero, se lo e' tienilo come intero
                if(temp.isnumeric()):
                    temp = int(temp)
                # Altrimenti check se e' un float
                else:
                    # Prova a convertirlo a float
                    try:
                        temp = float(temp)
                    # Se non e' convertibile skippalo
                    except:
                        #print('Valore temp "{}" non valido, skippo'.format(temp))
                        continue
                
                # Salvo epoch e temp in una lista
                lista_appoggio = [epoch,temp]
                    
                # Aggiungi alla lista di liste la lista d'appoggio
                lista_di_liste.append(lista_appoggio)
        
        # Ritorna la lista di liste
        return lista_di_liste
        

# Data una lista di liste, con le liste contenenti [epoch, temperatura] la funzione restituisce una lista che segnala quante inversioni di trend avvengono in un'ora
def hourly_trend_changes(time_list):
    
    # Creo una lista inizialmente vuota che dovra' contenere tutte le ore presenti nella time_list, considerando che data un epoch: se la parte intera di questa epoch/3600 e' uguale alla parte intera (di un altra epoch) ottenuta da epoch/3600 queste due epoch appartengono alla stessa ora
    lista_ore = []

    # Check se abbiamo almeno 2 registrazioni [epoch,temperature] per stabilire un trend
    if(len(time_list) < 2):
        raise ExamException('Errore, nel parametro "{}", non ci sono abbastanza registrazioni [epoch,temperature] per stabilire un trend'.format(time_list))

    # Ciclo sulla lista di liste 
    for item in time_list:


        # Se la lista_ore e' vuota salvo la prima epoch che leggo

        if(lista_ore == []):
            lista_ore.append(floor(item[0] / 3600))

        elif(item[0] % 3600 == 0): # Se l'epoch % 3600 da' resto uguale a 0 allora abbiamo una nuova ora che salviamo nella lista
            lista_ore.append(item[0] / 3600) # La salvo

        # Se abbiamo che l'epoch % 3600 != 0 significa che non e' una misurazione (xx:00) se appartiene alla stessa ora, allora facendo un cast ad int di (item[0] / 3600) la parte decimale viene troncata e abbiamo la stessa parte intera. Se invece e' un'ora diversa allora la parte intera e' maggiore di quella precedente e quindi la voglio salvare nella mia lista ore

        elif(floor(item[0] / 3600) > lista_ore[-1]):
            lista_ore.append(floor(item[0] / 3600))
    
    # Print di tutte le ore registrate nella time_list
    #print(lista_ore)

    # Voglio crearmi una lista che contiene altre liste, queste liste contengono la temperatura registrata per ciascuna ora

    # Lista delle temperature registrate in un'ora (tpo)
    temp_per_ora = []
    # Lista delle liste delle temperatura registrata per ogni ora
    list_of_tpo = [] #
    # Variabile d'appoggio:
    # Indice per scorrere la lista_ore
    index = 0
    # i per indicare il contenuto della lista ore
    i = lista_ore[index]

    # Per ogni elemento nella time_list
    for item in time_list:
        # Controllo se appartiene ad i-esima ora della lista (le ore sono ordinate quindi posso sfruttare l'indice i)
        if(floor(item[0] / 3600) == i):
            # Salvo la temperatura appartenente alla i-esima ora nella lista
            temp_per_ora.append(item[1])
        
        # Se siamo all'ora succesiva
        else:
            # Mi salvo nella lista di liste la lista di temperature
            list_of_tpo.append(temp_per_ora)
            # Creo una nuova lista temperature
            temp_per_ora = []
            # Ci inserisco l'elemento che apparteneva all'ora successiva, senno' andrebbe perso
            temp_per_ora.append(item[1])
            # Incremento di 1 i, cosi' lista_ore[i] indica l'ora successiva
            index += 1
            i = lista_ore[index]
    
    # Quando il ciclo for finisce non viene aggiunta alla lista di liste l'ultima lista di temperature, lo faccio qui
    list_of_tpo.append(temp_per_ora)

    # Print di tutte le temperature per una determinata ora (il massimo e' 6 visto che consideriamo misurazioni su intervalli di 10 minuti)
    #for element in list_of_tpo:
        #print(element)

    # Calcolo dell'inversione dei trend

    # Variabile dove salvare il trend
    trend = 'Not set'
    # Variabile dove salvare il trend precedente
    previous_trend = 'Not set'
    # Variabile dove salvare l'ultimo elemento della lista di temperature
    ultimo_elem = 'Not set'
    # Lista dei cambiamenti di trend rilevati, e' quella che viene ritornata a fine funzione
    lista_trend = []
    
    # Leggi e indicizza la lista delle liste di temperature
    for j, element in enumerate(list_of_tpo):
        # Inizialmente gni ora ha 0 cambiamenti di trend rilevati
        cambiamenti_di_trend = 0

        # Se siamo alla prima ora della lista
        if(j == 0):
            # Le leggo e indicizzo gli elementi
            for i, item in enumerate(element):
                # Alla prima lettura ho solo 1 elemento e non posso calcolarmi il trend, segnalo che alla prossima lettura trend potra' essere calcolato e passo alla prossima iterazione
                if(trend == 'Not set'):
                    trend = 'Ready to set'
                    continue
                # Se previous_trend e' pronto per essere settato possiamo cominciare ad aggiornarlo prima del calcolo del nuovo trend
                if(previous_trend != 'Not set'):
                    previous_trend = trend
                # Mi calcolo il trend
                trend = element[i] - element[i-1]
                # Alla seconda lettura non ho un trend precedente con cui confrontare quello corrente, segnalo che alla prossima lettura previous_trend potra' essere calcolato e passo alla prossima iterazione
                if(previous_trend == 'Not set'):
                    previous_trend = 'Ready to set'
                    continue

                # Ora posso iniziare ad osservare i comportamenti dei trend
                # Se trend e previous_trend sono entrambi positivi, negativi oppure uno e' nullo allora non c'e' stato nessun cambiamento di trend e non devo incrementare nulla 
                if((trend >= 0 and previous_trend >= 0) or (trend <= 0 and previous_trend <= 0)):
                    continue

                # Se trend e previous trend rendono falsa una delle 2 espressioni booleane allora abbiamo un cambiamento di trend nell'ora e vado ad incrementare il mio contatore 
                else:
                    cambiamenti_di_trend += 1
                    #print("cambio di trend")
                    #print("{} - {}".format(element[i],element[i-1]))
            
            # Finito di leggere la prima ora mi salvo l'ultimo elemento dell'ora che mi servira' per calcolare il primo trend della prossima ora
            ultimo_elem = element[-1]
            # Salvo le variazioni di trend nella lista da ritornare
            lista_trend.append(cambiamenti_di_trend)

            # Abbiamo risolto il caso particolare del primo elemento e possiamo quindi passare ai casi generali, faccio saltare alla prossima iterazione il for che gestisce la lista delle liste di temperature
            continue


        # j = 1 quindi dalla seconda ora della lista
        # Dobbiamo calcolarci il nuovo trend sfruttando l'ultimo elemento della lista precedente che ho salvato ed il primo della lista corrente
        # Leggo ed indicizzo la mia lista di temperature
        for i, item in enumerate(element):
            
            # Se la prima ora aveva un solo elemento non e' stato calcolato alcun trend, ma con la seconda ora (che siamo sicuro contenga almeno 1 temperatura) possiamo calcolarci il trend e indicare che alla prossima temperatura possiamo calcolarci il previous_trend
            if(trend == 'Ready to set'):
                trend = element[i] - ultimo_elem
                previous_trend = 'Ready to set'
                continue
          
            # Controlliamo ci sia un trend (significante) da salvare in previous_trend
            if(trend != 0):
                    previous_trend = trend

            # Nel caso in cui i primi 2 elementi letti siano uguali quel trend e' pari a 0 ed alla terza chiamata previous_trend non lo registra perche' un trend nullo non ci serve per calcolarci eventuali variazioni. Lo settiamo di default a 0.
            if(previous_trend == 'Ready to set'):
                previous_trend = 0

            # Se siamo al primo elemento
            if(i == 0):
                # Allora trend e' dato dalla differenza tra il primo elem e l'ultimo della lista precedente
                trend = element[i] - ultimo_elem

                # Check se non c'e' un cambiamento di trend
                if((trend >= 0 and previous_trend >= 0) or (trend <= 0 and previous_trend <= 0)):
                    continue
                # Se c'e'
                else:
                    cambiamenti_di_trend += 1
                    #print("cambio di trend")
                    #print("{} - {}".format(element[i],element[i-1]))

            else:
                # Se non siamo al primo elemento allora il trend e' dato da (temperatura i-esima - la tempertura precedente)
                trend = element[i] - element[i-1]

                # Check se non c'e' un cambiamento di trend
                if((trend >= 0 and previous_trend >= 0) or (trend <= 0 and previous_trend <= 0)):
                    continue
                # Se c'e'
                else:
                    cambiamenti_di_trend += 1
                    #print("cambio di trend")
                    #print("{} - {}".format(element[i],element[i-1]))
            
        # Salvo l'ultimo elemento della lista temp
        ultimo_elem = element[-1]
        lista_trend.append(cambiamenti_di_trend)
    
    return lista_trend
            
##########################################################################################
########## Parte di soft testing del programma, cancellami/commentami alla fine ##########
##########################################################################################


# Quello che mi aspetto di ottenere per il file testing.csv
#expected_list_1 = [0,1,1,2,1,1]
#expected_list_2 = [0,2,4,2,1,4]
#expected_list_3 = [0,0,0,1]
#expected_list_4 = [0,0,0,1]
#testing = CSVTimeSeriesFile("testing4.csv")
#testing_list = testing.get_data()
#testing2 = CSVTimeSeriesFile("prova")
#print("Non c'e' il file ma il controllo e' in get_data()")
#print("Chiamo get_data()")
#testing2_list = testing2.get_data()

#for item in testing_list:
#    print(item)
#result = hourly_trend_changes(testing_list)
#print('\n\n')
#print('Expected list for csv file "{}"'.format(testing.name))
#if(testing.name == "testing.csv"):
#    print(expected_list_1)
#elif(testing.name == "testing2.csv"):
#    print(expected_list_2)
#elif(testing.name == "testing3.csv"):
#    print(expected_list_3)
#elif(testing.name == "testing4.csv"):
#    print(expected_list_4)
#print("\nResult")
#print(result)


###########################################################################################