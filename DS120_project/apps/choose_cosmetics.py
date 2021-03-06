#one of the pages of the app, where the person chooses its skintype and the product is recommended

import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate
import dash
import plotly.express as px
import pandas as pd
import pathlib
#import app
from app import app
import dash_table
import dash_bootstrap_components as dbc



# get relative data folder, we are doiing this, as the datasets are in the datasets folder, not the current directory
PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../datasets").resolve()

df = pd.read_csv(DATA_PATH.joinpath("Sephora_cosmetics_df.csv"))


app.config['suppress_callback_exceptions']=True

layout = html.Div(
       
    
    children = [
    html.Div([
        html.H1("Choose Cosmetics",
            style={
                'vertical-align':'buttom',
                'textAlign':'center',
                'font-family':'Segoe Print',
                
                
                'color':'#1A3E5C', 
                'background-color':'#AFC4D5', 
                'height':'70px',
                'text-align':'50PX',
                'border-radius':'25px',                
                "boxShadow": "0px 15px 30px -10px grey",
                
                }
        )   
    ]),
    
    
    

    html.Div([
        html.H1('We will help you to choose the best fitting skincare product.\n', 
        style={
            'margin':'25px',
            'text-align':'center',
            'color':'#1A3E5C',
            'font-family':'cursive'
        }),
        
            
        
    html.H2("Please specify the skincare product you want.", 
        style={
            'color':'#1A3E5C',
            'margin':'15px',
            'font-family':'cursive'
           
        }),
    dcc.Dropdown( #dropdown for product type
            id = 'product_dd',
            options=[
                {'label': 'Moisturizer', 'value': 'Moisturizer'},
                {'label': 'Cleanser', 'value': 'Cleanser'},
                {'label': 'Treatment', 'value': 'Treatment'},
                {'label': 'Eye cream', 'value': 'Eye cream'},
                {'label': 'Sun protect', 'value': 'Sun protect'},
                {'label': 'Face Mask', 'value': 'Face Mask'},
                {'label': 'Not sure', 'value' : 'Not sure'}
            ],
            style = {
                'color':'navy',
                'background-color':'#AFC4D5', 
                
                'margin-top':'25px',
                'margin-bottom':'25px',
                'borderRadius':'25px',
                'font-size':'20px',
            },
            #value=['Moisturizer'], #the default value set
            multi=True
        ),
    html.H2("Please, specify your skin type.\n", 
            style= {
                'color':'#1A3E5C',
                'margin':'15px',
                'margin-top':'70px',
                'font-family':'cursive'
            }),
    html.H2("Here is a picture that can help you determine the skin type. If anyway you cannot do it, please select 'Not sure' option.\n", 
        style= {
                'color':'#1A3E5C',
                'margin':'15px',
                'font-family':'cursive'
            }),
    html.Div([
    html.Img(
        src=app.get_asset_url('skintypes.jpg'),
        style={
            'border-style':'solid',
            'border-color':'navy',
            'borderRadius':'50px',
            
            'display':'block',
            
        }),
    ],
    style = {
        'text-align':'center',
        'margin-left':'20%',
        'margin-right':'20%'
    }),
    dcc.Dropdown( #dropdown for skin type
                id = 'skintype_dd',
                options=[
                    {'label': 'Oily', 'value': 'Oily'},
                    {'label': 'Dry', 'value': 'Dry'},
                    {'label': 'Combination', 'value': 'Combination'},
                    {'label': 'Sensitive', 'value': 'Sensitive'},
                    {'label' : 'Normal', 'value' : 'Normal'},
                    {'label': 'Not sure', 'value' : 'Not sure'}
                ],
                style = {
                'color':'navy',
                'background-color':'#AFC4D5', 
                'margin-top':'25px',
                'margin-bottom':'25px',
                'borderRadius':'25px',
                'font-size':'20px'
            },
                
                multi=True
            ),
    
    html.H2('Here is a table with the most suitable cosmetics products for you:', 
            style= {
                'color':'#1A3E5C',
                'margin':'20px',
                'font-family':'cursive'
            }),

    dash_table.DataTable(#this table is outputed based on the given labels and skin types. The table is updated every time the user changes the input

        id='my_output',
        style_header={
            'border':'1px solid indigo', 
            'fontWeight':'bold'},
        style_cell={
            'backgroundColor':'#98B2C8',
            'whiteSpace':'normal',
            'height':'auto',
            'color':'navy',
            'margin':'500px',
            'borderRadius':'25px',
            'border':'1px solid indigo',
            'textAlign':'left',
            'font-family':'cursive'
        
        },
        

        
    ),
    html.H1('Thank you for using our app!', 
        style = {
            'margin-top':'250px',
            'margin-left':'25px',
            'margin-right':'25px',
            'font-family':'cursive',
            'color':'#1A3E5C', 
            
        }),
    html.Img(#cute cat photo
        src=app.get_asset_url('cat.jpg'),
        style = {
            'margin-left':'25px',
            'height':'300px',
            
            
        }
    )
    ]),
    
],
style = {
    'backgroundColor':'lavender',
    'marginBottom':'0px',
    'margin-bottom':'0px',
    'margin-left':'10%',
    'margin-right':'10%',
    },

),

    
 



