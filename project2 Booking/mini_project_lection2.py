import pandas as pd

data = pd.read_csv("booking.csv", sep=";")
# Импортируйте библиотеку pandas как pd. Загрузите датасет bookings.csv с разделителем ;.
# Проверьте размер таблицы, типы переменных, а затем выведите первые 7 строк, чтобы посмотреть на данные.
print(data.shape)
print(data.dtypes)
print(data.head(7))
# Приведите названия колонок к нижнему регистру и замените пробелы на знак нижнего подчеркивания.
rename_columns = {}
for name in data.columns:
    rename_columns[name] = name.lower().replace(" ", "_")
data = data.rename(columns=rename_columns)
# Пользователи из каких стран совершили наибольшее число успешных бронирований? Укажите топ-5.
top_counries = data.query("is_canceled == 0").groupby("country", as_index=False).aggregate({"is_canceled": "count"}).sort_values("is_canceled", ascending=False)
print()
print(top_counries.head(5))
# На сколько ночей в среднем бронируют отели разных типов?
average_nights = data.groupby("hotel", as_index=False).aggregate({"stays_total_nights": "mean"}).round(0)
print()
print(average_nights)
# Иногда тип номера, полученного клиентом (assigned_room_type), отличается от изначально забронированного
# (reserved_room_type). Такое может произойти, например, по причине овербукинга.
# Сколько подобных наблюдений встретилось в датасете?
over_booking = data.query("assigned_room_type != reserved_room_type").shape[0]
print()
print(over_booking)
# Проанализируйте даты запланированного прибытия.
# – На какой месяц чаще всего успешно оформляли бронь в 2016? Изменился ли самый популярный месяц в 2017?
# - Сгруппируйте данные по годам и проверьте,
# на какой месяц бронирования отеля типа City Hotel отменялись чаще всего в каждый из периодов
top_month_2016 = data.query("arrival_date_year == 2016").query("is_canceled == 0").groupby("arrival_date_month", as_index=False).aggregate({"is_canceled": "count"})
index = top_month_2016.is_canceled.idxmax()
top_month_2017 = data.query("arrival_date_year == 2017").arrival_date_month.value_counts().idxmax()
if top_month_2016["arrival_date_month"][index] != top_month_2017:
    print()
    print("Самый популярный месяц изменился")
else:
    print()
    print("Самый популярный месяц не изменился")
most_common_canceled = (data.query("hotel == 'City Hotel' and is_canceled == 1")
                        .groupby("arrival_date_year").arrival_date_month.value_counts()
                        )
print(most_common_canceled)
print()
# Посмотрите на числовые характеристики трёх переменных: adults, children и babies.
# Какая из них имеет наибольшее среднее значение?
print(max(data.adults.mean(), data.children.mean(), data.babies.mean()))
max_mean = max(data.adults.mean(), data.children.mean(), data.babies.mean())
if max_mean == data.adults.mean():
    print("adults")
elif max_mean == data.children.mean():
    print("children")
elif max_mean == data.babies.mean():
    print("babies")
print()
# Создайте колонку total_kids, объединив children и babies.
# Отели какого типа в среднем пользуются большей популярностью у клиентов с детьми?
data["total_kids"] = data["children"] + data["babies"]
most_popular_for_children = data.groupby("hotel").aggregate({"total_kids": "mean"}).round(2)
print(most_popular_for_children)
print()
# Создайте переменную has_kids, которая принимает значение True,
# если клиент при бронировании указал хотя бы одного ребенка (total_kids), в противном случае – False.
# Посчитайте отношение количества ушедших пользователей к общему количеству клиентов,
# выраженное в процентах (churn rate). Укажите, среди какой группы показатель выше.
data["has_kids"] = (data["total_kids"] > 0)
res1 = round(data.query("is_canceled == 1 and has_kids == False").shape[0] / data.query("has_kids == False").shape[0] * 100, 2)
res2 = round(data.query("is_canceled == 1 and has_kids == True").shape[0] / data.query("has_kids == True").shape[0] * 100, 2)
print(f"{res1} - for group without kids; {res2} - for group with kids")



