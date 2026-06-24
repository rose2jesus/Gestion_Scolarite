import tkinter as tk
from tkinter import ttk, messagebox
import basedonnees as bd
from interface import (
    OngletTableauBord, OngletEtudiants, OngletEnseignants,
    OngletModules, OngletEvaluations, C,
)

APP_NOM = "SIGS — Système de Gestion de Scolarité"


class ApplicationPrincipale(tk.Tk):

    def __init__(self):
        super().__init__()
        self.title(APP_NOM)
        self.state("zoomed")   
        self.minsize(1000, 700)
        self.configure(bg=C["bg"])
        try:
            self.iconbitmap("icone.ico")
        except Exception:
            pass

        self._page_active = None
        self._nav_btns    = {}
        self._pages       = {}

        self._build()
        self._naviguer("dashboard")

    
    def _build(self):
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self._build_sidebar()
        self._build_content()

    def _build_sidebar(self):
        sidebar = tk.Frame(self, bg=C["sidebar"], width=210)
        sidebar.grid(row=0, column=0, sticky="ns")
        sidebar.grid_propagate(False)

        
        logo_frame = tk.Frame(sidebar, bg=C["sidebar"])
        logo_frame.pack(fill="x", pady=(24, 8))
        tk.Label(logo_frame, text="", bg=C["sidebar"],
                 fg="#FFFFFF", font=("Segoe UI", 28)).pack()
        tk.Label(logo_frame, text="SIGS", bg=C["sidebar"],
                 fg="#FFFFFF", font=("Segoe UI Semibold", 16)).pack()
        tk.Label(logo_frame, text="Scolarité USSEIN", bg=C["sidebar"],
                 fg="#A0B8AD", font=("Segoe UI", 8)).pack()

        
        tk.Frame(sidebar, bg="#2D5543", height=1).pack(fill="x", padx=16, pady=(8, 16))

        
        nav_items = [
            ("dashboard",    "",  "Tableau de bord"),
            ("etudiants",    "‍", "Étudiants"),
            ("enseignants",  "‍", "Enseignants"),
            ("modules",      "",  "Modules"),
            ("evaluations",  "",  "Évaluations"),
        ]
        for key, icone, texte in nav_items:
            b = self._nav_btn(sidebar, key, icone, texte)
            b.pack(fill="x", padx=8, pady=2)
            self._nav_btns[key] = b

        
        tk.Label(sidebar, text="v1.0 | 2024-2025",
                 bg=C["sidebar"], fg="#4A7A62",
                 font=("Segoe UI", 8)).pack(side="bottom", pady=12)

    def _nav_btn(self, parent, key, icone, texte):
        f = tk.Frame(parent, bg=C["sidebar"], cursor="hand2")

        lbl = tk.Label(f, text=f"  {icone}   {texte}",
                       bg=C["sidebar"], fg="#A0B8AD",
                       font=("Segoe UI", 10), anchor="w",
                       padx=8, pady=10)
        lbl.pack(fill="x")

        def on_click(_=None):
            self._naviguer(key)
        def on_enter(_):
            if self._page_active != key:
                f.config(bg=C["sidebar_h"])
                lbl.config(bg=C["sidebar_h"])
        def on_leave(_):
            if self._page_active != key:
                f.config(bg=C["sidebar"])
                lbl.config(bg=C["sidebar"])

        for w in [f, lbl]:
            w.bind("<Button-1>", on_click)
            w.bind("<Enter>",    on_enter)
            w.bind("<Leave>",    on_leave)

        f._lbl = lbl   
        return f

    def _build_content(self):
        self.content = tk.Frame(self, bg=C["bg"])
        self.content.grid(row=0, column=1, sticky="nsew")
        self.content.grid_rowconfigure(1, weight=1)
        self.content.grid_columnconfigure(0, weight=1)

        
        topbar = tk.Frame(self.content, bg=C["surface"],
                          highlightthickness=1,
                          highlightbackground=C["border"])
        topbar.grid(row=0, column=0, sticky="ew")

        self.lbl_topbar = tk.Label(topbar,
                                   text="",
                                   bg=C["surface"], fg=C["text"],
                                   font=("Segoe UI Semibold", 12),
                                   pady=10, padx=16)
        self.lbl_topbar.pack(side="left")

        tk.Label(topbar,
                 text="Université du Sine Saloum El-Hâdj Ibrahima Niass",
                 bg=C["surface"], fg=C["text2"],
                 font=("Segoe UI", 8), padx=16).pack(side="right")

        
        self.zone_pages = tk.Frame(self.content, bg=C["bg"])
        self.zone_pages.grid(row=1, column=0, sticky="nsew")

        
        classes = {
            "dashboard":   OngletTableauBord,
            "etudiants":   OngletEtudiants,
            "enseignants": OngletEnseignants,
            "modules":     OngletModules,
            "evaluations": OngletEvaluations,
        }
        titres = {
            "dashboard":   "  Tableau de Bord",
            "etudiants":   "  Étudiants",
            "enseignants": "  Enseignants",
            "modules":     "  Modules",
            "evaluations": "  Évaluations",
        }
        self._titres = titres
        for key, Cls in classes.items():
            page = Cls(self.zone_pages)
            
            self._pages[key] = page

    def _naviguer(self, key):
        
        for k, frame in self._nav_btns.items():
            lbl = frame._lbl
            if k == key:
                frame.config(bg=C["accent"])
                lbl.config(bg=C["accent"], fg="#FFFFFF")
            else:
                frame.config(bg=C["sidebar"])
                lbl.config(bg=C["sidebar"], fg="#A0B8AD")

        self._page_active = key
        self.lbl_topbar.config(text=self._titres.get(key, ""))

        
        for k, page in self._pages.items():
            page.pack_forget()
        self._pages[key].pack(fill="both", expand=True)

        
        if key == "dashboard":
            try:
                self._pages["dashboard"].actualiser()
            except Exception:
                pass




def main():
    if not bd.db.is_connected():
        root = tk.Tk()
        root.withdraw()
        messagebox.showerror(
            "Erreur de connexion",
            "Connexion MySQL échouée.\n\nVérifiez :\n"
            "• Que MySQL est démarré\n"
            "• Le mot de passe dans basedonnees.py\n"
            "• Que la base 'scolarite_db' existe"
        )
        root.destroy()
        return

    app = ApplicationPrincipale()
    app.mainloop()


if __name__ == "__main__":
    main()
