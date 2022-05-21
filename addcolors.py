import json

while True:
    r = open('dict.json','r')
    key = input("Key: ")
    if key == "CLEAR":
        if input('\nAre you sure you want to clear the dictionary (y,n)? ').lower() == "y":
            f = open('dict.json','w')
            f.write('')
            f.close()
            print('Successfully cleared the dictionary\n')
            continue
        else:
            continue
    value = input("Value: ")
    txt = r.read()
    if txt != "":
        dic = json.loads(txt)
    else:
        dic = dict()
    dic[key] = value.split(',')
    for i,v in enumerate(dic[key]):
        dic[key][i] = int(dic[key][i])
    toWrite = json.dumps(dic,indent=4,sort_keys=True)
    print(toWrite)
    w = open('dict.json','w')
    w.write(toWrite)
    w.close()
    r.close()
    print('\nWrote key', key, "with value", value, "to dictionary\n")