@app.callback(
    [Output(component_id='my_output', component_property="data"),
    Output(component_id='my_output', component_property="columns")],
    [Input(component_id='product_dd', component_property='value'),
    Input(component_id ='skintype_dd', component_property='value')]
)
#def update_output_div(input_value):#
#    return 'Output: {}'.format(input_value)
def cosmetics(label, skintype):
    '''this function takes label(skincare product) and the skin type. Both inputs must be lists of strings.
    There are 4 cases for this function.
        
    '''
    if label is None and skintype is None:
        raise PreventUpdate
    if ('Not sure' not in skintype) and ('Not sure' in label):
        df_full = df[df.Rank >=4.5]
        skintypes_test = {}
        for i in df_full.index:
            skins = []
            the_best_one_test = df_full[df_full.index == i]
            if the_best_one_test.Combination[i] == 1:
                skins.append('Combination')
            if the_best_one_test.Dry[i] == 1:
                skins.append('Dry')
            if the_best_one_test.Normal[i] == 1:
                skins.append('Normal')
            if the_best_one_test.Oily[i] == 1:
                skins.append('Oily')
            if the_best_one_test.Sensitive[i] ==1:
                skins.append('Sensitive')
            skintypes_test[i] = skins
        matched=[]
        for i, v in zip(skintypes_test.keys(), skintypes_test.values()):
            if set(skintype).issubset(set(v)):
                matched.append(i)
        final = df_full.loc[matched]
        final.drop_duplicates(inplace = True)
        final.sort_values('Rank', ascending=False, inplace=True)
        final.drop_duplicates('Label', inplace=True)
        final = final[['Label','Brand', 'Name', 'Price', 'Rank']]
        final.reset_index(inplace = True, drop=True)
        return final.to_dict('records'), [{"name": i, "id": i} for i in final.columns]

    elif ('Not sure' in skintype) and ('Not sure' not in label):
        df_label = df[df.Label.apply(lambda x: x in label)]
        df_label = df_label[df_label.Rank >=4.5]
        skintypes_test = {}
        for i in df_label.index:
            skins = []
            the_best_one_test = df_label[df_label.index == i]
            if the_best_one_test.Combination[i] == 1:
                skins.append('Combination')
            if the_best_one_test.Dry[i] == 1:
                skins.append('Dry')
            if the_best_one_test.Normal[i] == 1:
                skins.append('Normal')
            if the_best_one_test.Oily[i] == 1:
                skins.append('Oily')
            if the_best_one_test.Sensitive[i] ==1:
                skins.append('Sensitive')
            skintypes_test[i] = skins

        more_skins = []
        for i, v in zip(skintypes_test.keys(), skintypes_test.values()):
            if len(v) == 5:
                more_skins.append(i)
        if len(more_skins)==0:
            for i, v in zip(skintypes_test.keys(), skintypes_test.values()):
                if len(v) == len(max(skintypes_test.values())):
                    more_skins.append(i)


        final = df_label.loc[more_skins]
        final.drop_duplicates(inplace = True)
        final.sort_values('Rank', ascending=False, inplace=True)
        final.drop_duplicates('Brand', inplace=True)
        final = final[['Brand', 'Name', 'Price', 'Oily', 'Combination', 'Dry', 'Sensitive', 'Normal']]
        final.reset_index(inplace = True, drop=True)
        return final.to_dict('records'), [{"name": i, "id": i} for i in final.columns]

    elif ('Not sure' not in skintype) and ('Note sure' not in label):
        df_label = df[df.Label.apply(lambda x: x in label)]
        df_label = df_label[df_label.Rank >=4.5]
        skintypes_test = {}
        for i in df_label.index:
            skins = []
            the_best_one_test = df_label[df_label.index == i]
            if the_best_one_test.Combination[i] == 1:
                skins.append('Combination')
            if the_best_one_test.Dry[i] == 1:
                skins.append('Dry')
            if the_best_one_test.Normal[i] == 1:
                skins.append('Normal')
            if the_best_one_test.Oily[i] == 1:
                skins.append('Oily')
            if the_best_one_test.Sensitive[i] ==1:
                skins.append('Sensitive')
            skintypes_test[i] = skins

        matched=[]
        for i, v in zip(skintypes_test.keys(), skintypes_test.values()):
            if set(skintype).issubset(v):
                matched.append(i)

        final = df_label.loc[matched]
        final.drop_duplicates(inplace = True)
        final.sort_values('Rank', ascending=False, inplace=True)
        final.drop_duplicates('Brand', inplace=True)
        final = final[['Brand', 'Name', 'Price']]
        final.reset_index(inplace = True, drop=True)
        return(final.to_dict('records'), [{"name": i, "id": i} for i in final.columns])
    elif ('Not sure' in label) and ('Not sure' in skintype):
        df_full = df[df.Rank >=4.5]
        skintypes_test = {}
        for i in df_full.index:
            skins = []
            the_best_one_test = df_full[df_full.index == i]
            if the_best_one_test.Combination[i] == 1:
                skins.append('Combination')
            if the_best_one_test.Dry[i] == 1:
                skins.append('Dry')
            if the_best_one_test.Normal[i] == 1:
                skins.append('Normal')
            if the_best_one_test.Oily[i] == 1:
                skins.append('Oily')
            if the_best_one_test.Sensitive[i] ==1:
                skins.append('Sensitive')
            skintypes_test[i] = skins

        more_skins = []
        for i, v in zip(skintypes_test.keys(), skintypes_test.values()):
            if len(v) == 5:
                more_skins.append(i)
        if len(more_skins)==0:
            for i, v in zip(skintypes_test.keys(), skintypes_test.values()):
                if len(v) == len(max(skintypes_test.values())):
                    more_skins.append(i)


        final = df_full.loc[more_skins]
        final.drop_duplicates(inplace = True)
        final.sort_values('Rank', ascending=False, inplace=True)
        final.drop_duplicates('Label', inplace=True)
        final = final[['Label','Brand', 'Name', 'Price', 'Rank','Oily', 'Combination', 'Dry', 'Sensitive', 'Normal']]
        final.reset_index(inplace = True, drop=True)
        return(final.to_dict('records'), [{"name": i, "id": i} for i in final.columns])



# if __name__ == '__main__':
#     app.run_server(debug=True)