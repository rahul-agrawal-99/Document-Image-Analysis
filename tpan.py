import re
import csv
import dateutil.parser as dparser


def find_text_in_pan(text ,text_new):
    name = None
    gender = None
    ayear = None
    uid = None
    yearline = []
    genline = []
    nameline = []
    text1 = []
    genderStr = '(Female|Male|emale|male|ale|FEMALE|MALE|EMALE)$'


    # Searching for Year of Birth
    lines = text
    # print (lines)
    for wordlist in lines.split('\n'):
        xx = wordlist.split()
        if [w for w in xx if re.search('(Year|Birth|irth|YoB|YOB:|DOB:|DOB)$', w)]:
            yearline = wordlist
            break
        else:
            text1.append(wordlist)
    try:
        text2 = text.split(yearline, 1)[1]
    except Exception:
        pass

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

        text2 = text.split(genline, 1)[1]
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


    intlist = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9" ,"O" ,"o"]
    charlist = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "v" , "W", "X", "Y", "Z"
                'a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z' ,'0']

    # EJAPSO276M
    for i in range(len(text)):
        if (text[i] in charlist) and (text[i+1] in charlist) and (text[i+2] in charlist) and (text[i+3] in charlist) and (text[i+4] in charlist):
            if (text[i+5] in intlist or text[i+5] in charlist) and  (text[i+6] in intlist) and (text[i+7] in intlist) and (text[i+8] in intlist) and (text[i+9] in charlist):
                # print(text[i:i+10] , "*******")
                uid = text[i:i+10]
                break
        else :
            uid = "null"
            





    # Making tuples of data
    data = {}
    data['DOC_type'] = 'pan'
    data['Name'] = name
    data['Gender'] = gender
    data['Birth year'] = ayear
    if data['Name'] == "":
        try:
            data['Name'] = text_new[6]
        except:
            pass
            # print("blank name")
    if uid == "null":
        for k,j in enumerate(text_new):
            text = str(j)
            if len(text) > 9:
                i= 0
                if (text[i] in charlist) and (text[i+1] in charlist) and (text[i+2] in charlist) and (text[i+3] in charlist) and (text[i+4] in charlist):
                    if (text[i+5] in intlist or text[i+5] in charlist) and  (text[i+6] in intlist) and (text[i+7] in intlist) and (text[i+8] in intlist) and (text[i+9] in charlist):
                        data['Uid'] = text[i:i+10]
                        break
    else:
        data['Uid'] = uid

    return data
    