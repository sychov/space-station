# -*- coding: utf-8 -*-
"""----------------------------------------------------------
 Author:      alexey.sychov@gameloft.com
 Created:     21-06-2018
 Description: Simple tool for localization texts fulfilling.
----------------------------------------------------------"""


import os
import json
import fnmatch

from Tkinter import *
from ttk import Treeview, Button


class LocaleEditor(object):
    """Simple tool for adding and changing locale strings.
    """
    PATH_TO_LOCALES = './../gamedata/text/objects'
    CLASS_KEYS = [u'descriptions', u'actions']

    def __init__(self):
        """Init.
        """
        self._locales = {}
        self._mode = None
        self._header = None
        self._current_item_name = None

        self.setup_locales()
        self.make_gui()


        if self._locales:
            locale_name = self._locales.keys()[0]
            self.locale_listbox.activate(0)
            self.locale_listbox.selection_set(0)
            self._current_locale = locale_name
            self._current_locale_index = 0
            self.update_locale_classes()

        self.root.mainloop()
        self.save_locales()


    def make_gui(self):
        """Form and draw GUI. Set such GUI attributes to instance:

            root:                   main window;
            locale_listbox:         list of locales;
            change_locale_button:   button to change current locale;
            class_listbox:          list of object classes;
            add_class_button:       button to add class to locale;
            treeview:               tree of object keys and strings;
            key_entry:              entry to edit object key;
            text_entry:             entry to edit object string;
            update_button:          button to update selected object string;
        """
        FONT = ('Verdana', '11')

        self.root = root = Tk()
        root.geometry('1400x768+200+100')
        root.title('Locale text editor')

        # ---------------------- left ------------------------ #

        left_frame = Frame(root)
        left_frame.pack(side=LEFT, fill=Y, anchor=W)

        Label(left_frame, text='Locale:', font=FONT).pack(pady=(10, 0))

        # ------- locale ------- #

        locale_frame = Frame(left_frame)
        locale_frame.pack()

        self.locale_listbox = locale_listbox = Listbox(locale_frame, width=25,
                  height=6, font=FONT, activestyle=None, exportselection=False)
        locale_scrollbar = Scrollbar(locale_frame, orient=VERTICAL)
        locale_listbox.config(yscrollcommand=locale_scrollbar.set)
        locale_scrollbar.config(command=locale_listbox.yview)
        locale_listbox.pack(side=LEFT, padx=(10, 0), pady=10)
        locale_scrollbar.pack(side=LEFT, pady=10, fill=Y)

        for locale_name in self._locales:
            locale_listbox.insert(END, locale_name)

        # ------- change locale button ------- #

        self.change_locale_button = Button(left_frame, text='Change locale')
        self.change_locale_button.pack(padx=10, pady=10)

        Label(left_frame, text='Object classes:', font=FONT).pack(pady=(30, 5))

        # ------- classes ------- #

        class_frame = Frame(left_frame)
        class_frame.pack()

        self.class_listbox = class_listbox = Listbox(class_frame, width=25,
                 height=12, font=FONT, activestyle=None, exportselection=False)
        class_scrollbar = Scrollbar(class_frame, orient=VERTICAL)
        class_listbox.config(yscrollcommand=class_scrollbar.set)
        class_scrollbar.config(command=class_listbox.yview)
        class_listbox.pack(side=LEFT, padx=(10, 0), pady=10, fill=Y)
        class_scrollbar.pack(side=LEFT, pady=10, fill=Y)
        self.class_listbox.bind("<<ListboxSelect>>",
                                                  self._on_click_in_class_list)

        # ------- classes buttons ------- #

        self.del_class_button = Button(left_frame, text='Remove class')
        self.del_class_button.pack(padx=10, pady=(0, 10))

        self.add_class_entry = Entry(left_frame, font=FONT, width=25)
        self.add_class_entry.pack(padx=10, pady=(10, 0))

        self.add_class_button = Button(left_frame, text='Add class to locale')
        self.add_class_button.pack(padx=10, pady=10)

        # ---------------------- right ------------------------ #

        right_frame = Frame(root, bg='#eeeeee')
        right_frame.pack(expand=YES, fill=BOTH)

        # ------- bottom line ------- #

        bottom_frame = Frame(right_frame, bg='#eeeeee')
        bottom_frame.pack(side=BOTTOM, fill=X)

        self.update_button = Button(bottom_frame, text='...', state=DISABLED)
        self.update_button.pack(side=RIGHT, padx=10, pady=10)

        self.key_entry = Entry(bottom_frame, font=FONT, width=15)
        self.key_entry.pack(side=LEFT, padx=(10, 0), pady=12)

        self.text_entry = Entry(bottom_frame, font=FONT)
        self.text_entry.pack(side=LEFT, fill=X, expand=YES, padx=10, pady=12)

        # ------- tree view ------- #

        treeview_scrollbar = Scrollbar(right_frame, orient=VERTICAL)
        self.treeview = Treeview(
            right_frame,
            yscrollcommand=treeview_scrollbar.set,
            columns=('A', 'B'),
            show="tree")
        treeview_scrollbar.config(command=class_listbox.yview)
        self.treeview.pack(side=LEFT, expand=YES, fill=BOTH,
                                                    padx=(10, 0), pady=(10,0))
        treeview_scrollbar.pack(side=LEFT, padx=(0, 10), pady=(10, 0), fill=Y)
        self.treeview.tag_configure('header', font=('Sans','10','bold'))
        self.treeview.column("#0", stretch='no', width=150)
        self.treeview.column("A", stretch='no', minwidth=250)
        self.treeview.column("B", stretch='yes', minwidth=500)
        self.treeview.bind("<Button-1>", self._on_click_in_tree)


    def setup_locales(self):
        """Scan locales dir for locales files, form dictionsry with content.
        """
        locales = os.listdir(self.PATH_TO_LOCALES)
        for filename in fnmatch.filter(locales, '*.json'):
            with open(os.path.join(self.PATH_TO_LOCALES, filename)) as f:
                self._locales[filename.replace('.json', '')] = json.load(f)


    def update_locale_classes(self):
        """Update object classes list in locale.
        """
        self._current_class = ''
        for class_name in sorted(self._locales[self._current_locale]):
            self.class_listbox.insert(END, class_name)
            if not self._current_class:
                self._current_class = class_name
                self._current_class_index = 0
        self.class_listbox.activate(0)
        self.class_listbox.selection_set(0)
        self.update_class_tree()


    def update_class_tree(self):
        """Form and draw tree of chosen class in locale.
        """
        self.treeview.delete(*self.treeview.get_children())
        locale = self._locales[self._current_locale][self._current_class]
        for section_name in self.CLASS_KEYS:
            self.treeview.insert('', 'end', section_name, text=section_name,
                                                      open=True, tags='header')
            for key, value in locale[section_name].items():
                self.treeview.insert(
                    section_name,
                    END,
                    open=True,
                    values=[key, value],
                    text=u'└')


    def _on_click_in_class_list(self, event):
        """
        """
        index = int(self.class_listbox.curselection()[0])
        value = self.class_listbox.get(index)
        self._current_class = value
        self.update_class_tree()



    def _on_click_in_tree(self, event):
        """
        """
        item_name = self.treeview.identify_row(event.y)
        if not item_name:
            return

        tags = self.treeview.item(item_name, 'tags')
        if 'header' in tags:
            self._header = self.treeview.item(item_name, 'text')
            self.key_entry.delete(0, END)
            self.text_entry.delete(0, END)

            if self._mode != 'add':
                self._mode = 'add'
                self.update_button['text'] = 'Add'
                self.update_button['state'] = NORMAL
                self.update_button['command'] = self._add_class_field_text

        elif 'header' not in tags:

            self.key_entry.delete(0, END)
            self.text_entry.delete(0, END)
            key, value = self.treeview.item(item_name, 'values')
            self.key_entry.insert(0, key)
            self.text_entry.insert(0, value)
            self._current_item_name = item_name

            if self._mode != 'update':
                self._mode = 'update'
                self.update_button['text'] = 'Update'
                self.update_button['state'] = NORMAL
                self.update_button['command'] = self._update_class_field_text


    def _update_class_field_text(self):
        """
        """
        old_key = self.treeview.item(self._current_item_name, 'values')[0]
        new_key = self.key_entry.get()
        new_text = self.text_entry.get()

        class_obj = self._locales[self._current_locale][self._current_class]
        self.treeview.item(
                self._current_item_name,
                values=(new_key, new_text)
            )

        if old_key != new_key:
            del class_obj[old_key]

        class_obj[new_key] = new_text


    def _add_class_field_text(self):
        """
        """
        new_key = self.key_entry.get()
        new_text = self.text_entry.get()
        if not new_key:
            print 'error: no key'
            return

        class_obj = self._locales[self._current_locale][self._current_class]

        if new_key in class_obj[self._header]:
            print 'error: key exists'
            return

        class_obj[self._header][new_key] = new_text
        self.update_class_tree()

# --------------------------- main ---------------------------------- #

z = LocaleEditor()

