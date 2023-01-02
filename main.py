import tkinter
import random

ladje = [0, 2, 3, 3, 4, 5] #ustvari seznam ladij in njihovih dolžin
ladje_racunalnik = [0, 2, 3, 3, 4, 5]
stladje = 5 #število ladje (uporabljeno pri postavljanju)
stladje_racunalnik = 5 #število ladje računalnika (uporabljeno pri generaciji ladij na računalnikovi strani)
i = 4
i_racunalnik = 4
ze_ciljane = []
seznamus = []
x_origin = 0
y_origin = 0
zadete = []
potopljena = False
vrsteLadij = ["","Minolovca", "Podmornico", "Fregato","Križarko","Bojno Ladjo"]

#funkcija, ki pogleda, če je določeno število med dvema drugima številoma (uporabljena pri postavljanju ladjic)
def inclusive(a,b,c):
  return (b <= a <= c) or (c <= a <= b)

def ugasn_vse(kje):
    for y in range(10):
      for x in range(10):
        kje[y][x].tkButton.configure(state = tkinter.DISABLED)

def przgi_vse(kje):
  for y in range(10):
      for x in range(10):
        if kje[y][x].stanje >= 0:
          kje[y][x].tkButton.configure(state = tkinter.NORMAL)

def streljaj(y_koord, x_koord):
  global potopljena
  global zadete
  global ze_ciljane
  t = tabela[y_koord][x_koord]
  grogor = t.stanje
  ze_ciljane.append((x_koord, y_koord))
  if t.stanje > 0:
    t.tkButton.configure(highlightbackground="orange")
    ladje[grogor] -= 1
    t.stanje *= (-1)
    zadete.append((y_koord, x_koord))
    if ladje[grogor] == 0:
      for y in range(10):
        for x in range(10):
          if tabela[y][x].stanje == -grogor:
            tabela[y][x].tkButton.configure(highlightbackground="red")
            tabela[y][x].stanje = -98
            zadete.remove((y,x))
      potopljena = True
      napis.set("Računalnik je potopil %s!" %vrsteLadij[grogor])
    if sum(ladje) == 0:
      ugasn_vse(tabela)
      ugasn_vse(tabela_racunalnik)
      napis.set("Zgubil si!")
      return
  else:
    t.stanje = -99
    t.tkButton.configure(highlightbackground="blue")
 

def nakljucna_koordinata():
  global ze_ciljane
  global x_origin
  global y_origin
  nism_nasu = True
  while nism_nasu:
    x_origin = random.randrange(10)
    y_origin = random.randrange(10)
    t = tabela[y_origin][x_origin]
    if (x_origin, y_origin) not in ze_ciljane:
      nism_nasu = False


def ideja():
  global seznamus
  global x_origin
  global y_origin
  global potopljena
  global zadete
  if potopljena and zadete:
    (y_origin, x_origin) = zadete[0]
    seznamus.extend([(x_origin + 1, y_origin, +1, 0), (x_origin - 1, y_origin, -1, 0) , (x_origin, y_origin + 1, 0, +1), (x_origin, y_origin - 1, 0, -1)])
    potopljena == False
  while seznamus:
    (x, y, dx, dy) = seznamus.pop(0)
    if inclusive(x, 0, 9) and inclusive(y, 0, 9) \
      and ((x, y) not in ze_ciljane):
      if (tabela[y][x].stanje > 0 or inclusive(tabela[y][x].stanje, -5, -1 )):
        if inclusive(tabela[y][x].stanje, -5, -1 ):
          seznamus.insert(0, (x+dx*2,y+dy*2,dx,dy))
        else:
          seznamus.insert(0, (x+dx,y+dy,dx,dy))
      return (y, x)
  else:
    nakljucna_koordinata()
    if tabela[y_origin][x_origin].stanje > 0:
      seznamus.extend([(x_origin + 1, y_origin, +1, 0), (x_origin - 1, y_origin, -1, 0) , (x_origin, y_origin + 1, 0, +1), (x_origin, y_origin - 1, 0, -1)])
      potopljena = False
    return (y_origin, x_origin) 
    
  

