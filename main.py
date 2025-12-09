import json
import hashlib
from sendMail import SendMail
from substitutionsChecker import SubstitutionsChecker

cacheFile = '.state/knownSubstitutions.txt'

def mailSubject(student,date):
    return "Vertretungsplan: " + student["name"] + " am " + date
                    
def mailBody(student,date,substitutions,url):
    body = student["name"] + " hat am " + date + " möglicherweise Vertretung oder Ausfall." + '\n' 
    for sub in substitutions:
        body += "Stunde: " + sub["Stunde"] + ", "
        body += "Gruppe: " + sub["Gruppen"] + ", "
        body += "Fach: "   + sub["Fach"]   + ", "
        body += "Art: "   + sub["Art"]   + ", "
        body += '\n'
        body += "Hinweis: "+ sub["Hinweise"]
        body += '\n'
        body += "Quelle: " + url
        body += '\n'
        body += '\n'
    return body

def cacheSizeControl():
    # Limitiere Cache auf 100 Zeilen
    with open(cacheFile, "r") as f:
        lines = f.readlines()

    if len(lines) > 100:
        print("Cache size > 100 lines, will only keep latest 100.")
        lines = lines[-100:]

    # Datei überschreiben
    with open(cacheFile, "w") as f:
        f.writelines(lines)
               
def main():
    # erstelle Cache-Datei, falls sie noch nicht existiert
    try:
        with open(cacheFile, 'x') as file:
            file.write('')
    except FileExistsError:
        pass

    # lese Konfiguration
    with open('students.json') as file:
        students = json.load(file)
  
    for student in students:
        # der Vertretungsplan kennt 3 Tage
        for day in [0,1,2]:
            [date,substitutions,url] = SubstitutionsChecker.check(day, student["memberships"])
            # diese Variable entscheidet, ob eine Mail versendet werden sollte
            containsNews = False
            for sub in substitutions:
                print("Assessing found substition:")
                print(sub)
                toHash = ','.join([student["name"],date]+list(sub.values()))
                hashed = hashlib.sha256(toHash.encode('utf-8')).hexdigest()

                isKnownSubstitution = False
                with open(cacheFile) as f:
                    print("The substitutions hash is: " + hashed)
                    print(f.read())
                    if hashed in f.read():
                        print("This substitution is already known.")
                        isKnownSubstitution = True

                if not isKnownSubstitution:
                    print("This substition is new or changed")
                    containsNews = True 
                    with open(cacheFile, 'a') as file:
                        file.write(hashed + '\n')

            if containsNews:
                print("There is at least one new or changed substitution. Will continue to send info mail.")
                subject = mailSubject(student,date)
                body = mailBody(student,date,substitutions,url)
              
                for email in student["emails"]:
                    SendMail(email,subject,body).send()

    cacheSizeControl()

if __name__ == "__main__":
    main()
