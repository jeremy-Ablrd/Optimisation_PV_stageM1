import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import csv


def factor_transpo(i, gamma):
#Les différents paramètres
    f1 = pd.read_csv("secteurOuest_Annee.csv", delimiter=';')
    f2 = pd.read_csv("SoDa_HC3-METEO_lat-21.163_lon55.326_Annee.csv", delimiter=';')
    f2.drop(["Clear-Sky","Top of Atmosphere","Code","Temperature","Relative Humidity","Pressure","Wind speed", "Wind direction" ,"Rainfall","Snowfall","Snow depth"], axis=1)
    f3 = [f1, f2]
    f3 = pd.concat(f3, axis=1)
    zenith = 90 - f3['Zenith (refracted)']
    g = f3['Global Horiz']
    azimuth = f3['Azimuth angle'] - 180
    Dh = (1 / 3) * g
    alpha = 0.1

#Rayonnement direct S*
    def solar_direct(h, a, i, gamma):
        s = g * (np.cos(np.radians(h)) * np.sin(np.radians(i)) * np.cos(np.radians(gamma) - np.radians(a)) + np.sin(np.radians(h)) * np.cos(np.radians(i)))
        return s

#Rayonnement diffus D*
    def solar_diffus(i):
        h = zenith
        d = ((1 + np.cos(np.radians(i))) / 2) * Dh + alpha * ((1 - np.cos(np.radians(i))) / 2) * (Dh + g * np.sin(np.radians(h)))
        return d

#Calcule du boucle temps :
    def sum_operator(i):
        num = (solar_direct(zenith, azimuth, i, gamma) + solar_diffus(i))
        sum = num.sum(axis=0)
        return sum

#Calcule du facteur de transposition
    FT = sum_operator(i)/sum_operator(0)
    return FT

#Création de fichier avec titre : FactTrans, Inclinaison et orientation
with open('FactorT.csv', 'w') as csvtitre:
    csvtitre.write('FactTrans' + ',')
    csvtitre.write('Inclinaison' + ',')
    csvtitre.write('Orientation' + '\n')
    csvtitre.close()

#Boucle 'for' pour chaque i et gamma variant FT
for i in range(0, 90 + 1, 5):
    for gamma in range(-180, 180 + 1, 10):
        data = factor_transpo(i, gamma)

#Ajouter au fichier l'évalution du facteur de transposition
        with open('FactorT.csv', 'a+') as csvfile:
        #file = csv.writer(csvfile, delimiter=',')
            csvfile.write(str(data) + ",")
            csvfile.write(str(i) + ",")
            csvfile.write(str(gamma) + "\n")
            csvfile.close()

#Visualisation du graphique heatmap
f4 = pd.read_csv("FactorT.csv", delimiter=',')
flux = f4.pivot('Inclinaison', 'Orientation', 'FactTrans')
plt.figure(figsize=(9,6))
flux_data = sns.heatmap(flux, cmap="YlOrRd")
plt.show()

#f4 = pd.read_csv("FactorT.csv", delimiter=',')
#flux = f4.pivot('Inclinaison', 'Orientation', 'FactTrans')
#flux_data = sns.heatmap(flux, cmap="YlOrRd", xticklabels=10, yticklabels=5)
#plt.show()