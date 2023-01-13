import requests  # type: ignore
from bs4 import BeautifulSoup


def extract_news(parser):
    """ Extract news from a given web page """
    news_list = []

    tbl_list = parser.table.findAll("table")
    news_table = tbl_list[1]
    for row in news_table.findAll("tr")[:-2]:
        if row.attrs:
            if row["class"] == ["athing"]:
                news_list.append({})
                title_link = row.find("span", class_="titleline").a
                news_list[-1]["title"] = title_link.text
                news_list[-1]["url"] = title_link["href"]
        else:
            news_list[-1]["score"] = int(row.find("span", class_="score").text.split()[0])
            news_list[-1]["author"] = row.find("a", class_="hnuser").text

            last_link_in_row = row.find("span", class_="subline").findAll("a")[-1]
            if "comment" in last_link_in_row.text:
                news_list[-1]["comments"] = int(last_link_in_row.text.split()[0])
            else:
                news_list[-1]["comments"] = 0
    return news_list


def extract_next_page(parser):
    """ Extract next page URL """
    more_link = parser.find("a", class_="morelink")
    return more_link["href"]


def get_news(url, n_pages=1):
    """ Collect news from a given web page """
    news = []
    while n_pages:
        print("Collecting data from page: {}".format(url))
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        news_list = extract_news(soup)
        next_page = extract_next_page(soup)
        url = "https://news.ycombinator.com/" + str(next_page)
        news.extend(news_list)
        n_pages -= 1
    return news
