# Real-Time Algorithmic Trading System with Apache Flink, Redpanda, and News Sentiment Analysis

![project overview](https://miro.medium.com/v2/resize:fit:1100/format:webp/1*T01Pa7kYvHVaOICX0FbOdA.jpeg)

![real time trading](https://miro.medium.com/v2/resize:fit:1100/format:webp/1*6liCLeTDEQYNhwLBt4BKJg.gif)

A real-time algorithmic trading system that uses Apache Flink, Redpanda, and news sentiment analysis to process market data and execute trades via the Alpaca API. The system streams news and stock prices, analyzes sentiment, and generates trading signals automatically.

## Technologies Used
- Apache Flink
- Redpanda
- Alpaca API
- NLTK for sentiment analysis
- Docker
- Python

## Setup and Installation
1. Clone the repo.
2. Install dependencies in a virtual environment.
3. Set up API keys for Alpaca.
4. Launch Docker containers.
5. Run producer scripts for data ingestion.
6. Process streams with Flink SQL.
7. Start the signal handler for trade execution.

See the full article for details: [https://medium.com/@jushijun/building-a-real-time-algorithmic-trading-system-with-apache-flink-redpanda-and-news-sentiment-e884081e3251](https://medium.com/@jushijun/building-a-real-time-algorithmic-trading-system-with-apache-flink-redpanda-and-news-sentiment-e884081e3251).

## References

- Algorithmic Trading with Apache Flink | Hands-on guide https://www.udemy.com/course/algorithmic-trading-with-apache-flink-hands-on-guide/?srsltid=AfmBOorod4_tdlbVGjF4Ri3C9Af_txCY7omRPxxU-VdSSht6-u3ZcFIp

- CodeWithYu https://www.youtube.com/watch?v=7r_oO_uLbSM&t=1672s&ab_channel=CodeWithYu