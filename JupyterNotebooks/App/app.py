# Import data modules
import pandas as pd
# Import dash for web app
from dash import Dash, dcc, html, Input, Output, State
import dash_bootstrap_components as dbc

# Load in books data and books_similarity matrix
books = pd.read_pickle('../../Data/books.pkl')
similarity_scores = pd.read_pickle('../../Data/books_similarity_scores.pkl')

app = Dash(__name__, external_stylesheets=[dbc.themes.SKETCHY])
server = app.server

app.layout = html.Div([
    html.H1('Book Recommender', style={'font-size': '75px'}),
    dcc.Dropdown(
        id='book-selector',
        options=[{'label': f"{row['original_title']} by {row['author']}", 'value': row['work_id']} for _, row in books.iterrows()],
        multi=True,
        maxHeight=200,
        placeholder="Select Up to Five Books",
        style={'width': '90%', 'margin-left': 'auto', 'margin-right': 'auto','display': 'block'}
    ),
    html.Br(),
    html.Label('Choose Page Range:'),
    dcc.RangeSlider(
        id='page-range-slider',
        min=0,
        max=round(books['num_pages'].max() + 49, -2),
        step=50,
        marks={i: str(i) for i in range(0, int(books['num_pages'].max()), 100)},
        value=[0, round(books['num_pages'].max() + 49, -2)],
        allowCross=False
    ),
    html.Br(),
    html.Button("Get Recommendations", id='recommend-btn', n_clicks=0),
    html.Br(),
    html.Div(id='recommendations', style={'display': 'flex', 'flex-wrap': 'wrap', 'gap': '60px', 'justify-content': 'center', 'padding': '10px'})
    ],
    style={'text-align': 'center', 'justifyContent': 'center', 'backgroundColor': '#D6BB87'}
)

@app.callback(
    Output('recommendations', 'children'),
    Input('recommend-btn', 'n_clicks'),
    State('page-range-slider', 'value'),
    State('book-selector', 'value'),
)
def update_recommendations(n_clicks, page_range, selected_books):
    if n_clicks == 0:
        return "Select books and click 'Get Recommendations'"

    if not selected_books or len(selected_books) == 0:
        return "Please select at least one book."

    if len(selected_books) > 5:
        return "Please select no more than 5 books."

    # Get the max (changed from average) similarity_scores of each book compared to the books in book_list
    similarity_scores_sub = pd.DataFrame(similarity_scores.loc[:, selected_books].max(axis=1), columns=['mean_sim_score'])

    filtered_books = books[books['num_pages'].between(page_range[0], page_range[1], inclusive='both')]
    
    # Get all the information for each book and sort by mean_sim_score
    recommendations = (similarity_scores_sub.reset_index()
                                            .merge(filtered_books, left_on='index', right_on='work_id', how='inner')
                                            .sort_values(by='mean_sim_score', ascending=False)
                      )

    # Remove books from books_list from recommendations and return num_rec rows
    recommendations = recommendations[~recommendations['work_id'].isin(selected_books)].iloc[:5]

    cards = []
    for _, row in recommendations.iterrows():
        card = html.Div([
        html.Div([
            html.Div([
            # Front of card
            html.Div([
                html.Img(src=row['image_url'], style={'width': '120px', 'height': '180px', 'object-fit': 'cover'}),
                html.H4(row['original_title'], style={'margin': '5px 0 0 0', 'fontSize': '14px'}),
                html.P(row['author'], style={'fontSize': '12px'}),
            ], className='card-front'),

            # Back of card
            html.Div([
                html.P(row['description'], style={'fontSize': '10px'}),
                html.B('Rating'),
                html.P(row['avg_rating']),
                html.B('Year'),
                html.P(int(row['original_publication_year'])),
                html.B('Pages'),
                html.P(int(row['num_pages']))
            ], className='card-back')

                    ], className='card-flip')
                ], className='card-container')
        ])
        cards.append(card)

    return cards

if __name__ == '__main__':
    app.run(debug=True)