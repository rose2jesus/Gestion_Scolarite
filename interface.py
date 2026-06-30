# ============================================================
# interface.py — Interface graphique Tkinter (CRUD complet)
# SIGS - Système d'Information de Gestion de Scolarité
# USSEIN | L3 Informatique | 2024-2025
# ============================================================

import tkinter as tk
from tkinter import ttk, messagebox
import basedonnees as bd

# ══════════════════════════════════════════════════════════════
#  PALETTE & TOKENS
# ══════════════════════════════════════════════════════════════
C = {
    "bg":        "#F0EBE3",
    "surface":   "#FFFFFF",
    "sidebar":   "#1B3A2D",
    "sidebar_h": "#245C42",
    "accent":    "#1B6B4A",
    "accent_h":  "#14523A",
    "gold":      "#C8922A",
    "gold_h":    "#A37520",
    "danger":    "#C0392B",
    "danger_h":  "#992D22",
    "text":      "#1A1A2E",
    "text2":     "#6B7280",
    "border":    "#D5CBC0",
    "row_even":  "#F9F6F2",
    "row_odd":   "#FFFFFF",
    "sel":       "#D4EDE2",
    "entry_bg":  "#F5F1EB",
    "header_bg": "#EDE7DC",
}

FONT_TITLE = ("Segoe UI Semibold", 14)
FONT_LABEL = ("Segoe UI", 10)
FONT_SMALL = ("Segoe UI", 9)
FONT_BTN   = ("Segoe UI Semibold", 9)
FONT_TABLE = ("Segoe UI", 9)
PAD = 8


# ══════════════════════════════════════════════════════════════
#  COMPOSANTS DE BASE
# ══════════════════════════════════════════════════════════════

def mk_btn(parent, text, cmd, color=None, hover_color=None, w=12, fg="#FFFFFF"):
    color = color or C["accent"]
    hover_color = hover_color or C["accent_h"]
    b = tk.Button(parent, text=text, command=cmd,
                  bg=color, fg=fg, font=FONT_BTN,
                  relief="flat", bd=0, padx=10, pady=5,
                  width=w, cursor="hand2",
                  activebackground=hover_color, activeforeground=fg)
    b.bind("<Enter>", lambda e: b.config(bg=hover_color))
    b.bind("<Leave>", lambda e: b.config(bg=color))
    return b


def mk_entry(parent, var, w=20):
    return tk.Entry(parent, textvariable=var, width=w,
                    bg=C["entry_bg"], fg=C["text"],
                    relief="flat", font=FONT_LABEL,
                    insertbackground=C["accent"],
                    highlightthickness=1,
                    highlightbackground=C["border"],
                    highlightcolor=C["accent"])


def mk_combo(parent, var, vals, w=18):
    style = ttk.Style()
    style.configure("S.TCombobox",
                    fieldbackground=C["entry_bg"],
                    background=C["entry_bg"],
                    foreground=C["text"])
    c = ttk.Combobox(parent, textvariable=var, values=vals,
                     width=w, state="readonly",
                     font=FONT_LABEL, style="S.TCombobox")
    return c


def mk_label(parent, text, small=False, bold=False):
    font = FONT_SMALL if small else FONT_LABEL
    if bold:
        font = (font[0], font[1], "bold")
    return tk.Label(parent, text=text,
                    bg=C["surface"], fg=C["text2"], font=font, anchor="w")


def creer_treeview(parent, cols, widths):
    frame = tk.Frame(parent, bg=C["bg"])
    style = ttk.Style()
    style.theme_use("clam")
    style.configure("S.Treeview",
                    background=C["row_odd"],
                    foreground=C["text"],
                    rowheight=26,
                    fieldbackground=C["row_odd"],
                    font=FONT_TABLE, borderwidth=0)
    style.configure("S.Treeview.Heading",
                    background=C["header_bg"],
                    foreground=C["accent"],
                    font=("Segoe UI Semibold", 9),
                    relief="flat", padding=5)
    style.map("S.Treeview",
              background=[("selected", C["sel"])],
              foreground=[("selected", C["accent"])])
    style.layout("S.Treeview", [("Treeview.treearea", {"sticky": "nswe"})])
    style.configure("T.Vertical.TScrollbar",
                    background=C["border"], troughcolor=C["bg"],
                    arrowcolor=C["text2"], width=8)
    style.configure("T.Horizontal.TScrollbar",
                    background=C["border"], troughcolor=C["bg"],
                    arrowcolor=C["text2"], width=8)

    tree = ttk.Treeview(frame, columns=cols, show="headings",
                        style="S.Treeview", selectmode="browse")
    for col, w in zip(cols, widths):
        tree.heading(col, text=col)
        tree.column(col, width=w, anchor="w", minwidth=30)
    tree.tag_configure("pair",   background=C["row_even"])
    tree.tag_configure("impair", background=C["row_odd"])

    sb_v = ttk.Scrollbar(frame, orient="vertical",   command=tree.yview, style="T.Vertical.TScrollbar")
    sb_h = ttk.Scrollbar(frame, orient="horizontal", command=tree.xview, style="T.Horizontal.TScrollbar")
    tree.configure(yscrollcommand=sb_v.set, xscrollcommand=sb_h.set)
    tree.grid(row=0, column=0, sticky="nsew")
    sb_v.grid(row=0, column=1, sticky="ns")
    sb_h.grid(row=1, column=0, sticky="ew")
    frame.grid_rowconfigure(0, weight=1)
    frame.grid_columnconfigure(0, weight=1)
    return frame, tree


