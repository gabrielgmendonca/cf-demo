import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.metrics.pairwise import cosine_similarity

MAX_NAMES = 100
PLACES = [
    'Restaurante 🍝',
    'Boate 🪩',
    'Centro espírita 🙏',
    'Shopping 🛒',
    'Academia 💪',
    'Estádio de futebol ⚽',
    'Igreja 🕇',
    'Praia 🏖️',
    'Faculdade 🎓',
    'Parque 🌳',
    'Escola 📚',
]

place = st.sidebar.selectbox('De qual ambiente estamos falando?', PLACES)

default = 'ouvir música\nconversar\ncomer\nbeber'
activities = st.sidebar.text_area('O que as pessoas vão fazer nesse lugar?', default)
activities = activities.split('\n')

num_people = st.sidebar.number_input('Número de pessoas', min_value=0, max_value=12, value=4, step=2)

st.title(place)

female_names = pd.read_csv('https://raw.githubusercontent.com/MedidaSP/nomes-brasileiros-ibge/master/ibge-fem-10000.csv', nrows=MAX_NAMES)
male_names = pd.read_csv('https://raw.githubusercontent.com/MedidaSP/nomes-brasileiros-ibge/master/ibge-mas-10000.csv', nrows=MAX_NAMES)

women = female_names.sample(num_people // 2, weights='freq')['nome']
men = male_names.sample(num_people // 2, weights='freq')['nome']
people = pd.concat((women, men)).sample(frac=1)

df = pd.DataFrame(people)
COEF = 0.75 / len(activities)
for i, activity in enumerate(activities):
    df[activity] = np.random.binomial(1, 0.8 - i * COEF, size=num_people)
df = df.sort_values(by=activities, ascending=False)
df = df.set_index('nome')

sim = cosine_similarity(df)
np.fill_diagonal(sim, 0)
sim = pd.DataFrame(sim, index=df.index, columns=df.index)
sim = sim.div(sim.sum(axis=0), axis=1)
recommended = (df + sim.dot(df)).clip(upper=1)

button = False

fig = plt.figure()
if not button:
    ax = sns.heatmap(df, annot=True, cbar=False, cmap='coolwarm_r')
else:
    ax = sns.heatmap(recommended, annot=True, cbar=False, cmap='coolwarm_r')

button = st.checkbox('Recomendado')

ax.set_ylabel('', rotation=90)
ax.xaxis.tick_top()
st.pyplot(fig)
