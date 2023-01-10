import csv
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as ticker
from datetime import datetime
import os

# 한글 폰트 사용을 위해서 세팅
from matplotlib import font_manager, rc
font_path = "C:/Windows/Fonts/NGULIM.TTF"
font = font_manager.FontProperties(fname=font_path).get_name()
rc('font', family=font)

filepath = "./대기환경정보.csv"
f = open(filepath,
         'r', encoding='cp949')

data = csv.reader(f)
header = next(data)

dates = []
nums = []
negative_dates = []
negative_nums = []

for row in data:
    if row[3] == "-99":
        negative_dates.append(datetime.strptime(row[0][:8], "%Y%m%d"))
        negative_nums.append(int(row[3]))
    else:
        dates.append(datetime.strptime(row[0][:8], "%Y%m%d"))
        nums.append(int(row[3]))

print("통합대기환경지수가 -99인 날은")
for i in negative_dates:
    print(str(i)[:11])

plt.figure(figsize=(40, 20))
plt.title('서울 전체 시간에 따른 통합대기환경지수')

plt.plot(dates, nums, label='양수')
plt.scatter(dates, nums, marker='.')

ax = plt.gca()
ax.xaxis.set_major_locator(ticker.MultipleLocator(100))

plt.plot(negative_dates, negative_nums, 'k.',
         markersize=6, label='-99')
plt.xticks(rotation=45)
plt.legend()
plt.show()

os.system("pause")
