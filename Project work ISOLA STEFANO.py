import random #Importiamo il modulo random per la generazione di numeri casuali all'interno di un intervallo
import time
import copy
import math
print("-------------------------------------------------------------------------------------------------")
print("      SIMULAZIONE DEL PROCESSO DI PRODUZIONE DI 3 TIPOLOGIE DI PRODOTTI DEL GRUPPO PITTINI       ")
print("-------------------------------------------------------------------------------------------------")
print("")
#Di seguito vengono trascritte delle costanti globali, che possono essere modificate dal programmatre qualora ci sia necessità
MIN = 96
MAX = 288
CAPACITA_MIN_GIORNALIERA = 96
CAPACITA_MAX_GIORNALIERA = 288
TEMPO_MIN = 5
TEMPO_MAX = 15
#Definiamo una funzione per la generazione della quantità da produrre per ogni tipologia di prodotto
def genera_quantita_produzione(prodotti):
  quantita_da_produrre = {}
  print("-------------------------------------------------------------------------------------------------")  
  for prodotto in prodotti:
    quantita = random.randint(MIN, MAX) 
    quantita_da_produrre[prodotto] = quantita 
    print("QUANTITA' DA PRODURRE PER TIPOLOGIA DI PRODOTTO:\t",prodotto,"---->",quantita,"pezzi")
    print("--------------------------------------------------------------------------------------------")
  print("La quantità totale da produrre è quindi uguale a:\t",sum(quantita_da_produrre.values()),"pezzi")
  print("--------------------------------------------------------------------------------------------\n\n")
  return quantita_da_produrre
 
#Definiamo una funzione per la generazione dei parametri di produzione: Tempo_produzione_per_prodotto, Capacita_max_produzione_giorno e Capacita_max_totale
def generazione_parametri_di_produzione(prodotti):
  parametri_di_produzione = {
    'Tempo_produzione_per_prodotto' : {},
    'Capacita_max_produzione_giorno' : {},
    'Capacita_max_totale' : 0
  }
  for prodotto in prodotti:
    #Tempo di produzione per ogni prodotto
    Tempo_produzione_unita_prodotto = random.randint(TEMPO_MIN, TEMPO_MAX) #Generazione di una tempistica di produzione casuale di ogni prodotto (ad es. tra 1 e 5 minuti)
    parametri_di_produzione['Tempo_produzione_per_prodotto'][prodotto] = Tempo_produzione_unita_prodotto
    print("---------------------------------------------------------------------------------------------------------------------")
    print("Tempo di produzione del singolo prodotto:",prodotto,"--->",Tempo_produzione_unita_prodotto,"minuti") 
    Capacita_massima_giornaliera_prodotto = random.randint(CAPACITA_MIN_GIORNALIERA,CAPACITA_MAX_GIORNALIERA) 
    parametri_di_produzione['Capacita_max_produzione_giorno'][prodotto] = Capacita_massima_giornaliera_prodotto
    print("---------------------------------------------------------------------------------------------------------------------")
    print("CAPACITA' MASSIMA GIORNALIERA PER TIPOLOGIA DI PRODOTTO:\t",prodotto,"--->",Capacita_massima_giornaliera_prodotto,"pezzi")
    print("---------------------------------------------------------------------------------------------------------------------")
    
  #Capacità massima di produzione giornaliera complessiva  
  capacita_massima_totale = sum(parametri_di_produzione['Capacita_max_produzione_giorno'].values())
  parametri_di_produzione['Capacita_max_totale'] = capacita_massima_totale
  print("------------------------------------------------------------------")
  print("CAPACITA' GIORNALIERA COMPLESSIVA:\t",capacita_massima_totale,"pezzi")
  print("------------------------------------------------------------------")
  print("")
  return parametri_di_produzione

  
def calcola_tempo_totale_produzione(parametri_di_produzione, quantita_da_produrre):
  eccesso_per_prodotto = {}
  tempo_per_prodotto = 1
  tempo_totale_produzione = 0
  for prodotto, quantita in quantita_da_produrre.items():
    capacita_giornaliera_prodotto = parametri_di_produzione['Capacita_max_produzione_giorno'][prodotto]
    if quantita > capacita_giornaliera_prodotto:
      eccesso = quantita - capacita_giornaliera_prodotto
      eccesso_per_prodotto[prodotto] = eccesso
      tempo_per_prodotto = parametri_di_produzione['Tempo_produzione_per_prodotto'][prodotto] * quantita 
      print("")
      print("Per il prodotto",prodotto,"c'è un eccesso di",eccesso,"pezzi")
      print("Somma degli eccessi. . . .\t",sum(eccesso_per_prodotto.values()),"pezzi")
      print("Il tempo di produzione dei prodotti richiesti di",prodotto,"(",quantita,"pezzi) è di:\t",tempo_per_prodotto,"minuti")
      print("---------------------------------------------------------------------------------------------")
      print("")
      tempo_totale_produzione += tempo_per_prodotto
      tempo_totale_produzione_in_ore = (tempo_totale_produzione / 60)
    else:
      tempo_per_prodotto = parametri_di_produzione['Tempo_produzione_per_prodotto'][prodotto] * quantita 
      print("Nessun eccesso del prodotto",prodotto,"!")
      print("Il tempo di produzione dei prodotti richiesti di",prodotto,"(",quantita,"pezzi) è di:\t",tempo_per_prodotto,"minuti")
      print("---------------------------------------------------------------------------------------------")
      tempo_totale_produzione += tempo_per_prodotto
      tempo_totale_produzione_in_ore = (tempo_totale_produzione / 60)
  print("---------------------------------------------------------------------------------------------")
  print("IL TEMPO TOTALE DI PRODUZIONE DELL'INTERO LOTTO E' DI:\t",format(tempo_totale_produzione_in_ore,".2f"),"ore")
  print("---------------------------------------------------------------------------------------------")
  return tempo_totale_produzione_in_ore
