'''tab_parser.py proceses input tablature text of program, removing extraneous
text or characters before iteration.'''
import re

def filter_text(i):
    input = i.split('\n')
    input=list(filter(lambda x: "|" in x, input))
    return input

def process_text(t):
    tab=[]
    for s in range(6):
        string = ""
        for b in range(len(t)//6):
            string += t[s + 6*b][1:]
        string = string.replace("|","")
        string = re.split('(\-)',string)
        tab+=[list(filter(None, string))]
    return tab
