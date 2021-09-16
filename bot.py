# SnapDirecte - An original script by MathiAs2Pique_ #


import pyperclip
import pyautogui #BlueStacks control
import requests #HTTP(s) requets
from requests import request as req #HTTP(s) requests
from datetime import datetime as date #Date obtention
import datetime
import base64 #Base64 decoding
import re #Regex
import time
import json #Storing in file

######### A remplir ! #########
identifiant = "user"
motdepasse = "pass"

def _callback(matches):
    id = matches.group(1)
    try:
        return chr(int(id))
    except:
        return id

def decode_unicode_references(data):
    ret = re.sub("&#(\d+)(;|(?=\s))", _callback, data.replace('&nbsp;', ' '))
    ret = ret.replace("&eacute;", "é")
    ret = ret.replace("&egrave;", "è")
    ret = ret.replace("&agrave;", "à")
    return ret
class api:
    def init(self):
        try:


            payload = 'data={ "identifiant": "'+identifiant+'", "motdepasse": "'+motdepasse+'", "acceptationCharte": true }'
            response = req("POST", "https://api.ecoledirecte.com/v3/login.awp", data=payload).json()
            self.token = response['token']
            self.eleveid = str(response['data']['accounts'][0]['id'])
        except:
            print("erreur api (init)")
            self.token = None
            self.eleveid = 0

    def getDevoirsDate(self, dateChar):
        try:
            self.init(self)
            payload = 'data={"token":"'+self.token+'"}'
            response = req("POST", "https://api.ecoledirecte.com/v3/Eleves/"+self.eleveid+"/cahierdetexte.awp?verbe=get", data=payload).json()
            try:
                if response["data"][dateChar] is not None:
                    devoirs_jour = api.describeDateDevoirs(self, dateChar)
                    return  True, devoirs_jour
            except:
                return False, None
        except:
            return False, None

    def describeDateDevoirs(self, date):
        try:
            self.init(self)
            payload = 'data={"token":"'+self.token+'"}'
            return(req("POST", "https://api.ecoledirecte.com/v3/Eleves/"+ self.eleveid +"/cahierdetexte/"+ date +".awp?verbe=get&", data=payload).json())
        except:
            return None
    def getNotes(self):
        self.init(self)
        payload = 'data={"token":"'+self.token+'"}'
        response = req("POST", "https://api.ecoledirecte.com/v3/eleves/"+self.eleveid+"/notes.awp?verbe=get", data=payload).json()
        print(response)

    def messages(self):
            self.init(self)
            payload = 'data={"token":"'+self.token+'"}'
            response = req("POST", "https://api.ecoledirecte.com/v3/eleves/"+self.eleveid+"/messages.awp", data=payload).json()
            print(response)



class guicontrol:
    def goChat():
        # Entrer dans la page chat
        chatLocation = pyautogui.locateOnScreen('chat.png', confidence=0.9)
        pyautogui.click(chatLocation)
        print("CLICK !1 ")
        time.sleep(0.2)
        chatLocation = pyautogui.locateOnScreen('chat_vide.png', confidence=0.9)
        pyautogui.click(chatLocation)
        print("CLICK !2 ")
        time.sleep(0.5)

    def goDm():
        # Entrer dans le dm
        pyautogui.scroll(2)
        time.sleep(1)
        chatLocation = pyautogui.locateOnScreen('group.png', confidence=0.9)
        pyautogui.moveTo(chatLocation)
        pyautogui.move(-35, 10)
        pyautogui.click()
        time.sleep(1)
        pyautogui.click(pyautogui.locateOnScreen('finalDm.png', confidence=0.9))
        print("CLICK !3 ")
        time.sleep(0.5)

    def sendDm(text):
        # Envoyer le dm
        pyperclip.copy(text)
        pyautogui.hotkey('ctrl', 'v', interval=0.1)
        time.sleep(0.5)
        pyautogui.hotkey('enter')

    def returnToAccueil():
        # Quitter le DM et revenir à l'accueil
        time.sleep(0.2)
        chatLocation = pyautogui.locateOnScreen('retour.png')
        pyautogui.click(chatLocation)
        print("CLICK !4 ")
        time.sleep(0.3)
        chatLocation = pyautogui.locateOnScreen('photo.png')
        pyautogui.click(chatLocation)
        print("CLICK !5 ")
        pyautogui.move(-50, 0)