def charger_tree(tree, data):
    for item in tree.get_children():
        tree.delete(item)
    for i, row in enumerate(data):
        tag = "pair" if i % 2 == 0 else "impair"
        tree.insert("", "end", values=row, tags=(tag,))


def barre_recherche(parent, callback):
    """Retourne un frame avec champ de recherche."""
    f = tk.Frame(parent, bg=C["surface"],
                 highlightthickness=1, highlightbackground=C["border"])
    tk.Label(f, text="🔍", bg=C["surface"], fg=C["text2"],
             font=FONT_LABEL).pack(side="left", padx=(6, 2))
    var = tk.StringVar()
    def _safe_callback(*_):
        try:
            callback(var.get())
        except AttributeError:
            # Le widget appelant (ex: self.tree) n'est pas encore
            # construit au moment où le texte placeholder est inséré.
            pass
    var.trace_add("write", _safe_callback)
    e = tk.Entry(f, textvariable=var, bg=C["surface"], fg=C["text"],
                 relief="flat", font=FONT_LABEL, insertbackground=C["accent"])
    e.pack(side="left", fill="x", expand=True, ipady=5, padx=(0, 6))
    placeholder = "Rechercher…"
    e.insert(0, placeholder); e.config(fg=C["text2"])
    e.bind("<FocusIn>",  lambda ev: (e.delete(0,"end"), e.config(fg=C["text"])) if e.get()==placeholder else None)
    e.bind("<FocusOut>", lambda ev: (e.insert(0,placeholder), e.config(fg=C["text2"])) if not e.get() else None)
    return f


def bandeau_boutons(parent, actions):
    """
    Crée une barre de boutons horizontale.
    actions = liste de (texte, commande, couleur, hover, fg)
    """
    f = tk.Frame(parent, bg=C["header_bg"])
    for text, cmd, color, hover, fg in actions:
        mk_btn(f, text, cmd, color, hover, w=12, fg=fg).pack(side="left", padx=4, pady=6)
    return f


def section_card(parent, titre):
    """Carte blanche avec bandeau de titre."""
    outer = tk.Frame(parent, bg=C["surface"],
                     highlightthickness=1, highlightbackground=C["border"])
    header = tk.Frame(outer, bg=C["header_bg"])
    header.pack(fill="x")
    tk.Label(header, text=titre, bg=C["header_bg"], fg=C["accent"],
             font=("Segoe UI Semibold", 10), padx=10, pady=5).pack(side="left")
    tk.Frame(outer, bg=C["border"], height=1).pack(fill="x")
    body = tk.Frame(outer, bg=C["surface"])
    body.pack(fill="x", padx=PAD, pady=PAD)
    return outer, body


# ══════════════════════════════════════════════════════════════
#  ONGLET ÉTUDIANTS
# ══════════════════════════════════════════════════════════════

