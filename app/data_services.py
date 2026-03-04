from collections import defaultdict, deque, Counter
from typing import Optional, Any
from .schemas import TransactionData
import heapq
from functools import lru_cache
import itertools as it
from collections import Counter
import pandas as pd
import numpy as np
from datetime import datetime

class TradeService:
    def __init__(self):
        self.data_memo = []
        self.in_memory_dict = {}
        self.created_time = datetime.now()
        self.updated_time = datetime.now()

    def ingest(self, trade_data:list[TransactionData]) -> int:
        self.data_memo += trade_data
        for t in trade_data:
            print(t)
            self.in_memory_dict[t.id] = t
        self.updated_time = datetime.now()
        return self.get_size()

    def get_size(self) -> int:
        return len(self.data_memo)

    def get_dataframe(self) -> pd.DataFrame:
        instance_list = [trans.model_dump(by_alias=True) for trans in self.data_memo]
        return pd.DataFrame(instance_list)

    def query(self, transaction_id: str) -> Optional[TransactionData]:
        return self.in_memory_dict.get(transaction_id)

    def store(self):
        pass

    def update(self, updated_trade_data:list[TransactionData]) -> int:
        self.data_memo = updated_trade_data
        self.updated_time = datetime.now()
        return self.get_size()
