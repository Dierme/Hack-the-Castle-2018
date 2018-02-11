import  requests

url = 'https://api.wit.ai/entities?v=20160526'

auth_tok = 'XEXPZR2CLQQIXLS7ZS4CMWUNZM7NIERE'

hed = {'Authorization': 'Bearer ' + auth_tok}


def getData(value, expressions) :
    return {"doc": value+"Doc", "lookups": ["trait"], "id": (value+"UD"), "values": [{"value": value, "expressions": expressions}]}


def addEntity(value, epxresstions) :
    return requests.post(url = url, json = getData(value, epxresstions), headers=hed)
