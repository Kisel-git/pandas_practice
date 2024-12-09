import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# Импортируйте данные data.csv.zip (в папке) с кодировкой ISO-8859-1.
# Запишите полученный датафрейм в retail, а названия колонок сохраните в переменную retail_columns.
retail = pd.read_csv("data.csv.zip", encoding="ISO-8859-1", compression="zip")
retail_columns = retail.columns.tolist()
print(retail_columns)
# Проверьте, встречаются ли в данных повторяющиеся наблюдения, и в качестве ответа укажите их количество.
# Если они есть, то удалите их из retail.
duplicates = retail.duplicated()
print(f"В данных {duplicates.sum()} повторов")
retail = retail.drop_duplicates()
print(f"В данных {retail.duplicated().sum()} повторов")
print("Повторы успешно удалены")
# Данные содержат в себе записи как и об успешных транзакциях, так и об отмененных.
# Если пользователь отменил заказ, в начале номера транзакции (InvoiceNo) ставится C (canceled).
# Сколько всего заказов отменили пользователи?
d = {}
for elem in retail_columns:
    d[elem] = elem.lower().replace(" ", "_")
retail = retail.rename(columns=d)
c = retail.invoiceno.apply(lambda st: True if st[0] == "C" else False)
print(f"Количество отмененных заказов {c.sum()}")
# Теперь отфильтруйте данные и оставьте в retail только те заказы, где Quantity > 0.
# В качестве ответа укажите число оставшихся строк.
print("Количество отфильтрованных записей", end=" - ")
print(retail.query("quantity > 0").shape[0])
# Посчитайте число заказов для каждого пользователя (CustomerID) из Германии (Germany).
# Оставьте только тех, кто совершил более N транзакций (InvoiceNo), где N – 80% процентиль.
# Запишите полученные id пользователей в germany_top (не весь датафрейм, только id).
# Идентификатор заказа – InvoiceNo. Для каждого заказа в данных может встречаться более 1 строки.
count_of_transaction = (retail.query("country == 'Germany'").groupby("customerid", as_index=False).
                        agg({"invoiceno": pd.Series.nunique}).
                        rename(columns={"invoiceno": "count_of_transaction"}))
print(count_of_transaction)
q = count_of_transaction.count_of_transaction.quantile(q=0.8)
germany_top = count_of_transaction.query("count_of_transaction > @q").customerid
print(germany_top)
# Используя объект с id пользователей (germany_top), полученный на предыдущем шаге, отфильтруйте наблюдения
# и оставьте в данных записи только по интересующим нас юзерам. Результирующий датафрейм запишите в top_retail_germany.
top_retail_germany = retail.query("customerid in @germany_top")
print(top_retail_germany)
# Сгруппируйте top_retail_germany по коду товара (StockCode).
# Какой из продуктов добавляли в корзину чаще всего, кроме POST?
# Note: одним заказом считается единовременная покупка любого количества товара, т.е. без учета Quantity.
print("stock товара, который чаще всего добавляют в корзину", end=" - ")
print(top_retail_germany.groupby("stockcode", as_index=False).agg({"invoiceno": pd.Series.nunique}).
      rename(columns={"invoiceno": "count_of_unique_transaction"}).
      sort_values("count_of_unique_transaction", ascending=False).stockcode.tolist()[1])
# Вернемся к анализу полного датасета retail.
# Создайте колонку Revenue с суммой покупки, используя колонки Quantity и UnitPrice
retail["revenue"] = retail.quantity * retail.unitprice
print(retail.head())
# Для каждой транзакции (InvoiceNo), посчитайте финальную сумму заказа. В качестве ответа укажите топ-5 (InvoiceNo)
# по сумме заказа (через запятую с пробелом и в порядке убывания TotalRevenue)
sum_of_transaction = (retail.groupby("invoiceno", as_index=False).agg({"revenue": "sum"}).rename(columns={"revenue": "total_revenue"}).
                      sort_values("total_revenue", ascending=False).invoiceno.head().tolist())
print(*sum_of_transaction, sep=", ")

