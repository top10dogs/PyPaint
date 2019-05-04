from tkinter import *
from PIL import Image, ImageTk, ImageGrab, ImageFilter
from tkinter.colorchooser import *
from tkinter import filedialog
from random import *


# 01/05/2019
# PyPaint v1.2

# !! Les icones sont dans le dossier IcônePyPaint !!

# Fonctionnalités actuelles:
# - pinceau + changement de l'epaisseur avec molette
# - on peut creer des formes rectangles et ovales ainsi que des lignes
# - et on peut choisir la couleur du contour et du remplissage
# - on peut changer la couleur de l'outil
# - on peut ouvrir des images de notre ordinateur
# - on peut revenir en arrière (même pour les filtres)
# - on peut sauvegarder son dessin en format png ou jpg
# - on peut ajouter des filtres comme un flou ou une pixellisation et regler sa valeur
# - on peut utiliser un pot de peinture
# - on peut redimmensionner le canvas du dessin

# Changements:
# - La méthode de placement des frames dans la frame outil a changé
# - Certaines variables globales ont été supprimées afin de ne pas poser probleme avec des variables locales.
# - Toutes les outils utilisent la même fonction pour être choisie.
# - Il y'a desormais des icones pour les outils
# - On a le choix entre 10 couleurs predefinies

# Problèmes:
# - Lorsqu'on met un effet et qu'on veut en remettre un le canvas dessin enleve l'effet précedent



def quit(e=None):
    fen.destroy()


def screen():
    x0 = fen.winfo_rootx() + dessin.winfo_x()
    y0 = fen.winfo_rooty() + dessin.winfo_y()
    x1 = x0 + dessin.winfo_width()
    y1 = y0 + dessin.winfo_height()
    im = ImageGrab.grab((x0, y0, x1, y1))
    return im


def save(e=None):  # fonction test pour enregistrer les canvas en png (experimentale)
    imagepath = filedialog.asksaveasfilename(defaultextension="",
                                             filetypes=[("PNG(*.png)", "*.png"), ("JPEG(*.jpg;*.jpeg;*.jpe;*.jfif)", "*.jpg;*.jpeg;*.jpe;*.jfif"), ("Tous les fichiers", "*")])
    if imagepath != "":
        item = screen().save(imagepath)
        items.append(item)


def suppr(e=None):  # fonction qui reintialise toutes les variables lorqu'on click sur nouveau
    dessin.delete(ALL)
    w = 600
    h = 400
    dessin.config(width=w, height=h)


def openimage(e=None):  # fonction qui va vous demander d'ouvrir une image sur votre ordinateur
    global photo, w, h
    basewidth = 700
    filename = filedialog.askopenfilename(parent=fen, filetypes=[("PNG(*.png)", "*.png"), ("JPEG(*.jpg;*.jpeg;*.jpe;*.jfif)", "*.jpg;*.jpeg;*.jpe;*.jfif"), ("Tous les fichiers", "*")])
    if filename != "":
        suppr()
        im = Image.open(filename)
        w, h = im.size
        if w > 1000 or h > 800:  # si votre image est trop grande, on calcule la hauteur de limage en definissant
            w = basewidth
            wpercent = (w / float(im.size[0]))
            h = int((float(im.size[1]) * float(wpercent)))
            im = im.resize((w, h), Image.ANTIALIAS)
        photo = ImageTk.PhotoImage(im)
        dessin.config(width=w, height=h)
        dessin.create_image(w / 2, h / 2 -1, image=photo)


def undo(e=None):  # fonction qui supprime le dernier element de la liste items en retournant sa valeur
    if items:
        last = items.pop()
        if type(last) is list:
            for i in range(0, len(last)):
                dessin.delete(last[i])  # on supprime cette item du canvas dessin (ne fonctionne pas pour le pinceau
        else:
            dessin.delete(last)