##DEBUG##
# guicontrol.goDm()
# exit(1)
#########
# Main #
while True:
    today = date.now()
    checkHeure = today.strftime("%H,%M")
    print(checkHeure)
    try:
        lastMinute = 62
        if checkHeure != "16,58":
            if lastMinute != date.now().strftime('%M'):
                lastMinute = date.now().strftime('%M')
                print("Cron")
                #
                # Check des devoirs 
                #
                for x in range(0, 6, 1):
                    if x>0:
                        timestampDateDevoir = today + datetime.timedelta(days = x)
                    else:
                        timestampDateDevoir = today
                    dateDevoirs = timestampDateDevoir.strftime("%Y-%m-%d")
                    exist, objet = api.getDevoirsDate(api, dateDevoirs)
                    message = ""
                    message = message+"###### Devoir(s) pour " + timestampDateDevoir.strftime("%d %b, %Y") + " ######"
                    if exist:
                        for devoir in objet["data"]["matieres"]:
                            devoirId = '{"id": "'+str(devoir['id'])+'"}'
                            #On met l'id dans un fichier
                            fileData = ""
                            with open("var.txt", 'r+') as file:
                                towrite = json.loads(devoirId)
                                fileData = json.load(file)
                            true = True
                            for tdevoirId in fileData["cahierdetexte"]:
                                if str(tdevoirId["id"]) == str(devoir["id"]):
                                    true = False
                            if true:
                                matiere = devoir["matiere"]
                                prof = devoir['nomProf']
                                string = (re.sub('<[^<]+?>', '', base64.b64decode(devoir["aFaire"]["contenu"]).decode("utf-8")))
                                devoirs = decode_unicode_references(string)
                                message = message+"\n----------"
                                message = message+"\n"+matiere
                                message = message+"\n"+prof
                                message = message+"\n"+devoirs
                                fileData["cahierdetexte"].append(towrite)
                                time.sleep(1)
                                file2 = open("var.txt","w")
                                file2.close()
                                print("Nouvel ID log dans txt")
                                print(matiere)
                                with open("var.txt", 'r+') as file:
                                    json.dump(fileData, file, indent=4) #Pour le débug, plus simple d'avoir indent sur 4. A supprimer si tout marche bien.
                                print(message)
                                print(devoir['id'])
                                guicontrol.goChat()
                                guicontrol.goDm()
                                guicontrol.sendDm(message)
                                guicontrol.returnToAccueil()
                #
                # Check des notes à faire
                #

            time.sleep(30)

        else:
            print("Résumé")
            for x in range(0, 5, 1):
                if x>0:
                    timestampDateDevoir = today + datetime.timedelta(days = x)
                else:
                    timestampDateDevoir = today
                dateDevoirs = timestampDateDevoir.strftime("%Y-%m-%d")
                exist, objet = api.getDevoirsDate(api, dateDevoirs)
                message = ""
                message = message+"###### Devoirs pour " + timestampDateDevoir.strftime("%d %b, %Y") + " ######"
                if exist:
                    for devoir in objet["data"]["matieres"]:
                        matiere = devoir["matiere"]
                        prof = devoir['nomProf']
                        string = (re.sub('<[^<]+?>', '', base64.b64decode(devoir["aFaire"]["contenu"]).decode("utf-8")))
                        devoirs = decode_unicode_references(string)
                        message = message+"\n----------"
                        message = message+"\n"+matiere
                        message = message+"\n"+prof
                        message = message+"\n"+devoirs
                        print(message)
                        guicontrol.goChat()
                        guicontrol.goDm()
                        guicontrol.sendDm(message)
                        guicontrol.returnToAccueil()
            time.sleep(62)
    except Exception as e:
        print("Erreur durant le script principal.")
        print ("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        print(e)
        print ("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        time.sleep(2)
