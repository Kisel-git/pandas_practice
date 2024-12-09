import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os


# Соберите все данные из папки data в один датафрэйм, имеющий следующие столбцы:
# колонки из самих файлов (product_id, quantity), а также имя пользователя (name),
# и дата этих покупок (date, соответствует названию папки, где лежит папка с пользователем)
data = pd.DataFrame()
print(list(os.walk("data")))
for elem in list(os.walk("data")):
    if len(elem[-1]) != 0 and elem[-1] != ['.DS_Store']:
        path_to_csv = (str(elem[-1])).strip("'[]'")
        path = f"{elem[0]}/{path_to_csv}"
        temp_df = pd.read_csv(path, encoding="UTF8", encoding_errors="replace")
        elements_of_path = path.split("/")
        temp_df["name_of_user"] = elements_of_path[-2]
        temp_df["date_of_deal"] = elements_of_path[-3]
        data = pd.concat((data, temp_df))
data = data.drop(columns="Unnamed: 0")
print(data)
# Выясните, какой пользователь купил больше всего товаров.
# Если их несколько, то перечислите имена через запятую с пробелом и в алфавитном порядке.
most_payer_user = data.groupby("name_of_user", as_index=False).agg({"quantity": "sum"}).rename(columns={"quantity": "amount_of_products"})
maximum = most_payer_user.amount_of_products.max()
print("names_of_top_users")
print(most_payer_user.name_of_user[most_payer_user.amount_of_products == maximum].tolist())
# Найдите топ-10 товаров по числу проданных единиц за всё время и постройте барплот.
# Сколько было продано единиц товара с product_id==56?
top_products = (data.groupby("product_id", as_index=False).agg({"quantity": "sum"}).
                rename(columns={"quantity": "amount_of_sales"}).sort_values("amount_of_sales", ascending=False))
print("id_of_top_products")
print(top_products.product_id.head(10).tolist())
# Визуализируйте продажи по дням.
days_sailing = sns.countplot(data, x="date_of_deal", color="violet")
plt.show()
# Сколько пользователей приобрели какой-либо товар повторно (более 1 раза)?
# Повтором будем считать покупку товара с одинаковым product_id, совершенную в разные дни.
print("Количество пользователей, которые приобрели товар повторно")
print(data.groupby(["product_id", "name_of_user"]).agg({"date_of_deal": pd.Series.nunique}).query("date_of_deal > 1")
      .shape[0])

