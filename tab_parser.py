#tab parser processes SINGLE line of tablature
import player

def filter_text(i):
    input = i.split('\n')
    input=list(filter(lambda x: "|" in x, input))
    return input

if number elements not divisible by 6, throw error

def process_text(t):
    tab=[]
    for s in range(6):
        string = ""
        for b in range(len(t)//6):
            try:
                string += t[s + 6*b][1:]
            except ValueError:
                print('Improper number of strings')
        string = string.replace("|","")
        tab+=[string]
    return tab


list(map(lambda x: len(x), tab[1]))


tab = process_text(filter_text(input))
tab= list(map(lambda x: x.split("-"), tab))
tab = *tab.
n=len(' '.join(tab[1]))
while start<n:




for i in range(200):
    generate_note(list(map(lambda x: x[i], a)))


list(map(play,strings))
