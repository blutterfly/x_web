import pandas as pd

def import_data(name):
    df = pd.read_excel("Inflation-data.xlsx", sheet_name=name)
    df = df.drop(["Country Code", "IMF Country Code", "Indicator Type", "Series Name", "Unnamed: 58"], axis=1)
    df = (df.melt(id_vars = ['Country', 'Note'], 
              var_name = 'Date', value_name = 'Inflation'))
    df = df.pivot_table(index='Date', columns='Country',  
                        values='Inflation', aggfunc='sum')
    return df

inf_df = import_data("hcpi_a")
food_df = import_data("fcpi_a")
energy_df = import_data("ecpi_a")



import pandas as pd
import matplotlib.pyplot as plt
import panel as pn
from holoviews import opts
import hvplot.pandas

pn.config.template = 'fast'
pn.config.template.title="Panel Inflation Monitoring Application"

country_widget = pn.widgets.Select(name="Country", value="Switzerland", options=list(inf_df.columns))

def pivot_series(inf_df, country):
    df = pd.DataFrame({'Date':inf_df[country].index, 'Inflation':[round(i, 3) for i in inf_df[country].values]})
    df = df.pivot_table(values='Inflation', columns='Date')
    return df

def make_df_plot(country):
    df = pivot_series(inf_df, country)
    return pn.pane.DataFrame(df.iloc[:, : 17])

def make_df_plot2(country):
    df = pivot_series(inf_df, country)
    return pn.pane.DataFrame(df.iloc[:, 17:34])

def make_df_plot3(country):
    df = pivot_series(inf_df, country)
    return pn.pane.DataFrame(df.iloc[:, 34:])

bound_plot = pn.bind(make_df_plot, country=country_widget)
bound_plot2 = pn.bind(make_df_plot2, country=country_widget)
bound_plot3 = pn.bind(make_df_plot2, country=country_widget)
panel_app = pn.Column(country_widget, bound_plot, bound_plot2, bound_plot3)
panel_app.servable()

years_widget = pn.widgets.RangeSlider(name='Years Range', start=1970, end=2022, value=(1970, 2022), step=1)

def make_inf_plot(country, years):
    df = inf_df[country].loc[inf_df[country].index.isin(range(years[0], years[1]))]
    return df.hvplot(height=300, width=400, label=country + ' Overall Inflation')


bound_plot = pn.bind(make_inf_plot, country=country_widget, years=years_widget)
panel_app = pn.Column(years_widget, bound_plot)
panel_app.servable()

type_plot_widget = pn.widgets.Select(name="Inflation Type", value="Food", options=["Food", "Energy"])

def make_type_plot(plt_type, country, years):
    if plt_type == "Food":
        df = food_df[country].loc[inf_df[country].index.isin(range(years[0], years[1]))]
        return df.hvplot(height=300, width=400, label=country + ' Food Inflation')
    else:
        df = energy_df[country].loc[inf_df[country].index.isin(range(years[0], years[1]))]
        return df.hvplot(height=300, width=400, label=country + ' Energy Inflation')

bound_plot = pn.bind(make_type_plot, plt_type=type_plot_widget, country=country_widget, years=years_widget)
panel_app = pn.Column(type_plot_widget, bound_plot)
panel_app.servable()

hvexplorer = hvplot.explorer(inf_df)
pn.Column(
    '## Feel free to explore the entire dataset!', hvexplorer
).servable()

# TODO  fix error
# panel serve panel_example.py --autoreload --show
# pip