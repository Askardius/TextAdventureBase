"""controls the games visuals and interaction with adventureManager"""
"""import and global variable declaration"""
from tkinter import *
from tkinter import ttk
import Tkinter as tk
import tkFont
import os
from adventureManager import *

button_width = 400
button_height = 100
button_font_size = 24
heading_font_size = 36
small_fontsize = 16
font_type = 'Helvetica'

global heading_font
global small_font

"""class for initialising Tk and frame management"""
class StarterApp(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self._frame = None
        self.minsize(1000,1000) #https://stackoverflow.com/questions/21958534/how-can-i-prevent-a-window-from-being-resized-with-tkinter
        self.title("Text Adventure Base")
        self.resizable(width=False, height=False)
        self.setup_textsize()
        self.switch_frame(StartPage)

    def setup_textsize(self):
        global heading_font
        heading_font = tkFont.Font(family=font_type, size=heading_font_size)
        global small_font
        small_font = tkFont.Font(family=font_type, size = small_fontsize)
        #https://stackoverflow.com/questions/37068708/how-to-change-font-size-in-ttk-button
        s = ttk.Style()
        s.configure('my.TButton', font =(font_type, button_font_size))

    def switch_frame(self, frame_class):
        """Destroys current frame and replaces it with a new one."""
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack()


"""startpage view"""


class StartPage(ttk.Frame):
    def __init__(self, master):
        ttk.Frame.__init__(self, master)

        content_frame = ttk.Frame(self)
        content_frame.grid()
        content_frame['padding'] = (150, 25, 150, 100)

        """setting up wrapping frames"""
        # https://stackoverflow.com/questions/46284901/how-do-i-resize-buttons-in-pixels-tkinter
        # widget have to be wrapped into frames for size management, so the size of the frame controls the size of its inner widget

        heading_frame = ttk.Frame(content_frame, width = 600, height = 150, relief = 'groove')
        heading_frame.propagate(0)
        heading_frame.grid(row=0, pady = 75)

        #frame for select_adventure_button
        select_adventure_frame = ttk.Frame(content_frame, width = button_width, height = button_height)
        select_adventure_frame.propagate(0)
        select_adventure_frame.grid(row=1)

        #frame for load_savegame_button
        load_savegame_frame = ttk.Frame(content_frame, width = button_width, height = button_height)
        load_savegame_frame.propagate(False)
        load_savegame_frame.grid(row=2, pady = 75)

        #frame for import_adventure_button
        import_adventure_frame = ttk.Frame(content_frame, width = button_width, height = button_height)
        import_adventure_frame.propagate(False)
        import_adventure_frame.grid(row=3)

        """setting up inner widgets"""
        # setting up inner widgets and assigning them to the already created frames

        heading_label = ttk.Label(heading_frame, text='Text Adventure Base', font = heading_font, anchor = W)
        heading_label.pack(expand = True)

        #redirects to SelectAdventurePage
        select_adventure_button = ttk.Button(select_adventure_frame, text="Select Adventure", style = 'my.TButton',
                                  command=lambda: master.switch_frame(SelectAdventurePage))
        select_adventure_button.pack(expand = 1, fill = tk.BOTH)

        #redirects to SelectSavegamePage
        load_savegame_button = ttk.Button(load_savegame_frame, text="Load Savegame", style = 'my.TButton',
                                  command=lambda: master.switch_frame(SelectSavegamePage))
        load_savegame_button.pack(expand = 1, fill = tk.BOTH)

        #import button opens adventures folder in explorer by using open_adventures_folder() method from adventureManager
        import_adventure_button = ttk.Button(import_adventure_frame, text="Import Adventure", style = 'my.TButton',
                                  command=lambda: open_adventures_folder())
        import_adventure_button.pack(expand = 1, fill = tk.BOTH)


"""adventure selection view"""


class SelectAdventurePage(ttk.Frame):
    def __init__(self, master):
        ttk.Frame.__init__(self, master)

        content_frame = ttk.Frame(self)
        content_frame.grid()
        content_frame['padding'] = (150, 100, 150, 100)

        """setting up wrapping frames"""
        # https://stackoverflow.com/questions/46284901/how-do-i-resize-buttons-in-pixels-tkinter
        # widget have to be wrapped into frames for size management, so the size of the frame controls the size of its inner widget

        heading_frame = ttk.Frame(content_frame, width = 600, height = 150, relief = 'groove')
        heading_frame.propagate(False)
        heading_frame.grid(row=0)

        adventures_frame = ttk.Frame(content_frame, width = 600-17, height = 150*3 , relief = 'groove')
        adventures_frame.propagate(False)
        adventures_frame.grid(row=1, column = 0, pady = 25, sticky = W)


        """setting up inner widgets"""
        # setting up inner widgets and assigning them to the already created frames

        heading_label = ttk.Label(heading_frame, text='Adventure Selection', font = heading_font, anchor = W)
        heading_label.pack(expand = True)

        #using standard sized buttons so they don't have to be wrapped
        back_button = ttk.Button(content_frame, text = "Back", command=lambda: master.switch_frame(StartPage))
        back_button.grid(row=2, sticky = W)

        #! This Button need the correct 'command' assignment !#
        start_button = ttk.Button(content_frame, text = "Start", command=lambda: master.switch_frame(StartPage))
        start_button.grid(row=2, sticky = E)

        #load_all_adventures() #uncomment to test what population looks like - don't use in final version

        #using adventureManager method get_adventure_list() to populate listbox
        anames = StringVar(value = get_adventure_list())

        #create and populate listbox
        adventures_listbox = Listbox(adventures_frame, listvariable = anames, font = small_font)
        adventures_listbox.pack(expand = True, fill = BOTH)

        #creating scrollbar and assigning it to listbox
        adventure_scrollbar = ttk.Scrollbar(content_frame, orient = VERTICAL, command=adventures_listbox.yview)
        adventures_listbox.configure(yscrollcommand=adventure_scrollbar.set)
        adventure_scrollbar.grid(row = 1, column = 0, sticky = 'ens', pady = 25)


"""savegame selection view"""


class SelectSavegamePage(ttk.Frame):
    def __init__(self, master):
        ttk.Frame.__init__(self, master)

        content_frame = ttk.Frame(self)
        content_frame.grid()
        content_frame['padding'] = (150, 100, 150, 100)

        """setting up wrapping frames"""
        # https://stackoverflow.com/questions/46284901/how-do-i-resize-buttons-in-pixels-tkinter
        # widget have to be wrapped into frames for size management, so the size of the frame controls the size of its inner widget

        heading_frame = ttk.Frame(content_frame, width = 600, height = 150, relief = 'groove')
        heading_frame.propagate(False)
        heading_frame.grid(row=0)

        savegame_display_frame = ttk.Frame(content_frame, width = 600-17, height = 150*3 , relief = 'groove')
        savegame_display_frame.propagate(False)
        savegame_display_frame.grid(row=1, column = 0, pady = 25, sticky = W)

        """setting up inner widgets"""
        # setting up inner widgets and assigning them to the already created frames

        heading_label = ttk.Label(heading_frame, text='Savegame Selection', font = heading_font, anchor = W)
        heading_label.pack(expand = True)

        back_button = ttk.Button(content_frame, text = "Back", command=lambda: master.switch_frame(StartPage))
        back_button.grid(row=2, sticky = W)

        #! This Button need the correct 'command' assignment !#
        load_button = ttk.Button(content_frame, text = "Start", command=lambda: master.switch_frame(StartPage))
        load_button.grid(row=2, sticky = E)

        #! This Button need the correct 'command' assignment !#
        delete_button = ttk.Button(content_frame, text = "Delete", command=lambda: master.switch_frame(StartPage))
        delete_button.grid(row=2)

        #load_all_savegames() #uncomment to test what population looks like - don't use in final version

        #using adventureManager method get_savegame_list() to polulate listbox
        snames = StringVar(value = get_savegame_list())

        #create and populate Listbox
        savegames_listbox = Listbox(savegame_display_frame, listvariable = snames, font = small_font)
        savegames_listbox.pack(expand = True, fill = BOTH)

        #creating scrollbar and assigning it to Listbox
        adventure_scrollbar = ttk.Scrollbar(content_frame, orient = VERTICAL, command=savegames_listbox.yview)
        savegames_listbox.configure(yscrollcommand=adventure_scrollbar.set)
        adventure_scrollbar.grid(row = 1, column = 0, sticky = 'ens', pady = 25)

if __name__ == "__main__":
    app = StarterApp()
    app.mainloop()
