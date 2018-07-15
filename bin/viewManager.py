"""controls the games visuals and interaction with adventureManager"""
"""import and global variable declaration"""
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import tkFont
import os
from adventureManager import *

content_space_width = 400
button_height = 100
button_font_size = 24
heading_font_size = 36
small_fontsize = 16
font_type = 'Helvetica'

global heading_font
global small_font

"""class for initialising Tk and frame management"""
class StarterApp(Tk):
    def __init__(self):
        Tk.__init__(self)
        self._frame = None
        self.title('Text Adventure Hub')
        self.resizable(width=False, height=False)
        self.setup_textsize()
        self.switch_frame(StartPage(self))

        init_logic()

    def setup_textsize(self):
        global heading_font
        heading_font = tkFont.Font(family=font_type, size=heading_font_size)
        global small_font
        small_font = tkFont.Font(family=font_type, size = small_fontsize)
        #https://stackoverflow.com/questions/37068708/how-to-change-font-size-in-ttk-button
        s = ttk.Style()
        s.configure('my.TButton', font =(font_type, button_font_size))

    def switch_frame(self, frame):
        """Destroys current frame and replaces it with a new one."""
        if self._frame is not None:
            self._frame.destroy()
        if frame is not None:
            self._frame = frame
            self._frame.pack()


"""startpage view"""


class StartPage(ttk.Frame):
    def __init__(self, master):
        ttk.Frame.__init__(self, master)

        """ ########### """
        """ GUI aspects """
        """ ########### """

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
        select_adventure_frame = ttk.Frame(content_frame, width = content_space_width, height = button_height)
        select_adventure_frame.propagate(0)
        select_adventure_frame.grid(row=1)

        #frame for load_savegame_button
        load_savegame_frame = ttk.Frame(content_frame, width = content_space_width, height = button_height)
        load_savegame_frame.propagate(False)
        load_savegame_frame.grid(row=2, pady = 75)

        #frame for import_adventure_button
        import_adventure_frame = ttk.Frame(content_frame, width = content_space_width, height = button_height)
        import_adventure_frame.propagate(False)
        import_adventure_frame.grid(row=3)

        """setting up inner widgets"""
        # setting up inner widgets and assigning them to the already created frames

        heading_label = ttk.Label(heading_frame, text='Text Adventure Hub', font = heading_font, anchor = W)
        heading_label.pack(expand = True)

        #redirects to SelectAdventurePage
        select_adventure_button = ttk.Button(select_adventure_frame, text="Select Adventure", style = 'my.TButton',
                                  command=lambda: master.switch_frame(SelectAdventurePage(master)))
        select_adventure_button.pack(expand = 1, fill = BOTH)

        #redirects to SelectSavegamePage
        load_savegame_button = ttk.Button(load_savegame_frame, text="Load Savegame", style = 'my.TButton',
                                  command=lambda: master.switch_frame(SelectSavegamePage(master)))
        load_savegame_button.pack(expand = 1, fill = BOTH)

        #import button opens adventures folder in explorer by using open_adventures_folder() method from adventureManager
        import_adventure_button = ttk.Button(import_adventure_frame, text="Import Adventure", style = 'my.TButton',
                                  command=lambda: open_adventures_folder())
        import_adventure_button.pack(expand = 1, fill = BOTH)


"""adventure selection view"""


class SelectAdventurePage(ttk.Frame):
    def __init__(self, master):
        ttk.Frame.__init__(self, master)

        """ ########### """
        """ GUI aspects """
        """ ########### """

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
        back_button = ttk.Button(content_frame, text = "Back", command=lambda: master.switch_frame(StartPage(master)))
        back_button.grid(row=2, sticky = W)

        #! This Button need the correct 'command' assignment !#
        start_button = ttk.Button(content_frame, text = "Start", command=lambda: start_adventure())
        start_button.grid(row=2, sticky = E)

        """ ################# """
        """ Logic integration """
        """ ################# """

        #using adventureManager method get_adventure_list() to populate listbox
        anames = StringVar(value = get_adventure_list())

        #create and populate listbox
        adventures_listbox = Listbox(adventures_frame, listvariable = anames, font = small_font, selectmode = SINGLE)
        adventures_listbox.pack(expand = True, fill = BOTH)

        #creating scrollbar and assigning it to listbox
        adventure_scrollbar = ttk.Scrollbar(content_frame, orient = VERTICAL, command=adventures_listbox.yview)
        adventures_listbox.configure(yscrollcommand=adventure_scrollbar.set)
        adventure_scrollbar.grid(row = 1, column = 0, sticky = 'ens', pady = 25)

        def start_adventure():
            index = adventures_listbox.curselection()
            if not index:
                None
            else:
                adventure_name = adventures_listbox.get(index[0])
                load_adventure(adventure_name)
                set_next_chapter(0)
                master.switch_frame(AdventurePage(master))


