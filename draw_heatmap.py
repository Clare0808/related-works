import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# 讀取 Excel 檔案，內容包含各地區的平均房價資料
df = pd.read_excel("month_average_house_price_data.xlsx")

# 定義要處理的縣市清單
city_list = ["台北市", "基隆市", "新北市", "宜蘭縣", "桃園市", "新竹縣", "新竹市", "台中市", "苗栗縣", "彰化縣", "南投縣", "雲林縣", "嘉義縣", "嘉義市", "台南市", "高雄市", "屏東縣", "台東縣", "花蓮縣", "澎湖縣", "金門縣", "連江縣"]

# 逐一處理每個縣市
for city in city_list :
    price_data = []  # 儲存該縣市各地區的平均房價
    location_data = []  # 儲存該縣市各地區的名稱（去掉縣市名稱）

    # 遍歷資料中的 位置 欄位
    for item in df["位置"] :
        if city in item :# 如果該位置屬於目前處理的縣市
            # 取出該位置的平均總價
            price_data.append(df[df["位置"] == item]["平均總價"].values[0])
            # 去除縣市名稱僅保留地區名
            location_data.append(item.replace(city, ""))

    # 將房價與地區名稱轉成 NumPy 陣列
    price_matrix = np.array(price_data)
    location_matrix = np.array(location_data, dtype=object)

    # 取得資料長度
    data_length = len(price_data)

    # 將資料排成接近正方形的矩陣
    row_size = int(np.sqrt(data_length))  # 行數取平方根
    column_size = data_length // row_size  # 列數用整除計算
    total_size = row_size * column_size  # 矩陣總容量

    # 若容量不足則增加行列數
    if total_size < data_length :
        row_size += 1
        column_size += 1

        total_size = row_size * column_size

    # 計算需要補齊的空格數
    less_data = total_size - data_length

    # 將房價矩陣補齊，缺失值填入 NaN
    price_matrix_padded = np.pad(price_matrix, (0, less_data), mode="constant", constant_values=np.nan)
    # 將地區名稱矩陣補齊，缺失值填入 "Nan"
    location_matrix_padded = np.pad(location_matrix, (0, less_data), mode="constant", constant_values="Nan")

    # 重新 reshape 成 row_size x column_size 的矩陣
    price_matrix_padded = price_matrix_padded.reshape(row_size, column_size)
    location_matrix_padded = location_matrix_padded.reshape(row_size, column_size)

    # 繪製熱力圖，顏色代表房價高低
    plt.imshow(price_matrix_padded, cmap="hot", interpolation="nearest")

    # 找出矩陣中的最大值，用來判斷文字顏色
    matrix_max = np.nanmax(price_matrix_padded)
    # 設定字型為微軟正黑體，支援中文顯示
    plt.rcParams["font.family"] = "Microsoft JhengHei"

    # 在每個格子中標註地區名稱
    for row in range(row_size) :
        for column in range(column_size) :
            price = price_matrix_padded[row][column]  # 該格的房價
            label = location_matrix_padded[row][column]  # 該格的地區名

            # 房價高於最大值的一半，以黑字顯示
            if price > matrix_max * 0.5 :
                plt.text(column, row, label, ha="center", va="center", color="black", fontsize=8)
            else :  # 房價低於最大值的一半，以白字顯示
                plt.text(column, row, label, ha="center", va="center", color="white", fontsize=8)

            # 若是缺失值，一律用黑字表示
            if label == "Nan" :
                plt.text(column, row, label, ha="center", va="center", color="black", fontsize=8)

    # 加上顏色刻度條
    plt.colorbar()
    
    # 設定中文標題
    plt.title(
        f"{city}各地區房價熱力圖",
        fontdict={"fontname": "Microsoft JhengHei", "fontsize": 14}
    )

    # 將結果存成圖片
    plt.savefig(f"{city}房價熱力圖.jpg")

    # 關閉圖表，避免重疊
    plt.close()