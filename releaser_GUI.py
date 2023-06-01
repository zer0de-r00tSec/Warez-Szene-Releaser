#! /usr/bin/env python3
# -*- coding: utf-8 -*-
#
#
# ToDo
# Improve error handling -> output to the log
#     raise Exception("Packing failed")
# Exception: Packing failed
#
# GUI Updaten, Config bereich etc. dupe APIs adden ...
#
#
#

import tkinter as tk
from tkinter import filedialog
import tkinter.ttk as ttk
import sys,os
import subprocess
import configparser

# HELPER FiLES
import releaser_support

_script = sys.argv[0]
_location = os.path.dirname(_script)

___AUTHOR___  = 'zer0.de^r00tSec'
___VERSION___ = '2.0'

_bgcolor = '#d9d9d9'  # X11 color: 'gray85'
_fgcolor = '#000000'  # X11 color: 'black'
_compcolor = '#d9d9d9' # X11 color: 'gray85'
_ana1color = '#ececec' # Closest X11 color: 'gray92'
_bgmode = 'light' 

_DEBUG = 0

_style_code_ran = 0
def _style_code():
    global _style_code_ran
    if _style_code_ran:
       return
    style = ttk.Style()
    if sys.platform == "win32":
       style.theme_use('winnative')
    style.configure('.',background=_bgcolor)
    style.configure('.',foreground=_fgcolor)
    style.configure('.',font='TkDefaultFont')
    style.map('.',background =
       [('selected', _compcolor), ('active',_ana1color)])
    if _bgmode == 'dark':
       style.map('.',foreground =
         [('selected', 'white'), ('active','white')])
    else:
       style.map('.',foreground =
         [('selected', 'black'), ('active','black')])
    style.configure('Vertical.TScrollbar',  background=_bgcolor,
        arrowcolor= _fgcolor)
    style.configure('Horizontal.TScrollbar',  background=_bgcolor,
        arrowcolor= _fgcolor)
    _style_code_ran = 1

