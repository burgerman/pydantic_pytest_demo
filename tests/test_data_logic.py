import pandas as pd
import pytest
from app.data_services import TradeService
from app.schemas import TransactionData
from utils.utils import get_statistics_df

@pytest.fixture(scope="class", autouse=True)
def service():
    return TradeService()

class TestDataLogic:
    def test_ingest_trade_data(self, service):
        trade_data = [
            TransactionData(transaction_id='tx01', type='type1', counterparty='TD', amount=1000.5, tags=['food', 'utilities'], transaction_timestamp='2025-12-22 13:30:15'),
            TransactionData(transaction_id='tx02', type='type2', counterparty='RBC', amount=800.0, tags=['utilities'], transaction_timestamp='2025-12-22 15:10:45'),
            TransactionData(transaction_id='tx03', type='type1', counterparty='CIBC', amount=100.8, tags=['food'], transaction_timestamp='2025-12-23 00:10:00'),
            TransactionData(transaction_id='tx04', type='type1', counterparty='blue_origin', amount=4500.00, tags=['aerospace', 'research'], transaction_timestamp='2025-12-23 01:15:00'),
            TransactionData(transaction_id='tx05', type='type2', counterparty='uber', amount=42.50, tags=['transport', 'travel'], transaction_timestamp='2025-12-23 03:45:12'),
            TransactionData(transaction_id='tx06', type='type1', counterparty='Scotiabank', amount=1200.00, tags=['food', 'reoccurring'], transaction_timestamp='2025-12-23 06:00:00'),
            TransactionData(transaction_id='tx07', type='type3', counterparty='starbucks', amount=5.75,tags=['food', 'beverage'], transaction_timestamp='2025-12-23 08:20:45'),
            TransactionData(transaction_id='tx08', type='type2', counterparty='google_cloud', amount=299.99,tags=['infrastructure'], transaction_timestamp='2025-12-23 09:10:00'),
            TransactionData(transaction_id='tx09', type='type1', counterparty='apple', amount=1299.00,tags=['hardware', 'asset'], transaction_timestamp='2025-12-23 10:30:00'),
            TransactionData(transaction_id='tx10', type='type2', counterparty='slack', amount=15.00,tags=['software', 'subscription'], transaction_timestamp='2025-12-23 12:00:00'),
            TransactionData(transaction_id='tx11', type='type1', counterparty='BMO', amount=85.20, tags=['food'],transaction_timestamp='2025-12-23 14:15:22'),
            TransactionData(transaction_id='tx12', type='type3', counterparty='chevron', amount=65.00,tags=['fuel', 'logistics'], transaction_timestamp='2025-12-23 15:45:00'),
            TransactionData(transaction_id='tx13', type='type2', counterparty='github', amount=7.00, tags=['dev_tools'],transaction_timestamp='2025-12-23 17:05:10'),
            TransactionData(transaction_id='tx14', type='type1', counterparty='amazon', amount=245.50,tags=['supplies', 'office'], transaction_timestamp='2025-12-23 19:30:00'),
            TransactionData(transaction_id='tx15', type='type1', counterparty='gts', amount=310.00,tags=['food', 'audit_pending'], transaction_timestamp='2025-12-23 21:10:00'),
            TransactionData(transaction_id='tx16', type='type2', counterparty='netflix', amount=19.99,tags=['entertainment'], transaction_timestamp='2025-12-23 23:55:00'),
            TransactionData(transaction_id='tx17', type='type1', counterparty='verizon', amount=110.00,tags=['utilities', 'telecom'], transaction_timestamp='2025-12-24 02:20:00'),
            TransactionData(transaction_id='tx18', type='type3', counterparty='whole_foods', amount=156.75,tags=['groceries'], transaction_timestamp='2025-12-24 05:40:15'),
            TransactionData(transaction_id='tx19', type='type1', counterparty='RBC', amount=500.00, tags=['food', 'bonus'],transaction_timestamp='2025-12-24 07:15:00'),
            TransactionData(transaction_id='tx20', type='type2', counterparty='adobe', amount=52.99,tags=['creative', 'subscription'], transaction_timestamp='2025-12-24 09:00:00'),
            TransactionData(transaction_id='tx21', type='type1', counterparty='microsoft', amount=450.00,tags=['license', 'software'], transaction_timestamp='2025-12-24 10:45:30'),
            TransactionData(transaction_id='tx22', type='type2', counterparty='zoom', amount=14.99, tags=['comms'],transaction_timestamp='2025-12-24 12:30:00'),
            TransactionData(transaction_id='tx23', type='type3', counterparty='fedex', amount=32.10, tags=['shipping'],transaction_timestamp='2025-12-24 14:05:00')
        ]
        current_size = service.get_size()
        assert current_size == 0
        result = service.ingest(trade_data)
        assert result == 23

    def test_get_dataframe(self, service):
        df = service.get_dataframe()
        assert df is not None
        assert df.shape[0] == 23
        assert df.shape[1] == 6

    def test_get_statistics_df(self, service):
        df = service.get_dataframe()
        df['timestamp'] = pd.to_datetime(df['transaction_timestamp'])
        df['timestamp'] = df['timestamp'].dt.to_period('d')
        assert df.shape[1] == 7
        # timestamp as index
        stats = get_statistics_df(df, ['timestamp'], 'amount', ['sum', 'max', 'min', 'mean', 'median'])
        assert stats is not None
        stats.sort_index(ascending=True, inplace=True)
        assert min(stats['sum'].values) == stats['sum'].min()
        assert max(stats['sum'].values) == stats['sum'].max()
        # period object -> time date string
        assert str(stats['sum'].idxmin()) == '2025-12-24'
        assert str(stats['sum'].idxmax()) == '2025-12-23'

    def test_update(self, service):
        df = service.get_dataframe()
        new_df = df[:20]
        assert new_df.shape[0] == 20
        assert new_df.shape[1] == 6
        selected_data_dict = new_df.to_dict(orient='records')
        updated_trade_data = [TransactionData.model_validate(record) for record in selected_data_dict]
        updated_size = service.update([TransactionData.model_validate(record) for record in updated_trade_data])
        assert updated_size == 20