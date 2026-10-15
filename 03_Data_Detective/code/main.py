import csv, sys

dataarr = []

def validate(arr):
    for i in arr:
        if arr[i] == "-1":
            return False
        if i == None:
            return False
    return True


#Stage 1 Read the file and understand each record
try:
    with open('./03_Data_Detective/hand_check.csv', 'r') as f:
        data = csv.DictReader(f)
        for row in data:
            dataarr.append(row)

except FileNotFoundError:
    print("file not found. Does it exist?")
    sys.exit()



#Stage 2 Normalise and validate individual rows
for i in dataarr:
    for x in ["record_id", "match_id", "player", "character", "kills", "deaths", "damage", "won"]:
        dataarr[dataarr.index(i)][x] = str(i[x]).strip()

    if i["character"].lower() not in ["ranger", "mage", "tank", "assassin"]:
        dataarr[dataarr.index(i)]["character"] = "-1"
    else:
        dataarr[dataarr.index(i)]["character"] = dataarr[dataarr.index(i)]["character"].capitalize()

    try:
        if int(i['kills']) > 50 or int(i['kills']) < 0 or "." in i['kills']:
            dataarr[dataarr.index(i)]["kills"] = '-1'
    except:
            dataarr[dataarr.index(i)]["kills"] = '-1'
    try:
        if int(i['damage']) > 20000 or int(i['damage']) < 0:
                dataarr[dataarr.index(i)]["damage"] = '-1'
    except:
        dataarr[dataarr.index(i)]["damage"] = '-1'
    try:
        if str(i["won"]).lower() != "true" or str(i["won"]).lower() != "false":
            if str(i["won"]).lower() == "true":
                dataarr[dataarr.index(i)]["won"] = True
            elif str(i["won"]).lower() == "false":
                dataarr[dataarr.index(i)]["won"] = False
            else: 
                dataarr[dataarr.index(i)]["won"] = "-1"
    except: 
        dataarr[dataarr.index(i)]["won"] = "-1"

    if not i["player"]:
        dataarr[dataarr.index(i)]["player"] = '-1'


#vStage 3 Resolve duplicates and reconcile the audit

record_ids = {}
validated = []
to_get_rid_of = []
to_consolidate = []


for i in dataarr:
    if validate(i):
        validated.append(i)

for i in range(len(validated)):
    for x in range(len(validated)):
        #print(validated[i]["record_id"], validated[x]["record_id"], i, x)
        if validated[i]["record_id"] == validated[x]["record_id"] and i != x:
            if validated[i] == validated[x]:
                to_consolidate.append(validated[i]["record_id"])
            else:
                #print(f"different\n{validated[i]}\n{validated[x]}")
                to_get_rid_of.append(validated[i]["record_id"])

for i in to_get_rid_of:
    if i in to_consolidate:
        to_consolidate.pop(to_consolidate.index(i))

print(to_consolidate)
print(to_get_rid_of)

for i in validated:
    print(i)