class main:
    def __init__(self, top=None):
        '''This class configures and populates the toplevel window.
           top is the toplevel containing window.'''

        self.source_file = self.get_last_path("source_file")
        self.source_config = self.get_last_path("config_file")
        self.entrySource = self.get_last_path("input_dir")
        self.entryDest = self.get_last_path("output_dir")

        top.geometry("678x601+609+109")
        top.minsize(1, 1)
        top.maxsize(2545, 1050)
        top.resizable(0,  0)
        top.title(f"Warez/P2P Releaser {___VERSION___}")
        top.configure(highlightcolor="black")

        self.top = top
        self.combobox = tk.StringVar()

        _style_code()
        self.TLabelframe1 = ttk.Labelframe(self.top)
        self.TLabelframe1.place(relx=0.012, rely=0.233, relheight=0.356
                , relwidth=0.975)
        self.TLabelframe1.configure(relief='')
        self.TLabelframe1.configure(text='''main''')
        
        # SOURCE BUTTON
        self.Button1 = tk.Button(self.TLabelframe1)
        self.Button1.place(relx=0.862, rely=0.14, height=21, width=76
                , bordermode='ignore')
        self.Button1.configure(activebackground="#f9f9f9")
        self.Button1.configure(takefocus="6")
        self.Button1.configure(command=self.onselectdir)
        self.Button1.configure(text='''Source''')
        
        # SAVE TO BUTTON
        self.Button2 = tk.Button(self.TLabelframe1)
        self.Button2.place(relx=0.862, rely=0.327, height=21, width=76
                , bordermode='ignore')
        self.Button2.configure(activebackground="#f9f9f9")
        self.Button2.configure(takefocus="4")
        self.Button2.configure(command=self.onsavedir)
        self.Button2.configure(text='''Dest''')
        
        # TEXTBOX SOURCE DiR
        self.Entry1 = tk.Entry(self.TLabelframe1)
        self.Entry1.place(relx=0.242, rely=0.14, height=23, relwidth=0.599
                , bordermode='ignore')
        self.Entry1.configure(background="white")
        self.Entry1.configure(font="TkFixedFont")
        self.Entry1.configure(selectbackground="#c4c4c4")
        self.Entry1.configure(takefocus="1")
        self.Entry1.insert(0,f"{self.entrySource}")
        
        
        # TEXTBOX DEST DiR
        self.Entry2 = tk.Entry(self.TLabelframe1)
        self.Entry2.place(relx=0.242, rely=0.327, height=23, relwidth=0.599
                , bordermode='ignore')
        self.Entry2.configure(background="white")
        self.Entry2.configure(font="TkFixedFont")
        self.Entry2.configure(selectbackground="#c4c4c4")
        self.Entry2.configure(takefocus="2")
        self.Entry2.insert(0,f"{self.entryDest}")
        

        # LABEL SOURCE DiR
        self.Label2 = tk.Label(self.TLabelframe1)
        self.Label2.place(relx=0.061, rely=0.14, height=21, width=115
                , bordermode='ignore')
        self.Label2.configure(activebackground="#f9f9f9")
        self.Label2.configure(justify='right')
        self.Label2.configure(text='''Source Directory:''')
        
        # LABEL DEST DiR
        self.Label3 = tk.Label(self.TLabelframe1)
        self.Label3.place(relx=0.015, rely=0.327, height=21, width=148
                , bordermode='ignore')
        self.Label3.configure(activebackground="#f9f9f9")
        self.Label3.configure(justify='right')
        self.Label3.configure(text='''Destination Directory:''')
        

        # LABEL SOURCE OF FiLE
        self.Label4 = tk.Label(self.TLabelframe1)
        self.Label4.place(relx=0.091, rely=0.514, height=21, width=92
                , bordermode='ignore')
        self.Label4.configure(activebackground="#f9f9f9")
        self.Label4.configure(justify='right')
        self.Label4.configure(text='''Source of File:''')


        # LABEL CONFiG SELECT
        self.Label5 = tk.Label(self.TLabelframe1)
        self.Label5.place(relx=0.483, rely=0.514, height=21, width=92
                , bordermode='ignore')
        self.Label5.configure(activebackground="#f9f9f9")
        self.Label5.configure(justify='right')
        self.Label5.configure(text='''Select Config:''')
        

        # COMBOLiST CONFiG
        self.TCombobox1 = ttk.Combobox(self.TLabelframe1)
        self.TCombobox1.place(relx=0.635, rely=0.514, relheight=0.098
                , relwidth=0.208, bordermode='ignore')
        self.TCombobox1.configure(exportselection="0")
        self.TCombobox1.configure(textvariable=self.combobox)
        
        self.configs_found = []
        self.configs_found = self.find_ini_files()
        self.value_list1 = self.configs_found
        self.TCombobox1.configure(values=self.value_list1)
        self.TCombobox1.current(self.source_config)

       
        # COMBOLiST FiLE SOURCE
        self.TCombobox2 = ttk.Combobox(self.TLabelframe1)
        self.TCombobox2.place(relx=0.242, rely=0.514, relheight=0.098
                , relwidth=0.221, bordermode='ignore')
        self.value_list2 = ['WEB','BDRIP','DVDRiP']
        self.TCombobox2.configure(values=self.value_list2)
        self.TCombobox2.current(self.source_file)


        # CONSOLE FRAME
        self.TLabelframe2 = ttk.Labelframe(self.top)
        self.TLabelframe2.place(relx=0.012, rely=0.607, relheight=0.293
                , relwidth=0.973)
        self.TLabelframe2.configure(relief='')
        self.TLabelframe2.configure(text='''Console''')


        # CONSOLE OUTPUT/LOG WiNDOW
        self.console = ScrolledText(self.TLabelframe2)
        self.console.place(relx=0.012, rely=0.114, relheight=0.852
                , relwidth=0.976, bordermode='ignore')
        self.console.configure(background="white")
        self.console.configure(font="TkTextFont")
        self.console.configure(insertborderwidth="3")
        self.console.configure(selectbackground="#c4c4c4")
        self.console.configure(startline="1")
        self.console.configure(wrap="word")


        # PROGRESS FRAME
        self.TLabelframe3 = ttk.Labelframe(self.top)
        self.TLabelframe3.place(relx=0.012, rely=0.912, relheight=0.073
                , relwidth=0.973)
        self.TLabelframe3.configure(relief='')
        self.TLabelframe3.configure(text='''progress''')

        
        # GO BUTTON
        self.Button3 = tk.Button(self.TLabelframe1)
        self.Button3.place(relx=0.862, rely=0.841, height=21, width=76
                , bordermode='ignore')
        self.Button3.configure(activebackground="#f9f9f9")
        self.Button3.configure(command=lambda: self.start(self.Entry1.get(), self.Entry2.get(), "./config/" + self.TCombobox1.get(), self.TCombobox2.get()))
        self.Button3.configure(takefocus="6")
        self.Button3.configure(text='''Go!''')    


        # TOTAL PROGRESSBAR
        self.TProgressbar1 = ttk.Progressbar(self.TLabelframe3)
        self.TProgressbar1.place(relx=0.012, rely=0.455, relwidth=0.974
                , relheight=0.0, height=19, bordermode='ignore')
        self.TProgressbar1.configure(length="789")

        self.Label1 = tk.Label(self.top)
        self.Label1.place(relx=0.012, rely=0.017, height=112, width=658)
        self.Label1.configure(activebackground="#f9f9f9")
        photo_location = os.path.join(_location,"bild.gif")
        global _img0
        _img0 = tk.PhotoImage(file=photo_location)
        self.Label1.configure(image=_img0)
        self.Label1.configure(justify='left')

        # ON STARTUP
        if platform.system() == 'Windows':
            self.separator = "\\"
        else:
            self.separator = "/"         

        self.console.insert(tk.INSERT,"we are rdy...\n")

    def onselectdir(self):
        self.last_path = self.get_last_path("input_dir")
        self.Entry1.delete(0)
        initialdir = self.last_path
        title = 'Verzeichnis Wählen zum Öffnen'
        self.source = filedialog.askdirectory(initialdir=initialdir, title=title)        
        if self.source:
            self.Entry1.delete(0, 255)
            self.source = f"{self.source}{self.separator}"
            self.Entry1.insert(0,f"{self.source}")
            self.save_last_path(self.source, "input_dir")
            
    def onsavedir(self):
        self.last_path = self.get_last_path("output_dir")
        self.Entry2.delete(0, 255)
        initialdir = self.last_path
        title = 'Verzeichnis Wählen zum Speichern'
        self.destination = filedialog.askdirectory(initialdir=initialdir, title=title)
        if self.destination:
            self.Entry2.delete(0, 255)
            self.destination = f"{self.destination}{self.separator}"
            self.Entry2.insert(0,f"{self.destination}")
            self.save_last_path(self.destination,"output_dir")

    def find_ini_files(self):
        self.ini_files = []
        for filename in os.listdir("./config"):
            if filename.endswith('.ini'):
                if filename != "history.ini":
                    self.ini_files.append(filename)
                    self.ini_files.sort()
        return self.ini_files

    def save_last_path(self,path,what):
        config = configparser.ConfigParser()
        config.read('./config/history.ini')
        config['LastPath'][f'{what}'] = path
        with open('history.ini', 'w') as configfile:
            config.write(configfile)

    def get_last_path(self,what):
        config = configparser.ConfigParser()
        config.read('./config/history.ini')
        last_path = config['LastPath'][f'{what}']
        return last_path

    def log_update(self,text):
        self.console.insert(tk.INSERT,f"{text}\n")
        self.console.update_idletasks()

    def start(self, source, destination, config_file, file_source):
        # CLEAN CONSOLE/PROGRESSBAR
        self.TProgressbar1['value'] = 0
        self.console.delete(1.0, tk.END)

        # SAVE SETTiNGS
        self.save_last_path(str(self.TCombobox1.current()),"config_file")
        self.save_last_path(str(self.TCombobox2.current()),"source_file")
        list_of_checks = ['Dirs','NFO','Packing','Creating','done']

        if _DEBUG == 1:
            self.log_update(f"VARS:")
            self.log_update(f"Source.........: {source}")
            self.log_update(f"Destination....: {destination}")
            self.log_update(f"Config File....: {config_file}")
            self.log_update(f"File Source....: {file_source}")
            self.log_update(f"list Config")

        # START RLS.py WiTH VARs
        proc = subprocess.Popen(f"python releaser_CLI.py {source} {destination} {file_source} {config_file} 0", stdout=subprocess.PIPE, shell=True)

        output, error = proc.communicate()

        if error:
            self.log_update(f"{error}")
        else:
            line = output.decode('utf-8') 
            for check in list_of_checks:
                if check in line:
                    self.TProgressbar1.step(10)
                if "Finish" in line:
                    self.TProgressbar1['value'] = 100
            self.log_update(line)