def wheel(event):  # fonction qui permet de regler l'epaisseur du trait avec la molette
    global epaisseur
    if event.delta > 0 and epaisseur < 50:
        epaisseur += 1
    elif event.delta < 0 and epaisseur > 1:
        epaisseur -= 1
    rond = dessin.create_oval(event.x - epaisseur / 2, event.y - epaisseur / 2,
                              event.x + epaisseur / 2, event.y + epaisseur / 2, width=1)
    dessin.after(50, dessin.delete, rond)
    s.set(epaisseur)


def scale(val):  # fonction qui permet de changer lepaisseur avec une reglette
    global epaisseur
    epaisseur = int(val)


def pinceaul(e):  # fonction qui va commencer a dessiner le trait
    global lastx, lasty
    lastx, lasty = e.x, e.y
    dessin.bind("<B1-Motion>", lambda event: pinceau(event, "1"))


def pinceau2(e):
    global lastx, lasty
    dessin.bind("<B3-Motion>", lambda event: pinceau(event, "2"))
    lastx, lasty = e.x, e.y


def pinceau(e, outil):  # fonction qui va dessiner lorqu'on bouge la souris
    global lastx, lasty, epaisseur, ligne
    x, y = e.x, e.y
    if outil == "1":
        couleur = color
    elif outil == "2":
        couleur = color2
    item = dessin.create_line((lastx, lasty, x, y), width=epaisseur, capstyle="round", smooth=True, fill=couleur)
    ligne.append(item)
    lastx, lasty = x, y
    status["text"] = (e.x, e.y)


def mousedown(e, forme):  # fonction qui va creer un rectangle au point ou se trouve la souris
    global item
    firstx, firsty = e.x, e.y
    dessin.bind("<B1-Motion>", lambda event: mousemove(event, firstx, firsty))
    if forme == bouton_rectangle:
        item = dessin.create_rectangle(firstx, firsty, firstx, firsty, outline=color, width=epaisseur)
    elif forme == bouton_oval:
        item = dessin.create_oval(firstx, firsty, firstx, firsty, outline=color, width=epaisseur)
    elif forme == bouton_ligne:
        item = dessin.create_line(firstx, firsty, firstx, firsty, width=epaisseur, capstyle="round", smooth=True,
                                  fill=color)

    if b3["relief"] == SUNKEN:
        dessin.itemconfig(item, fill=color2)

    if b2["relief"] == RAISED and active_button != bouton_ligne:
        dessin.itemconfig(item, outline="")


def mousemove(e, firstx, firsty):  # fonction qui va changer les coordonnees du rectangle pour quil suive la souris
    dessin.coords(item, firstx, firsty, e.x, e.y)


def texte(e): #fonction texte
    item = Entry(dessin, bd = 0, fg = color)
    item.place(x = e.x, y = e.y)


def graph(event):  # fonction aerograph
    global ligne
    for i in range(0, 18):
        rand_posx = event.x + randint(-10, 10)
        rand_posy = event.y + randint(-10, 10)
        item = dessin.create_rectangle(rand_posx, rand_posy, rand_posx + 1, rand_posy + 1, outline=color, width=1)
        ligne.append(item)


def release(e):  # fonction qui place litem dessiné dans la liste items lorqu'on lache le bouton 1
    global ligne
    if active_button == bouton_pinceau or active_button == bouton_graph or active_button == bouton_pot and ligne:
        items.append(ligne)
        ligne = []
    elif active_button != bouton_pinceau and item:
        items.append(item)