print("\n\n\n\n")


TEMPERATURA_FUSIONE = 1620
TARGET_LUNGHEZZA = 2
TOLLERANZA_LUNGHEZZA = 0.2
PACCO_STOCCATO = 10

class Billetta:
  def __init__(self,id_billetta):
    self.billetta = id_billetta
    self.stato = "...."
    self.lunghezza = 0
    self.ammaccature = False
    self.qualita_superata = False
    
  def aggiornamento_stato_billetta(self,nuovo_stato):
    self.stato = nuovo_stato
    print("Stato della billetta prodotta n°",self.billetta,":",nuovo_stato)
    
  def impostazione_caratteristiche_billetta (self, lunghezza, ammaccature):
    print("Lunghezza di",lunghezza)
    self.lunghezza = lunghezza
    self.ammaccature = ammaccature
    if ammaccature == False: 
      print("Non presenta ammaccature")
    else:
      print("Presenta ammaccature")
      
    
  def definisci_qualita_billetta(self,qualita_superata):
    self.qualita_superata = qualita_superata
    if qualita_superata:
      print("CONFORME")
    else:
      print("NON CONFORME")
    print("")

class Produzione_billetta:
  def __init__(self):
    self.materiale_forno = 0
    self.forno_vuoto = True
    self.temperatura_forno = 0
    self.billette_da_produrre = {}
    self.billette_prodotte = []
    self.pacchi_prodotti = 0 
    self.prossima_billetta = 1
    self.ammaccaure = False
    self.lunghezza = 0
    self.controllo_billetta = 1
  
  def carica_forno(self):
    print("FASE DI CARICAMENTO FORNO")
    tempo_processo = random.randint(1,5)#secondi
    ferro_riciclato_richiesto = random.randint(10, 100)
    ferro_riciclato_disponibile = random.randint(10,100)
    if ferro_riciclato_disponibile >= ferro_riciclato_richiesto:
      print("Materiale riciclato richiesto =",ferro_riciclato_richiesto,"kg\nMateriale riciclato disponibile =",ferro_riciclato_disponibile,"kg")
      self.materiale_forno = ferro_riciclato_disponibile
      self.forno_vuoto = False   
      print("Caricamento di",self.materiale_forno,"kg di materiale ferroso ricilato.......")
      time.sleep(tempo_processo)
      print("Caricameto completato! Il forno è stato caricato in",tempo_processo,"secondi.\nIl materiale è pronto per la fusione!")
      return True
    else:
      print("Materiale riciclato richiesto =",ferro_riciclato_richiesto,"\nMateriale riciclato disponibile =",ferro_riciclato_disponibile)
      print("Caricamento del forno non completato")
      return False
    
  def fusione_forno(self):
    print("FASE DI FUSIONE")
    if self.forno_vuoto:
      print("Materiale non caricato! Impossibile inizare la fusione")
      return False
    else:
      print("Aumento temperatua del forno EAF. . . . . .")
      while self.temperatura_forno < TEMPERATURA_FUSIONE:
        self.temperatura_forno += random.randint(100,120)
        time.sleep(1)
      print("Temperatura di",self.temperatura_forno,"°C raggiunta!\nInizio della fusione......")
      time.sleep(10)
      print("Fusione completata!\nProdotto pronto per la colata continua!")
      return True
    
  def colata_continua(self):
    print("FASE DI COLATA CONTINUA")
    if self.forno_vuoto or self.temperatura_forno < TEMPERATURA_FUSIONE:
      print("Impossibile iniziare la fase di colata continua!")
      return False
    else:
      self.forno_vuoto = False
      materiale_colato = random.randint(1,10)
      tempo_totale = 0
      print("Trasferimento materiale da forno a stampo.....")
      while self.materiale_forno > 0:
        self.materiale_forno -= materiale_colato
        tempo_colata = random.randint(1,2)
        tempo_totale += tempo_colata
      time.sleep(tempo_totale)
      self.materiale_forno = 0
      print("Colatura completata!\nMateriale pronto per il raffreddamento")
      return True
      
  def raffreddamento(self):
    print("FASE DI RAFFREDDAMENTO")
    if self.forno_vuoto or self.temperatura_forno < TEMPERATURA_FUSIONE:
      print("Impossibile iniziare la fase di raffreddamento")
    else:
      tempo_raffreddamento = random.randint(10,20)
      if self.materiale_forno == 0:
        print("Fase di raffreddamento tramite spruzzi d'acqua. . . .")
        time.sleep(tempo_raffreddamento)
        print("Raffreddamento completato! Materiale pronto per il taglio")
      
  def taglio_e_controllo_qualita(self,quantita_billette):
    print("FASE DI TAGLIO E CONTROLLO QUALITA'")
    if not self.forno_vuoto:
      self.billette_da_produrre = copy.deepcopy(quantita_billette)
      numero_billette = self.billette_da_produrre['BILLETTA']
      billette_conformi = []
      billette_non_conformi =[]
      print("Ricordiamo che andremo a produrre",numero_billette,"billette, quindi taglieremo le billette fino a raggiungere il numero prestabilito")
      tolleranza_lunghezza_billette = TARGET_LUNGHEZZA * (TOLLERANZA_LUNGHEZZA / 100)
      lunghezza_max = TARGET_LUNGHEZZA + tolleranza_lunghezza_billette
      lunghezza_min = TARGET_LUNGHEZZA - tolleranza_lunghezza_billette
      print("Taglio di",numero_billette,"billette. . . . . .")
      for _ in range (numero_billette):
        billetta_corrente = self.prossima_billetta
        billetta = Billetta(billetta_corrente)
        self.prossima_billetta += 1
        lunghezza_billetta = random.uniform(lunghezza_min, lunghezza_max)
        ammaccature_presenti = random.random() < 0.05
        billetta.aggiornamento_stato_billetta("Tagliata")
        billetta.impostazione_caratteristiche_billetta(lunghezza_billetta, ammaccature_presenti)
        self.billette_prodotte.append(billetta)
        if lunghezza_billetta and not ammaccature_presenti:
          billetta.definisci_qualita_billetta(True)
          billette_conformi.append(billetta)
        else:
          if ammaccature_presenti or not lunghezza_billetta:
            billetta.definisci_qualita_billetta(False)
            billette_non_conformi.append(billetta)
        time.sleep(1)
      print("Processo di taglio completato: sono state prodotte",len(self.billette_prodotte),"billette")
      print("Tra queste ci sono",len(billette_conformi),"billette conformi e",len(billette_non_conformi),"billette non coformi")
      print("Le billette non conformi verranno utilizzate come scarto per un nuovo ciclo di produzione")
      self.billette_prodotte = billette_conformi
      return True
    else:
      print("Impossibile iniziare taglio e controllo qualità!")
    
  def stoccaggio(self):
    print("FASE DI STOCCAGGIO")
    if not self.billette_da_produrre:
      print("Impossibile inziare la fase di stoccaggio!")
    else:
      tempo_stoccaggio = random.randint(5,10)
      billette_residue = len(self.billette_prodotte)
      print("Inizio fase di stoccaggio")
      while billette_residue >= PACCO_STOCCATO:
        self.pacchi_prodotti += 1
        billette_residue -= PACCO_STOCCATO  
        print("Preparazione pacco. . . .\nPacco n°",self.pacchi_prodotti,"stoccato\nContiene",PACCO_STOCCATO,"billette.")
        print("")
        time.sleep(tempo_stoccaggio)       
      print("Stoccaggio completato! Sono stati ultimati",self.pacchi_prodotti,"pacchi di billette.")
      if billette_residue > 0:
        time.sleep(tempo_stoccaggio)
        ultimo_pacco_creato = 1
        print("Sono rimaste",billette_residue,"billette con le quali è stato prodotto un ultimo pacco")
      pacchi_totali_stoccati = self.pacchi_prodotti + ultimo_pacco_creato
      print("In totale sono quindi stati stoccati",pacchi_totali_stoccati,"pacchi")
      