class OngletEtudiants(tk.Frame):
    COLS = ("ID","Matricule","Nom","Prénom","Naissance","Email","Téléphone","Filière","Niveau","Année")
    LARG = (35, 95, 95, 95, 90, 160, 95, 90, 55, 55)

    def __init__(self, parent):
        super().__init__(parent, bg=C["bg"])
        self._id = None
        self._build()
        self.charger()

    def _build(self):
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # ── Ligne 0 : titre + recherche ──────────────────
        top = tk.Frame(self, bg=C["bg"])
        top.grid(row=0, column=0, sticky="ew", padx=PAD, pady=(PAD, 4))
        tk.Label(top, text="👨‍🎓  Gestion des Étudiants",
                 bg=C["bg"], fg=C["text"], font=FONT_TITLE).pack(side="left")
        barre_recherche(top,
            lambda t: charger_tree(self.tree,
                bd.rechercher_etudiants(t) if t.strip() and t != "Rechercher…"
                else bd.get_tous_etudiants())
        ).pack(side="right", fill="x", expand=True, padx=(12, 0))

        # ── Ligne 1 : tableau (expand) ───────────────────
        ft, self.tree = creer_treeview(self, self.COLS, self.LARG)
        ft.grid(row=1, column=0, sticky="nsew", padx=PAD, pady=(0, 4))
        self.tree.bind("<<TreeviewSelect>>", self._on_sel)

        # ── Ligne 2 : formulaire (taille fixe) ───────────
        card_outer, b = section_card(self, "✏️  Fiche Étudiant")
        card_outer.grid(row=2, column=0, sticky="ew", padx=PAD, pady=(0, 4))

        self.v = {k: tk.StringVar() for k in
                  ["mat","nom","prenom","naiss","email","tel","filiere","niveau","annee"]}

        # Ligne A : 3 champs texte
        for i, (lbl, key) in enumerate([("Matricule *","mat"),("Nom *","nom"),("Prénom *","prenom")]):
            tk.Label(b, text=lbl, bg=C["surface"], fg=C["text2"], font=FONT_SMALL, anchor="w"
                     ).grid(row=0, column=i*2, sticky="w", padx=(0,4))
            mk_entry(b, self.v[key], w=16).grid(row=1, column=i*2, sticky="ew", padx=(0,10), pady=(2,4))

        # Ligne B : 3 champs texte
        for i, (lbl, key) in enumerate([("Date naissance","naiss"),("Email","email"),("Téléphone","tel")]):
            tk.Label(b, text=lbl, bg=C["surface"], fg=C["text2"], font=FONT_SMALL, anchor="w"
                     ).grid(row=2, column=i*2, sticky="w", padx=(0,4))
            mk_entry(b, self.v[key], w=16).grid(row=3, column=i*2, sticky="ew", padx=(0,10), pady=(2,4))

        # Ligne C : filière / niveau / année
        specs = [("Filière","filiere",["Informatique","MPI","AgroTIC","SVT","Autre"],14),
                 ("Niveau","niveau",["L1","L2","L3","M1","M2"],8),
                 ("Année inscription","annee",None,8)]
        for i, (lbl, key, vals, w) in enumerate(specs):
            tk.Label(b, text=lbl, bg=C["surface"], fg=C["text2"], font=FONT_SMALL, anchor="w"
                     ).grid(row=4, column=i*2, sticky="w", padx=(0,4))
            if vals:
                mk_combo(b, self.v[key], vals, w=w).grid(row=5, column=i*2, sticky="ew", padx=(0,10), pady=(2,4))
            else:
                mk_entry(b, self.v[key], w=w).grid(row=5, column=i*2, sticky="ew", padx=(0,10), pady=(2,4))

        for i in range(6):
            b.grid_columnconfigure(i, weight=1)

        # ── Ligne 3 : boutons (taille fixe) ──────────────
        bbar = bandeau_boutons(self, [
            ("＋ Ajouter",    self.ajouter,   C["accent"],  C["accent_h"], "#FFF"),
            ("✎ Modifier",    self.modifier,  C["gold"],    C["gold_h"],   C["text"]),
            ("✕ Supprimer",   self.supprimer, C["danger"],  C["danger_h"], "#FFF"),
            ("↺ Actualiser",  self.charger,   C["text2"],   "#4B5563",     "#FFF"),
            ("⌫ Effacer",     self._effacer,  C["border"],  "#C0B8B0",     C["text"]),
        ])
        bbar.grid(row=3, column=0, sticky="ew", padx=PAD, pady=(0, PAD))

    def charger(self):
        charger_tree(self.tree, bd.get_tous_etudiants())
        self._effacer()

    def _on_sel(self, _):
        sel = self.tree.selection()
        if not sel: return
        row = self.tree.item(sel[0])["values"]
        self._id = row[0]
        keys = ["mat","nom","prenom","naiss","email","tel","filiere","niveau","annee"]
        for k, v in zip(keys, row[1:]):
            self.v[k].set(v if v else "")

    def _effacer(self):
        self._id = None
        for v in self.v.values(): v.set("")

    def _vals(self):
        v = self.v
        ann = int(v["annee"].get()) if v["annee"].get().isdigit() else None
        return (v["mat"].get(), v["nom"].get(), v["prenom"].get(),
                v["naiss"].get() or None, v["email"].get() or None,
                v["tel"].get() or None, v["filiere"].get() or None,
                v["niveau"].get() or None, ann)

    def ajouter(self):
        try:
            if not self.v["mat"].get() or not self.v["nom"].get():
                messagebox.showwarning("Champ manquant", "Matricule et Nom sont obligatoires.")
                return
            bd.ajouter_etudiant(*self._vals())
            messagebox.showinfo("Succès", "Étudiant ajouté ✓")
            self.charger()
        except Exception as e:
            messagebox.showerror("Erreur", str(e))

    def modifier(self):
        if not self._id:
            messagebox.showwarning("Sélection", "Cliquez d'abord sur un étudiant dans le tableau.")
            return
        try:
            bd.modifier_etudiant(self._id, *self._vals())
            messagebox.showinfo("Succès", "Étudiant modifié ✓")
            self.charger()
        except Exception as e:
            messagebox.showerror("Erreur", str(e))

    def supprimer(self):
        if not self._id:
            messagebox.showwarning("Sélection", "Cliquez d'abord sur un étudiant dans le tableau.")
            return
        nom = f"{self.v['prenom'].get()} {self.v['nom'].get()}"
        if messagebox.askyesno("Confirmer", f"Supprimer {nom} ?\nSes évaluations seront aussi supprimées."):
            try:
                bd.supprimer_etudiant(self._id)
                messagebox.showinfo("Supprimé", "Étudiant supprimé.")
                self.charger()
            except Exception as e:
                messagebox.showerror("Erreur", str(e))


