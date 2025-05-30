import plotly.graph_objects as go
import dash_core_components as dcc
import dash_html_components as html


def render_tab(df):
    df['weekday'] = df['tran_date'].dt.day_name()
    grouped = df[df['total_amt']>0].groupby(['Store_type', 'weekday'])['total_amt'].sum().unstack(level=1)
    
    heatmap = go.Figure(data=[go.Heatmap(
        x=grouped.columns,
        y=grouped.index,
        z=grouped.values,
        colorscale='Viridis'
    )], layout=go.Layout(
        title='Udział kanałów sprzedaży według dnia tygodnia',
    ))

    gender_dist = df.groupby(['Store_type', 'Gender'])['cust_id'].nunique().unstack()
    gender_fig = go.Figure(data=[
        go.Bar(name='Kobiety', x=gender_dist.index, y=gender_dist['F']),
        go.Bar(name='Mężczyźni', x=gender_dist.index, y=gender_dist['M'])
    ])
    gender_fig.update_layout(
        title='Rozkład płci klientów według kanału sprzedaży',
        barmode='group'
    )

    prod_cat_dist = df[df['total_amt'] > 0].groupby(['Store_type', 'prod_cat'])['total_amt'].sum().unstack()
    prod_cat_fig = go.Figure()
    
    for prod_cat in prod_cat_dist.columns:
        prod_cat_fig.add_trace(go.Bar(
            name=prod_cat,
            x=prod_cat_dist.index,
            y=prod_cat_dist[prod_cat],
            text=[f'{val/1e6:.2f}M' for val in prod_cat_dist[prod_cat]],
            textposition='auto',
        ))
    
    prod_cat_fig.update_layout(
        title='Rozkład kategorii produktów według kanału sprzedaży',
        barmode='stack',
        legend_title='Kategoria produktu'
    )

    layout = html.Div([
        html.H1('Kanały sprzedaży', style={'text-align': 'center'}),
        
        html.Div([
            html.Div([
                dcc.Graph(id='heatmap-sales', figure=heatmap)
            ], style={'width': '50%'}),
            html.Div([
                dcc.Graph(id='gender-distribution', figure=gender_fig)
            ], style={'width': '50%'})
        ], style={'display': 'flex'}),

        html.Div([
            html.Div([
                dcc.Graph(id='prod-cat-distribution', figure=prod_cat_fig)
            ], style={'width': '100%'})
        ])
    ])

    return layout