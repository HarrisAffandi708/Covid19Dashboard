from covid_data_handler import parse_csv_data, process_covid_csv_data
from covid_news_handling import articles, news_API_request

def test_parse_csv_data():
    data= parse_csv_data('nation_2021-10-28.csv')
    assert len(data) == 639

def test_process_csv_data():
    last7days_cases , current_hospital_cases , total_deaths = process_covid_csv_data(parse_csv_data('nation_2021-10-28.csv'))
    assert last7days_cases == 240299
    assert current_hospital_cases == 7019
    assert total_deaths == 141544

def test_articles():
    news_api = news_API_request()
    news = articles(news_api)
    assert news
    assert len(news) == 10