# ══════════════════════════════════════════════════════════════
#  ONGLET ENSEIGNANTS
# ══════════════════════════════════════════════════════════════

class OngletEnseignants(tk.Frame):
    COLS = ("ID","Matricule","Nom","Prénom","Email","Téléphone","Spécialité","Grade","Statut")
    LARG = (35, 85, 90, 90, 150, 95, 125, 135, 85)

    def __init__(self, parent):
        super().__init__(parent, bg=C["bg"])
        self._id = None
        self._build()
        self.charger()

    def _build(self):
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        top = tk.Frame(self, bg=C["bg"])
        top.grid(row=0, column=0, sticky="ew", padx=PAD, pady=(PAD, 4))
        tk.Label(top, text="👨‍🏫  Gestion des Enseignants",
                 bg=C["bg"], fg=C["text"], font=FONT_TITLE).pack(side="left")
        barre_recherche(top,
            lambda t: charger_tree(self.tree,
                bd.rechercher_enseignants(t) if t.strip() and t != "Rechercher…"
                else bd.get_tous_enseignants())
        ).pack(side="right", fill="x", expand=True, padx=(12, 0))

        ft, self.tree = creer_treeview(self, self.COLS, self.LARG)
        ft.grid(row=1, column=0, sticky="nsew", padx=PAD, pady=(0, 4))
        self.tree.bind("<<TreeviewSelect>>", self._on_sel)

        card_outer, b = section_card(self, "✏️  Fiche Enseignant")
        card_outer.grid(row=2, column=0, sticky="ew", padx=PAD, pady=(0, 4))

        self.v = {k: tk.StringVar() for k in
                  ["mat","nom","prenom","email","tel","spe","grade","statut"]}

        gauche = [("Matricule *","mat"),("Nom *","nom"),("Prénom *","prenom"),("Email","email")]
        droite = [("Téléphone","tel"),("Spécialité","spe"),("Grade","grade")]

        for i, (lbl, key) in enumerate(gauche):
            tk.Label(b, text=lbl, bg=C["surface"], fg=C["text2"], font=FONT_SMALL, anchor="w"
                     ).grid(row=i*2, column=0, sticky="w", padx=(0,6))
            mk_entry(b, self.v[key], w=22).grid(row=i*2+1, column=0, sticky="ew", padx=(0,12), pady=(2,4))

        for i, (lbl, key) in enumerate(droite):
            tk.Label(b, text=lbl, bg=C["surface"], fg=C["text2"], font=FONT_SMALL, anchor="w"
                     ).grid(row=i*2, column=1, sticky="w", padx=(0,6))
            mk_entry(b, self.v[key], w=22).grid(row=i*2+1, column=1, sticky="ew", padx=(0,12), pady=(2,4))

        tk.Label(b, text="Statut", bg=C["surface"], fg=C["text2"], font=FONT_SMALL, anchor="w"
                 ).grid(row=6, column=1, sticky="w", padx=(0,6))
        mk_combo(b, self.v["statut"], ["Permanent","Vacataire"], w=20
                 ).grid(row=7, column=1, sticky="ew", padx=(0,12), pady=(2,4))

        b.grid_columnconfigure(0, weight=1)
        b.grid_columnconfigure(1, weight=1)

        bbar = bandeau_boutons(self, [
            ("＋ Ajouter",   self.ajouter,   C["accent"],  C["accent_h"], "#FFF"),
            ("✎ Modifier",   self.modifier,  C["gold"],    C["gold_h"],   C["text"]),
            ("✕ Supprimer",  self.supprimer, C["danger"],  C["danger_h"], "#FFF"),
            ("↺ Actualiser", self.charger,   C["text2"],   "#4B5563",     "#FFF"),
            ("⌫ Effacer",    self._effacer,  C["border"],  "#C0B8B0",     C["text"]),
        ])
        bbar.grid(row=3, column=0, sticky="ew", padx=PAD, pady=(0, PAD))

    def charger(self):
        charger_tree(self.tree, bd.get_tous_enseignants())
        self._effacer()

    def _on_sel(self, _):
        sel = self.tree.selection()
        if not sel: return
        row = self.tree.item(sel[0])["values"]
        self._id = row[0]
        keys = ["mat","nom","prenom","email","tel","spe","grade","statut"]
        for k, v in zip(keys, row[1:]):
            self.v[k].set(v if v else "")

    def _effacer(self):
        self._id = None
        for v in self.v.values(): v.set("")

    def _vals(self):
        v = self.v
        return (v["mat"].get(), v["nom"].get(), v["prenom"].get(),
                v["email"].get() or None, v["tel"].get() or None,
                v["spe"].get() or None, v["grade"].get() or None,
                v["statut"].get() or "Permanent")

    def ajouter(self):
        try:
            if not self.v["mat"].get() or not self.v["nom"].get():
                messagebox.showwarning("Champ manquant", "Matricule et Nom sont obligatoires.")
                return
            bd.ajouter_enseignant(*self._vals())
            messagebox.showinfo("Succès", "Enseignant ajouté ✓")
            self.charger()
        except Exception as e:
            messagebox.showerror("Erreur", str(e))

    def modifier(self):
        if not self._id:
            messagebox.showwarning("Sélection", "Cliquez d'abord sur un enseignant.")
            return
        try:
            bd.modifier_enseignant(self._id, *self._vals())
            messagebox.showinfo("Succès", "Enseignant modifié ✓")
            self.charger()
        except Exception as e:
            messagebox.showerror("Erreur", str(e))

    def supprimer(self):
        if not self._id:
            messagebox.showwarning("Sélection", "Cliquez d'abord sur un enseignant.")
            return
        nom = f"{self.v['prenom'].get()} {self.v['nom'].get()}"
        if messagebox.askyesno("Confirmer", f"Supprimer {nom} ?"):
            try:
                bd.supprimer_enseignant(self._id)
                messagebox.showinfo("Delete", "Enseignant supprimé.")
                self.charger()
            except Exception as e:
                messagebox.showerror("Erreur", str(e))


