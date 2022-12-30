import tkinter
ladje = [2, 3, 3, 4, 5] #ustvari seznam ladij in njihovih dolžin
stladje = 4 #število ladje (uporabljeno pri postavljanju)
stladje_racunalnik = 4 #število ladje računalnika (uporabljeno pri generaciji ladij na računalnikovi strani)

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
    if stladje == -1:  
      for y in range(10): 
        for x in range(10):
          tabela[y][x].tkButton.configure(state = tkinter.DISABLED)
          tabela_racunalnik[y][x].tkButton.configure(state = tkinter.NORMAL)

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

i = ladje[stladje] - 1
#funkcija, ki poišče, kje se pojavijo gumbi za risanje ladjice, ko pritisnemo poljuben gumb
#med fazo postavljanja ladjic
def iskanjeladjice(l_x, l_y, kje): #kje je uporabljeno, da lahko isto funkcijo uporabi tudi računalnik
  for y in range(10):
    for x in range(10):
      t = kje[y][x]
      krizanje = False
      t.tkButton.configure(state = tkinter.DISABLED)
      #pogleda, če je na pravilnem mestu
      if (t.x == l_x + i and t.y == l_y) \
          or (t.x == l_x - i and t.y == l_y) \
          or (t.y == l_y + i and t.x == l_x) \
          or (t.y == l_y - i and t.x == l_x):

        #pogleda, če je med začetnim gumbom in gumbom, ki bi se rad pojavil že kakšen gumb, katerega stanje
        #ni enako 0 (ima že ladjico na sebi)
        for vy in range(10):
          for vx in range(10):
            if (inclusive(vx,t.x,l_x)) and (inclusive(vy,t.y,l_y)) and (tabela[vy][vx].stanje != 0):
              krizanje = True

        #če se ne križa s katerokoli ladjico in so prejšnji pogoji izpolnjeni, se bo pobarval sivo
        if not krizanje:
          t.drugiKonec = tabela[l_y][l_x]
          t.tkButton.configure(highlightbackground="grey",command=t.risiLadjico, state = tkinter.NORMAL)

okno.mainloop()


