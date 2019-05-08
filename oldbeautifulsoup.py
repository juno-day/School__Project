import requests 
from bs4 import BeautifulSoup
from datetime import datetime
import smtplib
from email.mime.text import MIMEText

r = requests.get('https://events.gotsport.com/events/schedule.aspx?eventid=73009&FieldID=0&applicationID=5233711&action=Go')

c = r.content

soup = BeautifulSoup(c,'html.parser')

tables_for_games = soup.find_all('table',{'border':'0','cellspacing':'0','cellpadding':'10','class':'standings'})

x = 0
time_div = tables_for_games[x].find_all('div',{'class':'MatchTime'})
date_of_game = tables_for_games[x].find_all('th',{'colspan':'7','class':'GroupBoxHeading','style':'background-color:;'})
location = tables_for_games[x].find_all('div',{'style':'padding:2px;font-weight:bold;'})
location_href = location[0].find_all('a')[0]
location_href = 'https://events.gotsport.com/events/'+str(location_href['href'])
home_team = tables_for_games[x].find_all('td',{'class':'homeTeam'})
home_team_href = home_team[0].find_all('a')
home_team_href = home_team_href[0]['href']
home_team_href = 'https://events.gotsport.com/'+home_team_href
home_team_name = home_team[0].text
away_team = tables_for_games[x].find_all('td',{'class':'awayTeam'})
away_team_href = away_team[0].find_all('a')
away_team_href = away_team_href[0]['href']
away_team_href = 'https://events.gotsport.com/'+away_team_href
away_team_name = away_team[0].text
print(time_div[0].text[0:])
print(date_of_game[0].text)
print(location[0].text)
print(location_href)
print()
print(home_team_name,'is the home team')
print(home_team_href)
print()
print(away_team_name,'is the away team')
print(away_team_href)
to_send = str(time_div[0].text[0:])+'\n'+str(date_of_game[0].text)+'\n\n'
to_send = to_send+str(location[0].text)+'\n'+str(location_href)+'\n\n'
to_send = to_send+str(home_team_name+' is the home team(wear white)')+'\n'+str(home_team_href)+'\n\n'
to_send = to_send+str(away_team_name+' is the away team(wear orange)')+'\n'+str(away_team_href)
mail = smtplib.SMTP('smtp.gmail.com',587)
mail.ehlo()
mail.starttls()
mail.login('shoryamal@gmail.com','moon2012')

msg = MIMEText(to_send)
sender = 'shoryamal@gmail.com'
recipients = ['shoryamal@gmail.com','smalani@gmail.com','sarika.malani@gmail.com']
msg['Subject'] = "soccer game"
msg['From'] = sender
msg['To'] = ", ".join(recipients)

# mail.sendmail(sender,recipients,message.encode('utf-8'))
result = mail.sendmail(sender,recipients,msg.as_string())
mail.quit()
print(result)