# ══════════════════════════════════════════════════════════════
#  ONGLET MODULES
# ══════════════════════════════════════════════════════════════

class OngletModules(tk.Frame):
    COLS = ("ID","Code","Intitulé","Crédits","Vol.H","Filière","Niveau","Semestre","Enseignant")
    LARG = (35, 75, 200, 55, 50, 90, 55, 65, 155)

    def __init__(self, parent):
        super().__init__(parent, bg=C["bg"])
        self._id = None
        self._map_ens = {}
        self._build()
        self.charger()

    def _build(self):
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        top = tk.Frame(self, bg=C["bg"])
        top.grid(row=0, column=0, sticky="ew", padx=PAD, pady=(PAD, 4))
        tk.Label(top, text="📚  Gestion des Modules",
                 bg=C["bg"], fg=C["text"], font=FONT_TITLE).pack(side="left")

        ft, self.tree = creer_treeview(self, self.COLS, self.LARG)
        ft.grid(row=1, column=0, sticky="nsew", padx=PAD, pady=(0, 4))
        self.tree.bind("<<TreeviewSelect>>", self._on_sel)

        card_outer, b = section_card(self, "✏️  Fiche Module")
        card_outer.grid(row=2, column=0, sticky="ew", padx=PAD, pady=(0, 4))

        self.v = {k: tk.StringVar() for k in
                  ["code","intitule","credits","volume","filiere","niveau","semestre","ens"]}
        self.v["credits"].set("3")
        self.v["volume"].set("30")

        # Ligne 1 : code, crédits, volume
        for i, (lbl, key, w) in enumerate([("Code *","code",10),("Crédits","credits",5),("Vol. horaire","volume",5)]):
            tk.Label(b, text=lbl, bg=C["surface"], fg=C["text2"], font=FONT_SMALL, anchor="w"
                     ).grid(row=0, column=i, sticky="w", padx=(0,6))
            mk_entry(b, self.v[key], w=w).grid(row=1, column=i, sticky="ew", padx=(0,10), pady=(2,4))

        # Ligne 2 : intitulé (pleine largeur)
        tk.Label(b, text="Intitulé *", bg=C["surface"], fg=C["text2"], font=FONT_SMALL, anchor="w"
                 ).grid(row=2, column=0, columnspan=3, sticky="w")
        mk_entry(b, self.v["intitule"], w=55).grid(row=3, column=0, columnspan=3, sticky="ew", pady=(2,4))

        # Ligne 3 : filière, niveau, semestre
        specs = [("Filière","filiere",["Informatique","MPI","AgroTIC","SVT","Autre"],14),
                 ("Niveau","niveau",["L1","L2","L3","M1","M2"],8),
                 ("Semestre","semestre",["S1","S2","S3","S4","S5","S6"],6)]
        for i, (lbl, key, vals, w) in enumerate(specs):
            tk.Label(b, text=lbl, bg=C["surface"], fg=C["text2"], font=FONT_SMALL, anchor="w"
                     ).grid(row=4, column=i, sticky="w", padx=(0,6))
            mk_combo(b, self.v[key], vals, w=w).grid(row=5, column=i, sticky="ew", padx=(0,10), pady=(2,4))

        # Ligne 4 : enseignant
        tk.Label(b, text="Enseignant responsable", bg=C["surface"], fg=C["text2"], font=FONT_SMALL, anchor="w"
                 ).grid(row=6, column=0, columnspan=3, sticky="w")
        self.combo_ens = mk_combo(b, self.v["ens"], [], w=50)
        self.combo_ens.grid(row=7, column=0, columnspan=3, sticky="ew", pady=(2,4))

        for i in range(3):
            b.grid_columnconfigure(i, weight=1)

        bbar = bandeau_boutons(self, [
            (" Ajouter",   self.ajouter,   C["accent"],  C["accent_h"], "#FFF"),
            (" Modifier",   self.modifier,  C["gold"],    C["gold_h"],   C["text"]),
            ("✕ Supprimer",  self.supprimer, C["danger"],  C["danger_h"], "#FFF"),
            (" Actualiser", self.charger,   C["text2"],   "#4B5563",     "#FFF"),
            (" Effacer",    self._effacer,  C["border"],  "#C0B8B0",     C["text"]),
        ])
        bbar.grid(row=3, column=0, sticky="ew", padx=PAD, pady=(0, PAD))

    def _maj_combo_ens(self):
        self._map_ens = {}
        noms = ["(Aucun)"]
        for row in bd.get_tous_enseignants():
            lbl = f"{row[2]} {row[3]}"
            self._map_ens[lbl] = row[0]
            noms.append(lbl)
        self.combo_ens["values"] = noms

    def charger(self):
        self._maj_combo_ens()
        charger_tree(self.tree, bd.get_tous_modules())
        self._effacer()

    def _on_sel(self, _):
        sel = self.tree.selection()
        if not sel: return
        row = self.tree.item(sel[0])["values"]
        self._id = row[0]
        keys = ["code","intitule","credits","volume","filiere","niveau","semestre"]
        for k, v in zip(keys, row[1:8]):
            self.v[k].set(v if v else "")
        self.v["ens"].set(row[8] if row[8] else "(Aucun)")

    def _effacer(self):
        self._id = None
        for v in self.v.values(): v.set("")
        self.v["credits"].set("3")
        self.v["volume"].set("30")

    def _vals(self):
        v = self.v
        cr  = int(v["credits"].get()) if v["credits"].get().isdigit() else 3
        vol = int(v["volume"].get())  if v["volume"].get().isdigit()  else 30
        eid = self._map_ens.get(v["ens"].get(), None)
        return (v["code"].get(), v["intitule"].get(), cr, vol,
                v["filiere"].get() or None, v["niveau"].get() or None,
                v["semestre"].get() or None, eid)

    def ajouter(self):
        try:
            if not self.v["code"].get() or not self.v["intitule"].get():
                messagebox.showwarning("Champ manquant", "Code et Intitulé sont obligatoires.")
                return
            bd.ajouter_module(*self._vals())
            messagebox.showinfo("Succès", "Module ajouté ✓")
            self.charger()
        except Exception as e:
            messagebox.showerror("Erreur", str(e))

    def modifier(self):
        if not self._id:
            messagebox.showwarning("Sélection", "Cliquez d'abord sur un module dans le tableau.")
            return
        try:
            bd.modifier_module(self._id, *self._vals())
            messagebox.showinfo("Succès", "Module modifié ✓")
            self.charger()
        except Exception as e:
            messagebox.showerror("Erreur", str(e))

    def supprimer(self):
        if not self._id:
            messagebox.showwarning("Sélection", "Cliquez d'abord sur un module dans le tableau.")
            return
        if messagebox.askyesno("Confirmer", f"Supprimer « {self.v['intitule'].get()} » ?"):
            try:
                bd.supprimer_module(self._id)
                messagebox.showinfo("Supprimé", "Module supprimé.")
                self.charger()
            except Exception as e:
                messagebox.showerror("Erreur", str(e))