def useoutil(outil):  # fonction qui va definir la forme ou loutil selon le bouton actionne
    dessin.unbind("<MouseWheel>")
    dessin.unbind("<Button-1>")
    dessin.unbind("<B1-Motion>")
    activatebutton(outil)
    s.config(state = NORMAL)
    if outil == bouton_oval or outil == bouton_rectangle:
            b2.config(state = NORMAL)
            b3.config(state=NORMAL)
    else:
        b2.config(state=DISABLED)
        b3.config(state=DISABLED)
    if outil == bouton_rectangle:
        status.config(text="Outil Rectangle")
        dessin.bind("<Button-1>", lambda event:mousedown(event, outil))
    elif outil == bouton_oval:
        status.config(text="Outil Cercle")
        dessin.bind("<Button-1>", lambda event:mousedown(event, outil))
    elif outil == bouton_ligne:
        b2.config(state = DISABLED, relief  = SUNKEN)
        b3.config(state = DISABLED, relief = RAISED)
        status.config(text="Outil Ligne")
        dessin.bind("<Button-1>", lambda event:mousedown(event, outil))
    elif outil == bouton_pinceau:
        status.config(text="Outil Pinceau")
        dessin.bind("<Button-1>", pinceaul)
        dessin.bind("<MouseWheel>", wheel)
        dessin.bind("<Button-3>", pinceau2)
    elif outil == bouton_texte:
        dessin.bind("<Button-1>", texte)
        status.config(text="Outil Texte (Double clickez pour entrer du texte)")
    elif outil == bouton_graph:
        status.config(text="Outil Graph")
        dessin.bind("<B1-Motion>", graph)
        dessin.unbind("<Button-1>")
    elif outil == bouton_pot:
        status.config(text="Outil Pot de peinture")
        dessin.bind("<Button-1>", pot2)
    elif outil == bouton_pipette:
        status.config(text="Outil Pipette")
        dessin.bind("<Button-1>", pipette)
    if b2["relief"] !=SUNKEN and outil != bouton_pinceau:
        s.config(state = DISABLED)


def activatebutton(button):  # fonction qui va changer laffichage du bouton actionne
    global active_button
    active_button.config(relief=RAISED)
    button.config(relief=SUNKEN)
    active_button = button




def filter(effect):  # fonction qui va creer une fenetre gerant les filtres
    global photoprev
    im2 = screen()
    photoprev = ImageTk.PhotoImage(im2)

    window = Toplevel(fen)

    canvas_photo = Canvas(window, width=200, height=200)
    canvas_photo.pack(side=TOP)

    preview = canvas_photo.create_image(200/2, 200/2, image = photoprev )

    ss = Scale(window, orient='horizontal', to=10, length=250, command=lambda val: scalefilter(val, im2, canvas_photo, effect, preview))

    if effect == "flou":
        ss.config(resolution = 0.5)
        ss.set(0)
        window.title("Flou Gaussien")
    elif effect == "pixel":
        ss.config(resolution=1, from_= 200)
        ss.set(200)
        window.title("Pixellisation")

    ss.pack()
    bbbb = Button(window, text="Ok", command = lambda:boutonfilter(window))
    bbbb.pack(side=BOTTOM)


def boutonfilter(window):
    item = dessin.create_image(dessin.winfo_width() / 2, dessin.winfo_height() / 2, image=photoprev)
    items.append(item)
    window.destroy()


def scalefilter(val, im2, canvas_photo, effect, preview): #fonction qui va changer la previsualisation du filtre
    global photoprev, imgprev
    if effect == "flou":
        imgprev = im2.filter(ImageFilter.GaussianBlur(radius=float(val)))
        photoprev = ImageTk.PhotoImage(imgprev)

    elif effect == "pixel":
        imgprev = im2.resize((int(val),int(val)),resample=Image.BILINEAR)
        result = imgprev.resize(im2.size, Image.NEAREST)
        photoprev = ImageTk.PhotoImage(result)

    canvas_photo.itemconfig(preview, image = photoprev)


def pot2(e):
    im = screen()

    xsize, ysize = im.size
    orig_value = im.getpixel((e.x, e.y))
    fill_value = "#015000"

    voisins_a_tester = {(e.x, e.y)}

    while voisins_a_tester:
        x, y = voisins_a_tester.pop()
        if im.getpixel((x, y)) == orig_value:
            im.putpixel((x,y), 120)
            item = dessin.create_rectangle(x  , y   , x   , y  , outline= color2, width = 1)
            ligne.append(item)
            if x > 0 and im.getpixel((x - 1 , y)) == orig_value:
                voisins_a_tester.add((x - 1, y))
            if x < (xsize -1) and im.getpixel((x + 1 , y)) == orig_value:
                voisins_a_tester.add((x + 1, y))
            if y > 0 and im.getpixel((x, y - 1)) == orig_value:
                voisins_a_tester.add((x, y - 1))
            if y < (ysize -1) and im.getpixel((x , y + 1)) == orig_value:
                voisins_a_tester.add((x, y + 1))

