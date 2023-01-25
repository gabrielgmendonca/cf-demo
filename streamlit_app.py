import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

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

num_people = st.sidebar.number_input('Número de pessoas', min_value=0, max_value=12, value=8)

st.title(place)

female_names = pd.read_csv('https://raw.githubusercontent.com/MedidaSP/nomes-brasileiros-ibge/master/ibge-fem-10000.csv', nrows=MAX_NAMES)
male_names = pd.read_csv('https://raw.githubusercontent.com/MedidaSP/nomes-brasileiros-ibge/master/ibge-mas-10000.csv', nrows=MAX_NAMES)

women = female_names.sample(num_people // 2, weights='freq')['nome']
men = male_names.sample(num_people // 2, weights='freq')['nome']
people = pd.concat((women, men)).sample(frac=1)

df = pd.DataFrame(people)
for activity in activities:
    df[activity] = np.random.randint(2, size=num_people)
df = df.sort_values(by=activities, ascending=False)
df = df.set_index('nome')

fig = plt.figure()
ax = sns.heatmap(df, annot=True, cbar=False, cmap='RdYlGn')
ax.set_ylabel('')
ax.xaxis.tick_top()
st.pyplot(fig)