# ══════════════════════════════════════════════════════════════
#  ONGLET ÉVALUATIONS
# ══════════════════════════════════════════════════════════════

class OngletEvaluations(tk.Frame):
    COLS = ("ID","Étudiant","Module","Type","Note","Coeff.","Date","Semestre","Année")
    LARG = (35, 165, 80, 75, 55, 50, 90, 65, 85)

    def __init__(self, parent):
        super().__init__(parent, bg=C["bg"])
        self._id = None
        self._map_etu = {}
        self._map_mod = {}
        self._build()
        self.charger()

    def _build(self):
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        top = tk.Frame(self, bg=C["bg"])
        top.grid(row=0, column=0, sticky="ew", padx=PAD, pady=(PAD, 4))
        tk.Label(top, text="📝  Saisie des Notes & Évaluations",
                 bg=C["bg"], fg=C["text"], font=FONT_TITLE).pack(side="left")

        ft, self.tree = creer_treeview(self, self.COLS, self.LARG)
        ft.grid(row=1, column=0, sticky="nsew", padx=PAD, pady=(0, 4))
        self.tree.bind("<<TreeviewSelect>>", self._on_sel)

        card_outer, b = section_card(self, "✏️  Nouvelle Évaluation")
        card_outer.grid(row=2, column=0, sticky="ew", padx=PAD, pady=(0, 4))

        self.v = {k: tk.StringVar() for k in
                  ["etu","mod","type","note","coef","date","sem","annee"]}
        self.v["coef"].set("1.0")
        self.v["annee"].set("2024-2025")

        # Ligne 1 : étudiant
        tk.Label(b, text="Étudiant *", bg=C["surface"], fg=C["text2"], font=FONT_SMALL, anchor="w"
                 ).grid(row=0, column=0, columnspan=4, sticky="w")
        self.combo_etu = mk_combo(b, self.v["etu"], [], w=55)
        self.combo_etu.grid(row=1, column=0, columnspan=4, sticky="ew", padx=(0,10), pady=(2,4))

        # Ligne 2 : module
        tk.Label(b, text="Module *", bg=C["surface"], fg=C["text2"], font=FONT_SMALL, anchor="w"
                 ).grid(row=2, column=0, columnspan=4, sticky="w")
        self.combo_mod = mk_combo(b, self.v["mod"], [], w=55)
        self.combo_mod.grid(row=3, column=0, columnspan=4, sticky="ew", padx=(0,10), pady=(2,4))

        # Ligne 3 : type, semestre, note, coef, date, année
        row3 = [
            ("Type *",          "type", ["CC","TP","Examen","Rattrapage"], True,  10),
            ("Semestre",        "sem",  ["S1","S2","S3","S4","S5","S6"],   True,  6),
            ("Note * (0-20)",   "note", None, False, 7),
            ("Coefficient",     "coef", None, False, 6),
            ("Date (AAAA-MM-JJ)","date",None, False, 12),
            ("Année acad.",     "annee",None, False, 10),
        ]
        for i, (lbl, key, vals, is_combo, w) in enumerate(row3):
            tk.Label(b, text=lbl, bg=C["surface"], fg=C["text2"], font=FONT_SMALL, anchor="w"
                     ).grid(row=4, column=i, sticky="w", padx=(0,4))
            if is_combo:
                mk_combo(b, self.v[key], vals, w=w).grid(row=5, column=i, sticky="ew", padx=(0,8), pady=(2,4))
            else:
                mk_entry(b, self.v[key], w=w).grid(row=5, column=i, sticky="ew", padx=(0,8), pady=(2,4))

        for i in range(6):
            b.grid_columnconfigure(i, weight=1)

        bbar = bandeau_boutons(self, [
            ("＋ Enregistrer", self.ajouter,   C["accent"],  C["accent_h"], "#FFF"),
            ("✎ Modifier",     self.modifier,  C["gold"],    C["gold_h"],   C["text"]),
            ("✕ Supprimer",    self.supprimer, C["danger"],  C["danger_h"], "#FFF"),
            ("↺ Actualiser",   self.charger,   C["text2"],   "#4B5563",     "#FFF"),
            ("⌫ Effacer",      self._effacer,  C["border"],  "#C0B8B0",     C["text"]),
        ])
        bbar.grid(row=3, column=0, sticky="ew", padx=PAD, pady=(0, PAD))

    def _maj_combos(self):
        self._map_etu = {}
        noms = []
        for row in bd.get_tous_etudiants():
            lbl = f"{row[2]} {row[3]}  ({row[1]})"
            self._map_etu[lbl] = row[0]
            noms.append(lbl)
        self.combo_etu["values"] = noms

        self._map_mod = {}
        mods = []
        for row in bd.get_tous_modules():
            lbl = f"{row[1]} — {row[2]}"
            self._map_mod[lbl] = row[0]
            mods.append(lbl)
        self.combo_mod["values"] = mods

    def charger(self):
        self._maj_combos()
        charger_tree(self.tree, bd.get_toutes_evaluations())
        self._effacer()

    def _on_sel(self, _):
        sel = self.tree.selection()
        if not sel: return
        row = self.tree.item(sel[0])["values"]
        self._id = row[0]
        ev = bd.get_evaluation_par_id(self._id)
        if ev:
            for lbl, eid in self._map_etu.items():
                if eid == ev[1]:
                    self.v["etu"].set(lbl); break
            for lbl, mid in self._map_mod.items():
                if mid == ev[2]:
                    self.v["mod"].set(lbl); break
        self.v["type"].set(row[3])
        self.v["note"].set(row[4])
        self.v["coef"].set(row[5])
        self.v["date"].set(row[6] if row[6] else "")
        self.v["sem"].set(row[7]  if row[7]  else "")
        self.v["annee"].set(row[8] if row[8] else "")

    def _effacer(self):
        self._id = None
        for k, v in self.v.items(): v.set("")
        self.v["coef"].set("1.0")
        self.v["annee"].set("2024-2025")

    def _vals(self):
        v = self.v
        eid = self._map_etu.get(v["etu"].get())
        mid = self._map_mod.get(v["mod"].get())
        if not eid or not mid:
            raise ValueError("Veuillez sélectionner un étudiant et un module.")
        try:
            note = float(v["note"].get())
            if not 0 <= note <= 20: raise ValueError()
        except ValueError:
            raise ValueError("La note doit être un nombre entre 0 et 20.")
        return (eid, mid, v["type"].get(), note,
                float(v["coef"].get() or 1.0),
                v["date"].get() or None,
                v["sem"].get() or None,
                v["annee"].get() or None)

    def ajouter(self):
        try:
            bd.ajouter_evaluation(*self._vals())
            messagebox.showinfo("Succès", "Évaluation enregistrée ✓")
            self.charger()
        except Exception as e:
            messagebox.showerror("Erreur", str(e))

    def modifier(self):
        if not self._id:
            messagebox.showwarning("Sélection", "Cliquez sur une évaluation dans le tableau.")
            return
        try:
            bd.modifier_evaluation(self._id, *self._vals())
            messagebox.showinfo("Succès", "Évaluation modifiée ✓")
            self.charger()
        except Exception as e:
            messagebox.showerror("Erreur", str(e))

    def supprimer(self):
        if not self._id:
            messagebox.showwarning("Sélection", "Cliquez d'abord sur une évaluation dans le tableau.!!!")
            return
        if messagebox.askyesno("Confirmer", "Supprimer cette évaluation ?"):
            try:
                bd.supprimer_evaluation(self._id)
                messagebox.showinfo("Supprimé", "Évaluation supprimée.")
                self.charger()
            except Exception as e:
                messagebox.showerror("Erreur", str(e))