def getcolor(bouton):  # fonction qui va soit ouvrir une fenetre demandant la couleur que vous voulez ou changez la couleur selon le bouton clique
    global color, color2
    if bouton == "ask":
        if lbc["relief"] == SUNKEN:
            color = askcolor()[1]
            bc.config(bg=color)
        if lbc2["relief"] == SUNKEN:
            color2 = askcolor()[1]
            bc2.config(bg=color2)
    else:
        if lbc["relief"] == SUNKEN:
            color = bouton
            bc.config(bg=color)
        if lbc2["relief"] == SUNKEN:
            color2 = bouton
            bc2.config(bg=color2)


def etatcouleur(bouton):
    if bouton == lbc:
        lbc.config(relief = SUNKEN)
        lbc2.config(relief = RAISED)
    if bouton == lbc2:
        lbc.config(relief=RAISED)
        lbc2.config(relief=SUNKEN)



def etatforme(bouton):
    if bouton["relief"] == RAISED:
        bouton.config(relief = SUNKEN)
        if bouton == b2:
            s.config(state = NORMAL)
    elif bouton["relief"] == SUNKEN:
        bouton.config(relief = RAISED)
        if bouton == b2:
            s.config(state = DISABLED)


def pipette(e):
    global color
    im = screen()
    getcolor('#%02x%02x%02x' % im.getpixel((e.x, e.y)))
    print(color)


def resize():
    conprop = IntVar()
    wtext, htext = StringVar(), StringVar()
    wtext.set(w)
    htext.set(h)

    im = screen()
    window = Toplevel(fen)
    window.title("Redimensionner")
    window.geometry("+%d+%d" % ( fen.winfo_width()/2 ,  fen.winfo_height()/2))
    window.resizable(False, False)
    window.attributes("-toolwindow", 1)

    label1 = Label(window, text= "Horizontal")
    label1.grid(row = 0, column = 0, pady = 5)
    entry1 = Entry(window, width = 10, textvariable = wtext)
    entry1.grid(row = 0, column = 1, columnspan = 2)
    entry1.bind('<Key>', lambda event: calculresize(wtext, htext, "entry1", conprop))

    label2 = Label(window, text="Vertical")
    label2.grid(row = 1, column = 0)
    entry2 = Entry(window, width = 10,textvariable = htext)
    entry2.grid(row = 1, column = 1,columnspan = 2)

    conserv = Checkbutton(window, text = "Conserver les proportions", variable = conprop)
    conserv.grid(row = 2, column = 0, columnspan = 2, pady = 5)

    valid = Button(window, text = "Valider", command = lambda:validresize(wtext, htext, window, im))
    valid.grid(row = 3, column = 1)

    annul = Button(window, text = "Annuler", command = lambda:window.destroy())
    annul.grid(row = 3, column = 2, pady = 2, padx = 2)


def calculresize(wtext, htext, en, conprop):
    if conprop.get() == 1:
        if en == "entry1":
            w1 = int(wtext.get())
            htext.set(int((w1*h)/w))
    else:
        pass


def validresize(wtext, htext, window, im):
    global w,h, photoresize
    
    w = int(wtext.get())
    h = int(htext.get())
    im = im.resize((w, h), Image.ANTIALIAS)
    photoresize = ImageTk.PhotoImage(im)
    dessin.config(width=w, height=h)
    item = dessin.create_image(w / 2, h / 2 -1, image=photoresize)
    items.append(item)

    window.destroy()



# ----------------------------------------------------------------

