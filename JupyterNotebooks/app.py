# Import data modules
import pandas as pd

# Import dash for web app
from dash import Dash, dcc, html, Input, Output, State

# Load in books data and books_similarity matrix
books = pd.read_pickle('../Data/books.pkl')
similarity_scores = pd.read_pickle('../Data/books_similarity_scores.pkl')

def content_based_recommender(selected_ids, page_range):

    # Get the average similarity_scores of the books in the book list for each book
    similarity_scores_sub = pd.DataFrame(similarity_scores.loc[:, selected_ids].mean(axis=1), columns=['mean_sim_score'])

    filtered_books = books[books['num_pages'].between(page_range[0], page_range[1], inclusive='both')]
    
    # Get all the information for each book and sort by mean_sim_score
    recommendations = (similarity_scores_sub.reset_index()
                                            .merge(filtered_books, left_on='index', right_on='work_id', how='inner')
                                            .sort_values(by='mean_sim_score', ascending=False)
                      )

    # Remove books from books_list from recommendations and return num_rec rows
    recommendations = recommendations[~recommendations['work_id'].isin(selected_ids)].iloc[:5]
        
    return recommendations

def collaborative_recommender(selected_ids):
    return content_based_recommender(selected_ids)

app = Dash(__name__)
server = app.server

app.layout = html.Div([
    html.H1('Build a Reading List', style={'textAlign': 'center'}),

    html.Label("Select up to 5 books you like:"),
    dcc.Dropdown(
        id='book-selector',
        options=[{'label': f"{row['original_title']} by {row['author']}", 'value': row['work_id']} for _, row in books.iterrows()],
        multi=True,
        maxHeight=200,
        placeholder="Search and select books...",
        style={'width': '60%'}
    ),
    html.Br(),
    html.Label('Choose Page Range:'),
    dcc.RangeSlider(
        id='page-range-slider',
        min=0,
        max=round(books['num_pages'].max() + 49, -2),
        step=50,
        marks={i: str(i) for i in range(0, int(round(books['num_pages'].max() + 49, -2)), 100)},
        value=[0, round(books['num_pages'].max() + 49, -2)],
        allowCross=False
    ),
    html.Label("Choose recommendation type:"),
    dcc.RadioItems(
        id='rec-type',
        options=[
            {'label': 'Similar Books (Content-Based)', 'value': 'content'},
            {'label': 'Similar Users Liked (Collaborative)', 'value': 'collaborative'}
        ],
        value='content',
        labelStyle={'display': 'inline-block', 'margin-right': '20px'}
    ),

    html.Br(),
    html.Button("Get Recommendations", id='recommend-btn', n_clicks=0),

    html.H2("Recommendations:"),
    html.Div(id='recommendations', style={'display': 'flex', 'flex-wrap': 'wrap', 'gap': '50px', 'justify-content': 'center', 'padding': '20px'})
])

@app.callback(
    Output('recommendations', 'children'),
    Input('page-range-slider', 'value'),
    Input('recommend-btn', 'n_clicks'),
    State('book-selector', 'value'),
    State('rec-type', 'value')
)
def update_recommendations(page_range, n_clicks, selected_books, rec_type):
    if n_clicks == 0:
        return "Select books and click 'Get Recommendations'"

    if not selected_books or len(selected_books) == 0:
        return "Please select at least one book."

    if len(selected_books) > 5:
        return "Please select no more than 5 books."

    if rec_type == 'content':
        recs = content_based_recommender(selected_books, page_range)
    else:
        recs = collaborative_recommender(selected_books)

    cards = []
    for _, row in recs.iterrows():
        card = html.Div([
        html.Div([
            html.Div([
            # Front of card
            html.Div([
                html.Img(src=row['image_url'], style={'width': '120px', 'height': '180px', 'object-fit': 'cover'}),
                html.H4(row['original_title'], style={'margin': '5px 0 0 0', 'fontSize': '14px'}),
                html.P(f"by {row['author']}", style={'fontSize': '12px'}),
            ], className='card-front'),

            # Back of card
            html.Div([
                html.P(row['description'], style={'fontSize': '10px'}),
                html.P(f"Rating: {row['avg_rating']}"),
                html.P(f"Year: {row['original_publication_year']}"),
                html.P(f"Pages: {row['num_pages']}")
            ], className='card-back')

                    ], className='card-flip')
                ], className='card-container')
        ])
        cards.append(card)

    return cards

if __name__ == '__main__':
    app.run_server(debug=True)