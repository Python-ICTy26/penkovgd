from bottle import (
    route, run, template, request, redirect
)

from scraputils import get_news
from db import News, session
from bayes import NaiveBayesClassifier


@route("/news")
def news_list():
    s = session()
    rows = s.query(News).filter(News.label == None).all()
    return template('news_template', rows=rows)


@route("/add_label/")
def add_label():
    s = session()
    label = request.query["label"]
    news_id = request.query["id"]
    news_to_edit = s.query(News).filter(News.id == news_id).one()
    news_to_edit.label = label
    s.commit()
    redirect("/news")


@route("/update")
def update_news():
    news = get_news("https://news.ycombinator.com/newest")
    s = session()
    for new in news:
        if len(s.query(News).filter(News.author == new["author"], News.title == new["title"]).all()) == 0:
            s.add(News(
                title=new["title"],
                author=new["author"],
                url=new["url"],
                comments=new["comments"],
                points=new["score"],
            ))
    s.commit()
    redirect("/news")


@route("/classify")
def classify_news():
    s = session()
    labeled_news = s.query(News).filter(News.label != None).all()
    labeled_news = [(n.title, n.label) for n in labeled_news]
    X_train = [n[0] for n in labeled_news]
    y_train = [n[1] for n in labeled_news]
    model = NaiveBayesClassifier()
    model.fit(X_train, y_train)
    unlabeled_news = s.query(News).filter(News.label == None).all()
    predictions = model.predict([n.title for n in unlabeled_news])
    rows = []
    for title, label in predictions.items():
        if label == "good":
            rows.append(s.query(News).filter(News.title == title).first())
    for title, label in predictions.items():
        if label == "maybe":
            rows.append(s.query(News).filter(News.title == title).first())
    for title, label in predictions.items():
        if label == "never":
            rows.append(s.query(News).filter(News.title == title).first())
    return template('news_template', rows=rows)


if __name__ == "__main__":
    run(host="localhost", port=8080)
