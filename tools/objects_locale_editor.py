# -*- coding: utf-8 -*-
"""----------------------------------------------------------
 Author:      alexey.sychov@gameloft.com
 Created:     21-06-2018
 Description: Simple tool for localization texts fulfilling.
----------------------------------------------------------"""


import os
import json
import fnmatch

from Tkinter import Tk, Frame, Listbox, Label, Scrollbar, Entry
from Tkinter import LEFT, RIGHT, TOP, BOTTOM, Y, X, W, YES, NORMAL, DISABLED, \
                    VERTICAL, END, BOTH
from ttk import Treeview, Button
from tkMessageBox import askyesno, showerror


class LocaleEditor(object):
    """Simple tool for adding and changing locale strings.
    Formats:

        Every locale stored in separate file, like "rus.json".

        Every locale is a dictionary, where locale names are keys, and
        game object classes dictionaries are values.

        Every game object class is a dictionary, where sections in
        CLASS_KEYS list are keys, and section content is dictionary.

        Every section is a dictionary, where keys are key strings
        for in-game text, and values are game logic text strings.
    """
    PATH_TO_LOCALES = './../gamedata/text/objects'
    CLASS_KEYS = [u'descriptions', u'actions']

    def __init__(self):
        """Init.
        """
        # ~ Init vars ~
        self._locales = {}
        self._mode = None
        self._header = None
        self._current_item_name = None
        self._current_class = None
        self._header = None
        self._current_locale = None
        self._was_changes = False

        # ~ Initialize env ~

        self._setup_locales()
        self._make_gui()
        self._select_first_locale()
        self._root.mainloop()


    def _make_gui(self):
        """Form and draw GUI. Set such GUI attributes to instance:

            _root:                   main window;
            _locale_listbox:         list of locales;
            _sync_locales_button:    button to synchronize locales;
            _class_listbox:          list of object classes;
            _add_class_button:       button to add class to locale;
            _del_class_button:       button to del class from locale;
            _treeview:               tree of object keys and strings;
            _key_entry:              entry to edit object key;
            _text_entry:             entry to edit object string;
            _update_button:          button to update selected object string;
        """
        FONT = ('Verdana', '11')

        self._root = root = Tk()
        root.geometry('1400x768+200+100')
        root.title('Locale text editor')
        root.protocol("WM_DELETE_WINDOW", self._on_closing)

        # ---------------------- left ------------------------ #

        left_frame = Frame(root)
        left_frame.pack(side=LEFT, fill=Y, anchor=W)

        Label(left_frame, text='Locale:', font=FONT).pack(pady=(10, 0))

        # ------- locale ------- #

        locale_frame = Frame(left_frame)
        locale_frame.pack()

        self._locale_listbox = locale_listbox = Listbox(locale_frame, width=25,
                  height=6, font=FONT, activestyle=None, exportselection=False)
        locale_scrollbar = Scrollbar(locale_frame, orient=VERTICAL)
        locale_listbox.config(yscrollcommand=locale_scrollbar.set)
        locale_scrollbar.config(command=locale_listbox.yview)
        locale_listbox.pack(side=LEFT, padx=(10, 0), pady=10)
        locale_scrollbar.pack(side=LEFT, pady=10, fill=Y)

        for locale_name in self._locales:
            locale_listbox.insert(END, locale_name)
        locale_listbox.bind("<<ListboxSelect>>", self._on_click_in_locales_list)

        # ------- locales button ------- #

        locale_frame = Frame(left_frame)
        locale_frame.pack()

        self._sync_locales_button = Button(left_frame, text='Sync locales',
                                                command=self._sync_all_locales)
        self._sync_locales_button.pack(padx=10, pady=10)

        Label(left_frame, text='Object classes:', font=FONT).pack(pady=(30, 5))

        # ------- classes ------- #

        class_frame = Frame(left_frame)
        class_frame.pack()

        self._class_listbox = class_listbox = Listbox(class_frame, width=25,
                 height=12, font=FONT, activestyle=None, exportselection=False)
        class_scrollbar = Scrollbar(class_frame, orient=VERTICAL)
        class_listbox.config(yscrollcommand=class_scrollbar.set)
        class_scrollbar.config(command=class_listbox.yview)
        class_listbox.pack(side=LEFT, padx=(10, 0), pady=10, fill=Y)
        class_scrollbar.pack(side=LEFT, pady=10, fill=Y)
        self._class_listbox.bind("<<ListboxSelect>>",
                                                  self._on_click_in_class_list)

        # ------- classes buttons ------- #

        self._del_class_button = Button(
            left_frame,
            text='Remove class',
            command=self._remove_class_from_locale)
        self._del_class_button.pack(padx=10, pady=(0, 10))

        self.add_class_entry = Entry(left_frame, font=FONT, width=25)
        self.add_class_entry.pack(padx=10, pady=(10, 0))

        self._add_class_button = Button(
            left_frame,
            text='Add class to locale',
            command=self._add_class_to_locale)
        self._add_class_button.pack(padx=10, pady=10)

        # ---------------------- right ------------------------ #

        right_frame = Frame(root, bg='#eeeeee')
        right_frame.pack(expand=YES, fill=BOTH)

        # ------- bottom line ------- #

        bottom_frame = Frame(right_frame, bg='#eeeeee')
        bottom_frame.pack(side=BOTTOM, fill=X)

        self._update_button = Button(bottom_frame, text='...', state=DISABLED)
        self._update_button.pack(side=RIGHT, padx=10, pady=10)

        self._key_entry = Entry(bottom_frame, font=FONT, width=15)
        self._key_entry.pack(side=LEFT, padx=(10, 0), pady=12)

        self._text_entry = Entry(bottom_frame, font=FONT)
        self._text_entry.pack(side=LEFT, fill=X, expand=YES, padx=10, pady=12)

        # ------- tree view ------- #

        treeview_scrollbar = Scrollbar(right_frame, orient=VERTICAL)
        self._treeview = Treeview(
            right_frame,
            yscrollcommand=treeview_scrollbar.set,
            columns=('A', 'B'),
            show="tree")
        treeview_scrollbar.config(command=class_listbox.yview)
        self._treeview.pack(side=LEFT, expand=YES, fill=BOTH,
                                                    padx=(10, 0), pady=(10,0))
        treeview_scrollbar.pack(side=LEFT, padx=(0, 10), pady=(10, 0), fill=Y)
        self._treeview.tag_configure('header', font=('Sans','10','bold'))
        self._treeview.column("#0", stretch='no', width=150)
        self._treeview.column("A", stretch='no', minwidth=250)
        self._treeview.column("B", stretch='yes', minwidth=500)
        self._treeview.bind("<Button-1>", self._on_click_in_tree)


    def _setup_locales(self):
        """Scan locales dir for locales files, form dictionsry with content.
        """
        locales = os.listdir(self.PATH_TO_LOCALES)
        for filename in fnmatch.filter(locales, '*.json'):
            with open(os.path.join(self.PATH_TO_LOCALES, filename)) as f:
                self._locales[filename.replace('.json', '')] = json.load(f)


    def _update_locale_classes(self):
        """Update object classes list in locale.
        """
        self._class_listbox.delete(0,'end')
        self._current_class = None
        for class_name in sorted(self._locales[self._current_locale]):
            self._class_listbox.insert(END, class_name)
            if not self._current_class:
                self._current_class = class_name
        self._class_listbox.activate(0)
        self._class_listbox.selection_set(0)
        self._update_class_tree()


    def _update_class_tree(self):
        """Form and draw tree of chosen class in locale.
        """
        self._treeview.delete(*self._treeview.get_children())
        if not self._current_class:
            return

        locale = self._locales[self._current_locale][self._current_class]
        for section_name in self.CLASS_KEYS:
            self._treeview.insert('', 'end', section_name, text=section_name,
                                                      open=True, tags='header')
            for key, value in sorted(locale[section_name].items()):
                self._treeview.insert(
                    section_name,
                    END,
                    open=True,
                    values=[key, value],
                    text=u'└')


    def _select_first_locale(self):
        """First locale selection. Usually on event.
        """
        if self._locales:
            locale_name = self._locales.keys()[0]
            self._locale_listbox.activate(0)
            self._locale_listbox.selection_set(0)
            self._current_locale = locale_name
            self._update_locale_classes()


    def _on_closing(self):
        """Ask user about saving locales data back to files.
        Quit after.
        """
        if self._was_changes and askyesno(
                                 'Quitting', 'Save changes in locales files?'):
            for locale_name in self._locales:
                with open(os.path.join(
                       self.PATH_TO_LOCALES, locale_name + '.json'), 'w') as f:
                    json.dump(self._locales[locale_name], f, indent=4)
        self._root.destroy()


    def _on_click_in_locales_list(self, event):
        """Event: selecting some of locales.
        """
        index = int(self._locale_listbox.curselection()[0])
        value = self._locale_listbox.get(index)
        self._current_locale = value
        self._update_locale_classes()


    def _on_click_in_class_list(self, event):
        """Event: selecting some of locale clasees.
        """
        index = int(self._class_listbox.curselection()[0])
        value = self._class_listbox.get(index)
        self._current_class = value
        self._update_class_tree()


    def _on_click_in_tree(self, event):
        """Event: clicking to treeview.
        """
        item_name = self._treeview.identify_row(event.y)
        if not item_name:
            return

        tags = self._treeview.item(item_name, 'tags')

        if 'header' in tags:
            self._header = self._treeview.item(item_name, 'text')

            if self._mode != 'add':
                self._mode = 'add'

            if self._update_button['state'] != NORMAL:
                self._update_button['text'] = 'Add'
                self._update_button['state'] = NORMAL
                self._update_button['command'] = self._add_class_field_text

        elif 'header' not in tags:

            self._key_entry.delete(0, END)
            self._text_entry.delete(0, END)
            key, value = self._treeview.item(item_name, 'values')
            self._key_entry.insert(0, key)
            self._text_entry.insert(0, value)
            self._current_item_name = item_name

            if self._mode != 'update':
                self._mode = 'update'

            if self._update_button['state'] != NORMAL:
                self._update_button['text'] = 'Update'
                self._update_button['state'] = NORMAL
                self._update_button['command'] = self._update_class_field_text


    def _update_class_field_text(self):
        """Change text (and possible key) of some field. Callback.
        """
        self._was_changes = True

        old_key = self._treeview.item(self._current_item_name, 'values')[0]
        new_key = self._key_entry.get()
        new_text = self._text_entry.get()

        class_obj = self._locales[self._current_locale][self._current_class]

        if new_key:
            self._treeview.item(
                    self._current_item_name,
                    values=(new_key, new_text)
                )

        parent_name = self._treeview.parent(self._current_item_name)
        section_name = self._treeview.item(parent_name)['text']
        if old_key != new_key:
            del class_obj[section_name][old_key]

        if new_key:
            class_obj[section_name][new_key] = new_text
        else:
            self._treeview.delete(self._current_item_name)
            self._current_item_name = None
            self._update_button['text'] = '...'
            self._update_button['state'] = DISABLED
            self._update_button['command'] = None


    def _add_class_field_text(self):
        """Add key and text to some field. Callback.
        """
        self._was_changes = True

        new_key = self._key_entry.get()
        new_text = self._text_entry.get()
        if not new_key:
            showerror('Error!', 'Please, choose a key for this text first!')
            return

        class_obj = self._locales[self._current_locale][self._current_class]

        if new_key in class_obj[self._header]:
            showerror('Error!', 'This key already exists!')
            return

        class_obj[self._header][new_key] = new_text
        self._update_class_tree()


    def _add_class_to_locale(self):
        """Add new class to locale.
        """
        self._was_changes = True

        class_name = self.add_class_entry.get()
        if class_name:
            self._locales[self._current_locale][class_name] = new_class = {}
            for section_name in self.CLASS_KEYS:
                new_class[section_name] = {}
            self._update_locale_classes()


    def _remove_class_from_locale(self):
        """Remove class from locale.
        """
        self._was_changes = True

        index = int(self._class_listbox.curselection()[0])
        class_name = self._class_listbox.get(index)
        if class_name and askyesno(
                           'Question', 'Are you sure to delete object class?'):
            del self._locales[self._current_locale][class_name]
            self._update_locale_classes()


    def _sync_all_locales(self):
        """Make full locales synchronization.
        If some key exists in one locale and is absent in another one,
        it is added with an the empty string value.
        """
        self._was_changes = True

        # ~ Get whole structure ~

        resulted = {}
        for locale in self._locales:
            for class_ in self._locales[locale]:
                if class_ not in resulted:
                    resulted[class_] = {}
                for section_name in self._locales[locale][class_]:
                    if section_name not in resulted[class_]:
                        resulted[class_][section_name] = []
                    for key in self._locales[locale][class_][section_name]:
                        if key not in resulted[class_][section_name]:
                            resulted[class_][section_name].append(key)

        # ~ Update every locale ~

        for locale in self._locales:
            for class_ in resulted:
                if class_ not in self._locales[locale]:
                    self._locales[locale][class_] = {}
                for section_name in resulted[class_]:
                    if section_name not in self._locales[locale][class_]:
                        self._locales[locale][class_][section_name] = {}
                    for key in resulted[class_][section_name]:
                        if key not in self._locales[locale][class_][
                                                                 section_name]:
                            self._locales[locale][class_][section_name][
                                                                      key] = ''
        self._update_locale_classes()

# --------------------------- main ---------------------------------- #

z = LocaleEditor()

