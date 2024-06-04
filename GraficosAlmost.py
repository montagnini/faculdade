#Barra
import matplotlib.pyplot as plt
import pandas as pd
import re
import json

# Dados do modelo da coluna
#/kaggle/input/the-movies-dataset/movies_metadata.csv
df = pd.read_csv('C:\\Users\\Wemon\\OneDrive\\Área de Trabalho\\Nova pasta\\faculdade\\movies_metadata.csv', low_memory=False)

def preparaIndicesHistograma():
    indices = []
    value = 1880
    while value < 2021:
        indices.append(value)
        value += 10
        
    return indices


generosQuantidade = {}
anosTotais = {}
notasPorGeneroTotal = {}
i = 0
for indice, row in df.iterrows():
    genero = row['genres']
    data = row['release_date']
    nota = float(row['vote_average'])
    
    #logica para os generos:
    genero = genero.replace("'", '"')
    array_generos = json.loads(genero)
    
    for generoFilme in array_generos:
        filme = generoFilme['name']
        
        if filme in generosQuantidade:
            generosQuantidade[filme] += 1
        else:
            generosQuantidade[filme] = 1

        #Verifica se a nota é válida
        if not pd.isna(nota):
            #Verifica se o genero já foi obtido, se sim, soma no valor total para obtenção da nota
            if filme in notasPorGeneroTotal:
                notasPorGeneroTotal[filme] += nota
            else:
                notasPorGeneroTotal[filme] = nota
        else:
            #Apenas filmes avaliados estarão na lista de generos.
            generosQuantidade[filme] -= 1

    if(data and len(str(data)) > 0 and not data is None and re.match(r'\d{4}-\d{1,2}-\d{1,2}', str(data))):
        ano = pd.to_datetime(data).year
        if ano in anosTotais:
            anosTotais[ano] += 1
        else:
            anosTotais[ano] = 1
        

#Limpeza de dados de genero
generosFinal = {}
notasGeneroFinal = {}
for genero in generosQuantidade:
    #limpeza de dados 
    if generosQuantidade[genero] > 10:
        generosFinal[genero] = generosQuantidade[genero]
        notasGeneroFinal[genero] = notasPorGeneroTotal[genero]


#Preparação gráfico de dispersão

generoPorNota = {}  
for genero in generosFinal:
    totalGenero = generosFinal[genero] 
    totalNota = notasGeneroFinal[genero]
    mediaFinalPorGenero = round(totalNota/totalGenero, 2)
    generoPorNota[genero] = mediaFinalPorGenero

notas_ordenadas = sorted(generoPorNota.items(), key=lambda item: item[1], reverse=False)

#Gráficos
fig, (barras, dispersao, histograma) = plt.subplots(nrows=3, ncols=1, figsize=(25,10))
plt.subplots_adjust(hspace=0.45, top=0.95, bottom=0.08)

# Cria o gráfico de barras
barras.bar(list(generosFinal.keys()),  list(generosFinal.values()))
barras.set_xlabel("Genero")
barras.set_ylabel("Quantidade")
barras.set_title("Quantidade de filme por genero")


# Cria o gráfico de dispersão
generos, notas = zip(*notas_ordenadas)
dispersao.scatter(generos, notas)

dispersao.set_xlabel("Genero")
dispersao.set_ylabel("Nota")
dispersao.set_title("Genero por nota")


#Cria o gráfico de Histograma

anos = [year for year, _ in sorted(anosTotais.items(), key=lambda x: x[0])]
frequencia = [freq for _, freq in sorted(anosTotais.items(), key=lambda x: x[0])]
#
histograma.hist(anos, weights=frequencia, bins=26, edgecolor='black')
histograma.set_xticks(preparaIndicesHistograma())
histograma.set_xlabel("Ano")
histograma.set_ylabel("Contagem de registros")
histograma.set_title("Histograma de filmes por ano")


plt.show()
