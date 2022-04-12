from datetime import datetime

from pytrends.request import TrendReq

from model import PhraseTrends
from .base import BaseProcessor
from utils.datetime import query_format


class TrendsProcessor(BaseProcessor[PhraseTrends]):

    def __init__(self, url: str):
        self.url = url
        self.search_tool = TrendReq(hl='en-US', tz=360)

    def get(self, phrase: str, start_date: datetime, end_date: datetime) -> PhraseTrends:
        timeframe = f"{query_format(start_date)} {query_format(end_date)}"

        self.search_tool.build_payload(kw_list=[phrase], timeframe=timeframe)
        data = self.search_tool.interest_over_time()

        return PhraseTrends(data.to_numpy().flatten().tolist())

