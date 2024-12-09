import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

data = pd.read_csv("avocado_full.csv")
print(data.head())
print(data.dtypes)
print(data.info())
aver_data = pd.read_csv("avocado_mean.csv")
print(aver_data)
window = aver_data["AveragePrice"].rolling(3).mean().round(2)
print("Максимальное значение средней цены авокадо")
print(window.max())
fig, ax = plt.subplots(nrows=3, ncols=2)
w1 = sns.lineplot(x=aver_data["Date"], y=aver_data["AveragePrice"].rolling(2).mean().round(2), ax=ax[0][0])
w2 = sns.lineplot(x=aver_data["Date"], y=aver_data["AveragePrice"].rolling(4).mean().round(2), ax=ax[1][0])
w3 = sns.lineplot(x=aver_data["Date"], y=aver_data["AveragePrice"].rolling(10).mean().round(2), ax=ax[0][1])
w4 = sns.lineplot(x=aver_data["Date"], y=aver_data["AveragePrice"].rolling(50).mean().round(2), ax=ax[1][1])
w1.set_title("Окно 2")
w2.set_title("Окно 4")
w3.set_title("Окно 10")
w4.set_title("Окно 50")
avocado_ewm = aver_data["AveragePrice"].ewm(span=2)
plt.show()