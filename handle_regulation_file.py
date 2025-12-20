from PyPDF2 import PdfReader
import unicodedata
import re
import pandas as pd

reader = PdfReader("公司法.pdf") # 讀取 PDF 檔案

text = ""
for page in reader.pages:
    text += page.extract_text() + "\n"  # 提取每一頁的文字內容

text = unicodedata.normalize("NFKC", text)  # 進行 Unicode 正規化

raw_list = re.split(r"\n", text)  # 以換行符號分割文字內容

# 合併不以句號或冒號結尾的行
merged = ""
merged_list = []
for raw_data in raw_list :
    raw_data = raw_data.replace(" ", "")

    raw_data += "next"
    
    if not str(raw_data).endswith((r"。next\n", ":next")) :
        merged += raw_data
    else :
        merged += raw_data
        merged_list.append(merged)
        merged = ""

if merged :
    merged_list.append(merged)

lines_list = []
for merged_data in merged_list :
    lines = re.split(r"(?<=。)\s*next", merged_data)  # 根據句號分割段落
    for line in lines :
        line = re.sub(r"next", "", line)
        lines_list.append(line)

cleaned_list = []
for line_data in lines_list :
    title_slices = re.split(r"(\s*第\s*[1234567890]+\s*條)\s*", line_data)  # 根據條號分割
    for title_slice in title_slices :
        subtitle_slices = re.split(r"(\s*第\s*[1234567890]+\s*\-\s*[1234567890]+\s*條)\s*", title_slice)
        for subtitle_slice in subtitle_slices :
            cleaned_list.append(subtitle_slice)

# df = pd.DataFrame({"content": cleaned_list})
df = pd.DataFrame({
    "A": "",
    "B": cleaned_list
})

for index, row in df.iterrows() :
    if re.match(r"(\s*第\s*[1234567890]+\s*條)\s*|(\s*第\s*[1234567890]+\s*\-\s*[1234567890]+\s*條)\s*", row["B"]) :
        print("1 stage")
        title = row["B"]

        counter = 1
        counter_sub = 1

        for subIndex in range(index + 1, len(df)) :
            print("2 stage")
            subRow = df.loc[subIndex]

            if re.match(r"[1234567890]+\s*", subRow["B"]) :
                print("3-1 stage")
                df.at[subIndex, "A"] = title + "第" + str(counter) + "項"
                df.at[subIndex, "B"] = re.sub(r"[1234567890]+\s*", "", subRow["B"])
                counter += 1
            elif subRow["B"] == "" :
                df.at[subIndex, "A"] = ""
            elif re.match(r"(\s*第\s*[1234567890]+\s*條)\s*|(\s*第\s*[1234567890]+\s*\-\s*[1234567890]+\s*條)\s*", subRow["B"]) :
                break
            elif re.match(r"\s*[一二三四五六七八九十]+、\s*", str(subRow["B"])) :
                df.at[subIndex, "A"] = title + "第" + str(counter) + "項" + "第" + str(counter_sub) + "款"
                df.at[subIndex, "B"] = re.sub(r"\s*[一二三四五六七八九十]+、\s*", "", subRow["B"])
                counter_sub += 1
            else :
                print("3-2 stage")
                df.at[subIndex, "A"] = title
                df.at[subIndex, "B"] = subRow["B"]

df = df[df["B"].str.strip() != ""]
df = df[~df["B"].str.match(r"(\s*第\s*[1234567890]+\s*條)\s*|(\s*第\s*[1234567890]+\s*\-\s*[1234567890]+\s*條)\s*")]
df.to_excel("公司法條文.xlsx", index=False)