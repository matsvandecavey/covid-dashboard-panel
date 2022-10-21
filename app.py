import panel as pn

import pandas as pd
import hvplot.pandas

df = pd.read_csv(
    r'https://storage.googleapis.com/covid19-open-data/v3/hospitalizations.csv',
    skiprows=range(1,374907),
    nrows=10980)

df_BE = df.loc[[x.startswith('BE') for x in df.location_key]]
df_BE = df_BE.set_index('date').dropna(axis=1)

df_BE.index = pd.to_datetime(df_BE.index)

variables = [x for x in df_BE.columns if not x =='location_key']
locations = list(df_BE.location_key.unique())

w_var = pn.widgets.Select(options=variables,name='variable to plot')
w_loc = pn.widgets.MultiSelect(options=locations,
    name='location',
    value=['BE'],
    height=200)

def return_loc(loc,plot_var):
    df_loc_BE = df_BE.query(f'location_key in {loc}')
    return df_loc_BE.hvplot(y=plot_var,by='location_key')

dashboard = pn.Column('## Covid in Belgium',
    w_loc,
    w_var,
    pn.bind(return_loc,loc=w_loc,plot_var=w_var))

dashboard.servable()