#on initialise toutes les variables
color = '#000000'
color2 = '#ffffff'
epaisseur = 5
w, h = 600, 400
items, ligne = [], []
item = ""
couleurs = ["black", "gray", "red", "yellow", "orange", "white", "#6b2e00", "blue", "purple", "green", "#dbe8fc"]

# ----------------------------------------------------------------

fen = Tk()
fen.configure(bg = couleurs[10])
fen.geometry("900x600+200+100")  # on cree la fenetre de notre paint
fen.title("PyPaint1.2")

icone = PhotoImage(file="icone_PyPaint.png")
fen.tk.call('wm', 'iconphoto', fen._w, icone)

# ----------------------------------------------------------------

menu = Menu(fen)  # menu qui possede un sous-menu contenant des commandes comme nouveau, ouvrir et couleur
fen.config(menu=menu)

filemenu = Menu(menu, tearoff=0)
menu.add_cascade(label="Fichier", menu=filemenu)

filemenu.add_command(label="Nouveau", command=suppr, accelerator="Ctrl+N")
menu.bind_all("<Control-n>", suppr)
filemenu.add_command(label="Ouvrir", command=openimage, accelerator="Ctrl+O")
menu.bind_all("<Control-o>", openimage)
filemenu.add_command(label="Enregistrer", command=save, accelerator="Ctrl+S")
menu.bind_all("<Control-s>", save)
filemenu.add_separator()
filemenu.add_command(label="Quitter", command=quit, accelerator="Ctrl+Q")
menu.bind_all("<Control-q>", quit)

filemenu2 = Menu(menu, tearoff=0)
menu.add_cascade(label="Edition", menu=filemenu2)

filemenu2.add_command(label="Annuler", command=undo, accelerator="Ctrl+Z")
menu.bind_all("<Control-z>", undo)
filemenu2.add_command(label="Redimensionner", command= resize)

filemenu3 = Menu(menu, tearoff=0)
menu.add_cascade(label="Filtres", menu=filemenu3)

filemenu3.add_command(label="Flou Gaussien", command = lambda: filter("flou"))
filemenu3.add_command(label="Pixellisation", command = lambda: filter("pixel"))

# ----------------------------------------------------------------

status = Label(fen, text="Veuillez choisir un outil.", relief=SUNKEN, anchor=W)  # status bar

# ----------------------------------------------------------------

dessin = Canvas(fen, width=w, height=h, bg="white", highlightthickness=0)  # canvas contenant le dessin

# ----------------------------------------------------------------

btnrec = PhotoImage(file='ico/btnrec.png')
btnoval = PhotoImage(file='ico/btnoval.png')
btnligne = PhotoImage(file='ico/btnligne.png')
btngomme = PhotoImage(file='ico/btngomme.png')
btncrayon = PhotoImage(file='ico/btncrayon.png')
btnspray = PhotoImage(file='ico/btnspray.png')
btntexte = PhotoImage(file='ico/btntexte.png')
btnpot = PhotoImage(file='ico/btnpot.png')

# ----------------------------------------------------------------

tool = Frame(fen, height=100)  # frame contenant les boutons des outils

# ------------------------------
outils = Frame(tool, width=20, padx=5)

bouton_pinceau = Button(outils, image=btncrayon, command=lambda: useoutil(bouton_pinceau))
bouton_pinceau.grid(row=0, column=0)

active_button = bouton_pinceau

bouton_graph = Button(outils, image=btnspray, command=lambda: useoutil(bouton_graph))
bouton_graph.grid(row=0, column=1)


bouton_texte = Button(outils, image=btntexte, command=lambda: useoutil(bouton_texte))
bouton_texte.grid(row = 1, column = 0)

bouton_pot = Button(outils, image=btnpot, command=lambda: useoutil(bouton_pot))
bouton_pot.grid(row = 1, column = 1)

bouton_pipette = Button(outils, bitmap = "gray75", command=lambda:useoutil(bouton_pipette))
bouton_pipette.grid(row = 0, column = 2)

