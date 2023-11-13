
import json
with open('artefactos.json') as arte_file :
  artefactos = arte_file.read()
artefactos = json.loads(artefactos)

def items_toStr(items):
    str_items = map(str,items)
    ret = ""
    for item in str_items:
        ret = ret + artefactos[item] + "\n"
    return ret

om = items_toStr([1,2,7])
print(om)