# THE FOLLOWiNG CODE iS ADDED TO FACiLiTATE THE SCROLLED WiDGETS YOU SPECiFiED.
class AutoScroll(object):
    '''Configure the scrollbars for a widget.'''
    def __init__(self, master):
        #  ROZEN. ADDED THE TRY-EXCEPT CLAUSES SO THAT THiS CLASS
        #  COULD BE USED FOR SCROLLED ENTRY WiDGET FOR WHiCH VERTiCAL
        #  SCROLLiNG iS NOT SUPPORTED. 5/7/14.
        try:
            vsb = ttk.Scrollbar(master, orient='vertical', command=self.yview)
        except:
            pass
        hsb = ttk.Scrollbar(master, orient='horizontal', command=self.xview)
        try:
            self.configure(yscrollcommand=self._autoscroll(vsb))
        except:
            pass
        self.configure(xscrollcommand=self._autoscroll(hsb))
        self.grid(column=0, row=0, sticky='nsew')
        try:
            vsb.grid(column=1, row=0, sticky='ns')
        except:
            pass
        hsb.grid(column=0, row=1, sticky='ew')
        master.grid_columnconfigure(0, weight=1)
        master.grid_rowconfigure(0, weight=1)
        # COPY GEOMETRY METHODS OF MASTER (TAKEN FROM SCROLLEDTEXT.PY)
        methods = tk.Pack.__dict__.keys() | tk.Grid.__dict__.keys() \
                  | tk.Place.__dict__.keys()
        for meth in methods:
            if meth[0] != '_' and meth not in ('config', 'configure'):
                setattr(self, meth, getattr(master, meth))

    @staticmethod
    def _autoscroll(sbar):
        '''Hide and show scrollbar as needed.'''
        def wrapped(first, last):
            first, last = float(first), float(last)
            if first <= 0 and last >= 1:
                sbar.grid_remove()
            else:
                sbar.grid()
            sbar.set(first, last)
        return wrapped

    def __str__(self):
        return str(self.master)

