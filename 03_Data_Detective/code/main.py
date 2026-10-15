import csv, sys

dataarr = []

def validate(arr):
    for i in arr:
        if arr[i] == "-1":
            return False
        if i == None:
            return False
    return True

def average(arr):
    total = 0
    for i in arr:
        total += int(i)
    return total/len(arr)

#Stage 1 Read the file and understand each record
try:
    with open('./03_Data_Detective/game_matches.csv', 'r') as f:
    #with open('./03_Data_Detective/hand_check.csv', 'r') as f:
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

out = []

for i in validated:
    if i["record_id"] in to_consolidate and i in out:
        print("skipping duplicate")
    elif i["record_id"] in to_consolidate:
        out.append(i)
    elif i["record_id"] not in to_get_rid_of:
        out.append(i)
    else:
        print("getting rid of this")


#4.1 character statistics

characters = {}
characters_num = {
    "Ranger": 0,
    "Mage": 0,
    "Tank": 0,
    "Assassin": 0
}

for i in out:
    char = i["character"]
    characters_num[char] += 1
    if char not in characters:
        characters[char] = {
            "kills": [i["kills"]],
            "damage": [i["damage"]],
            "won": [i["won"]]
        }
    else:
        characters[char]["kills"].append(i["kills"])
        characters[char]["damage"].append(i["damage"])
        characters[char]["won"].append(i["won"])

for i in characters:
    print(f"{i} kills: {average(characters[i]["kills"])}")
    print(f"{i} damage: {average(characters[i]["damage"])}")
    print(f"{i} win percent: {average(characters[i]["won"])*100}")

for i in characters_num.keys():
    print(f"{i} - got {characters_num[i]}")

#4.2 player statistics

players = {}
players_out = {}

for i in out:
    print(i["player"])
    if i["player"] in players_out:
        players_out[i["player"]] += 1
    else:
        players_out[i["player"]] = 1



for i in out:
    player = i["player"]
    if player not in players:
        players[player] = {
            "kills": [i["kills"]],
            "damage": [i["damage"]],
            "won": [i["won"]]
        }
    else:
        players[player]["kills"].append(i["kills"])
        players[player]["damage"].append(i["damage"])
        players[player]["won"].append(i["won"])



for i in players:
    print(f"{i} kills: {average(players[i]["kills"])}")
    print(f"{i} damage: {average(players[i]["damage"])}")
    print(f"{i} win percent: {average(players[i]["won"])*100}")

players_out_sorted = {}
for key in sorted(players_out, key=players_out.get):
    players_out_sorted[key] = players_out[key]
    
for i in players_out_sorted.keys():
    print(f"{i} - got {players_out_sorted[i]}")