import csv

csv_file = open( 'list.csv', 'w', newline='', encoding='utf-8')
writer = csv.writer(csv_file)

file = open("q.txt", "r", encoding="utf-8")
Q = ""
A = ""
B = ""
C = ""
D = ""
ans = ""
for line in file : 
    line = line.replace(" ", "").replace("\n", "").replace("\r", "").replace(",", "，").replace("【单选题】", "").replace("【判断题】", "")
    if "（）" in line or "()" in line:
        Q = line
    elif "A、" in line:
        A = line[2:]
    elif "B、" in line:
        B = line[2:]
    elif "C、" in line:
        C = line[2:]
    elif "D、" in line:
        D = line[2:]
    elif "正确答案" in line:
        ans = line.replace("正确答案", "")
        if "√" in ans :
            writer.writerow([Q,"√"])
        elif "×" in ans :
            writer.writerow([Q,"×"])
        elif "A" in ans :
            writer.writerow([Q,A])
        elif "B" in ans :
            writer.writerow([Q,B])
        elif "C" in ans :
            writer.writerow([Q,C])
        elif "D" in ans :
            writer.writerow([Q,D])
file.close()
csv_file.close()