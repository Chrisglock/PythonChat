import json
with open('artefactos.json') as f:
   artefactos = json.load(f)

print(artefactos['1'])
items_users = {}
items_users["user1"] = [1,3,4,5]
items_users["user2"] = [6,7,8,9]
def get_item_names(items):
    items = map(str,items)
    con = ""
    for item in items:
        con = con + artefactos["1"]
    return con
def trade(socket1,socket2):
    i = get_item_names(items_users["user1"])
    return 0