category = Label(outils, text="Outils", fg = "#636363")
category.grid(row=2, column=0, columnspan=2, sticky = S)

outils.grid(row=0, column=0, sticky=N + S)
outils.grid_rowconfigure(2, weight = 1)

Frame(tool, width=2,bg = couleurs[10]).grid(row = 0, column = 1, sticky = N+S)

# ------------------------------

formes = Frame(tool, width=40, height=30, padx=5)

bouton_rectangle = Button(formes, image=btnrec, command=lambda: useoutil(bouton_rectangle))
bouton_rectangle.grid(row=0, column=0)

bouton_oval = Button(formes, image=btnoval, command=lambda: useoutil(bouton_oval))
bouton_oval.grid(row=0, column=1)

bouton_ligne = Button(formes, image=btnligne, command=lambda: useoutil(bouton_ligne))
bouton_ligne.grid(row=0, column=2)


b2 = Button(formes, text="Contour", command= lambda: etatforme(b2),state = DISABLED, relief = SUNKEN, width = 10)
b2.grid(row = 0, column = 3, padx = (7,0))

b3 = Button(formes, text="Remplissage", command= lambda: etatforme(b3), state = DISABLED, width = 10)
b3.grid(row = 1, column = 3, padx = (7,0))


category2 = Label(formes, text="Formes", fg = "#636363")
category2.grid(row=2, column=0, columnspan=4, sticky = S)

formes.grid(row=0, column=2, sticky=N + S)
formes.grid_rowconfigure(2, weight = 1)

Frame(tool, width=2,bg = couleurs[10]).grid(row = 0, column = 3, sticky = N+S)

# ------------------------------

couleur = Frame(tool, padx=5)

lbc = Button(couleur, text = "Couleur 1", command = lambda:etatcouleur(lbc), relief = SUNKEN)
lbc.grid(row = 0, column = 0)

bc = Label(couleur, bg=color, width = 2, relief = SUNKEN )
bc.grid(row=0, column=1, padx = (3, 7))


lbc2 = Button(couleur, text = "Couleur 2", command = lambda:etatcouleur(lbc2))
lbc2.grid(row = 1, column = 0)

bc2 = Label(couleur, bg=color2, width = 2, relief = SUNKEN )
bc2.grid(row=1, column=1, padx = (3, 7))


framecouleurs = Frame(couleur)

n=-1   #on cree une boucle qui va cree 10 boutons avec des couleurs predefinies
for column in range(1, 6):
    for row in range(1,3):
        n += 1
        Button(framecouleurs, width = 2, bg = couleurs[n], command =lambda n=n:getcolor(couleurs[n])).grid(row = row, column = column, padx = 1, pady = 1)

framecouleurs.grid(row=0, column=2, sticky=N + S, rowspan = 2)

buttonchoose = Button(couleur, text = "Perso.", command =lambda:getcolor("ask"))
buttonchoose.grid(row = 0, column = 8, rowspan = 2, padx = 3)


category3 = Label(couleur, text="Couleur", fg = "#636363")
category3.grid(row=2, column=0, columnspan=10, sticky = S)

couleur.grid(row=0, column=4, sticky=N + S)


Frame(tool, width=2,bg = couleurs[10]).grid(row = 0, column = 5, sticky = N+S)

# ------------------------------

s = Scale(tool, orient='horizontal', from_=1, to=50, resolution=1, length=300, label='Epaisseur', command=scale)
s.set(epaisseur)
s.config(state = DISABLED)
s.grid(row=0, column=6, sticky = N+S)

Frame(tool, width=2,bg = couleurs[10]).grid(row = 0, column = 7, sticky = N+S)

# ----------------------------------------------------------------

status.pack(side=BOTTOM, fill=X)  # on pack tous les widgets

tool.pack(side=TOP, fill=X)

dessin.pack(side=TOP, anchor="w", padx = 5, pady = 5)

dessin.bind("<ButtonRelease-1>", release)
dessin.bind("<ButtonRelease-3>", release)

# ----------------------------------------------------------------

fen.mainloop()
