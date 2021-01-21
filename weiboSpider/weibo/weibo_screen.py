import csv
import pandas as pd

# 筛选与疫情相关联的微博内容并保留需要的条目
f1 = open("人民日报\\人民日报微博(2).csv", "a", encoding="UTF-8", newline='')
csv_writer = csv.writer(f1)

with open('人民日报\\人民日报12.08-01.08.csv', 'r', encoding='utf-8') as f:
    next(f)
    reader = csv.reader(f)
    for row in reader:
        if ("疫情" in row[1]) or ("病毒" in row[1]) or ("抗疫" in row[1]):
            csv_writer.writerow([row[0], row[1], row[6], row[8], row[9], row[10]])
