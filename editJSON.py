from iteration_utilities import duplicates
import json
import csv
import os

def listDups(listNums):
    return list(duplicates(listNums))

num = input("데이터 종( 86 / 87 ) : ")

dt = ''

if num == '86':
    dt = '86 특이도로'
elif num == '87':
    dt = '87 로드마크'
86

rt = 'E:\\2D\\'f'{dt}\\XIILAB\\'

url = os.walk(rt)
src = os.walk(rt)

rootList = []
fileList = []
csvRow = []
keys = ['root', 'fileName']

wCsv = []
editFileName = []
wrongCsvRoot = []
wrongFileList = []
cntWrongName = []
wrongKeys = ['root', 'fileName', 'count', 'newFileName']



for root, dirs, files in url:
    for jsonFile in files:
        newName = str(jsonFile)[:-5]
        wrongCnt = 0
        spd_first_name = ""
        spd_second_name = ""

        if('light' not in str(jsonFile)) and ('night' not in str(jsonFile)):
            wrongCnt += 1
            spd_first_name = str(jsonFile).split('_')[0]
            spd_second_name = str(jsonFile).split('_')[2] + '_' + str(jsonFile).split('_')[3] + '_' + str(jsonFile).split('_')[4]

            if(str(jsonFile[5]) == 'l'):
                newName = spd_first_name + '_light_' + spd_second_name

            elif(str(jsonFile[5]) == 'n'):
                newName = spd_first_name + '_night_' + spd_second_name
            else:
                pass
        else:
            pass
        
        if('clear' not in str(jsonFile)) and ('rainy' not in str(jsonFile)) and ('foggy' not in str(jsonFile)):
            wrongCnt += 1
            spd_first_name = newName.split('_')[0] + '_' + newName.split('_')[1]
            spd_second_name = newName.split('_')[3]+ '_' +newName.split('_')[4]

            if(str(jsonFile[11]) == 'c'):
                newName = spd_first_name + '_clear_' + spd_second_name
            elif(str(jsonFile[11]) == 'r'):
                newName = spd_first_name + '_rainy_' + spd_second_name
            elif(str(jsonFile[11]) == 'p'):
                newName = spd_first_name + '_foggy_' + spd_second_name
            else:
                pass
        else:
            pass

        if('smooth' not in str(jsonFile)) and ('traffic' not in str(jsonFile)):
            wrongCnt += 1
            spd_first_name = newName.split('_')[0] + '_' + newName.split('_')[1] + '_' + newName.split('_')[2]
            spd_second_name = newName.split('_')[4]

            if(str(jsonFile[17]) == 's'):
                newName = spd_first_name + '_smooth_' + spd_second_name
            elif(str(jsonFile[17]) == 't'):
                newName = spd_first_name + '_traffic_' + spd_second_name
            else:
                pass
        else:
            pass

        if (str(jsonFile)[-6] == ')') and (wrongCnt == 0):
            wrongCnt += 1
            newName = newName[:-11]
        elif (str(jsonFile)[-6] == ')') and (wrongCnt > 0):
            wrongCnt += 1
            newName = newName[:-3]
        else:
            pass

        if wrongCnt > 0:
            wrongCsvRoot.append(root)
            wrongFileList.append(jsonFile)
            cntWrongName.append(wrongCnt)
            editFileName.append(newName)

            jsonTime = str(newName.split('_')[1])
            jsonWeather = str(newName.split('_')[2])
            jsonFlow = str(newName.split('_')[3])
            jsonFilePath = root + '\\' + jsonFile

            with open(str(jsonFilePath), 'r', encoding='utf-8') as js:
                jf = json.loads(js.read())
            
            jf["images"][0]["filename"] = f"{newName}.png"
            jf["images"][0]["time"] = f"{jsonTime}"
            jf["images"][0]["weather"] = f"{jsonWeather}"
            jf["images"][0]["flow"] = f"{jsonFlow}"

            with open(jsonFilePath, 'w', encoding='utf-8') as njs:
                json.dump(jf, njs, ensure_ascii=False, indent='\t')

            os.rename(os.path.join(root, jsonFile), os.path.join(root, f'{newName}.json'))
        else:
            pass
    
for i in range(len(wrongFileList)):
    wrongCsvList = [wrongCsvRoot[i], wrongFileList[i], cntWrongName[i], editFileName[i]]
    wCsv.append(wrongCsvList)

with open(f'{num}wrong.csv', 'w', newline='') as wcsv:
    write = csv.writer(wcsv)
    write.writerow(wrongKeys)
    write.writerows(wCsv)

wcsv.close()

for root, dirs, files in src:
    for p in files:
        if '.json' in p:
            rootList.append(root)
            fileList.append(p)

dup_file_list = listDups(fileList)


for i in range(len(rootList)):
    if fileList[i] in dup_file_list:
        tmp_list = [rootList[i], fileList[i]]
        csvRow.append(tmp_list)

with open(f'{num}conflict.csv', 'w', newline='') as s:
    write = csv.writer(s)
    write.writerow(keys) 
    write.writerows(csvRow)

s.close()

# for x, y in csvRow:
#     print(x, y)

# print(csvRow[1][1])

with open(f'{num}.csv', 'r', encoding='utf-8') as dd:
    nine = csv.reader(dd)
    
    for row in nine:
        for x, y in csvRow:
            pngname = row[1][:-4]
            jsonname = y[:-5]
            if (jsonname == pngname) and (str(row[0]) == str(x).split('\\')[4]):
                nfn = row[2][:-4]
                nfroot = x + '\\' + y
                print(nfn)
                with open(nfroot, 'r', encoding='utf-8') as sjf:
                    secondjf = json.loads(sjf.read())

                    secondjf["images"][0]["filename"] = f"{nfn}.png"

                with open(nfroot, 'w', encoding='utf-8') as ljf:
                    json.dump(secondjf, ljf, ensure_ascii=False, indent='\t')

                os.rename(os.path.join(x, y), os.path.join(x, f'{nfn}.json'))
            else:
                pass

dd.close()