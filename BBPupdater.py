import scheduler
import time
import datetime
import requests, json, os
import discord

filedir = os.path.dirname(os.path.realpath(__file__))
jsonfilepath = filedir + "/scriptFiles/currentScopesJSON.txt"
msgfilepath = filedir + "/scriptFiles/currentScopesMsg.txt"

schedule = scheduler.Scheduler()

def cls():
    os.system('cls' if os.name=='nt' else 'clear')

def h1RequestAll():
    scopeJson = {}
    updateMessage = {}
    next = "https://api.hackerone.com/v1/hackers/programs?page[size]=100"
    login = ('-H1_USERNAME-', '-H1_API_KEY-')
	# Personal Credentials Required Above
    accepts = { 'Accept': 'application/json' }
    while next:
        url = next
        data = requests.get(url, headers=accepts, auth=login)
        finalJson = json.loads(data.text)
        try:
            next = finalJson['links']['next']
        except:
            next = ""
        for i in range(len(finalJson['data'])):
            handle = finalJson['data'][i]['attributes']['handle']
            name = finalJson['data'][i]['attributes']['name']
            first = False
            url = "https://api.hackerone.com/v1/hackers/programs/" + handle
    	    login = ('-H1_USERNAME-', '-H1_API_KEY-')
		# Personal Credentials Required Above
            accepts = { 'Accept': 'application/json' }
            data = requests.get(url, headers=accepts, auth=login)
            scopes = json.loads(data.text)
            for relationship in scopes['relationships']['structured_scopes']['data']:
                if relationship['attributes']['eligible_for_bounty'] and (relationship['attributes']['asset_type'] == "URL" or relationship['attributes']['asset_type'] == "Domain"):
                    if first == False:
                        scopeJson[handle] = {}
                        scopeJson[handle]['name'] = name
                        scopeJson[handle]['scopes'] = {}
                        scopeJson[handle]['scopes'][relationship['attributes']['asset_identifier']] = relationship['attributes']['updated_at']
                        first = True
                    else:
                        scopeJson[handle]['scopes'][relationship['attributes']['asset_identifier']] = relationship['attributes']['updated_at']
    with open(jsonfilepath, "r+") as file:
        readFile = file.read()
        file.seek(0)
        if readFile == '':
            file.write(json.dumps(scopeJson))
            updateMessage = scopeJson
        else:
            oldScopes = json.loads(readFile)
            for handle in scopeJson:
                first = True
                for updateDate in scopeJson[handle]['scopes']:
                    if not handle in oldScopes.keys():
                        updateMessage[handle] = scopeJson[handle]
                        updateMessage[handle]['name'] += ' - NEW'
                        break
                    else:
                        if not updateDate in oldScopes[handle]['scopes'].keys():
                            if first == True:
                                updateMessage[handle] = {}
                                updateMessage[handle]['name'] = scopeJson[handle]['name']
                                updateMessage[handle]['scopes'] = {}
                                updateMessage[handle]['scopes'][updateDate] = scopeJson[handle]['scopes'][updateDate]
                                first = False
                            else: 
                                updateMessage[handle]['scopes'][updateDate] = scopeJson[handle]['scopes'][updateDate]
                        elif datetime.datetime.fromisoformat(oldScopes[handle]['scopes'][updateDate]) < datetime.datetime.fromisoformat(scopeJson[handle]['scopes'][updateDate]):
                            if first == True:
                                updateMessage[handle] = {}
                                updateMessage[handle]['name'] = scopeJson[handle]['name']
                                updateMessage[handle]['scopes'] = {}
                                updateMessage[handle]['scopes'][updateDate] = scopeJson[handle]['scopes'][updateDate]
                                first = False
                            else: 
                                updateMessage[handle]['scopes'][updateDate] = scopeJson[handle]['scopes'][updateDate]
            file.write(json.dumps(scopeJson))
    return updateMessage

def discMsg(mess):
    if mess != {}:
        with open(msgfilepath, "w+") as file:
            for key, value in mess.items():
                file.write("--------------------------\n")
                file.write(value['name'] + " - " + key + "\n")
                file.write("--------------------------\n\n")
                for key, value in value['scopes'].items():
                    file.write("    SCOPE NAME -- {}\n    UPDATED AT -- {}\n\n".format(key, value))
        fileToSend = discord.File(fp=msgfilepath, description="update times")
        webhook = discord.SyncWebhook.from_url("-DISCORD_WEBHOOK_LINK-")
	    # Personal Credentials Required Above
        webhook.send(file=fileToSend)

def job():
    if not os.path.exists(filedir + "/scriptFiles"):
        os.makedirs(filedir + "/scriptFiles")
    mess = h1RequestAll()
    discMsg(mess)

job()
schedule.cyclic(datetime.timedelta(minutes=30), job)
while True:
    schedule.exec_jobs()
    cls()
    print(schedule)
    time.sleep(30)