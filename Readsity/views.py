from django.shortcuts import render
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn import neighbors
import wikipedia


df = pd.read_csv('./books.csv', error_bad_lines=False)

def home(request):
    return render(request, "index.html")

def blog(request):
    return render(request, "search_result.html")

def search_page(request):
    return render(request, "search.html")

df.columns = df.columns.str.strip()
def num_into_obj(x):
    if 0 <= x <= 1:
        return 'between 0 and 1'
    elif 1 <= x <= 2:
        return 'between 1 and 2'
    elif 2 <= x <= 3:
        return 'between 2 and 3'
    elif 3 <= x <= 4:
        return 'between 3 and 4'
    else:
        return 'between 4 and 5'

df['rating_obj'] = df['average_rating'].apply(num_into_obj)

rating_df = pd.get_dummies(df['rating_obj'])
language_df = pd.get_dummies(df['language_code'])

features = pd.concat([rating_df, language_df, df['average_rating'], df['ratings_count'], df['title']], axis=1)
features.set_index('title', inplace=True)

min_max_scaler = MinMaxScaler()
features_scaled = min_max_scaler.fit_transform(features)

model = neighbors.NearestNeighbors(n_neighbors=6, algorithm='brute', metric='cosine')
model.fit(features_scaled)

dist, idlist = model.kneighbors(features_scaled)

def result(request):
    df = pd.read_csv('./books.csv', error_bad_lines=False)
    df.columns = df.columns.str.strip()
    query = request.GET.get("q")
    res = {}
    if df[df['title'] == query]:
        res = {'Name': df['title']}
    return render(request, "search.html", res)


def BookRecommender(request):
    global context
    try:
        book_name = request.GET.get("q")
        suggested_book = request.GET.get("r_book")

        if suggested_book is not None:
            book_name = suggested_book

        about_book = wikipedia.summary(str(book_name)+' book')

        if book_name is None:
            book_name = list(df['title'].value_counts().index)
        book_list_name = []
        book_id = df[df['title'] == book_name].index
        book_id = book_id[0]
        for newid in idlist[book_id]:
            book_list_name.append(df.loc[newid])

        context = {'books': book_list_name, 's_book': book_name, 'about_book': about_book}
        return render(request, "blog.html", context)
    except:
        msg = {'msg': 'Book Not found !'}
        return render(request, 'search.html', msg)


