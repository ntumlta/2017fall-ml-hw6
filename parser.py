import csv
import time
import re
import pyexcel_xlsx
import collections

# store passed student
students = {}

# put your deadline time here
deadline =time.strptime("2018-01-04 23:59:59", "%Y-%m-%d %H:%M:%S")
praser = re.compile('^[a-zA-Z]+\d\d\d\d\d\d\d\d')

# put your baseline
baseline = 0.34421

# replace ml2017fall-hw6-publicleaderboard.csv with your download data from kaggle
with open('ml2017fall-hw6-publicleaderboard.csv', 'r') as raw_data:
    raw_csv = csv.reader(raw_data, delimiter=',')
    raw_csv.__next__()
    for line in raw_csv:
        time_raw = time.strptime(line[2], "%Y-%m-%d %H:%M:%S")
        if time_raw < deadline:
            m = praser.match(line[1])
            if m:
                if m.group() not in students.keys():
                    students[m.group().lower()] = line[-1]
                else:
                    if line[-1] > students[m.group().lower()]:
                        students[m.group().lower()] = line[-1]

# replace ML2017Fall_hw6_score.xlsx with your download file from google excel
excel = pyexcel_xlsx.get_data('ML2017Fall_hw6_score.xlsx')

# Kaggle & Bonus is your sheet name
sheet1 = excel['Kaggle & Bonus']

# early_pass(0.8%) is the title of the line which you want to fill
filled_idx = sheet1[0].index('early_pass(0.8%)')

# 381 is the end idx of your content
for i in range(1,381):
    id_ = sheet1[i][0]
    try:
        if float(students[id_])>=baseline:
            sheet1[i][filled_idx]=1
        else:
            sheet1[i][filled_idx]=0
    except KeyError:
        sheet1[i][filled_idx]=0
pyexcel_xlsx.save_data('ML2017Fall_hw6_score.xlsx', excel)
# recommand that you can use copy paste to google excel rather than replace