def racunalnik_cilja():
  global x_origin
  global y_origin
  global ze_ciljane
  global ladje
  (y, x) = ideja()
  streljaj(y, x)
    
  

#class knofek z vsemi podatki, ki jih mora vsak posamezen gumb imeti
class Knofek:
  def __init__(self, x, y, button,frame):
    self.x = x
    self.y = y
    self.tkButton = button
    self.tkFrame = frame
    self.stanje = 0

#funkcija, ki se izvede v primeru, da kliknemo na gumb na naši strani (uporabljena za postavljanje ladic)
  def klik(self):
    self.tkButton.configure(highlightbackground="black")
    iskanjeladjice(self.x, self.y, tabela)

  
#funkcija, ki se izvede v primeru, da kliknemo na gumb na računalnikovi strani (uporabljena za streljanje na ladjice)
  def klik_racunalnik(self):
    global ladje_racunalnik
    ugasn_vse(tabela_racunalnik)
    if self.stanje > 0:
      grogor = self.stanje
      self.tkButton.configure(highlightbackground="orange")
      ladje_racunalnik[self.stanje] -= 1
      self.stanje *= (-1)
      if ladje_racunalnik[self.stanje*(-1)] == 0:
        for y in range(10):
          for x in range(10):
            if tabela_racunalnik[y][x].stanje == self.stanje:
              tabela_racunalnik[y][x].tkButton.configure(highlightbackground="red")
        napis.set("Igralec je potopil %s!" %vrsteLadij[grogor])
      if sum(ladje_racunalnik) == 0:
        ugasn_vse(tabela)
        ugasn_vse(tabela_racunalnik)
        napis.set("Zmagal si!")
        return
    else:
      self.stanje = -99
      self.tkButton.configure(highlightbackground="blue")
    racunalnik_cilja()
    przgi_vse(tabela_racunalnik)
    
#funkcija, ki nariše ladjico po tem, ko si izberemo, kam jo bomo postavili
  def risiLadjico(self):
    global napis
    global stladje
    global i
    for y in range(10):
      for x in range(10):
        t = tabela[y][x]
        if inclusive(y ,self.drugiKonec.y, self.y) and inclusive(x, self.drugiKonec.x, self.x): #če se x in y določenega gumba nahaja med prej izbranima x in y koordinata,
          t.tkButton.configure(highlightbackground="black", state = tkinter.DISABLED) # se pobarva črno in izklopi
          t.stanje = stladje #spremeni stanje (s tem vemo, katera vrsta ladje je na njem)
        elif t.stanje != 0: #v primeru da ima gumb že nastavljeno stanje, mu nič ne spremeni
          pass
        else: #vse gumbe, ki jih nismo pobarvali, nastavi nazaj na normalno
          t.tkButton.configure(
            state = tkinter.NORMAL,
            highlightbackground = "white",
            command = t.klik)
    stladje = stladje - 1 #spremeni spremenljivke, s katerimi vemo, katero ladjo postavljamo
    i = ladje[stladje] - 1
    #v primeru da so vse ladje postavljene, se vsi gumbi na naši strani izklopijo,
    #vsi na računalnikovi strani pa vklopijo
    if stladje == 0:  
      ugasn_vse(tabela)
      napis.set("Streljaj!")
      for y in range(10):
        for x in range(10):
          tabela_racunalnik[y][x].tkButton.configure(state = tkinter.NORMAL)

#pogleda, če je med začetnim gumbom in gumbom, ki bi se rad pojavil že kakšen gumb, katerega stanje
#ni enako 0 (ima že ladjico na sebi)
def a_se_kriza(x_1, x_2, y_1, y_2, kje):
  krizanje = False
  for vy in range(10):
    for vx in range(10):
      if (inclusive(vx, x_1 , x_2)) and (inclusive(vy, y_1, y_2)) and (kje[vy][vx].stanje != 0):
        krizanje = True
  return krizanje


def racunalnikRiseLadjico(x_1, x_2, y_1, y_2):
  global stladje_racunalnik
  for y in range(10):
    for x in range(10):
      if inclusive(y ,y_2, y_1) and inclusive(x, x_2, x_1):
        #tabela_racunalnik[y][x].tkButton.configure(highlightbackground = "black")
        tabela_racunalnik[y][x].stanje = stladje_racunalnik

