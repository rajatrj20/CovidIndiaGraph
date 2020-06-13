import urllib.request, json, re 
from collections import defaultdict
from matplotlib.pyplot import figure
import matplotlib.pyplot as plt

def valueToDec(x, y, z):
  #Function to convert into Float values between [0,1] for RGB
  return (x/255, y/255, z/255)

data = None
number_of_graphs=4 #Number of Different Categories (Confirmed, Active, Recovered, Deceased)

with urllib.request.urlopen("https://api.covid19india.org/data.json") as url:
    data = json.loads(url.read().decode())

#Dictionaries to hold data Month-wise
datesByMonthDict = defaultdict(list)
totalConfirmedMonthWiseDict = defaultdict(list)
totalRecoveredMonthWiseDict = defaultdict(list)
totalActiveMonthWiseDict = defaultdict(list)
totalDeceasedMonthWiseDict = defaultdict(list)

for value in data["cases_time_series"]:
  monthValue = re.sub("[0-9 ]+", "", value["date"])
  datesByMonthDict[monthValue].append((re.sub("[A-Za-z ]+", "", value["date"])))
  totalConfirmedMonthWiseDict[monthValue].append(int(value["totalconfirmed"]))
  totalRecoveredMonthWiseDict[monthValue].append(int(value["totalrecovered"]))
  totalActiveMonthWiseDict[monthValue].append(int(value["totalconfirmed"]) - int(value["totaldeceased"]) - int(value["totalrecovered"]))
  totalDeceasedMonthWiseDict[monthValue].append(int(value["totaldeceased"]))

fig,ax =  plt.subplots(len(datesByMonthDict), number_of_graphs, figsize=(12*number_of_graphs,30))

i=0
for month in datesByMonthDict:
    #Plot for Confirmed Cases
    ax[i][0].set(ylabel=month, title='Total')
    ax[i][0].bar(datesByMonthDict[month], totalConfirmedMonthWiseDict[month], color=valueToDec(186, 218, 85), width=0.6)
    for j, v in enumerate(totalConfirmedMonthWiseDict[month]):
      ax[i][0].text(j, v, str(v), color=valueToDec(46, 34, 87), ha='center')

    #Plot for Active Cases
    ax[i][1].set(ylabel=month, title='Active')
    ax[i][1].bar(datesByMonthDict[month], totalActiveMonthWiseDict[month], color=valueToDec(255, 165, 0), width=0.6)
    for j, v in enumerate(totalActiveMonthWiseDict[month]):
      ax[i][1].text(j, v, str(v), color=valueToDec(0, 0, 0), ha='center')

    #Plot for Recovered Cases
    ax[i][2].set(ylabel=month, title='Recovered')
    ax[i][2].bar(datesByMonthDict[month], totalRecoveredMonthWiseDict[month], color=valueToDec(127, 229, 240), width=0.6)
    for j, v in enumerate(totalRecoveredMonthWiseDict[month]):
      ax[i][2].text(j, v, str(v), color=valueToDec(240, 138, 127), ha='center')
    
    #Plot for Deaths Cases
    ax[i][3].set(ylabel=month, title='Deaths')
    ax[i][3].bar(datesByMonthDict[month], totalDeceasedMonthWiseDict[month], color=valueToDec(217, 83, 79), width=0.6)
    for j, v in enumerate(totalDeceasedMonthWiseDict[month]):
      ax[i][3].text(j, v, str(v), color=valueToDec(79, 213, 217), ha='center')
    i+=1

plt.show()
