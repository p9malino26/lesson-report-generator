import csv
from string import ascii_uppercase as ALL_CAPS
from os.path import realpath
import os

ASSET_PATH=os.path.dirname(__file__)

HOURLY_RATES_FNAME=os.path.join(ASSET_PATH, "hourly_rates.txt")
REPORT_MASTER_FNAME=os.path.join(ASSET_PATH, "report_master.org")
RECEIPT_MASTER_FNAME=os.path.join(ASSET_PATH, "receipt_master.org")
REPORT_FNAME="report.org"
RECEIPT_FNAME="receipt.org"

def readFieldValues(field_value_str: str) -> dict:
    output = {}

    field = value = ""
    for c in field_value_str:
        if c == '#':
            state='appending_field'
            if value != '':
                value = value.strip()
                output[field] = value
                field = value = ""
                
        elif c in [' ', '\n'] and state == "appending_field":
            state = "appending_value"

        if state == "appending_field":
            field+=c
        else:
            value+=c

    value = value.strip()
    output[field] = value
    return output
        

def substituteAll(main_string: str, substitutions: dict[str,str]):
    
    main_string = main_string.replace('\\#', '#')
    for find, replace in substitutions.items():
        main_string = main_string.replace(find, replace)

    blank_field_lines = []
    for i,l in enumerate(main_string.splitlines()):
        l = l.strip()
        if l == '': continue
        if '+' in l: continue
        if '#' in l:
            blank_field_lines.append(i)

    return main_string, blank_field_lines

def run(args):
    i = 0
    while i < len(args):
        if args[i] == "--hourly-rates":
            HOURLY_RATES_FNAME = args[i + 1]
            i += 1
        else:
            report_content_file = args[i]

        i += 1

        
    field_vals = readFieldValues(open(report_content_file, 'r').read()) 
    hourly_rates_tbl = {}
    with open(HOURLY_RATES_FNAME, 'r') as hourly_rates_file:
        for l in hourly_rates_file.readlines():
            k_v = l.strip().split(' ') 
            hourly_rates_tbl[k_v[0]] = k_v[1]


    if '#DURATION' not in field_vals:
        field_vals['#DURATION'] = "1"

    field_vals['#HOURLYRATE'] = hourly_rates_tbl[field_vals['#STUDENT']]
    field_vals['#TOTALCOST'] = str(int(field_vals['#HOURLYRATE']) * int(field_vals['#DURATION']))

    report_str, unsubbed_report = substituteAll(open(REPORT_MASTER_FNAME, 'r').read(), field_vals)
    receipt_str, unsubbed_receipt = substituteAll(open(RECEIPT_MASTER_FNAME, 'r').read(), field_vals)

    for typ, unsubbed in [('report', unsubbed_report), ('receipt', unsubbed_receipt)]:
        if unsubbed != []:
            print("Warning! Unsubstituted fields on line(s)", unsubbed, "of", typ)

    open(REPORT_FNAME, 'w').write(report_str)
    open(RECEIPT_FNAME, 'w').write(receipt_str)