TEMPERATURA_PRERISCALDO = 1050
LUNGHEZZA_BILLETTA = 4
NUMERO_BILLETTE_DA_LAVORARE = random.randint(10, 20)
LUNGHEZZA_STANDARD_MATASSA= 150



class Vergella:
  def __init__(self,id_vergella):
    self.vergella = id_vergella
    self.peso = 0
    self.stato = ""
    
  def aggiornamento_stato_vergella(self, nuovo_stato):
    self.stato = nuovo_stato
    print("Stato della porzione di vergella",self.vergella,":",nuovo_stato)
  
  def aggiornamento_stato_matassa(self, nuovo_stato):
    self.nuovo_stato = nuovo_stato
    print("Stato della matassa",self.vergella,":",nuovo_stato)
    
      
    
class Produzione_vergella:
  def __init__(self):
    self.sezione_billetta = random.randint(120,160)#mm
    self.prossima_billetta = 1
    self.temperatura_forno = 0
    self.billetta_preriscaldata = False
    self.calibratore_4_passi = False
    self.riduzione_effettuata = False
    self.misuratore= False
    self.controllo_eseguito = False
    self.diametro_ok =False
    self.tagliata = False
    self.temperatura_ok = False
    self.prossima_porzione = 1
    self.matassa_ok = 1
    self.spire_formate = False
    self.matassa_completa = 1
    self.matassa_formata = False
    self.diametro_iniziale_billetta = math.sqrt(4*self.sezione_billetta**2/3.14)#Espresso in mm 
    self.vergella_da_produrre = {}      
    self.matasse_da_produrre = 0
    #self.difetti = 0
    #bobine_difettate = []
    #bobine_ottimali = []

  
  
  def preriscaldo (self, numero_billette):
    print("FASE DI PRERISCALDO")
    print("Si richiede la produzione di vergella partendo da",NUMERO_BILLETTE_DA_LAVORARE,"billette di diametro",self.diametro_iniziale_billetta)
    print("Preriscaldo",NUMERO_BILLETTE_DA_LAVORARE,"billette di sezione",self.sezione_billetta,"X",self.sezione_billetta,"mm quadri.....")
    while self.temperatura_forno < TEMPERATURA_PRERISCALDO:
      self.temperatura_forno += random.randint(100, 110)
      time.sleep(1)
    print("Temperatura di",self.temperatura_forno,"raggiunta")
    for _ in range (NUMERO_BILLETTE_DA_LAVORARE):
      billetta_da_inserire = self.prossima_billetta
      billetta = Billetta(billetta_da_inserire)
      self.prossima_billetta += 1
      time.sleep(1)
      billetta.aggiornamento_stato_billetta("PRERISCALDATA")
    print("Preriscaldo completato!")
    self.billetta_preriscaldata = True
    print("")
    return numero_billette
      
  def riduzione_verticale_orizzontale(self, numero_billette):
    print("Inizio riduzione delle",NUMERO_BILLETTE_DA_LAVORARE,"billette.....")
    if self.calibratore_4_passi:
      print("Impossibile iniziare la riduzione")
    else:
      elenco_diametri = [6,8,12]
      diametro_richiesto = random.choice(elenco_diametri)
      print("Si richiede di ottenere un diametro di",diametro_richiesto,"mm.....")
      for _ in range (NUMERO_BILLETTE_DA_LAVORARE):
        billetta_da_ridurre = self.prossima_billetta
        billetta = Billetta(billetta_da_ridurre)
        riduzione_singola_billetta = random.uniform (0.2, 0.5)
        while self.diametro_iniziale_billetta > diametro_richiesto:
         self.diametro_iniziale_billetta -= riduzione_singola_billetta
         self.riduzione_effettuata = True
        if abs(self.diametro_iniziale_billetta - diametro_richiesto) < 0.50:
          print("Diametro della billetta n°",(self.prossima_billetta - NUMERO_BILLETTE_DA_LAVORARE),"di",self.diametro_iniziale_billetta,"mm: OK\tRIDOTTA")
          self.diametro_ok = True
          self.prossima_billetta += 1
        else:
          print("Diametro della billetta n°",(self.prossima_billetta - NUMERO_BILLETTE_DA_LAVORARE),"di",self.diametro_iniziale_billetta,"mm:  KO\tRIDOTTA")
          self.diametro_ok = False
          self.controllo_eseguito = True
          self.prossima_billetta += 1
      print("Riduzione completata! Pronti per la fase di taglio")
      print("")
    return numero_billette
           
  def taglio (self, quantita_vergella):
    print("FASE DI TAGLIO")
    self.vergella_da_produrre = copy.deepcopy(quantita_vergella)
    quantita_vergella = self.vergella_da_produrre['VERGELLA']
    sezione_billetta_metri_quadri = (self.sezione_billetta**2) / 10**6
    volume_billetta = sezione_billetta_metri_quadri * LUNGHEZZA_BILLETTA
    sezione_prodotto = 3.14*(self.diametro_iniziale_billetta/1000)**2
    volume_prodotto = volume_billetta
    lunghezza_prodotto = volume_prodotto / sezione_prodotto
    print("Per ogni billetta ottenuto prodotto di lunghezza",lunghezza_prodotto,"metri")
    lunghezza_tot_prodotto = lunghezza_prodotto *NUMERO_BILLETTE_DA_LAVORARE
    print("Il lunghezza totale del prodotto da tagliare è di",lunghezza_tot_prodotto)
    print("Ogni matassa richiede",LUNGHEZZA_STANDARD_MATASSA,"metri")
    if self.diametro_ok == False:
      print("Impossibile inziare la fase di taglio")
      self.tagliata == False
    else:
      print("Taglio del prodotto....")
      time.sleep(20)
      while lunghezza_tot_prodotto > LUNGHEZZA_STANDARD_MATASSA and self.matasse_da_produrre < quantita_vergella:
        self.matasse_da_produrre += 1
        lunghezza_tot_prodotto -= LUNGHEZZA_STANDARD_MATASSA
      print("Processo di taglio completato!\nSi produrranno",self.matasse_da_produrre,"matasse")
      print("Eccedenza di",lunghezza_tot_prodotto,"metri usata per prossimo ciclo di produzione",".2f")
      self.tagliata = True
    return self.matasse_da_produrre
        
  def raffreddamento_ventilazione(self, matasse_da_preparare):
    print("FASE DI RAFFREDDAMENTO E VENTILAZIONE")
    if self.tagliata == False:
      print("Impossibile iniziare la fase di raffreddamento e ventilazione")
    else:
      temperatura_vergella = random.randint(850, 900)
      print("Raffreddamento e ventilazione del prodotto....")
      for _ in range (self.matasse_da_produrre):
          self.temperatura_forno -= random.randint(10, 20)
          matassa_da_formare = self.prossima_porzione
          matassa = Vergella(matassa_da_formare)
          print("Il prodotto tagliato n°",self.prossima_porzione,"ha raggiunto la temperatura ottimale di",temperatura_vergella,"°C")
          self.prossima_porzione += 1
          time.sleep(0.5)
          matassa.aggiornamento_stato_vergella("PRODOTTA")
      print("Raffreddamento e ventilazione completati\nInizio patentamento ad aria")
      self.temperatura_ok = True
    return matasse_da_preparare
  
  def patentamento_ad_aria(self, spire_completate):
    print("FASE DI PATENTAMENTO AD ARIA")
    if self.temperatura_ok == False:
      print("Impossibile iniziare il patentamento ad aria")
    else:
      for _ in range(self.matasse_da_produrre):
        spire = self.matassa_ok
        spire_completate = Vergella(spire)
        print("La porzione di vergella",self.matassa_ok,"ha formato le spire!")
        self.matassa_ok += 1
        self.spire_formate = True
        time.sleep(0.5)
      return spire_completate

  def confezionamento_stoccaggio(self, matasse_completate):
    print("FASE DI CONFEZIONAMENTO E STOCCAGGIO")
    if self.spire_formate == False:
      print("Impossibile iniziare la fase di confezionamento e stoccaggio")
    else:
      for i in range(self.matasse_da_produrre):
        fine_matassa = self.matassa_ok
        matassa = Vergella(fine_matassa)
        print("Matassa",self.matassa_completa,"entra nel pozzo rotante")
        time.sleep(0.5)
        print("Inizio rilegatura e pressatura....")
        print("Matassa RILEGATA E PRESSATA")
        time.sleep(0.5)
        self.matassa_formata = True
        print("Inizio stoccaggio...")
        time.sleep(1)
        print("Matassa COMPLETA E STOCCATA")
        print("-"*20)
        matasse_completate = self.matasse_da_produrre
        if i < matasse_completate - 1:
          print("In attesa della matassa",self.matassa_completa,"prima di iniziare con l'altra")
          self.matassa_completa += 1
      print(self.matassa_completa,"matasse completate e stoccate")
      print("FINE CICLO DI PRODUZIONE")
      return matasse_completate
    
    
