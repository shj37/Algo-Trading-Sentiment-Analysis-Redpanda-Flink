import json
from typing import List
from datetime import datetime, date
from alpaca_trade_api import REST
from alpaca_trade_api.common import URL
from alpaca.common import Sort
from kafka import KafkaProducer
from nltk.sentiment.vader import SentimentIntensityAnalyzer as SIA
import pprint

from alpaca_config.keys import config

sia = SIA()
def get_sentiment(text):
    scores = sia.polarity_scores(text)
    return scores['compound']

def get_producer(brokers: List[str]):
    producer = KafkaProducer(
        bootstrap_servers=brokers,
        key_serializer=str.encode,
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )
    return producer


def produce_historical_news(
        redpanda_client: KafkaProducer,
        start_date: str,
        end_date: str,
        symbols: List[List[str]],
        topic: str
    ):
    key_id = config['key_id']
    secret_key = config['secret_key']
    base_url = config['news_base_url']

    api = REST(key_id=key_id, secret_key=secret_key, base_url=URL(base_url))

    for symbol in symbols:
        news = api.get_news(
            symbol=symbol[0],
            start=start_date,
            end=end_date,
            limit=6000,
            sort=Sort.ASC,
            include_content=False,
        )

        #print(news)

        j = 0

        for i, row in enumerate(news):
            article = row._raw
            # filter out news whose headline does not contain the symbol or company name
            should_proceed = any(term.lower() in article['headline'].lower() for term in symbol)
            if not should_proceed:
                continue

            timestamp_ms = int(row.created_at.timestamp() * 1000)
            timestamp = datetime.fromtimestamp(row.created_at.timestamp())

            article['timestamp'] = timestamp.strftime('%Y-%m-%d %H:%M:%S')
            article['timestamp_ms'] = timestamp_ms
            article['data_provider'] = 'alpaca'
            article['sentiment'] = get_sentiment(article['headline'] + (" " + article['summary'].strip() if len(article['summary'].strip())> 0 else ""))
            article.pop('symbols')
            article['symbol'] = symbol[0]

            # pprint.pprint(article)
            # print("*************")

            try:
                future = redpanda_client.send(
                    topic=topic,
                    key=symbol[0],
                    value=article,
                    timestamp_ms=timestamp_ms
                )

                j+=1

                _ = future.get(timeout=10)
                print(f'Sent {j} articles to {topic}')
            except Exception as e:
                print(f'Failed to send article: {article}')
                print(e)


if __name__ == '__main__':
    redpanda_client = get_producer(config['redpanda_brokers'])
    produce_historical_news(
        redpanda_client,
        topic='market-news',
        start_date='2025-03-01',
        end_date=date.today().strftime('%Y-%m-%d'),
        symbols=[['NVDA', 'NVIDIA']] # the first item must be a stock symbol
    )

    redpanda_client.close()