

import time

import threading

import tkinter as tk

 

from tkinter import filedialog, messagebox

from tkinter import ttk

 

class MonaLisaGUI(tk.Frame):

    """ Base Class to encapsule a tk Frame object """

   

    choice = False

    gui_dict = {'1': {"choice": "1",

                      "text_input": "1",

                      "text_output": "1"},

                '2': {"choice": "1.",

                      "text_input": "2",

                      "texnput": "2:",

                      "text_output": "2:"}}

 

    def __init__(self, master):

        """ Initialize the format to be displayed first """

        tk.Frame.__init__(self, master)

        self.root = master

        self.root.update()

        self.grid(row=9, column=2, columnspan=1)

        self.dirinname = None

        self.diroutname = None

        self.error = False

 

class WelcomeLayer(MonaLisaGUI):

    """ First MonaLisa GUI layer shown to the user """

 

    def __init__(self, master):

        super().__init__(master)

        self.show_first_layer()

        self.choice = '0'

 

    def show_first_layer(self):

        """ Write the first-to-be-displayed content in the Frame """

        # Main Label, grid and empty lines

        self.main_label = tk.Label(self, text="MonaLisa execution tool")

        self.main_label.config(font=("Liberation Mono", 10, "bold"), fg="black")

        self.main_label.grid(row=1, column=1, sticky="W", padx=5, pady=5)

        # Ask the user for the next step

        self.first_label = tk.Label(self, text="Welcome to MonaLisa! What would you like to do?")

        self.first_label.grid(row=3, column=1, sticky="W", padx=5, pady=5)

        # Give the user a choice to conduct 2 different tasks

        self.browse1 = tk.Button(self, text = '', fg = 'black')#,  bg="ivory3")

       self.browse1.grid(row=4, column=1, sticky="EW", padx=5, pady=5)

        self.browse2 = tk.Button(self, text = '', fg = 'black')#,  bg="ivory3")

        self.browse2.grid(row=5, column=1, sticky="EW", padx=5, pady=5)

        # Add a blank line

        self.blank_label = tk.Label(self, text=" ", width=60)

        self.blank_label.grid(row=6, column=2, sticky="W", padx=5, pady=5)

        # Add a help button on the right side of the screen

        self.help = tk.Button(self, text = "Help")

        self.help.grid(row=3, column=2, sticky="E", padx=5, pady=5)

 

    def reset_widgets(self):

        """ Remove all widgets and go back to the first page """

        for widget in self.winfo_children():

            widget.destroy()

        self.update()

 

 

