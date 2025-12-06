# JenaPlanWeimarVertretungsplanMailer
Für die Schüler*innen der Jenaplan-Schule Weimar und deren Eltern.

Werde aktiv per Email informiert, wenn der Vertretungsplan Informationen enthält, die dich betreffen. 

Es werden alle 3 online zur Verfügung stehenden Pläne geprüft.

# Verwendung via GitHub Action
Zum regelmäßigen, automatisierten Aufruf des Skripts verwende ich GitHub Actions. 
Das erspart mir einen eigenen Service zur Benachrichtigung zu betreiben.
Das Skript wird 1x pro Stunde aufgerufen, liest alle Stundenpläne und benachrichtigt mich ggf.

Ein Run dauert mit 2 konfigurierten Schülern circa 30 Sekunden. Das summiert sich im Monat ca. 360 Minuten CI/CD-Zeit.
Zur Einordnung: Mit einem kostenlosen GitHub-Account hat man 2000 Minuten CI/CD-Budget im Monat.

## 1. Repository forken
Anleitung, falls nötig:
https://docs.github.com/de/pull-requests/collaborating-with-pull-requests/working-with-forks/fork-a-repo

## 2. Emailadresse anlegen
Das Skript benötigt einen Email-Server (SMTP) und ein Nutzerkonto an diesem, um Emails versenden zu können.
Ich empfehle hierzu ein separates Emailkonto anzulegen, da GitHub diese Zugangsdaten einsehen kann.

Es gibt zahlreiche Anbieter für kostenlose Emailadressen, die Mailversand per SMTP ermöglichen.
Beispiele (keine Empfehlung): gmx.de, mail.de, web.de

## 3. Email konfigurieren
Zum erfolgreichen Mailversand via GitHub Action ist die Definition von 5 Repository-Secrets notwendig.

Die Server-Konfiguration findet man beim jeweiligen Email-Anbieter. Z.B.
- [https://hilfe.web.de/pop-imap/pop3/serverdaten.html](https://hilfe.web.de/pop-imap/pop3/serverdaten.html)
- [https://hilfe.gmx.net/pop-imap/imap/imap-serverdaten.html](https://hilfe.gmx.net/pop-imap/pop3/serverdaten.html)
- [https://mail.de/de/hilfe/nachrichten/externe_e-mail_clients/pop3-imap-smtp_einstellungen](https://mail.de/de/hilfe/nachrichten/externe_e-mail_clients/pop3-imap-smtp_einstellungen)

| Secret Bezeichner | Bedeutung |
| ---               | --- |
| EMAIL_SMTP_SERVER | Der SMTP-Server des gewählten Email-Anbieters (z.B. smtp.mail.de) |
| EMAIL_SMTP_PORT   | Der zugehörige Port, auf dem der Mailserver SMTP via TLS unterstützt (z.B. 587) |
| EMAIL_USER        | Der Nutzeraccount, i.d.R. die zugehörige Emailadresse (z.B. username@mail.de) |
| EMAIL_PASSWORD    | Das Passwort zum Nutzeraccount |
| EMAIL_SENDER      | Die Email-Adresse (username@mail.de) |

<img width="1200" height="915" alt="image" src="https://github.com/user-attachments/assets/3eda6eb7-1df9-4015-8212-fad79e6aa6f7" />

## 4. Zu benachrichtigende Gruppen und Adressat konfigurieren
Das Skript betrachtet die Spalte "Gruppen" im Vertretungsplan und vergleicht die Zellen mit einem gegebenen Muster (via regulärem Ausdruck).
Beispiel: Als Zweitklässler*in in der Stammgruppe "Delfine" muss man den Vertretungsplan für folgende Gruppen beachten:
"Del","2","2c","UG","UG-C","UG-2C"

Außerdem sind der Name des Schülers/der Schülerin und die Email-Adresse(n) zu definieren, die benachrichtigt werden sollen.

Eine Beispielkonfiguration für 2 Schüler.
- Max von den Delfinen, 1. Klasse. Seine Eltern werden benachrichtigt, wenn eine seiner Gruppenzugehörigkeiten im Vertretungsplan auftauchen.
- Moritz von den Wölfen, 6. Klasse. Er erhält seine Benachrichtigung selbst. 

```
[
  {
    "name": "Max",
    "emails": [
      "mutter@gmx.de",
      "vater@gmx.de"
    ],
    "memberships": [
      "Del",
      "UG-(.*)?C",
      "^UG$",
      "1c",
      "^1$"
    ]
  },
  {
    "name": "Moritz",
    "emails": [
      "moritz@web.de"
    ],
    "memberships": [
      "Wöl",
      "MG-(.*)?C",
      "^MG$",
      "6c",
      "^6$"
    ]
  }
]

```
Dies Konfiguration muss als Repository-Secret in mit der Bezeichnung `STUDENTS` hinterlegt werden.
<img width="1189" height="821" alt="image" src="https://github.com/user-attachments/assets/94bb1ae4-2793-467e-bf71-d85f2a2fd8dc" />


# Limitierungen
1. Benachrichtigungen gibt es nur bei Hinzukommen oder Änderung eines relevanten Eintrags im Vertretungsplan. 
Gelegentlich verschwinden Einträge wieder aus dem Vertretungsplan.
Darüber informiert das Tool in seiner aktuellen Form nicht.

2. Der Vertretungsplan ist nicht dafür gedacht maschinell gelesen zu werden.
Daher kommt es immer mal zu Änderungen am Format oder Bezeichnungen, die dem Menschen kaum auffallen, aber den Algorithmus zum stolpern bringen.
In dem Fall muss das Skript den neuen Umständen angepasst werden.
