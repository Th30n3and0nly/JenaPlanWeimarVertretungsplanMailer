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
    # limit cache to 100 lines
    with open(cacheFile, "r") as f:
        lines = f.readlines()

    if len(lines) > 100:
        print("Cache size > 100 lines. I will only keep latest 100.")
        lines = lines[-100:]

    # Datei überschreiben
    with open(cacheFile, "w") as f:
        f.writelines(lines)
               
def main():
    # our cache file will contain hashes for already known substitutions to mitigate email spam
    try:
        with open(cacheFile, 'x') as file:
            file.write('')
    except FileExistsError:
        pass
        
    with open('students.json') as file:
        students = json.load(file)
  
    for student in students:
        # the substitution plan knows 3 days (today, tomorrow and the day after tomorrow (ignoring weekends, holidays, etc.))
        for day in [0,1,2]:
            [date,substitutions,url] = SubstitutionsChecker.check(day, student["memberships"])
            
            # containsNews decides if a mail will be sent or not
            containsNews = False
            for sub in substitutions:
                print("Assessing found substition:")
                print(date)
                print(student["name"])
                print(sub)
                toHash = ','.join([student["name"],date]+list(sub.values()))
                hashed = hashlib.sha256(toHash.encode('utf-8')).hexdigest()
                print("The substitutions hash is: " + hashed)
                
                isKnownSubstitution = False
                with open(cacheFile) as f:
                    knownSubstitutions =  f.read()
                print("The known, hashed substitutions are:")
                print(knownSubstitutions)
                
                if hashed in knownSubstitutions:
                    print("This substitution is already known.")
                    isKnownSubstitution = True

                if not isKnownSubstitution:
                    print("This substition is new or changed.")
                    containsNews = True 
                    with open(cacheFile, 'a') as file:
                        file.write(hashed + '\n')

            if containsNews:
                print("There is at least 1 new or changed substitution. Will continue to send info mail.")
                subject = mailSubject(student,date)
                body = mailBody(student,date,substitutions,url)
              
                for email in student["emails"]:
                    SendMail(email,subject,body).send()

    cacheSizeControl()

if __name__ == "__main__":
    main()
