import re
import csv
import dateutil.parser as dparser
from nltk.tokenize import  word_tokenize


def find_text_in_adhar(text , textnew):
    name = None
    gender = None
    ayear = None
    data = {}
    yearline = []
    genline = []
    nameline = []
    text1 = []
    genderStr = '(Female|Male|emale|male|ale|FEMALE|MALE|EMALE)$'


    # Searching for Year of Birth
    lines = text
    for wordlist in lines.split('\n'):
        xx = wordlist.split()
        if [w for w in xx if re.search('(Year|Birth|irth|YoB|YOB:|DOB:|DOB)$', w)]:
            yearline = wordlist
            break
        else:
            text1.append(wordlist)
   

    try:
        yearline = re.split('Year|Birth|irth|YoB|YOB:|DOB:|DOB', yearline)[1:]
        yearline = ''.join(str(e) for e in yearline)
        if yearline:
            ayear = dparser.parse(yearline, fuzzy=True).year
    except Exception:
        pass

    # Searching for Gender
    try:
        for wordlist in lines.split('\n'):
            xx = wordlist.split()
            if [w for w in xx if re.search(genderStr, w)]:
                genline = wordlist
                break

        if 'Female' in genline or 'FEMALE' in genline:
            gender = "Female"
        if 'Male' in genline or 'MALE' in genline:
            gender = "Male"
    except Exception:
        pass

    # Read Database
    with open('namesdb//namedb.csv', 'r') as f:
        reader = csv.reader(f)
        newlist = list(reader)
    newlist = sum(newlist, [])

    # Searching for Name and finding exact name in database
    try:
        
        text1 = filter(None, text1)
        for x in text1:
            for y in x.split():
                if y.upper() in newlist:
                    nameline.append(x)
                    break
        name = ' '.join(str(e) for e in nameline)
    except Exception:
        pass


    intlist = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
    uid_found = False
    for i in range(len(text)):
        if text[i] in intlist:
            if text[i+1] in intlist:
                if text[i+2] in intlist:
                    if text[i+3] in intlist:
                            if text[i+5] in intlist:
                                if text[i+6] in intlist:
                                    if text[i+7] in intlist:
                                            data['Uid']  = text[i:i+14]
                                            uid_found = True
                                            break
            

    if name == '':
        wt = word_tokenize(' '.join(textnew))
        for index ,t in enumerate(wt):
            if t.upper() in newlist:
                name  = t.capitalize() + " " + wt[index+1].capitalize()
              
    
    # Making tuples of data
    
    data['DOC_type'] = 'Adhar'
    data['Name'] = name
    data['Gender'] = gender
    data['Birth year'] = ayear
    if uid_found == False :
        for i in textnew:
            ids = "".join(i.split())
            # print(ids)
            if len(ids)>8:
                # print("eligible :",ids)
                try:
                    data['Uid'] = int(ids)
                    # print("uid found in easyocr")
                except:
                    data['Uid'] = None
    return data
    