LUNGHEZZA_FILO = 100      
LUNGHEZZA_TARGET_LONG = 5
LUNGHEZZA_TARGET_TRASV = 3
PASSO_LONG = 0.2
PASSO_TRASV = 0.2

class Rete_elettrosaldata:
  def __init__(self, id_rete):
    self.rete = id_rete
    self.stato = "....."
    self.lunghezza_trasversale = 0
    self.lunghezza_longitudinale = 0
    self.difetti = False
    self.qualita_superata = False
    
  def aggiornamento_stato_rete(self, nuovo_stato):
    self.stato = nuovo_stato
    print("Stato della rete",self.rete,":",nuovo_stato)
  
  def definisci_qualita_rete(self,qualita_superata):
    if qualita_superata:
      print("CONFORME")
    else:
      print("NON CONFORME")

class Produzione_rete_elettrosaldata:
  def __init__(self):
    self.metri_filo_disponibili = 0.0
    self.lunghezza_filo = 0
    self.lunghezza_filo_caricato = 0
    self.lunghezza_filo_giornaliera = 0
    self.carrello_vuoto = True
    self.bobina_svolta = False
    self.reti_da_produrre = {}
    self.reti_in_lavorazione = []
    self.reti_dopo_taglio = []
    self.reti_dopo_posizionamento = []
    self.contatore_reti_lavorate = 0
    self.contatore_reti_dopo_taglio = 0
    self.cont_reti_dopo_posizionamento = 0
    self.reti_prodotte = [] #Reti dopo la fine della lavorazione, prima dello stoccaggio
    self.pacchi_prodotti = 0
    self.reti_tot = 0 #Copia del numero di reti giornaliere
    self.reti_conformi = []
    self.reti_non_conformi = []
    self.problema_taglio = False
    self.problema_saldatura_punto = False
    self.problema_saldatura_totale = False
    
    
    
  def calcolo_filo_necessario(self, lunghezza_long, lunghezza_trasv, passo_long, passo_trasv):
    self.numero_fili_long = int(lunghezza_long / passo_long) + 1
    self.lunghezza_fili_long = self.numero_fili_long * lunghezza_long
    self.numero_fili_trasv = int(lunghezza_trasv / passo_trasv) + 1
    self.lunghezza_fili_trasv = self.numero_fili_trasv * lunghezza_trasv
    self.lunghezza_filo = self.lunghezza_fili_trasv + self.lunghezza_fili_long
    print("Filo necessario per la produzione di una rete:",self.lunghezza_filo,"metri")
    return self.lunghezza_filo, self.lunghezza_fili_long, self.lunghezza_fili_trasv
  
  def svolgitura_raddrizzatura(self,reti_giornaliere):
    print("FASE DI SVOLGITURA E RADDRIZZATURA")
    #Copia del valore delle reti da produrre giornalmente
    self.reti_da_produrre = copy.deepcopy(reti_giornaliere)
    self.reti_tot = self.reti_da_produrre['RETE ELETTROSALDATA']
    print("Si richiede di produrre",self.reti_tot,"reti elettrosaldate")
    time.sleep(5)
    #Calcolo della quantità di filo necessaria per produrre le reti giornaliere
    self.lunghezza_filo_giornaliera = self.lunghezza_filo * self.reti_tot
    print("Si richiede quindi di caricare",self.lunghezza_filo_giornaliera,"metri di filo")
    #Sapendo che una bobina di vergella è lunga 100 metri, andiamo a vedere quante bobine carichiamo per produrre le reti giornaliere
    bobine_caricate = 0
    print("Carico filo nell'impianto.....")
    while self.lunghezza_filo_caricato < self.lunghezza_filo_giornaliera:
      self.lunghezza_filo_caricato += 100
      bobine_caricate += 1
      filo_eccedente = self.lunghezza_filo_caricato - self.lunghezza_filo_giornaliera
      time.sleep(0.05)
    print("Caricamento completato!\nSono state caricate",bobine_caricate,"bobine per produrre le",self.reti_tot,"reti, per un totale di",self.lunghezza_filo_caricato,"metri")
    print("L'eccedenza di",filo_eccedente,"metri verrà usata per il prossimo ciclo di produzione")
    self.bobina_svolta = True
    for _ in range (self.reti_tot):
      self.contatore_reti_lavorate += 1
      nuova_rete = Rete_elettrosaldata(self.contatore_reti_lavorate)
      nuova_rete.aggiornamento_stato_rete("FILO CARICATO")
      self.reti_in_lavorazione.append(nuova_rete)
      time.sleep(0.2)    
    print("Pronti per la fase di taglio")
    self.reti_in_lavorazione = self.reti_tot
    return bobine_caricate, self.reti_tot, self.lunghezza_filo_caricato, self.reti_in_lavorazione
  
  def taglio_filo(self):
    print("FASE DI TAGLIO DEL FILO")
    if self.bobina_svolta == False:
      print("Impossibile iniziare la fase di taglio")
    else:
      estrazione_valore_trasversale = self.calcolo_filo_necessario(LUNGHEZZA_TARGET_LONG, LUNGHEZZA_TARGET_TRASV, PASSO_LONG, PASSO_TRASV)
      lunghezza_filo_trasv_rete = estrazione_valore_trasversale[1]
      print("Lunghezza del filo trasversale richiesto per ogni rete è di",lunghezza_filo_trasv_rete,"metri")
      print("Lunghezza trasversale filo per le bobine richieste:",lunghezza_filo_trasv_rete * self.reti_tot )
      for rete_corrente in range(self.reti_in_lavorazione):
        self.contatore_reti_dopo_taglio += 1
        rete_corrente = Rete_elettrosaldata(self.contatore_reti_dopo_taglio)
        problema_taglio = random.random() < 0.01
        self.lunghezza_filo_giornaliera -= lunghezza_filo_trasv_rete
        if problema_taglio:
          rete_corrente.aggiornamento_stato_rete("PROBLEMA TAGLIO")
          rete_corrente.definisci_qualita_rete(False)
          self.reti_non_conformi.append(rete_corrente)
        else:
          rete_corrente.aggiornamento_stato_rete("TAGLIO OK")
          self.reti_dopo_taglio.append(rete_corrente)
      print(self.lunghezza_filo_giornaliera)
      print("Reti che possono continuare la produzione:",len(self.reti_dopo_taglio))
      print("Reti scartate :",len(self.reti_non_conformi))
      self.reti_dopo_taglio = self.reti_tot
      return self.reti_dopo_taglio, self.reti_non_conformi
  
  def posizionamento(self):
    print("FASE DI POSIZIONAMENTO DEL FILO TRASVERSALE")
    if not self.taglio_filo:
      print("Impossibile iniziare posizionamento")
    else:
      self.cont_reti_dopo_posizionamento = 1
      self.cont_filo_posizionato = 0
      for rete_corrente in range(self.reti_dopo_taglio):
        rete_corrente = Rete_elettrosaldata(self.cont_reti_dopo_posizionamento)
        time.sleep(0.5)
        print("Posizionamento dei fili trasversali per la rete n°",self.cont_reti_dopo_posizionamento)
        for _ in range (self.numero_fili_trasv):
          self.cont_filo_posizionato += 1
        rete_corrente.aggiornamento_stato_rete("POSIZIONAMENTO FILO TRASVERSALE COMPLETATO")
        time.sleep(0.5)
        print("-"*30)
        self.cont_reti_dopo_posizionamento += 1
        self.reti_dopo_posizionamento.append(rete_corrente)
      print("Posizionamento di",self.numero_fili_trasv * self.reti_dopo_taglio," metri di filo completato")
      print("Pronti per la saldatura")
      self.reti_dopo_posizionamento = self.reti_tot
      return self.reti_dopo_posizionamento
        
  def saldatura(self):
    print("FASE DI SALDATURA")
    if not self.posizionamento:
      print("Impossibile iniziare la fase di saldatura")
    else:
      print("Reti da lavorare dopo il posizionamento:",self.reti_dopo_posizionamento)
      self.cont_reti_dopo_saldatura = 1
      self.cont_punti_incrocio = 0
      for rete_corrente in range(self.reti_dopo_posizionamento):
        rete_corrente = Rete_elettrosaldata(self.cont_reti_dopo_saldatura)
        numero_punti_incrocio = self.numero_fili_long * self.numero_fili_trasv
        print("Fusione punti di incrocio tra fili longitudinali e fili trasversali per la rete n°",self.cont_reti_dopo_saldatura)
        for _ in range(numero_punti_incrocio):
          self.problema_saldatura_punto = random.random() < 0.09
          self.cont_punti_incrocio += 1
          if self.problema_saldatura_punto == True:
            self.problema_saldatura_totale == True
          else:
            self.problema_saldatura_totale == False
        if self.problema_saldatura_totale == True:
          rete_corrente.aggiornamento_stato_rete("PROBLEMA SALDATURA")
          rete_corrente.definisci_qualita_rete(False)
          self.reti_non_conformi.append(rete_corrente)
          time.sleep(0.5)
          print("-"*30)
        else:
          rete_corrente.aggiornamento_stato_rete("SALDATURA OK")
          self.reti_conformi.append(rete_corrente)
          time.sleep(0.5)
          print("-"*30)
        self.cont_reti_dopo_saldatura += 1
      self.reti_conformi = self.reti_tot
      print("Saldatura completata!\nReti non conformi:",len(self.reti_non_conformi),"\nReti totali conformi per il taglio finale:",self.reti_tot)
      return self.reti_non_conformi, self.reti_tot
    
  def taglio_finale(self):
    print("FASE DI TAGLIO FINALE")
    estrazione_valore_longitudinale = self.calcolo_filo_necessario(LUNGHEZZA_TARGET_LONG, LUNGHEZZA_TARGET_TRASV, PASSO_LONG, PASSO_TRASV)
    lunghezza_filo_long_rete = estrazione_valore_longitudinale[2]
    print("La lunghezza del filo longitudinale per ogni rete è di",lunghezza_filo_long_rete,"metri") 
    self.contatore_reti_dopo_taglio_finale = 0
    for rete_corrente in range(self.reti_tot):
      self.contatore_reti_dopo_taglio_finale += 1
      rete_corrente = Rete_elettrosaldata(self.contatore_reti_dopo_taglio_finale)
      problema_taglio_finale = random.random() < 0.01
      self.lunghezza_filo_giornaliera -= lunghezza_filo_long_rete
      if problema_taglio_finale:
        rete_corrente.aggiornamento_stato_rete("PROBLEMA TAGLIO")
        rete_corrente.definisci_qualita_rete(False)
        self.reti_non_conformi.append(rete_corrente)
        time.sleep(0.5)
        print("-"*30)
      else:
        rete_corrente.aggiornamento_stato_rete("TAGLIO OK")
        rete_corrente.definisci_qualita_rete(True)
        self.reti_prodotte.append(rete_corrente)
        time.sleep(0.5)
        print("-"*30)
    print("Taglio finale completato!\nNumero totali di reti pronte per lo stoccaggio:\t",len(self.reti_prodotte))
    print("Filo rimanente:\t",self.lunghezza_filo_giornaliera)
    return self.reti_prodotte, self.lunghezza_filo_giornaliera
      
  def stoccaggio(self):
    print("FASE DI STOCCAGGIO")
    if not self.taglio_finale:
      print("Impossibile inziare la fase di stoccaggio!")
    else:
      tempo_stoccaggio = random.randint(5,10)
      reti_residue = len(self.reti_prodotte)
      print("Inizio fase di stoccaggio")
      while reti_residue >= PACCO_STOCCATO:
        self.pacchi_prodotti += 1
        reti_residue -= PACCO_STOCCATO  
        print("Preparazione pacco. . . .\nPacco n°",self.pacchi_prodotti,"stoccato\nContiene",PACCO_STOCCATO,"reti elettrosaldate.")
        print("")
        time.sleep(tempo_stoccaggio)       
      print("Stoccaggio completato! Sono stati ultimati",self.pacchi_prodotti,"pacchi di billette.")
      if reti_residue > 0:
        time.sleep(tempo_stoccaggio)
        print("Sono rimaste",reti_residue,"reti elettrosaldate con le quali è stato prodotto un ultimo pacco")
      pacchi_totali_stoccati += 1
      print("In totale sono quindi stati stoccati",pacchi_totali_stoccati,"pacchi")
      
   
