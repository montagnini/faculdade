#Barra
import matplotlib.pyplot as plt
import pandas as pd
import re
import json

# Dados do modelo da coluna
#/kaggle/input/the-movies-dataset/movies_metadata.csv
df = pd.read_csv('./movies_metadata.csv', low_memory=False)

#Função utilizada para criação dos indices do histograma
def preparaIndicesHistograma():
    indices = []
    value = 1880
    while value < 2021:
        indices.append(value)
        value += 5
    return indices

#Variável utilizada futuramente para o cálculo do gráfico de barras (Filme por genero)
generosQuantidade = {}
#Variável utilizada futuramente para o cálculo do gráfico de histograma (Filmes por ano)
anosTotais = {}
#Variável utilizada futuramente para o cálculo do gráfico de dispersão (Nota por genero)
notasPorGeneroTotal = {}

#Percorre as linhas do dataset
for indice, row in df.iterrows():
    #obtém o genero da linha
    genero = row['genres']
    #obtém a data da linha
    data = row['release_date']
    #obtém a nota da linha
    nota = float(row['vote_average'])
    
    #logica para os generos:
    #remove os caracteres que não são utilizados
    genero = genero.replace("'", '"')
    #Obtém o array de generos (mais do que um por filme)
    array_generos = json.loads(genero)
    
    #Percorre array de generos
    for generoFilme in array_generos:
        #Obtém o genero
        nomeGenero = generoFilme['name']

        #Verifica se o genero já foi obtido, se sim, soma no valor total para obtenção da quantidade
        if nomeGenero in generosQuantidade:
            generosQuantidade[nomeGenero] += 1
        else:
            generosQuantidade[nomeGenero] = 1

        #Verifica se a nota é válida
        if not pd.isna(nota):
            #Verifica se o genero já foi obtido, se sim, soma no valor total para obtenção da nota
            if nomeGenero in notasPorGeneroTotal:
                notasPorGeneroTotal[nomeGenero] += nota
            else:
                notasPorGeneroTotal[nomeGenero] = nota
        else:
            #Apenas filmes avaliados estarão na lista de generos.
            generosQuantidade[nomeGenero] -= 1

    #logica para anos:
    #Verifica se obteve corretamente a data e se ela está no formato correto (valores inválidos no meio)
    if(data and len(str(data)) > 0 and not data is None and re.match(r'\d{4}-\d{1,2}-\d{1,2}', str(data))):\
        #obtém o ano
        ano = pd.to_datetime(data).year
        #Verifica se o ano já foi obtido, se sim, soma no valor total para obtenção da quantidade
        if ano in anosTotais:
            anosTotais[ano] += 1
        else:
            anosTotais[ano] = 1
        

#Limpeza de dados de genero (existem dados com apenas 1 filme dentro do genero, gerando erro nas visualizações)
generosFinal = {}
notasGeneroFinal = {}
for genero in generosQuantidade:
    #limpeza de dados 
    if generosQuantidade[genero] > 10:
        #Adiciona nos arrays 'finais' utilizados futuramente para as visualizações
        generosFinal[genero] = generosQuantidade[genero]
        notasGeneroFinal[genero] = notasPorGeneroTotal[genero]


#Preparação gráfico de dispersão
generoPorNota = {}
#Percorre generos
for genero in generosFinal:
    totalGenero = generosFinal[genero] 
    totalNota = notasGeneroFinal[genero]
    #Calcula média
    mediaFinalPorGenero = round(totalNota/totalGenero, 2)
    #Adiciona no array final
    generoPorNota[genero] = mediaFinalPorGenero

#Gráficos
fig, (barras, dispersao, histograma) = plt.subplots(nrows=3, ncols=1, figsize=(25,10))

plt.subplots_adjust(hspace=0.45, top=0.95, bottom=0.08)

# Cria o gráfico de barras
#Dados
barras.bar(list(generosFinal.keys()),  list(generosFinal.values()), color='#ff8d00')

#Gráfico
barras.set_xlabel("Genero")
barras.set_ylabel("Quantidade")
barras.set_title("Quantidade de filme por genero")
barras.grid(True, which='both', linestyle='--', linewidth=0.25)

# Cria o gráfico de dispersão
#Dados
#Reordena 
notas_ordenadas = sorted(generoPorNota.items(), key=lambda item: item[1], reverse=False)

generos, notas = zip(*notas_ordenadas)
dispersao.scatter(generos, notas, color='#7C4DFF')

#Gráfico
dispersao.set_xlabel("Genero")
dispersao.set_ylabel("Nota")
dispersao.set_title("Genero por nota")
dispersao.grid(True, which='both', linestyle='--', linewidth=0.25)

#Cria o gráfico de Histograma
#Dados
anos = [year for year, _ in sorted(anosTotais.items(), key=lambda x: x[0])]
frequencia = [freq for _, freq in sorted(anosTotais.items(), key=lambda x: x[0])]

#Gráfico
histograma.hist(anos, weights=frequencia, bins=135, edgecolor='black', color='#018786')
histograma.set_xticks(preparaIndicesHistograma())
histograma.set_xlabel("Ano") 
histograma.set_ylabel("Contagem de registros")
histograma.set_title("Histograma de filmes por ano")
histograma.grid(True, which='both', linestyle='--', linewidth=0.25)


plt.show()