class firstLayer(MonaLisaGUI):

    """ Layer specific to the process """

    def __init__(self, master):

        super().__init__(master)

 

    def show_first_layer(self):

        """ Show the specific elements to the user, when the

        in the first layer was chosen

        """

        self.choice = '1'

        """ Show the general elements of the second frame to the user """

        # Add labels for the first layer

        self.first_label = tk.Label(self, text=self.gui_dict[self.choice]["choice"], font=("Liberation Mono", 10, "bold"))

        self.first_label.grid(row=1, column=1, sticky="W", padx=5, pady=(5, 0))

        # Text asking the user for an action

        self.dir_path_label_input = tk.Label(self, text=self.gui_dict[self.choice]["text_input"])

        self.dir_path_label_input.grid(row=2, column=1, sticky="W", padx=5, pady=(5, 0))

        # Add "Back"-Button in the corner

        self.back = tk.Button(self, text = 'Back to Start', fg = 'black')

        self.back.grid(row=2, column=2, sticky="E", padx=5, pady=(5, 0))

        # Add text bar to display the chosen path for the input folder

        self.dirinput = tk.Text(self, height=1)#, width = 70)

        self.dirinput.grid(row=3, column=1, sticky="W", padx=5, pady=(5, 0))

        self.dirinput.insert(tk.END, "Select the input folder...")

        # Add button to search for path

        self.browseinfolder = tk.Button(self, text = 'Browse', fg = 'black')

        self.browseinfolder.grid(row=3, column=2, sticky="W", padx=5, pady=(5, 0))

 

    def browse_input_folder(self):

        """ Open a window to select the directory from the Explorer """

        self.dirinname = filedialog.askdirectory(parent=self.root, mustexist = True, title='Select your input folder')

        if self.dirinname:

            self.dirinput.delete('1.0', tk.END)

            self.dirinput.insert('1.0', self.dirinname)

 

    def show_output_file_path(self, self_path):

        """ Show the elements for  """

        self.diroutname = self_path

        # Text asking the user for an action

        self.dir_path_label_output = tk.Label(self, text=self.gui_dict[self.choice]["text_output"])

        self.dir_path_label_output.grid(row=4, column=1, sticky="W", padx=5, pady=(5, 0))

        # Add text bar to display the chosen path for the output folder

        self.diroutput = tk.Text(self, height=1)#, width = 70)

        self.diroutput.grid(row=5, column=1, sticky="W", padx=5, pady=(5, 0))

        self.diroutput.insert(tk.END, self_path)

        # Add button to search for path

        self.browseoutfolder = tk.Button(self, text = 'Browse', fg = 'black')

        self.browseoutfolder.grid(row=5, column=2, sticky="W", padx=5, pady=(5, 0))

        # Add text field showing the progress

        self.infofield = tk.Text(self, height=28, font=("Verdana", "8"))

        self.infofield.grid(row=6, column=1, sticky="WE", padx=5, pady=(5, 0))

        self.infofield.insert(tk.END, "Please check  \n\nPress 'Start'of the files ... ")

        # create a Scrollbar and associate it with txt

        self.scrollb = tk.Scrollbar(self, command=self.infofield.yview)

        self.scrollb.grid(row=6, column=2, sticky='NSW')

        self.infofield['yscrollcommand'] = self.scrollb.set

        # Start button

        self.start = tk.Button(self, text = 'Start', fg = 'black')

        self.start.grid(row=7, column=2, sticky="W", padx=5, pady=(5, 0))

 

    def browse_output_folder(self):

        """ Open a window to select the directory from the Explorer """

        self.diroutname = filedialog.askdirectory(parent=self.root, mustexist=True, title='Select your output folder')

        if self.diroutname:

            self.diroutput.delete('1.0', tk.END)

            self.diroutput.insert('1.0', self.diroutname)

 

   def reset_widgets(self):

        """ Remove all widgets and go back to the first page """

        for widget in self.winfo_children():

            widget.destroy()

 

    def start_process(self):

        """ Show progress in a text field """

        # Replace the Start button with the Exit/Cancel button

        self.start.destroy()

        # Add a cancel button underneath

        self.cancel = tk.Button(self, text = 'Cancel', fg = 'black')

        self.cancel.grid(row=7, column=2, sticky="W", padx=5, pady=(5, 0))

        # Add text depending on the process running

        self.infofield.delete('1.0', tk.END)

        self.infofield.insert('1.0', "\n\nThis might take a few minutes ...")

 

    def build_progress_bar(self, maximum):

        """ Build the progress bar """

        self.progressbar = ttk.Progressbar(self, orient=tk.HORIZONTAL,

                                           mode="determinate",

                                           maximum=maximum)

        self.progressbar.grid(row=7, column=1, sticky='WE', padx=5, pady=(5, 0))

 

    def write_line(self, msg):

        """ Writes the log to the gui text field """

        self.infofield.insert('1.0', msg)

 

    def update_progress_bar(self, value):

        """ Updates the progress """

        self.progressbar["value"] = value

 

    def throw_error(self, msg):

        """ If an error encountered, display it in a message box """

        tk.messagebox.showerror("Error", msg)

        self.error = True

 

    def final_elements(self, max):

        """ Adds final elements """

        # Stops the progress bar and destroy it

        self.progressbar.stop()

        self.progressbar.configure(mode="determinate", value=max)

        if self.error == True:

            self.infofield.insert('1.0', "Error encountered! \n\nPress 'Back to Start' to restart the process.\n\n")

            self.cancel.destroy()

            # Add a "Done" button

            self.done = tk.Button(self, text = 'Exit', fg = 'black', state='disabled')

            self.done.grid(row=7, column=2, sticky="W", padx=5, pady=(5, 0))

        else:

            self.infofield.insert('1.0', "Process finished successfully! \n\nPress 'Exit' to close the window or 'Back to Start' to start a new process.\n\n")

            self.cancel.destroy()

            # Add a "Done" button

            self.done = tk.Button(self, text = 'Exit', fg = 'black')

            self.done.grid(row=7, column=2, sticky="W", padx=5, pady=(5, 0))

 

 

