import pytest
from app.calcStats import CalcTradeStats
import os
from pathlib import Path

@pytest.fixture(scope="class", autouse=True)
def calc_stats_service():
    path = Path(__file__).resolve().parent.parent
    return CalcTradeStats(inputFile=os.path.join(path,'data','trades.csv'),
                          outputFile=os.path.join(path,'data','enrichedTrades.csv'))

class TestCalcStats:
    def test_enrich(self, calc_stats_service):
        calc_stats_service.enrich()
        test_df = calc_stats_service.trade_data
        
        assert test_df is not None
        assert test_df.shape[0] == 796
        assert test_df.shape[1] == 17

        assert 'SymbolBought' in test_df.columns
        assert 'SymbolSold' in test_df.columns
        assert 'SymbolPosition' in test_df.columns
        assert 'SymbolNotional' in test_df.columns
        assert 'ExchangeBought' in test_df.columns
        assert 'ExchangeSold' in test_df.columns
        assert 'TotalBought' in test_df.columns
        assert 'TotalSold' in test_df.columns
        assert 'TotalBoughtNotional' in test_df.columns
        assert 'TotalSoldNotional' in test_df.columns

    def test_output(self, calc_stats_service):
        if calc_stats_service.trade_data is None:
            calc_stats_service.enrich()
            
        calc_stats_service.output_to_file()
        assert os.path.exists(calc_stats_service.outputFile)

        if os.path.exists(calc_stats_service.outputFile):
            os.remove(calc_stats_service.outputFile)

    def test_sum_stats(self, calc_stats_service, capsys):
        if calc_stats_service.trade_data is None:
            calc_stats_service.enrich()
            
        stats = calc_stats_service.sum_stats()
        assert stats is not None
        captured = capsys.readouterr()
        assert "Shares Bought:" in captured.out
        assert "Shares Sold:" in captured.out
        assert "Notional Bought:" in captured.out
        assert "Notional Sold:" in captured.out
        assert "Per Exchange Volumes:" in captured.out
        assert "Average fill size:" in captured.out
        assert "Median fill size:" in captured.out
        assert "Top 10 most active Symbols:" in captured.out