import time
import tkinter as tk 

from tkinter import ttk

class UserInterface(tk.Frame):
    def __init__(self, master):
        """ Initialize the general format to be displayed first """
        tk.Frame.__init__(self, master)
        self.root = master
        self.root.update()
        self.grid(row=9, column=2, columnspan=1)


class TableLayer(UserInterface):
    """ Display the first page for the user containing the table """
    def __init__(self, master, table):
        super().__init__(master)
        self.table = table
        self.show_TableLayer()
        self.show_table()

    def show_table(self):
        """ Display all entries present in the table """
        # Display Header
        self.entity_label = tk.Label(self, text="Entity Name", width=15)
        self.entity_label.grid(row=5, column=1,  padx=5, pady=(5, 0))
        self.entity_label.config(font=("Liberation Mono", 10, "bold"), fg="black")
        self.country_label = tk.Label(self, text="Country", width=15)
        self.country_label.grid(row=5, column=2,  padx=5, pady=(5, 0))
        self.country_label.config(font=("Liberation Mono", 10, "bold"), fg="black")
        self.partner_label = tk.Label(self, text="Partner-Nr.", width=15)
        self.partner_label.grid(row=5, column=3,  padx=5, pady=(5, 0))
        self.partner_label.config(font=("Liberation Mono", 10, "bold"), fg="black")
        self.parent_label = tk.Label(self, text="Parent", width=15)
        self.parent_label.grid(row=5, column=4,  padx=5, pady=(5, 0))
        self.parent_label.config(font=("Liberation Mono", 10, "bold"), fg="black")
        # Display the table entries
        for i, row in enumerate(self.table):
            for j, cell in enumerate(row):
                self.country_input = tk.Text(self, height=1, width=15)
                self.country_input.grid(row=i+6, column=j+1, sticky="EW", padx=5, pady=(5, 0))
                self.country_input.insert(tk.END, cell)


    def show_TableLayer(self):
        """ Write the first-to-be-displayed content in the Frame """
        # Main Label, grid and empty lines
        self.main_label = tk.Label(self, text="Entity Master data (Stammdaten Gesellschaften)")
        self.main_label.config(font=("Liberation Mono", 14, "bold"), fg="black")
        self.main_label.grid(row=1, column=1, columnspan=4, padx=5, pady=5)

        # Give the user the possibility to add entries
        self.browse1 = tk.Button(self, text = 'Add Entity (Geselschaft hinzufügen)', fg = 'black', width=40, bg='green', font=("Liberation Mono", 10, "bold"))
        self.browse1.grid(row=4, column=1, columnspan=4, sticky="E", padx=5, pady=5)

        self.browse2 = tk.Button(self, text = 'Exit', fg = 'black', font=("Liberation Mono", 10, "bold"))
        self.browse2.grid(row=4, column=1, sticky="W", padx=5, pady=5)

        # Add a blank line
        self.blank_label = tk.Label(self, text=" ", width=30)
        self.blank_label.grid(row=6, column=2, sticky="W", padx=5, pady=5)


    def reset_widgets(self):

        """ Remove all widgets and go back to the first page """
        for widget in self.winfo_children():
            widget.destroy()
        self.update()


class EntityLayer(UserInterface):
    """ Layer to load entities to the db """

    def __init__(self, master, db_lists):
        super().__init__(master)
        self.country_choices = [country[0] for country in db_lists[0]]
        self.entities_choices = [entity[0] for entity in db_lists[1]]

    def reset_widgets(self):
        """ Remove all widgets and go back to the first page """
        for widget in self.winfo_children():
            widget.destroy()

    def callback_int(self, P):
        """ Callback to make sure the user can only enter certain chars """
        if (str.isdigit(P) or P == "") and len(str(P))<=4:
            return True
        else:
            return False

    def show_EntityLayer(self):
        # Add labels for the first layer

        self.first_label = tk.Label(self, text="Add entity (Gesellschaft hinzufügen)", font=("Liberation Mono", 14, "bold"))
        self.first_label.grid(row=1, column=1, columnspan=4,  padx=5, pady=(5, 0))

        # Ask for entity name
        self.enity_name_input_label = tk.Label(self, text="Entity Name (Gesellschaftsname")
        self.enity_name_input_label.grid(row=2, column=1, sticky="E", padx=5, pady=(5, 0))

        # Add text bar to ask for entity name
        self.entity_name_input = tk.Entry(self,  width=50)
        self.entity_name_input.grid(row=2, column=2, sticky="W", padx=5, pady=(5, 0))
        self.entity_name_input.insert(tk.END, "")
        
        # Ask for country
        self.tkvar_country = tk.StringVar(self.root)
        self.country_input_label = tk.Label(self, text="Country (Land)")
        self.country_input_label.grid(row=3, column=1, sticky="E", padx=5, pady=(5, 0))
        # Add text bar to ask for parent
        self.popupMenu_country = ttk.OptionMenu(self, self.tkvar_country, *self.country_choices)
        self.popupMenu_country.grid(row=3, column=2, sticky="W", padx=5, pady=(5, 0))

        # Ask for partner
        self.partner_input_label = tk.Label(self, text="Partner-Nr.")
        self.partner_input_label.grid(row=4, column=1, sticky="E", padx=5, pady=(5, 0))

        # Add text bar to ask for partner
        vcmd_int = (self.register(self.callback_int))
        self.partner_input = tk.Entry(self, width=50, validate = 'all',  validatecommand=(vcmd_int, '%P'))
        self.partner_input.grid(row=4, column=2, sticky="W", padx=5, pady=(5, 0))
        self.partner_input.insert(tk.END, "")

        # Ask for parent
        self.parent_input_label = tk.Label(self, text="Parent (Mutter)")
        self.parent_input_label.grid(row=5, column=1, sticky="E", padx=5, pady=(5, 0))

        # Add text bar to ask for parent
        self.tkvar_parent = tk.StringVar(self.root)
        self.popupMenu_parent = ttk.OptionMenu(self, self.tkvar_parent, *self.entities_choices)
        self.popupMenu_parent.grid(row=5, column=2, sticky="W", padx=5, pady=(5, 0))

        
        # Add buttons ok/cancel
        self.browse_ok = tk.Button(self, text = 'OK', fg = 'black', bg='green', width=20, font=("Liberation Mono", 10, "bold"))
        self.browse_ok.grid(row=7, column=1, sticky="W", padx=5, pady=(5, 0))
        self.browse_cancel = tk.Button(self, text = 'Cancel', fg = 'black', bg='green', width=20, font=("Liberation Mono", 10, "bold"))
        self.browse_cancel.grid(row=7, column=2, sticky="W", padx=5, pady=(5, 0))