# ══════════════════════════════════════════════════════════════
#  ONGLET TABLEAU DE BORD
# ══════════════════════════════════════════════════════════════

class OngletTableauBord(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=C["bg"])
        self._build()
        self.actualiser()

    def _build(self):
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        tk.Label(self, text="📊  Tableau de Bord",
                 bg=C["bg"], fg=C["text"],
                 font=FONT_TITLE).grid(row=0, column=0, sticky="w",
                                       padx=PAD, pady=(PAD, 6))

        # Cartes statistiques
        cartes = tk.Frame(self, bg=C["bg"])
        cartes.grid(row=0, column=0, sticky="e", padx=PAD, pady=(PAD, 6))

        infos = [
            ("etudiants",   "Étudiants",   "👨‍🎓", C["accent"]),
            ("enseignants", "Enseignants", "👨‍🏫", C["gold"]),
            ("modules",     "Modules",     "📚",  "#7C3AED"),
            ("evaluations", "Évaluations", "📝",  C["danger"]),
        ]
        self.lbl_stats = {}
        for i, (key, titre, icone, color) in enumerate(infos):
            card = tk.Frame(cartes, bg=C["surface"],
                            highlightthickness=1, highlightbackground=C["border"])
            card.grid(row=0, column=i, padx=4)
            tk.Frame(card, bg=color, height=3).pack(fill="x")
            inner = tk.Frame(card, bg=C["surface"])
            inner.pack(padx=14, pady=8)
            tk.Label(inner, text=icone, bg=C["surface"], fg=color,
                     font=("Segoe UI", 18)).pack(anchor="w")
            lbl = tk.Label(inner, text="—", bg=C["surface"], fg=color,
                           font=("Segoe UI Semibold", 24))
            lbl.pack(anchor="w")
            tk.Label(inner, text=titre, bg=C["surface"], fg=C["text2"],
                     font=FONT_SMALL).pack(anchor="w")
            self.lbl_stats[key] = lbl

        # Tableau taux de réussite
        tk.Label(self, text="Taux de réussite par module",
                 bg=C["bg"], fg=C["text"],
                 font=("Segoe UI Semibold", 10)
                 ).grid(row=0, column=0, sticky="s", pady=(60, 0))

        cols = ("Module","Total notes","Réussites","Taux de réussite (%)")
        larg = (290, 110, 100, 160)
        ft, self.tree_taux = creer_treeview(self, cols, larg)
        ft.grid(row=1, column=0, sticky="nsew", padx=PAD, pady=(0, 4))

        mk_btn(self, "↺  Actualiser", self.actualiser,
               C["accent"], C["accent_h"], w=16
               ).grid(row=2, column=0, pady=(0, PAD))

    def actualiser(self):
        try:
            stats = bd.get_stats_globales()
            for key, lbl in self.lbl_stats.items():
                lbl.config(text=str(stats.get(key, "—")))
            charger_tree(self.tree_taux, bd.get_taux_reussite_modules())
        except Exception as e:
            messagebox.showerror("Erreur", str(e))