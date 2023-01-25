import streamlit as st
import pandas as pd
import seaborn as sns

num_people = st.number_input('Número de pessoas', 8)

default = 'ouvir música\nconversar\ncomer'
activities = st.text_area('O que as pessoas vão fazer nesse lugar?', default)
activities = activities.split('\n')

female_names = pd.read_csv('https://raw.githubusercontent.com/MedidaSP/nomes-brasileiros-ibge/master/ibge-fem-10000.csv')
male_names = pd.read_csv('https://raw.githubusercontent.com/MedidaSP/nomes-brasileiros-ibge/master/ibge-mas-10000.csv')

women = female_names.sample(num_people // 2, weights='freq')['nome']
men = male_names.sample(num_people // 2, weights='freq')['nome']
people = pd.concat((women, men)).sample(frac=1)

df = pd.DataFrame(people)
for activity in activities:
    df[activity] = np.random.randint(2, size=NUM_PEOPLE)
df = df.sort_values(by=activities, ascending=False)
df = df.set_index('nome')

ax = sns.heatmap(df, annot=True, cbar=False, cmap='RdYlGn');
st.pyplot(ax)
