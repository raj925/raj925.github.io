import json
import pandas as pd
import csv
import glob, os
os.chdir("./")
for file in glob.glob("*.json"):
    filename = file.split("_")
    date = filename[2] + "/" + filename[1] + "/" + filename[0]
    txt = open(file).read()
    
    txt = txt.replace('}"}','}}')
    txt = txt.replace('"{','{')
    txt = txt.replace('}",','},')
    f = open(file,"w")
    f.write(txt)
    f.close()
    dataJson = json.loads(txt)
    ID = dataJson["rawData"]["participantId"]
    gender = dataJson["rawData"]["miscTrials"][0]["0"]["answer"]
    age = dataJson["rawData"]["miscTrials"][0]["1"]["answer"]

    subjectFilename = '../private/' + filename[2] + filename[1] + filename[0] + '_' + ID + '_SUBJECT.csv'
    with open(subjectFilename, mode='w') as subject_file:
        subject_writer = csv.writer(subject_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        subject_writer.writerow(['ID', 'date', 'gender', 'age'])
        subject_writer.writerow([ID, date, gender, age])

    trials = dataJson["processedData"]["trials"]

    trialsFilename = '../public/' + filename[2] + filename[1] + filename[0] + '_' + ID + '_TRIALS.csv'
    with open(trialsFilename, mode='w') as trials_file:
        subject_writer = csv.writer(trials_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        subject_writer.writerow(['trialNumber', 'block', 'staircase', 'wherelarger', 'dotdifference', 'int1', 'cj1', 'cor1', 'int2', 'cj2', 'cor2', 'trialType', 'whichAdvisor', 'advAnswer', 'advCorrect', 'advConfidence', 'rt1', 'rt2'])
        for f in range(0,len(trials)):
            currentTrial = trials[f]
            if currentTrial["initialAnswer"] is not None:
                if currentTrial["initialAnswer"] == currentTrial["correctAnswer"]:
                    cor1 = 1
                else:
                    cor1 = 0
                if currentTrial["finalAnswer"] is None:
                    cor2 = None
                elif currentTrial["finalAnswer"] == currentTrial["correctAnswer"]:
                    cor2 = 1
                else:
                    cor2 = 0
                rt1 = currentTrial["timeInitialResponse"]-currentTrial["timeInitialStimOff"]
                rt1 = round((rt1/1000), 2)
                try:
                    rt2 = currentTrial["timeFinalResponse"]-currentTrial["timeFinalStart"]
                    rt2 = round((rt2/1000), 2)
                except:
                    rt2 = None
                subject_writer.writerow([currentTrial["id"], currentTrial["block"], currentTrial["practice"], currentTrial["correctAnswer"], currentTrial["dotDifference"], currentTrial["initialAnswer"], currentTrial["initialConfidence"], cor1, currentTrial["finalAnswer"], currentTrial["finalConfidence"], cor2, currentTrial["typeName"], currentTrial["advisorId"], currentTrial["advisorAnswer"], currentTrial["advisorCorrect"], currentTrial["advisorConfidence"], rt1, rt2])
