from tkinter import *
from tkinter.ttk import *
import time
import re

def save():
    content = text.get('1.0', END)
    # button.config(state=DISABLED)
    pattern = re.compile(r'antecedentes:', re.I)
    atc_matches = pattern.finditer(content)
    # print(atc_matches)

    personal_data = ''
    for match in atc_matches:
        # print(match.span())
        personal_data = content[0: match.span()[0]]
    #
    # print(personal_data)
    # name_pattern = r'Nombre y APELLIDO(:|=)\s?[a-z ]+(\t|\s{3,})'
    name_pattern = r'zzzzzzzz'
    # name_match = re.finditer(name_pattern, personal_data, re.I)
    # print(name_match)
    # name2 = re.match(name_pattern, personal_data, re.I).group(0)
    name2 = re.match(name_pattern, personal_data, re.I)
    # print(name2['span'])
    # print(name2.groups())
    print(name2)
    # for i in name2:
    #     print(i)
    # dni_pattern = re.compile(r'\bDNI:', re.I)
    # dni_match = dni_pattern.finditer(personal_data)

    # for matchs in name_match:
    #     print(matchs.span())
    #     print(type(matchs))
    # for match in dni_match:
    #     print(match)


window = Tk()

text = Text(window, width=20, height=10, pady=10, padx=10)
text.pack()
button = Button(window, text='Save', command=save)
button.pack()

window.mainloop()
