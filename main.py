from tkinter import *
from tkinter.ttk import *
import time
import re
import time
import math
from datetime import datetime
def normalize(str):
    replacements = (
        ("á","a"),
        ("é","e"),
        ("í","i"),
        ("ó","o"),
        ("ú","u")
    )
    for a, b in replacements:
        str = str.replace(a,b)
    return str

comorbilities = {
    1:['hipertension arterial', 'hta'],
    2:['tabaquismo', 'tabaquista'],
    3:['dbt', 'diabetes miellitus'],
    4:['sifilis', 'lues']
}


epicrisis = ''

all_data = {
    "name": '',
    "DNI": '',
    "birth_day": '',
    "admission_date": '',
    "egress_date": '',
    "CD4": {
        "before": '',
        "during": '',
        'measure': 'cel/mm3'
    },
    "CV": {
        "measure": 'cp/ml',
        "before": '',
        "during": ''
    },
    "comorbilities": [],
    "evolution": ''
}

TARV = {
    "3TC": 'lamivudina',
    "FTC": 'emtricitabina',
    "EFV": "efavirens",
    "TDF": "tenofovir",
    "DTG": 'dolutegravir',
    "RTV": 'ritonavir',
}

def save():
    split_epicrisis = re.split(r'\n{2,}', epicrisis)
    datos_personales= antecedentes= enfermedad_actual= estudios= evolucion = ''

    for item in split_epicrisis:
        pass
        if re.search(r'Antecedentes:', item):
            antecedentes = item
        elif re.search(r'Nombre y Apellido:', item):
            datos_personales = item
        elif re.search(r'Enfermedad\sactual:', item):
            enfermedad_actual = item
        elif re.search(r'Evolucion:', item):
            evolucion = item
        elif re.search(r'Estudios:', item):
            estudios = item

    dni = re.search(r'DNI:\s\d+\.?\d+.?\d+', datos_personales.lower(), flags=re.I)
    if dni:
        dni = int(re.search(r'\d+', dni.group().replace('.', '').replace(',', '')).group())
        all_data['DNI'] = dni
    else:
        print('DNI NO existente')

    name = re.search(r'nombre y apellido:\s?(\w+\s){,4}\s{,2}', datos_personales.lower())
    if name:
        name = name.group().replace('nombre y apellido:', '').replace(r'\t|\s{2,}', '')
        name = re.split(r'\s', name)
        name = [i for i in name if i != '']
        name = ' '.join(name)
    all_data['name'] = name

    birth_day = re.search(r'Fecha de nacimiento:\s?(\d{1,2}(/|-)\d{1,2}(/|-)\d{1,4}|\d{1,2}(/|-)\d{1,4})', datos_personales, flags=re.I)
    if birth_day:
        birth_day = birth_day.group().lower().replace('fecha de nacimiento: ', '')
        for timeformat in ('%d/%m/%Y', '%d/%m/%y'):
            try:
                birth_day = datetime.strptime(birth_day, timeformat)
            except TypeError:
                pass
            except ValueError:
                pass

    if type(birth_day) == datetime:
        all_data['birth_day'] = birth_day
    else:
        pass

    admission_date = re.search(r'Fecha de ingreso:\s?(\d{1,2}(/|-)\d{1,2}(/|-)\d{1,4}|\d{1,2}(/|-)\d{1,4})', datos_personales, flags=re.I)
    if admission_date:
        admission_date = admission_date.group().lower().replace('fecha de ingreso: ', '')
        for timeformat in ('%d/%m/%Y', '%d/%m/%y'):
            try:
                admission_date = datetime.strptime(admission_date, timeformat)
            except TypeError:
                pass
            except ValueError:
                pass

    if type(admission_date) == datetime:
        all_data['admission_date'] = admission_date
    else:
        pass

    egress_date= re.search(r'Fecha de egreso:\s?(\d{1,2}(/|-)\d{1,2}(/|-)\d{1,4}|\d{1,2}(/|-)\d{1,4})',datos_personales,flags=re.I)
    if egress_date:
        string = 'fechadeegreso:'
        egress_date = egress_date.group().lower().replace(' ', '').replace(string, '')
        for timeformat in ('%d/%m/%Y', '%d/%m/%y'):
            try:
                egress_date = datetime.strptime(egress_date, timeformat)
                all_data['egress_date'] = egress_date
            except TypeError:
                pass
            except ValueError:
                pass

    tarv_list = []
    no_tarv = re.search(r'(abandono\sde\sTARV|\bsin\sTARV|\bsin\stratamiento\s(antirretroviral|antirretrovirus|antirv|anti\srv))', antecedentes, re.I)
    if no_tarv:
        tarv_list = None

    else:
        for key, value in TARV.items():
            result = re.search(rf'((\b|/){key}(/|\s)?|(\b|/){value}(/|\s)?)', antecedentes)
            if result:
                tarv_list.append(key)

    for value in comorbilities.values():
        if len(value) > 1:
            for item in value:
                if item in antecedentes.lower():
                    all_data['comorbilities'].append(item)
                    break
        else:
            if value[0] in antecedentes.lower():
                all_data['comorbilities'].append(value[0])


    cd4_before = re.search(r'CD4(\s|:|=)(\d+(\.|,)?\d+(\.|,)?\d+|\d{1,3})', enfermedad_actual, re.I)
    if cd4_before:
        cd4_before = re.search(r'\s(\d+(\.|,)?\d+|\d{1,3})', cd4_before.group()).group().replace(' ', '')
        all_data['CD4']['before'] = cd4_before


    cv_before = re.search(r'cv(\s+|:|=)\d+(\.|,)?\d+(\.|,)?\d+', enfermedad_actual, re.I)
    if cv_before:
        cv_before = re.search(r'\d+(\.|,)?\d+(\.|,)?\d+(\.|,)?\d+', cv_before.group()).group()
        all_data['CV']['before'] = cv_before

    cd4_during = re.search(r'CD4(\s|:|=)(\d+(\.|,)?\d+(\.|,)?\d+|\d{1,3})', estudios, re.I)
    if cd4_during:
        cd4_during = re.search(r'\s(\d+(\.|,)?\d+|\d{1,3})', cd4_during.group()).group().replace(' ', '')
        all_data['CD4']['during'] = cd4_during

    cv_during = re.search(r'cv(\s+|:|=)\d+(\.|,)?\d+(\.|,)?\d+', estudios, re.I)
    if cv_during:
        cv_during = re.search(r'\d+(\.|,)?\d+(\.|,)?\d+(\.|,)?\d+', cv_during.group()).group()
        all_data['CV']['during'] = cv_during

    death = re.search(r'(\bmuerte\s(del|de\sla)\spaciente|\bobito|\bfallecio)', evolucion, re.I)
    uti = re.search(r'\buti', evolucion, re.I)
    if death:
        all_data['evolution'] = 'obito'
    elif uti:
        all_data['evolution'] = 'uti'
    else:
        all_data['evolution'] = 'alta'

try:
    with open('epicrisis.txt') as file:
        epicrisis = file.read()
        epicrisis = normalize(epicrisis)
except:
    print('Error')

save()
print(all_data)
for key, value in all_data.items():
    # print(key)
    # print(value)
    if type(value) == list:
        print(str(key) + ' = ' + ', '.join(value))
    elif type(value) == dict:
        for key2, val in value.items():
            if type(val) == list:
                print(str(key) + ' = ' + str(key2) + ' = ' + ', '.join(val))
            else:
                print(str(key) + ' = ' + str(key2) + ' = ' + val)
    elif type(value) == datetime:
        print(key + ' = ' + value.strftime('%d/%m/%Y'))
    else:
        print(str(key) + ' = ' + str(value))


