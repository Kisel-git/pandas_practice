import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

data = pd.read_csv("transaction_data.csv")
print(data.head())
print(data.shape)
print(data.dtypes)
print(data.isnull().sum())
print(data.info())
# Какие значения находятся в колонке transaction? Сколько наблюдений относятся к тому или иному уровню?
# Визуализируйте результат с помощью барплота. Подумайте, как можно улучшить график.
print(data.transaction.value_counts())
fig, ax = plt.subplots(nrows=4, ncols=1)
sns.countplot(data, x="transaction", ax=ax[0])
# Сколько транзакций завершились ошибкой?
error_transaction = data.transaction.value_counts().reset_index()
print("Число транзакций, которые закончились ошибкой", end=": ")
print(error_transaction.query("transaction == 'error'")['count'].iloc[0])
# Сколько успешных транзакций осуществил каждый из пользователей?
# Постройте гистограмму распределения числа успешных транзакций.
success = data.query("transaction == 'successfull'").groupby("name", as_index=False).agg({"transaction": "count"})
sns.distplot(success.transaction, kde=False, ax=ax[1])
# Коллега прислал Вам обновленные данные. (transaction_data_updated.csv)
# Постройте сводную таблицу user_vs_minute_pivot, где в качестве столбцов будут использованы имена пользователей,
# строк – минуты, значений – число совершенных операций в указанную минуту. Пропущенные значения заполните нулями.
update_data = pd.read_csv("transaction_data_updated.csv")
print(update_data.head())
piv = (update_data.pivot_table(index="minute", columns="name", values="transaction", aggfunc="count", fill_value=0).
       reset_index())
print(piv)
sns.barplot(piv, x="minute", y=piv.sum(axis=1), ax=ax[2])
# Изучите представленный график. Помогите коллеге разобраться,  есть ли в данных ошибка, или же всё хорошо.
# Если в данные закралась ошибка, исправьте её и сохраните правильное число минут, прошедших с начала дня,
# в колонку true_minute.
update_data.date = pd.to_datetime(update_data.date)
update_data['true_minute'] = update_data.date.dt.minute + update_data.date.dt.hour * 60
sns.barplot(x=update_data.true_minute, y=update_data.groupby("true_minute", as_index=False).
            agg({"transaction": "count"}).transaction, ax=ax[3])
plt.show()
