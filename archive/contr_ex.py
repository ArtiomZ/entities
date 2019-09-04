

import os

import time

import threading

import webbrowser

 

from tkinter import Tk

 

from point_executadas_Snoring import pointConsolidator

from point_tax_match import point_tax_match

from gui_view import MonaLisaGUI, WelcomeLayer, SnoringLayer, SleepingLayer

 

class Controller():

 

    __version__ = "0.2.2"

 

    def __init__(self, Gui):

        self.Gui = Gui

        self.WelcomeLayer = WelcomeLayer(root)

        self.task = None

        self.retry = False

        self.configure_buttons()

        self.maximum = 100

 

    def configure_buttons(self):

        self.WelcomeLayer.browse1.config(command=self.show_Snoring_layer)

        self.WelcomeLayer.browse2.config(command=self.show_Sleeping_layer)

        self.WelcomeLayer.help.config(command=self.open_help_file)

 

    def open_help_file(self):

        """ Open the User Guide html file in a webbrowser """

        ie = webbrowser.get(webbrowser.iexplore)

        ie.open(os.path.join(os.getcwd(), "README.html"))

 

    def back_to_start(self):

        if self.task == 1:

            self.Snoring.reset_widgets()

        else:

            self.Sleeping.reset_widgets()

        self.__init__(self.Gui)

 

    def show_Snoring_layer(self):

        self.task = 1

        self.Snoring = SnoringLayer(root)

        self.WelcomeLayer.reset_widgets()

        self.Snoring.show_Snoring_layer()

        self.Snoring.browseinfolder.config(command=self.load_Snoring_elements)

        self.Snoring.back.config(command=self.back_to_start)

 

    def load_Snoring_elements(self):

        self.Snoring.browse_input_folder()

        self.Snoring.show_output_file_path(os.getcwd())

        self.Snoring.browseoutfolder.config(command=self.Snoring.browse_output_folder)

        self.Snoring.start.config(command=self.start_process)

 

    def show_Sleeping_layer(self):

        self.task = 2

        self.Sleeping = SleepingLayer(root)

        self.WelcomeLayer.reset_widgets()

        self.Sleeping.show_Sleeping_layer()

        self.Sleeping.browseinfolder.config(command=self.find_input_file)

        self.Sleeping.back.config(command=self.back_to_start)

 

    def find_input_file(self):

        """ Let the user choose the input file """

        self.Sleeping.browse_input_folder()

        self.Sleeping.show_arn_file_path()

        self.Sleeping.browsearn.config(command=self.load_Sleeping_elements)

        self.retry = True

 

    def load_Sleeping_elements(self):

        self.Sleeping.browse_arn_file()

        self.Sleeping.show_output_file_path(os.getcwd())

        self.Sleeping.browseoutfolder.config(command=self.Sleeping.browse_output_folder)

        self.Sleeping.start.config(command=self.start_process)

 

    def start_process(self):

        if self.task == 1:

            self.Snoring.start.config(state="disabled")

            self.Snoring.back.config(state="disabled")

            self.Snoring.browseinfolder.config(state="disabled")

            self.Snoring.browseoutfolder.config(state="disabled")

            self.Snoring.start_process()

            self.start_Snoring()

        else:

            self.Sleeping.start.config(state="disabled")

            self.Sleeping.back.config(state="disabled")

            self.Sleeping.browsearn.config(state="disabled")

            self.Sleeping.browseinfolder.config(state="disabled")

            self.Sleeping.browseoutfolder.config(state="disabled")

            self.Sleeping.start_process()

            self.start_Sleeping()

 

    def start_Snoring(self):

        """ Start the Snoring process

        by initiating a progress bar and calling

        the background model in a separate thread

        """

        self.input_folder = self.Snoring.dirinname

        self.output_folder = self.Snoring.diroutname

        self.Snoring.build_progress_bar(maximum=self.maximum)

        SnoringProcess(self, self.Gui, self.Snoring, self.input_folder, self.output_folder, self.maximum)

        self.Snoring.cancel.config(command=self.Gui.quit)

 

    def start_Sleeping(self):

        """ Start the Sleeping process

        by initiating a progress bar and calling

        the background model in a separate thread

        """

        self.input_folder = self.Sleeping.dirinname

        self.arn_filename = self.Sleeping.arn_filename

        self.output_folder = self.Sleeping.diroutname

        self.Sleeping.build_progress_bar(maximum=self.maximum)

        SleepingProcess(self, self.Gui, self.Sleeping, self.input_folder, self.arn_filename, self.output_folder, self.maximum)

        self.Sleeping.cancel.config(command=self.Gui.quit)

 

    def finish_up_Snoring(self):

        self.Snoring.back.config(state="normal")

        self.Snoring.final_elements(self.maximum)

        self.Snoring.done.config(command=self.Gui.quit)

        self.Snoring.back.config(command=self.back_to_start)

 

    def finish_up_Sleeping(self):

        self.Sleeping.back.config(state="normal")

        self.Sleeping.final_elements(self.maximum)

        self.Sleeping.done.config(command=self.Gui.quit)

        self.Sleeping.back.config(command=self.back_to_start)

 

 