print("*"*100)
print("SIMULAZIONE DEL CICLO DI PRODUZIONE DI 3 PRODOTTI DEL GRUPPO PITTINI: BILLETTA, FASCIO DI VERGELLA, RETE ELETTROSALDATA")
print("*"*100)


PRODUZIONE_BILLETTA = 1
PRODUZIONE_VERGELLA = 2
PRODUZIONE_RETE_ELETTROSALDATA = 3
ESCI_DAL_PROGRAMMA = 4

def viualizza_menu():
  print("Selezionare una delle seguenti opzioni di simulazione:")
  print("1. Produzione billetta")
  print("2. Produzione vergella")
  print("3. Rete elettrosaldata")
  
def main():
  prodotti_della_simulazione = ['BILLETTA', 'VERGELLA', 'RETE ELETTROSALDATA'] #Creazione della lista dei 3 prodotti con i quali si è sviluppata la simulazione
  time.sleep(20)
  quantita = genera_quantita_produzione(prodotti_della_simulazione)
  time.sleep(20)
  parametri = generazione_parametri_di_produzione(prodotti_della_simulazione)
  time.sleep(20)
  calcola_tempo_totale_produzione( parametri, quantita)
  
  scelta = 0
  while scelta != ESCI_DAL_PROGRAMMA:
    viualizza_menu()
    scelta = int(input("-------->\t"))
    if scelta == PRODUZIONE_BILLETTA:
      print("")
      print("--------------INIZIO SIMULAZIONE CICLO DI PRODUZIONE DELLA BILLETTA------------")
      print("")
      billetta = Produzione_billetta()
      billetta.carica_forno()
      print("")
      billetta.fusione_forno()
      print("")
      billetta.colata_continua()
      print("")
      billetta.raffreddamento()
      print("")
      billetta.taglio_e_controllo_qualita(quantita)
      print("")
      billetta.stoccaggio()
      print("")
      print("-------------FINE DEL PROCESSO DI PRODUZIONE!-------------")
    elif scelta == PRODUZIONE_VERGELLA:
      print("")
      print("--------------INIZIO SIMULAZIONE CICLO DI PRODUZIONE DELLA VERGELLA------------")
      print("")
      numero_billette = NUMERO_BILLETTE_DA_LAVORARE
      vergella = Produzione_vergella()
      vergella.preriscaldo(numero_billette)
      print("")
      vergella.riduzione_verticale_orizzontale(numero_billette)
      print("")
      vergella.taglio(quantita)
      print("")
      vergella.raffreddamento_ventilazione(quantita)
      print("")
      vergella.patentamento_ad_aria(quantita)
      print("")
      vergella.confezionamento_stoccaggio(quantita)
    elif scelta == PRODUZIONE_RETE_ELETTROSALDATA:
      print("")
      print("--------------INIZIO SIMULAZIONE CICLO DI PRODUZIONE DELLA RETE ELETTROSALDATA------------")
      print("")
      rete_elettrosaldata = Produzione_rete_elettrosaldata()
      rete_elettrosaldata.calcolo_filo_necessario(LUNGHEZZA_TARGET_LONG, LUNGHEZZA_TARGET_TRASV, PASSO_LONG, PASSO_TRASV)
      print("")
      rete_elettrosaldata.svolgitura_raddrizzatura(quantita)
      print("")
      rete_elettrosaldata.taglio_filo()
      print("")
      rete_elettrosaldata.posizionamento()
      print("")
      rete_elettrosaldata.saldatura()
      print("")
      rete_elettrosaldata.taglio_finale()
      print("")
      rete_elettrosaldata.stoccaggio()
     
main()


    
  


    
      






    
    


    
    