class secondLayer(MonaLisaGUI):

    """ Layer specific to the process """

    def __init__(self, master):

        super().__init__(master)

 

    def show_second_layer(self):

        """ Show the specific elements to the user, when the second option

        in the first layer was chosen

        """

        self.choice = '2'

        # Add labels for the first layer

        self.first_label = tk.Label(self, text=self.gui_dict[self.choice]["choice"], font=("Liberation Mono", 10, "bold"))

        self.first_label.grid(row=1, column=1, sticky="W", padx=5, pady=(5, 0))

        # Text asking the user for an action

        self.dir_path_label = tk.Label(self, text=self.gui_dict[self.choice]["text_input"])

        self.dir_path_label.grid(row=2, column=1, sticky="W", padx=5, pady=(5, 0))

        # Add "Back"-Button in the corner

        self.back = tk.Button(self, text = 'Back to Start', fg = 'black')

        self.back.grid(row=2, column=2, sticky="E", padx=5, pady=(5, 0))

        # Add text bar to display the chosen path

        self.dirinput = tk.Text(self, height=1)#, width = 70)

        self.dirinput.grid(row=3, column=1, sticky="W", padx=5, pady=(5, 0))

        self.dirinput.insert(tk.END, "Select the folder ...")

        # Add button to search for path

        self.browseinfolder = tk.Button(self, text = 'Browse', fg = 'black')

        self.browseinfolder.grid(row=3, column=2, sticky="W", padx=5, pady=(5, 0))

 

    def reset_widgets(self):

        """ Remove all widgets and go back to the first page """

        for widget in self.winfo_children():

            widget.destroy()

 

    def browse_input_folder(self):

        """ Open a window to select the directory from the Explorer """

        self.dirinname = filedialog.askdirectory(parent=self.root, mustexist = True, title='Select your folder')

        if self.dirinname:

            self.dirinput.delete('1.0', tk.END)

            self.dirinput.insert('1.0', self.dirinname)

 

    def show_file_path(self):

        """ Add text field and Search button to obtain the file path """

        self.dir_path_label2 = tk.Label(self, text=self.gui_dict[self.choice]["as"])

        self.dir_path_label2.grid(row=4, column=1, sticky="W", padx=5, pady=(5, 0))

        # Add text bar displaying the file path

        self.dir2 = tk.Text(self, height=1)#, width = 70)

        self.dir2.grid(row=5, column=1, sticky="W", padx=5, pady=(5, 0))

        self.dir2.insert(tk.END, "Select the text file cont values ...")

        # Add Search button

        self.browsen = tk.Button(self, text = 'Browse', fg = 'black')

        self.browsen.grid(row=5, column=2, sticky="W", padx=5, pady=(5, 0))

 

    def browse_n_file(self):

        """ Open a window to select the file from the Explorer """

        self.n_filename = filedialog.askopenfilename(filetypes=(("Text files", "*.txt"), ("CSV files", "*.csv")), parent = self, title="Select text file")

        self.dir2.delete('1.0', tk.END)

        self.dir2.insert('1.0', self.n_filename)

 

    def show_output_file_path(self, self_path):

        """ Show the elements for """

        self.diroutname = self_path

        self.dir_path_label_output = tk.Label(self, text=self.gui_dict[self.choice]["text_output"])

        self.dir_path_label_output.grid(row=6, column=1, sticky="W", padx=5, pady=(5, 0))

        # Add text bar to display the chosen path for the output folder

        self.diroutput = tk.Text(self, height=1)#, width = 70)

        self.diroutput.grid(row=7, column=1, sticky="W", padx=5, pady=(5, 0))

        self.diroutput.insert(tk.END, self.diroutname)

        # Add button to search for path

        self.browseoutfolder = tk.Button(self, text = 'Browse', fg = 'black')

        self.browseoutfolder.grid(row=7, column=2, sticky="W", padx=5, pady=(5, 0))

        # Add text field showing the progress

        self.infofield = tk.Text(self, height=20, font=("Verdana", "8"))

        self.infofield.grid(row=8, column=1, sticky="WE", padx=5, pady=(5, 0))

        self.infofield.insert(tk.END, " \n\nPress 'Start' to start... ")

        # Create a Scrollbar and associate it with txt

        self.scrollb = tk.Scrollbar(self, command=self.infofield.yview)

        self.scrollb.grid(row=8, column=2, sticky='NSW')

        self.infofield['yscrollcommand'] = self.scrollb.set

        # Add "Start" button after completing the forms

        self.start = tk.Button(self, text = 'Start', fg = 'black')

        self.start.grid(row=9, column=2, sticky="W", padx=5, pady=(5, 0))

 

    def browse_output_folder(self):

        """ Open a window to select the directory from the Explorer """

        self.diroutname = filedialog.askdirectory(parent=self.root, initialdir=self.diroutname, title='Select your output folder')

        if self.diroutname:

            self.diroutput.delete('1.0', tk.END)

            self.diroutput.insert('1.0', self.diroutname)

 

    def start_process(self):

        """ Show progress in a text field """

        # Replace the Start button with the Exit/Cancel button

        self.start.destroy()

        # Add a cancel button underneath

        self.cancel = tk.Button(self, text = 'Cancel', fg = 'black')

        self.cancel.grid(row=9, column=2, sticky="W", padx=5, pady=(5, 0))

        # Add text depending on the process running

        self.infofield.delete('1.0', tk.END)

        self.infofield.insert('1.0', "his might take a few minutes ...")

 

    def build_progress_bar(self, maximum):

        """ Build the progress bar """

        self.progressbar = ttk.Progressbar(self, orient=tk.HORIZONTAL,

                                           mode="determinate",

                                           maximum=maximum)

        self.progressbar.grid(row=9, column=1, sticky='WE', padx=5, pady=(5, 0))

 

    def write_line(self, msg):

        """ Writes the log to the gui text field """

        self.infofield.insert('1.0', msg)

 

    def update_progress_bar(self, value):

        """ Updates the progress """

        self.progressbar["value"] = value

 

    def throw_error(self, msg):

        """ If an error encountered, display it in a message box """

        tk.messagebox.showerror("Error", msg)

        self.error = True

 

    def final_elements(self, max):

        """ Adds final elements """

        # Stops the progress bar and destroy it

        self.progressbar.stop()

        self.progressbar.configure(mode="determinate", value=max)

        if self.error == True:

            self.infofield.insert('1.0', "Error encountered! \n\nPress 'Back to Start' to restart the process.\n\n")

            self.cancel.destroy()

            # Add a "Done" button

            self.done = tk.Button(self, text = 'Exit', fg = 'black', state='disabled')

            self.done.grid(row=9, column=2, sticky="W", padx=5, pady=(5, 0))

        else:

            self.infofield.insert('1.0', "Process finished successfully! \n\nPress 'Exit' to close the window or 'Back to Start' to start a new process.\n\n")

            self.cancel.destroy()

            # Add a "Done" button

            self.done = tk.Button(self, text = 'Exit', fg = 'black')

            self.done.grid(row=9, column=2, sticky="W", padx=5, pady=(5, 0))

 

 

 