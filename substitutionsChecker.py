import urllib.request
import re
from bs4 import BeautifulSoup as bs

class SubstitutionsChecker:
   
    @staticmethod
    def check(day, needles):
  
        urls = [
            "https://vplan.jenaplan-weimar.de/Vertretungsplaene/SchuelerInnen/subst_001.htm",
            "https://vplan.jenaplan-weimar.de/Vertretungsplaene/SchuelerInnen/subst_002.htm",
            "https://vplan.jenaplan-weimar.de/Vertretungsplaene/SchuelerInnen/subst_003.htm"
        ]
        
        page = urllib.request.urlopen(urls[day]).read()
        soup = bs(page,'html.parser')
        date = soup.body.find('div', attrs={'class' : 'mon_title'}).text
    
        tables = soup.find_all('table')
        headers = [header.text for header in tables[-1].find_all('th')]
        if(headers):
            substitutionPlan = list(filter(lambda x:x,[{headers[i]: cell.text for i, cell in enumerate(row.find_all('td'))} for row in tables[-1].find_all('tr')]))
        else:
            substitutionPlan = []
       
        substitutions = []      
        for line in substitutionPlan:
            for needle in needles:
                if(re.search(needle, line["Gruppen"])):
                    substitutions.append(line)

        return [date, substitutions, urls[day]]
