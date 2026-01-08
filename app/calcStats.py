import pandas as pd
import numpy as np

class CalcTradeStats:
    def __init__(self, inputFile, outputFile):
        self.inputFile = inputFile
        self.outputFile = outputFile
        self.trade_data = None

    def enrich (self):
        try:
            # Can use 'chunksize' for loading large data.
            df = pd.read_csv(self.inputFile, header=0, encoding='utf-8')
            df['Symbol'] = df['Symbol'].astype('category')
            df['FillExchange'] = df['FillExchange'].astype('category')
            df['Side'] = df['Side'].astype('category')
            df['EventType'] = df['EventType'].astype('category')

            df = df[df['EventType'] == 'TRADE'].copy()

            df['SymbolNotional'] = df['FillSize'] * df['FillPrice']

            b_size = np.where(df['Side'] == 'b', df['FillSize'], 0)
            s_size = np.where(df['Side'].isin(['s', 't']), df['FillSize'], 0)

            # tmp fields
            df['bs'] = b_size
            df['ss'] = s_size
            # To-Improve: use direct col assignment instead of assign() based on deep copy.
            df['SymbolBought'] = df.groupby('Symbol', observed=True)['bs'].cumsum()
            df['SymbolSold'] = df.groupby('Symbol', observed=True)['ss'].cumsum()

            df['SymbolPosition'] = df['SymbolBought'] - df['SymbolSold']

            df['ExchangeBought'] = df.groupby('FillExchange', observed=True)['bs'].cumsum()
            df['ExchangeSold'] = df.groupby('FillExchange', observed=True)['ss'].cumsum()

            df['TotalBought'] = np.cumsum(b_size)
            df['TotalSold'] = np.cumsum(s_size)

            b_notional = np.where(df['Side'] == 'b', df['SymbolNotional'], 0)
            s_notional = np.where(df['Side'].isin(['s', 't']), df['SymbolNotional'], 0)

            df['TotalBoughtNotional'] = np.cumsum(b_notional)
            df['TotalSoldNotional'] = np.cumsum(s_notional)

            # delete needless columns
            del df['bs']
            del df['ss']

            self.trade_data = df
            return self.trade_data
        except ValueError:
            print('Input file path not valid')
            return None

    def output_to_file(self):
        self.trade_data.to_csv(self.outputFile, index=False, header=True, mode='w+', sep=',', encoding='utf-8')

    def sum_stats(self):
        if self.trade_data is None:
            raise Exception('Data not available')
        df = self.trade_data
        print(f"Processed Trades: {len(df)}")
        sum_dict = {}

        shares_bought = int(df[df['Side'] == 'b']['FillSize'].sum())
        print(f"Shares Bought: {shares_bought:,}")
        sum_dict['Shares Bought'] = shares_bought

        shares_sold = int(df[df['Side'].isin(['s', 't'])]['FillSize'].sum())
        print(f"Shares Sold: {shares_sold:,}")
        sum_dict['Shares Sold'] = shares_sold
        notional_bought = df[df['Side'] == 'b']['SymbolNotional'].sum()
        print(f"Notional Bought: {notional_bought:,.2f}")
        sum_dict['Notional Bought'] = notional_bought

        notional_sold = df[df['Side'].isin(['s', 't'])]['SymbolNotional'].sum()
        print(f"Notional Sold: {notional_sold:,.2f}")
        sum_dict['Notional Sold'] = notional_sold

        exchanges = sorted(df['FillExchange'].unique())
        sum_dict['Exchanges'] = exchanges
        print("Per Exchange Volumes:")
        for exchange in exchanges:
            bought = int(df[(df['FillExchange'] == exchange) & (df['Side'] == 'b')]['FillSize'].sum())
            sold = int(df[(df['FillExchange'] == exchange) & (df['Side'].isin(['s', 't']))]['FillSize'].sum())
            print(f"{exchange} Bought: {bought:,}")
            print(f"{exchange} Sold: {sold:,}")

        avg_fill = df['FillSize'].mean()
        print(f"Average fill size: {avg_fill:,.2f}")
        sum_dict['Average fill size'] = avg_fill

        median_fill = int(df['FillSize'].median())
        print(f"Median fill size: {median_fill:,}")
        sum_dict['Median fill size'] = int(median_fill)

        print("Top 10 most active Symbols:")
        stock_volumes = df.groupby('Symbol', observed=True)['FillSize'].sum()
        top_10 = stock_volumes.sort_values(ascending=False).head(10)
        top_10_list = []
        for symbol, volume in top_10.items():
            print(f"{symbol}({int(volume):,})")
            top_10_list.append(f"{symbol}({int(volume):,})")
        sum_dict['Top 10 most active Symbols'] = top_10_list
        return sum_dict

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='Calculate Trade Statistics')
    parser.add_argument('--inputFile', required=True, help='input trades file path')
    parser.add_argument('--outputFile', required=True, help='output enriched file path')
    
    args = parser.parse_args()
    
    calc_instance = CalcTradeStats(args.inputFile, args.outputFile)
    enriched_df = calc_instance.enrich()
    if enriched_df is not None:
        calc_instance.output_to_file()
        calc_instance.sum_stats()