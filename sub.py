import plotly.express as px
import pandas as pd
import cufflinks as cf

df = pd.read_csv('OECDBLI2017.csv')
df.head()

new_data = df.set_index('Country')['Employment rate as pct'].sort_values(ascending=False)

fig = px.bar(x=new_data.index, y=new_data.values,
             title='Employment Rate by Country',
             labels={'x': 'Country', 'y': 'Employment Rate (%)'})
fig.show()