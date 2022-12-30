import tkinter
ladje = [2, 3, 3, 4, 5]
stladje = 4

# A is between B and C
#
def between(a,b,c):
  return (b < a < c) or (c < a < b)

def inclusive(a,b,c):
  return (b <= a <= c) or (c <= a <= b)

class Knofek:
  def __init__(self, x, y, button,frame):
    self.x = x
    self.y = y
    self.tkButton = button
    self.tkFrame = frame
    self.stanje = 0

  def klik(self):
    self.tkButton.configure(highlightbackground="black")
    iskanjeladjice(self.x, self.y)
  
  def ugasn(self):
    print ("goaa")
    

  def risiLadjico(self):
    global stladje
    global i
    for y in range(10):
      for x in range(10):
        t = tabela[y][x]
        if inclusive(y ,self.drugiKonec.y, self.y) and inclusive(x, self.drugiKonec.x, self.x):
          t.tkButton.configure(highlightbackground="black", state = tkinter.DISABLED)
          t.stanje = i
        elif t.stanje != 0:
          pass
        else:
          t.tkButton.configure(
            state = tkinter.NORMAL,
            highlightbackground = "white",
            command = t.klik)
    stladje = stladje - 1
    i = ladje[stladje] - 1
    if stladje == -1:
      for y in range(10):
        for x in range(10):
          tabela[y][x].tkButton.configure(state = tkinter.DISABLED)


okno = tkinter.Tk()
okno.geometry("1920x1280")

tabela = []
for y in range(10):
  tabela.append([])
  for x in range(10):
    frame = tkinter.Frame(okno, width=40, height=40)
    button = tkinter.Button(frame, highlightbackground="white")
    pametniKnofek = Knofek(x,y,button,frame)
    button.configure(command=pametniKnofek.klik)
    tabela[y].append(pametniKnofek)
    frame.grid_propagate(False)
    frame.columnconfigure(0, weight=1)
    frame.rowconfigure(0,weight=1)
    frame.grid(row=y, column=x)
    button.grid(sticky="wens")

i = ladje[stladje] - 1
def iskanjeladjice(l_x, l_y):
  for y in range(10):
    for x in range(10):
      t = tabela[y][x]
      krizanje = False
      t.tkButton.configure(state = tkinter.DISABLED)
      if (t.x == l_x + i and t.y == l_y) \
          or (t.x == l_x - i and t.y == l_y) \
          or (t.y == l_y + i and t.x == l_x) \
          or (t.y == l_y - i and t.x == l_x):

        
        for vy in range(10):
          for vx in range(10):
            if (inclusive(vx,t.x,l_x)) and (inclusive(vy,t.y,l_y)) and (tabela[vy][vx].stanje != 0):
              krizanje = True

        if not krizanje:
          t.drugiKonec = tabela[l_y][l_x]
          t.tkButton.configure(highlightbackground="grey",command=t.risiLadjico, state = tkinter.NORMAL)

okno.mainloop()


