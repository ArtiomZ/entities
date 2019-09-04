""" Following a model-view-controller pattern """
import os
import sys
import tkinter as tk 

from tkinter import ttk
from tkinter import Tk

from gui_view import UserInterface, TableLayer, EntityLayer
from model import DbModel


class Controller():
    def __init__(self, Gui):
        self.Gui = Gui
        self.table = self.load_table()
        self.TableLayer = TableLayer(root, self.table)
        self.configure_buttons()

    def back_to_start(self):
        """ Reset the tool """
        self.EntityLayer.reset_widgets()
        self.__init__(self.Gui)

    def load_table(self):
        with DbModel() as model:
            rows = model.display_all_content()
            return rows

    def configure_buttons(self):
        """ Button to enter new entities"""
        self.TableLayer.browse1.config(command=self.show_EntityLayer)
        self.TableLayer.browse2.config(command=self.exit)

    def exit(self):
        """ Exit the mainloop, close the application """
        sys.exit()

    def retrieve_db_lists(self):
        """ Obtain all countries available in the database"""
        with DbModel() as model:
            countries = model.display_all_countries()
            entities = model.display_all_entities()
            model.create_tree_table_if_not_exists()
            return countries, entities

    def show_EntityLayer(self):
        """ Show the entity adding mask """
        self.db_lists = self.retrieve_db_lists()
        self.EntityLayer = EntityLayer(root, self.db_lists)
        self.TableLayer.reset_widgets()
        self.EntityLayer.show_EntityLayer()
        # Save the  entity in the database when the user clicks "OK"
        self.EntityLayer.browse_ok.config(command=self.save_to_db)
        # Go back to start page when user clicks "Cancel"
        self.EntityLayer.browse_cancel.config(command=self.back_to_start)


    def save_to_db(self):
        """Save the user entries to the db """
        self.entity = self.EntityLayer.entity_name_input.get()
        self.country = self.EntityLayer.tkvar_country.get()
        self.partner = self.EntityLayer.partner_input.get()
        self.parent = self.EntityLayer.tkvar_parent.get()
        self.row = (self.entity, self.country, self.partner, self.parent);

        with DbModel() as model:
            model.insert_content(self.row)
        self.back_to_start()



if __name__ == '__main__':
    root = Tk()
    root.title("Entities")
    root.geometry('700x500')
    Gui = UserInterface(master=root)
    Application = Controller(Gui)
    root.mainloop()
    root.destroy()
