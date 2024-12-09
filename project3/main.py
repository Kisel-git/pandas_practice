import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Импортируйте библиотеку pandas как pd. Загрузите два датасета user_data и logs.
# Проверьте размер таблицы, типы переменных, наличие пропущенных значений, описательную статистику.
user_data = pd.read_csv("user.csv")
logs = pd.read_csv("logs.csv")
print(user_data.shape)
print(logs.shape)
print()
print(user_data.dtypes)
print(logs.dtypes)
print()
print(user_data.describe())
print(logs.describe())
print()
print(user_data.isnull().sum())
print()
print(logs.isnull().sum())
print()
# Какой клиент совершил больше всего успешных операций? (success == True)
most_loyalty = (logs.groupby("client", as_index=False).agg({"success": "sum"}).
                rename(columns={"success": "count_of_success_transaction"}).
                sort_values("count_of_success_transaction", ascending=False))
maximum = most_loyalty.count_of_success_transaction.max()
most_success = most_loyalty.query("count_of_success_transaction == @maximum").client
res1 = most_success.tolist()
res1 = sorted(res1)
print(" ".join(map(str, res1)))
print()
# С какой платформы осуществляется наибольшее количество успешных операций?
most_popular_platform = (logs.groupby("platform", as_index=False).agg({"success": "sum"}).
                         rename(columns={"success": "cout_of_success_transaction"}))
maximum = most_popular_platform.cout_of_success_transaction.max()
most_popular_platform = most_popular_platform.query("cout_of_success_transaction == @maximum").platform
res2 = most_popular_platform.tolist()
print(" ".join(map(str, res2)))
print()
# Какую платформу предпочитают премиумные клиенты?
data = user_data.merge(logs, on="client")
premium_clients = (data.query("premium == True").groupby("platform").agg({"client": "count"}).
                   rename(columns={"client": "number_of_premium_client"}).
                   sort_values("number_of_premium_client", ascending=False))
print(premium_clients.idxmax())
# Визуализируйте распределение возраста клиентов в зависимости от типа клиента (премиум или нет)
fig, ax = plt.subplots(nrows=5, ncols=1)
sns.distplot(data.query("premium == False").age, ax=ax[0], color="purple")
sns.distplot(data.query("premium == True").age, ax=ax[1], color="green")
sns.countplot(data, x="age", hue="premium", ax=ax[2])
# Постройте график распределения числа успешных операций
sns.distplot(data.groupby("client").agg({"success": "sum"}), ax=ax[3])
# Визуализируйте число успешных операций, сделанных на платформе computer, в зависимости от возраста,
# используя sns.countplot (x – возраст, y – число успешных операций).
# Клиенты какого возраста совершили наибольшее количество успешных действий?
sns.countplot(data.query("platform == 'computer' and success == 1"), x="age", ax=ax[4])
plt.show()


