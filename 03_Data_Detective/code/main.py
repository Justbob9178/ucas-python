import csv, io, os, sys

dataarr = []

#open files
try:
    with open('./game_matches.csv', 'r') as f:
        data = csv.DictReader(f)
        for row in data:
            dataarr.append(row)

except FileNotFoundError:
    print("file not found. Does it exist?")
    sys.exit()


#validation
for i in dataarr:
    if not i["record_id"].startswith("R") or not i["match_id"].startswith("M") or not i["player"].startswith("Player"):
        print(f"record id blank for {i}")
    if i["character"].lower().capitalize() != i["character"]:
        for char in ["ranger", "mage", "tank", "assassin"]:
            if i["character"].lower().replace(' ', '') == char:
                #print(f"capitalising {char.capitalize()} from {i["character"]}")
                dataarr[i]["character"] = char.capitalize()
    try:
        if int(i['kills']) > 50 or int(i['kills']) < 0:
            print(f"silly number {i}")
            dataarr[i]["kills"] = '-1'
    except ValueError:
        print("not int code here")