def _create_container(func):
    '''Creates a ttk Frame with a given master, and use this new frame to
    place the scrollbars and the widget.'''
    def wrapped(cls, master, **kw):
        container = ttk.Frame(master)
        container.bind('<Enter>', lambda e: _bound_to_mousewheel(e, container))
        container.bind('<Leave>', lambda e: _unbound_to_mousewheel(e, container))
        return func(cls, container, **kw)
    return wrapped

class ScrolledText(AutoScroll, tk.Text):
    '''A standard Tkinter Text widget with scrollbars that will
    automatically show/hide as needed.'''
    @_create_container
    def __init__(self, master, **kw):
        tk.Text.__init__(self, master, **kw)
        AutoScroll.__init__(self, master)

import platform
def _bound_to_mousewheel(event, widget):
    child = widget.winfo_children()[0]
    if platform.system() == 'Windows' or platform.system() == 'Darwin':
        child.bind_all('<MouseWheel>', lambda e: _on_mousewheel(e, child))
        child.bind_all('<Shift-MouseWheel>', lambda e: _on_shiftmouse(e, child))
    else:
        child.bind_all('<Button-4>', lambda e: _on_mousewheel(e, child))
        child.bind_all('<Button-5>', lambda e: _on_mousewheel(e, child))
        child.bind_all('<Shift-Button-4>', lambda e: _on_shiftmouse(e, child))
        child.bind_all('<Shift-Button-5>', lambda e: _on_shiftmouse(e, child))

def _unbound_to_mousewheel(event, widget):
    if platform.system() == 'Windows' or platform.system() == 'Darwin':
        widget.unbind_all('<MouseWheel>')
        widget.unbind_all('<Shift-MouseWheel>')
    else:
        widget.unbind_all('<Button-4>')
        widget.unbind_all('<Button-5>')
        widget.unbind_all('<Shift-Button-4>')
        widget.unbind_all('<Shift-Button-5>')

def _on_mousewheel(event, widget):
    if platform.system() == 'Windows':
        widget.yview_scroll(-1*int(event.delta/120),'units')
    elif platform.system() == 'Darwin':
        widget.yview_scroll(-1*int(event.delta),'units')
    else:
        if event.num == 4:
            widget.yview_scroll(-1, 'units')
        elif event.num == 5:
            widget.yview_scroll(1, 'units')

def _on_shiftmouse(event, widget):
    if platform.system() == 'Windows':
        widget.xview_scroll(-1*int(event.delta/120), 'units')
    elif platform.system() == 'Darwin':
        widget.xview_scroll(-1*int(event.delta), 'units')
    else:
        if event.num == 4:
            widget.xview_scroll(-1, 'units')
        elif event.num == 5:
            widget.xview_scroll(1, 'units')

def start_up():
    releaser_support.main()

if __name__ == '__main__':
    releaser_support.main()
