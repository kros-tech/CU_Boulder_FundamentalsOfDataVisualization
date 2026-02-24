import pandas as pd
import webbrowser
from operator import countOf
import altair as alt
from altair import Parameter

# 1. import data to a dataframe
movies = pd.read_csv('IMDB_Movies_Dataset.csv')
pd.set_option('display.max_columns', 13)
pd.options.display.width = 0

# 2. change columns to all camel case as one step to clean up data
movies.columns = ['Label', 'Title', 'AverageRating', 'Director', 'Writer',
       'Metascore', 'Cast', 'ReleaseDate', 'CountryOfOrigin', 'Languages',
       'Budget', 'Worldwide Gross', 'Runtime']

# 3. create new dataset with only the data in which we are interested
movies_new = movies[['Title', 'AverageRating', 'Director', 'ReleaseDate']]

# 4. pre-filter the data to only get those movies that have an Avg Rating >= 8.5
top_rated_movies = movies_new[movies_new['AverageRating'] > 8.6]
#print(top_rated_movies.tail())
print(top_rated_movies)

# 5. Create a selection object for the dropdown, including an "ALL" option
director_selection = alt.param(
    name='director_selection',
    bind=alt.binding_select(
        options=['ALL'] + sorted(top_rated_movies['Director'].unique().tolist()),
        name='Select Director: '
    ),
    value='ALL'
)

# 6. create sort parameter for the Rating
sort_order = alt.param(
    name='sort_order',
    bind=alt.binding_select(
        options=['Ascending', 'Descending'],
        name='Sort by rating: '
    ),
    value='Descending'
)

# 7. Create common method to save and open the chart
# save and open chart method
def save_and_open_chart(chart_name):
    html_chart_name = f'{chart_name}.html'
    chart_name.save(html_chart_name)
    webbrowser.open(html_chart_name)

####################################################
# 1. Create an ordered list chart with grouping by Director
chart_filterByDirector = (
    alt.Chart(top_rated_movies)
    .mark_bar()
    .encode(
        x=alt.X('AverageRating:Q', title='Rating'),
        y=alt.Y(
            'Title:N',
            title='Movie Title',
            sort=alt.SortField(field='sort_value', order='ascending')
        ),
        color='Director:N',
        tooltip=['Title:N', 'AverageRating:Q', 'Director:N', 'ReleaseDate:O']
    )
    .add_params(director_selection, sort_order)
    .transform_calculate(
        # sort_order is directly available in the expression
        sort_value="sort_order == 'Ascending' ? datum.AverageRating : -datum.AverageRating"
    )
    .transform_filter(
        # director_selection is also directly available
        "director_selection == 'ALL' || datum.Director == director_selection"
    )
    .properties(title='Top Movies with Director Filter')
)

save_and_open_chart(chart_filterByDirector)

####################################################