"""savegame selection view"""


class SelectSavegamePage(ttk.Frame):
    def __init__(self, master):
        ttk.Frame.__init__(self, master)

        """ ########### """
        """ GUI aspects """
        """ ########### """

        content_frame = ttk.Frame(self)
        content_frame.grid()
        content_frame['padding'] = (150, 100, 150, 100)


        """setting up wrapping frames"""
        # https://stackoverflow.com/questions/46284901/how-do-i-resize-buttons-in-pixels-tkinter
        # widget have to be wrapped into frames for size management, so the size of the frame controls the size of its inner widget

        heading_frame = ttk.Frame(content_frame, width = 600, height = 150, relief = 'groove')
        heading_frame.propagate(False)
        heading_frame.grid(row=0)

        savegame_display_frame = ttk.Frame(content_frame, width = 600-17, height = 450 , relief = 'groove')
        savegame_display_frame.propagate(False)
        savegame_display_frame.grid(row=1, column = 0, pady = 25, sticky = W)

        """setting up inner widgets"""
        # setting up inner widgets and assigning them to the already created frames

        heading_label = ttk.Label(heading_frame, text='Savegame Selection', font = heading_font, anchor = W)
        heading_label.pack(expand = True)

        back_button = ttk.Button(content_frame, text = 'Back', command=lambda: master.switch_frame(StartPage(master)))
        back_button.grid(row=2, sticky = W)

        delete_button = ttk.Button(content_frame, text = 'Delete', command=lambda: delete_selected_savegame())
        delete_button.grid(row=2)

        load_button = ttk.Button(content_frame, text = 'Load', command=lambda: load_selected_savegame())
        load_button.grid(row=2, sticky = E)


        """ ################# """
        """ Logic integration """
        """ ################# """

        #create and populate Listbox and add Scrollbar

        #using adventureManager method get_savegame_list() to polulate listbox
        snames = StringVar(value = get_savegame_list())

        savegames_listbox = Listbox(savegame_display_frame, listvariable = snames, font = small_font, selectmode = SINGLE)
        savegames_listbox.pack(expand = True, fill = BOTH)

        adventure_scrollbar = ttk.Scrollbar(content_frame, orient = VERTICAL, command=savegames_listbox.yview)
        savegames_listbox.configure(yscrollcommand=adventure_scrollbar.set)
        adventure_scrollbar.grid(row = 1, column = 0, sticky = 'ens', pady = 25)


        '''button functionality'''

        #savegame-load functionality for button
        def load_selected_savegame():
            index = savegames_listbox.curselection()
            if not index:
                None
            else:
                savegame_name = savegames_listbox.get(index[0])
                load_savegame(savegame_name) #function from adventureManager
                master.switch_frame(AdventurePage(master))

        def delete_selected_savegame():
            index = savegames_listbox.curselection()
            if not index:
                None
            else:
                if messagebox.askyesno(message='Wollen Sie den Spielstand entgueltig loeschen?') is True:
                    savegame_name = savegames_listbox.get(index[0])
                    delete_savegame(savegame_name)
                    #update_lists


"""Adventure view"""


