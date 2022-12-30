import tkinter
import random
ladje = [0, 2, 3, 3, 4, 5] #ustvari seznam ladij in njihovih dolžin
ladje_racunalnik = [0, 2, 3, 3, 4, 5]
stladje = 5 #število ladje (uporabljeno pri postavljanju)
stladje_racunalnik = 5 #število ladje računalnika (uporabljeno pri generaciji ladij na računalnikovi strani)
i = 4
i_racunalnik = 4


#funkcija, ki pogleda, če je določeno število med dvema drugima številoma (uporabljena pri postavljanju ladjic)
def inclusive(a,b,c):
  return (b <= a <= c) or (c <= a <= b)

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
    self.tkButton.configure(highlightbackground="yellow")
    
#funkcija, ki nariše ladjico po tem, ko si izberemo, kam jo bomo postavili
  def risiLadjico(self):
    global stladje
    global i
    for y in range(10):
      for x in range(10):
        t = tabela[y][x]
        if inclusive(y ,self.drugiKonec.y, self.y) and inclusive(x, self.drugiKonec.x, self.x): #če se x in y določenega gumba nahaja med prej izbranima x in y koordinata,
          t.tkButton.configure(highlightbackground="black", state = tkinter.DISABLED) # se pobarva črno in izklopi
          t.stanje = i #spremeni stanje (s tem vemo, katera vrsta ladje je na njem)
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
      for y in range(10): 
        for x in range(10):
          tabela[y][x].tkButton.configure(state = tkinter.DISABLED)
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
        tabela_racunalnik[y][x].tkButton.configure(highlightbackground = "black")
        tabela_racunalnik[y][x].stanje = stladje_racunalnik

#FUNKCIJA, KI SI IZMISLE POZICIJO ZA LADJO RACUNALNIKA
def izmisljotina():
  global stladje
  global stladje_racunalnik
  global i_racunalnik
  print("bruh")
  while stladje_racunalnik != 0:
    katera_bo = random.randint(0, 1)
    naklucn_x = random.randrange(0, 9)
    naklucn_y = random.randrange(0, 9)
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


