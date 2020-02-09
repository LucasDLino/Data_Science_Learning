import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

#Criação da população
population = np.random.randint(0,600, size=100)

#Lista contendo as amostras bootstraps
#Lista com as médias ("estatísticas") de cada amostra
samples = []
statistics = []
for i in range(100):
    bootsamples = np.random.choice(population, size=100, replace=True)
    samples.append(bootsamples)
    statistics.append(bootsamples.mean())

#Para visualização das amostras
show = pd.DataFrame(samples)

#Calculando o intervalo de confiança
alpha = float(input("Digite o intervalo de confiança: "))/100.0
percent_l = ((1.0-alpha)/2.0) * 100.0
percent_u = (alpha+((1.0-alpha)/2.0)) * 100.0
ordered = np.sort(statistics)
lower = np.percentile(ordered, percent_l)
upper = np.percentile(ordered, percent_u)

#Output
print("Intervalo de confiança de %.2f %%" %alpha*100)
print("Intervalo inferior: %.2f" %lower)
print("Intervalo superior: %.2f" %upper)
print("Média : %.2f" %np.mean(statistics))

fig = plt.figure(figsize=(16,9))

plt.hist(statistics)
plt.xlabel("Médias")
plt.ylabel("Qtd. de Amostras")
plt.title("Distribuição das médias das amostragens")
plt.show()

#Outra forma
results = {"mean": show.mean(axis=1)}
results = pd.DataFrame(results)
results = results.sort_values('mean')
bootstrap = {"mean": results.mean(axis=0), 'inf': results.quantile(percent_l/100.0), 'sup': results.quantile(percent_u/100.0)}
bootstrap = pd.DataFrame(bootstrap)