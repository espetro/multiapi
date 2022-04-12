from datetime import datetime

from pytrends.request import TrendReq

from model import PhraseTrends, PhraseTrendDay
from .base import BaseProcessor
from utils.datetime import query_format


class TrendsProcessor(BaseProcessor[PhraseTrends]):

    def __init__(self):
        self.url = None
        self.search_tool = TrendReq(hl='en-US', tz=360)

    def get(self, phrase: str, start_date: datetime, end_date: datetime) -> PhraseTrends:
        timeframe = f"{query_format(start_date)} {query_format(end_date)}"

        self.search_tool.build_payload(kw_list=[phrase], timeframe=timeframe)
        data = self.search_tool.interest_over_time().iloc[:, :1]

        return PhraseTrends(
            [PhraseTrendDay(query_format(date), value)
             for (date, value) in zip(data.index.tolist(), data.values.tolist())]
        )

