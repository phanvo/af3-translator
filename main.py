import xml.etree.ElementTree as ET
from xml.etree.ElementTree import ParseError
import tkFileDialog
import tkMessageBox
import os
import subprocess
import timeit
from Tkinter import *
from os.path import basename
from parse_datadictionary import *
from parse_componentarchitecture import *
from parse_statetransition import *


def set_window_center(root):
    root.update_idletasks()
    w = root.winfo_screenwidth()
    h = root.winfo_screenheight()
    size = tuple(int(_) for _ in root.geometry().split('+')[0].split('x'))
    x = w/2 - size[0]/2
    y = h/2 - size[1]/2
    root.geometry("%dx%d+%d+%d" % (size + (x, y)))


def reset_message():
    message_english.set('')
    message_ace.set('')
    message_english_id.set('')


def select_file():
    # Tk().withdraw()
    global full_path
    check = tkFileDialog.askopenfilename()
    raw_name = basename(check)
    print raw_name

    if raw_name is None or raw_name == '':
        if file_name.get()[12:] is not None:
            return
    elif 'af3' not in raw_name:
        tkMessageBox.showinfo("Info", "Please select correct AutoFocus3 file extension, i.e., af3")
        if file_name.get()[12:] is not None:
            return
        file_name.set('[ Current ] ')
        return

    file_name.set('[ Current ] ' + raw_name)
    full_path = check
    reset_message()


def execute_translation(schema_mode):
    if file_name.get()[12:] is None or file_name.get()[12:] == '':
        tkMessageBox.showinfo("Info", "Please select AutoFocus3 file")
        return

    #i = 0
    #f = open('runtime.txt', 'a')
    #while i < 10:
    #    start_time = timeit.default_timer()

    reset_message()
    init_pdf_parser()

    is_valid = parse_af3_file(schema_mode)

    if is_valid is False:
        if schema_mode == 1:
            message_english.set('Failed!')
        elif schema_mode == 2:
            message_ace.set('Failed!')
        else:
            message_english_id.set('Failed!')
        return

    if schema_mode == 1:
        message_english.set('Done!')
    elif schema_mode == 2:
        message_ace.set('Done!')
    else:
        message_english_id.set('Done!')

    exported_file = my_pdf_export_file(file_name.get()[12:], schema_mode)
    try:
        os.startfile(exported_file)
    except AttributeError:
        subprocess.call(['open', exported_file])

     #   elapsed = timeit.default_timer() - start_time
     #   try:
     #       f.write(str(elapsed) + '\n')
     #   except IOError:
     #       f.close()

     #   i += 1

    #f.close()


def parse_af3_file(translation_schema_mode):
    try:
        #tree = ET.parse(file_name.get())
        tree = ET.parse(full_path)
    except ParseError:
        tkMessageBox.showinfo("Info", "Parsing failure! File structured not supported!")
        return False

    root = tree.getroot()

    my_pdf_set_report_title(file_name.get()[12:], translation_schema_mode)
    my_pdf_set_text_color()

    for root_elem in root.iter('rootElements'):
        for key, value in root_elem.attrib.items():
            key = clean_str(key)
            value = clean_str(value)

            if key == 'type' and value == 'DataDictionary':
                my_pdf_set_section_title('Data Dictionary')
                parse_data_dictionary(root_elem, translation_schema_mode)

            if key == 'type' and value == 'ComponentArchitecture':
                my_pdf_set_section_title('Component Architecture')
                component_list = parse_component_architecture(root_elem, translation_schema_mode)

                my_pdf_set_section_title('State Transition Diagram')
                parse_state_transition(component_list, translation_schema_mode)

    my_pdf_end_report('-')
    return True


def about_info():
    message = 'Author: Phan Vo\n' \
              'Email: phanvo@gmail.com\n\n' \
              'Advisor: Maria Spichkova\n' \
              'Email: maria.spichkova@rmit.edu.au'
    tkMessageBox.showinfo("Info", message)

if __name__ == '__main__':
    master = Tk()
    master.title('AutoFocusNLS')

    Label(master, text="AutoFocus3 model translator", bg='grey', font='-weight bold').\
        grid(row=0, columnspan=2)

    Button(master, text="Select AutoFocus3 file", command=select_file, width=25, bd=3).\
        grid(row=1, column=0, sticky=W)
    file_name = StringVar()
    Label(master, textvariable=file_name, width=50, anchor=W, justify=LEFT).grid(row=1, column=1, sticky=W)
    file_name.set('[ Current ] ')

    Button(master, text="Translate to English", command=lambda: execute_translation(1), width=25, bd=3).\
        grid(row=2, column=0, sticky=W)
    message_english = StringVar()
    Label(master, textvariable=message_english, width=50).grid(row=2, column=1, sticky=W)

    Button(master, text="Translate to ACE", command=lambda: execute_translation(2), width=25, bd=3).\
        grid(row=3, column=0, sticky=W)
    message_ace = StringVar()
    Label(master, textvariable=message_ace, width=50).grid(row=3, column=1, sticky=W)

    Button(master, text="Translate to English with [ID]", command=lambda: execute_translation(3), width=25, bd=3). \
        grid(row=4, column=0, sticky=W)
    message_english_id = StringVar()
    Label(master, textvariable=message_english_id, width=50).grid(row=4, column=1, sticky=W)

    Button(master, text="About", command=about_info, width=30, bd=3).grid(row=5, columnspan=2)

    master.configure(background='grey')

    set_window_center(master)
    master.mainloop()