class SnoringProcess(threading.Thread):

    """ Threaded Snoring process """

    def __init__(self, Controller, Gui, Snoring, dirinname, diroutname, maximum):

        threading.Thread.__init__(self)

        self.Controller = Controller

        self.Snoring = Snoring

        self.dirinname = dirinname

        self.diroutname = diroutname

        self.start()



 

    def run(self):

        """ Start the background process """

        try:

            self.Cons = pointConsolidator(input_dir=self.dirinname,

                                             output_dir=self.diroutname,

                                             msgCallback=self.print_message,

                                             progressCallback=self.update_progressbar)

            self.Cons.pull()

        finally:

            self.Controller.finish_up_Snoring()

            self.Cons.remove_handlers()

 

    def print_message(self, msg):

        """ Write the log message to a text box """

        if '[ERROR]' in msg:

            self.throw_error(msg)

        else:

            self.Snoring.write_line(str(msg) + '\n')

 

    def throw_error(self, msg):

        """ Throw an error to the screen and cancel the process"""

        self.Snoring.throw_error(str(msg))

 

    def update_progressbar(self, perc):

        """ Update the progress bar in the view using the current progress in % """

        #self.perc = perc

        self.Snoring.update_progress_bar(perc)

 

 

class SleepingProcess(threading.Thread):

    """ Threaded Sleeping process """

    def __init__(self, Controller, Gui, Sleeping, dirinname, arn_filename, diroutname, maximum):

        threading.Thread.__init__(self)

        self.Controller = Controller

        self.Sleeping = Sleeping

        self.dirinname = dirinname

        self.arn_filename = arn_filename

        self.diroutname = diroutname

        self.start()

 

    def run(self):

        """ Start the background process """

        try:

            self.Rec = point_tax_match(_pulld_input=self.dirinname,

                                          _arn_input=self.arn_filename,

                                          _output_path=self.diroutname,

                                          msgCallback=self.print_message,

                                          progressCallback=self.update_progressbar)

            self.Rec.tax_match(self.Rec.input_file_info())

        # except TypeError as exception:

        #     pass

        finally:

            # Initiate the last Gui layer when the process has finished

            self.Controller.finish_up_Sleeping()

            self.Rec.remove_handlers()

 

    def print_message(self, msg):

        """ Write the log message to a text box """

        if '[ERROR]' in msg:

            self.throw_error(msg)

        else:

            self.Sleeping.write_line(str(msg) + '\n')

 

    def throw_error(self, msg):

        """ Throw an error to the screen and cancel the process"""

        self.R.throw_error(str(msg))

 

    def update_progressbar(self, perc):

        """ Update the progress bar in the view using the current progress in % """

        self.R.update_progress_bar(perc)

 

 

if __name__ == '__main__':

    root = Tk()

    root.title("MonaLisa")

    root.geometry('780x580')

    Gui = MonaLisaGUI(master=root)

    Application = Controller(Gui)

    root.mainloop()

    root.destroy()