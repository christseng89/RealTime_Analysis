import pickle
import yfinance as yf

tsla = yf.Ticker("TSLA")
print(tsla.recommendations.columns)

print("\nstrongBuy [0]: ", tsla.recommendations["strongBuy"].value_counts().keys()[0])
print("strongBuy [1]: ", tsla.recommendations["strongBuy"].value_counts().keys()[1])

print("\nstrongSell [0]: ", tsla.recommendations["strongSell"].value_counts().keys()[0])
print("strongSell [1]: ", tsla.recommendations["strongSell"].value_counts().keys()[1])

print("\nbuy [0]: ", tsla.recommendations["buy"].value_counts().keys()[0])
print("buy [1]: ", tsla.recommendations["buy"].value_counts().keys()[1])

print("\nsell [0]: ", tsla.recommendations["sell"].value_counts().keys()[0])
print("sell [1]: ", tsla.recommendations["sell"].value_counts().keys()[1])

with open('/tmp/script.out', 'wb+') as tmp_file:
    pickle.dump({'test': 'ok'}, tmp_file)