class AdventurePage(ttk.Frame):

    def __init__(self, master):
        ttk.Frame.__init__(self, master)

        self.follower = get_follower()

        """ ########### """
        """ GUI aspects """
        """ ########### """

        content_frame = ttk.Frame(self)
        content_frame.grid()
        content_frame['padding'] = (70, 100, 75, 100)

        """setting up wrapping frames"""
        # https://stackoverflow.com/questions/46284901/how-do-i-resize-buttons-in-pixels-tkinter
        # widget have to be wrapped into frames for size management, so the size of the frame controls the size of its inner widget

        text_frame = ttk.Frame(content_frame, width = 600-17, height = 150*3 , relief = 'groove')
        text_frame.propagate(False)
        text_frame.grid(row=0, column = 1, sticky = W)

        inventory_frame = ttk.Frame(content_frame, width = 150, height = 450)
        inventory_frame.propagate(False)
        inventory_frame.grid(row=0, column = 0)

        inventory_heading_frame = ttk.Frame(inventory_frame, width = 150, height = 50 , relief = 'groove')
        inventory_heading_frame.propagate(False)
        inventory_heading_frame.grid(row=0, column = 0, columnspan = 2, sticky = N)

        inventory_list_frame = ttk.Frame(inventory_frame, width = 150-17, height = 400-17, relief = 'groove')
        inventory_list_frame.propagate(False)
        inventory_list_frame.grid(row=1, column = 0, sticky = NW)

        backandsave_frame = ttk.Frame(content_frame, relief = 'groove')
        backandsave_frame.grid(row=0, column = 2, sticky = N)

        option_one_frame = ttk.Frame(content_frame, width = 600, height = button_height/2)
        option_one_frame.propagate(0)
        option_one_frame.grid(row=2, column = 1,  pady = 20)

        option_two_frame = ttk.Frame(content_frame, width = 600, height = button_height/2)
        option_two_frame.propagate(0)
        option_two_frame.grid(row=3, column = 1)

        option_three_frame =ttk.Frame(content_frame, width = 600, height = button_height/2)
        option_three_frame.propagate(0)
        option_three_frame.grid(row=4, column = 1, pady = 20)

        """button creation"""
        if len(self.follower) >= 1:
            option_one_button = ttk.Button(option_one_frame, text="Test1", style = 'my.TButton', command=lambda: progress_in_story(self.follower[0]))
            option_one_button.pack(expand = 1, fill = BOTH)

        if len(self.follower) >= 2:
            option_two_button = ttk.Button(option_two_frame, text="Test2", style = 'my.TButton', command=lambda: progress_in_story(self.follower[1]))
            option_two_button.pack(expand = 1, fill = BOTH)

        if len(self.follower) >= 3:
            option_three_button = ttk.Button(option_three_frame, text="Test3", style = 'my.TButton', command=lambda: progress_in_story(self.follower[2]))
            option_three_button.pack(expand = 1, fill = BOTH)

        """setting up inner widgets"""
        # setting up inner widgets and assigning them to the already created frames

        inventory_heading = ttk.Label(inventory_heading_frame, text='Inventory', font = small_font, anchor = W)
        inventory_heading.pack(expand = True)

        exit_button = ttk.Button(backandsave_frame, text = 'Exit', command=lambda: exit_adventure())
        exit_button.pack()

        #! This Button need the correct 'command' assignment !#
        save_button = ttk.Button(backandsave_frame, text = 'Save', command=lambda: save_progress())
        save_button.pack()


        """ ################# """
        """ Logic integration """
        """ ################# """


        inames = StringVar(value = tuple(get_inventory()))

        inventory_listbox = Listbox(inventory_list_frame, listvariable = inames, font = small_font)
        inventory_listbox.pack(expand = True, fill = BOTH)

        inventory_y_scrollbar = ttk.Scrollbar(inventory_frame, orient = VERTICAL, command=inventory_listbox.yview)
        inventory_listbox.configure(yscrollcommand=inventory_y_scrollbar.set)
        inventory_y_scrollbar.grid(row = 1, column = 1, sticky = 'ns')

        inventory_x_scrollbar = ttk.Scrollbar(inventory_frame, orient = HORIZONTAL, command=inventory_listbox.xview)
        inventory_listbox.configure(xscrollcommand=inventory_x_scrollbar.set)
        inventory_x_scrollbar.grid(row = 12, column = 0, sticky = 'swe')

        #create and populate textfield
        adventure_text = Text(text_frame, width = 40, height = 10, wrap = 'word', font = small_font, state = DISABLED)
        adventure_text.pack(expand = True, fill = BOTH)

        #creating scrollbar and assigning it to textfield
        adventure_scrollbar = ttk.Scrollbar(content_frame, orient = VERTICAL, command=adventure_text.yview)
        adventure_text.configure(yscrollcommand=adventure_scrollbar.set)
        adventure_scrollbar.grid(row = 0, column = 1, sticky = 'ens')

        adventure_text['state'] = 'normal'
        adventure_text.delete('1.0', '2.0')
        adventure_text.insert('1.0', get_chapter_text())
        adventure_text['state'] = 'disabled'

        #handles next step in adventure -> inventory handling should be moved to adventureManager
        def progress_in_story(next_chapter):
            set_next_chapter(next_chapter)
            master.switch_frame(AdventurePage(master))

        #for save button
        def save_progress(): #use adventure_name, chapter, inventory_list as parameters
            save_game()
            messagebox.showinfo('game saved', 'Das Spiel wurde gespeichert')

        #for exit button
        def exit_adventure():
            if messagebox.askyesno(message='Ungespeicherter Spielstand geht verloren, trotzdem fortfahren?') is True:
                master.switch_frame(StartPage(master))

if __name__ == "__main__":
    app = StarterApp()
    app.mainloop()