#FUNKCIJA, KI SI IZMISLE POZICIJO ZA LADJO RACUNALNIKA
def izmisljotina():
  global stladje
  global stladje_racunalnik
  global i_racunalnik
  while stladje_racunalnik != 0:
    katera_bo = random.randint(0, 1)
    naklucn_x = random.randrange(10)
    naklucn_y = random.randrange(10)
    if katera_bo == 0:
      drugi_x = naklucn_x + i_racunalnik
      drugi_y = naklucn_y
    else:
      drugi_y = naklucn_y + i_racunalnik
      drugi_x = naklucn_x
    if drugi_y > 9 or drugi_x > 9:
      continue
    
    if not a_se_kriza(naklucn_x, drugi_x, naklucn_y, drugi_y, tabela_racunalnik):
      racunalnikRiseLadjico(naklucn_x, drugi_x, naklucn_y, drugi_y)
      stladje_racunalnik = stladje_racunalnik - 1
      i_racunalnik = ladje_racunalnik[stladje_racunalnik] - 1

#ustvari glavno okno
okno = tkinter.Tk()
okno.geometry("1920x1280")
okno.title("Potapljanje Ladjic")

#GENERACIJA IGRALČEVIH GUMBOV
tabela = []
for y in range(10):
  tabela.append([])
  for x in range(10):
    frame = tkinter.Frame(okno, width=40, height=40)
    button = tkinter.Button(frame, highlightbackground="white")
    pametniKnofek = Knofek(x,y,button,frame)
    button.configure(command=pametniKnofek.klik)
    tabela[y].append(pametniKnofek)
    #koda ukradena iz stackoverflowa, ki naredi kvadraten gumb
    frame.grid_propagate(False)
    frame.columnconfigure(0, weight=1)
    frame.rowconfigure(0,weight=1)
    frame.grid(row=y, column=x)
    button.grid(sticky="wens")

#frame, ki loči naše in računalnikove gumbe
vmesno = tkinter.Frame(okno, width = 100, height = 400).grid(column = 10, row = 0, rowspan = 10)

#GENERACIJA RAČUNALNIKOVIH GUMBOV
tabela_racunalnik = []
for y in range(10):
  tabela_racunalnik.append([])
  for x in range(10):
    frame = tkinter.Frame(okno, width=40, height=40)
    button = tkinter.Button(frame, highlightbackground="white")
    neumniKnofek = Knofek(x,y,button,frame)
    button.configure(command=neumniKnofek.klik_racunalnik, state = tkinter.DISABLED)
    tabela_racunalnik[y].append(neumniKnofek)
    frame.grid_propagate(False)
    frame.columnconfigure(0, weight=1)
    frame.rowconfigure(0,weight=1)
    frame.grid(row=y, column=x+11)
    button.grid(sticky="wens")
izmisljotina()

napis = tkinter.StringVar()
label = tkinter.Label(okno, textvariable = napis, height = 1, font = ("Arial", 24)).grid(row = 11, column = 21)
napis.set("Postavi svoje ladje!")

#funkcija, ki poišče, kje se pojavijo gumbi za risanje ladjice, ko pritisnemo poljuben gumb
#med fazo postavljanja ladjic
def iskanjeladjice(l_x, l_y, kje): #kje je uporabljeno, da lahko isto funkcijo uporabi tudi računalnik
  for y in range(10):
    for x in range(10):
      t = kje[y][x]
      t.tkButton.configure(state = tkinter.DISABLED)
      #pogleda, če je na pravilnem mestu
      if (t.x == l_x + i and t.y == l_y) \
          or (t.x == l_x - i and t.y == l_y) \
          or (t.y == l_y + i and t.x == l_x) \
          or (t.y == l_y - i and t.x == l_x):

        #če se ne križa s katerokoli ladjico in so prejšnji pogoji izpolnjeni, se bo pobarval sivo
        if not a_se_kriza(t.x, l_x, t.y, l_y, tabela):
          t.drugiKonec = tabela[l_y][l_x]
          t.tkButton.configure(highlightbackground="grey",command=t.risiLadjico, state = tkinter.NORMAL)





okno.mainloop()


