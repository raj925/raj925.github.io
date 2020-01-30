# jsonConvert.py
# This script takes the JSON output from the web experiment and writes two CSVs of data for that participants
# The subject CSV is for information related to the participant.
# This includes age/gender and thus is stored in the private folder.
# The trials CSV is the data related to the experiment.
# After this script is run for incoming participant JSON data, aggregateData.py is run to combine CSVs.

# Author: Sriraj Aiyer

import json
import csv
import glob, os
import sys

# Stay in the current directory
currentDir = os.path.dirname(sys.argv[0])
currentDir = currentDir + "/JSONs"
os.chdir(currentDir)

logf = open("jsonConvertLog.txt", "w+")

# For all json files in the current directory
# No need to worry about the same json file being processed twice.
recentFiles = []
for subdir, dirs, files in os.walk("./"):
    for di in dirs:
        if (di[0] != "_"):
            lookin = "./" + di
            for jsonsubdir, jsondirs, jsonfiles in os.walk(lookin):
                dirTimes = []
                for jsonfile in jsonfiles:
                    jsonfilename = jsonfile.split("_")
                    time = jsonfilename[3] + jsonfilename[4] + jsonfilename[5]
                    time = int(float(time))
                    dirTimes.append(time)
            recentfile = str(max(dirTimes))
            recentfile = "./" + di + "/" + jsonfilename[0] + "_" + jsonfilename[1] + "_" + jsonfilename[2] + "_" + recentfile[0:2] + "_" + recentfile[2:4] + "_" + recentfile[4:6] + "_" + jsonfilename[6]
            recentFiles.append(recentfile)

for file in recentFiles:
    surveyData = [[],[],[],[]]
    questions = [[],[],[],[]]
    try:
        filename = file.split("_")
        filename[0] = ((filename[0]).split("/"))[2]
        
        # Get the data of this participant's experiment from the filename (DD/MM/YYYY)
        date = filename[2] + "/" + filename[1] + "/" + filename[0]

        # Read the JSON file
        txt = open(file).read()

        # Some weird formatting in the JSON file we need to deal with so it can be parsed properly.
        txt = txt.replace('}"}','}}')
        txt = txt.replace('"{','{')
        txt = txt.replace('}",','},')

        # We change the JSON as above and then rewrite the JSON file with the cleaned-up version.
        with open(file, mode='w') as json_file:
            json_file.write(txt)

        # Main python function for intepreting JSON data. Won't work without the cleanup above.
        dataJson = json.loads(txt)
        
        # Get the demographic data from the JSON
        ID = dataJson["rawData"]["participantId"]
        gender = dataJson["rawData"]["miscTrials"][0]["0"]["answer"]
        deviceUse = dataJson["rawData"]["miscTrials"][0]["1"]["answer"]
        age = dataJson["rawData"]["miscTrials"][0]["2"]["answer"]

        miscTrials = dataJson["rawData"]["miscTrials"]
        surveys = len(miscTrials)
        count = 0
        for x in range(1,surveys):
            if "0" in miscTrials[x]:
                for y in range(0,len(miscTrials[x])):
                    if str(y) in miscTrials[x]:
                        surveyData[count]
                        surveyData[count].append(miscTrials[x][str(y)]["answer"])
                        questions[count].append(miscTrials[x][str(y)]["question"])
                count = count + 1
            else:
                continue

        surveyData = list(filter(None, surveyData))
        questions = list(filter(None, questions))

        if len(surveyData) > 0:
            for n in range(0,len(surveyData)):
                surveyFilename = '../Surveys/' + filename[2] + filename[1] + filename[0] + '_' + ID + '_SURVEY' + str(n+1) + '.csv'
                with open(surveyFilename, mode='w') as survey_file:
                    survey_writer = csv.writer(survey_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                    survey_writer.writerow(questions[n])
                    survey_writer.writerow(surveyData[n])

        # Subject data filename is made up of date and participant ID and is saved in the private folder.
        subjectFilename = '../../private/Subjects/' + filename[2] + filename[1] + filename[0] + '_' + ID + '_SUBJECT.csv'
        
        # Open subject file to write. Creates new file if it doesn't already exist, otherwise it truncates the current file.
        with open(subjectFilename, mode='w') as subject_file:
            subject_writer = csv.writer(subject_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            
            # Write the column headers first.
            subject_writer.writerow(['ID', 'date', 'gender', 'age', 'deviceUse'])
            # Write the corresponding data under each column header.
            subject_writer.writerow([ID, date, gender, age, deviceUse])

        # Get trials data from the JSON.
        trials = dataJson["processedData"]["trials"]
        
        # Trials data filename is made up of date and participant ID and is saved in the public folder.
        trialsFilename = '../Trials/' + filename[2] + filename[1] + filename[0] + '_' + ID + '_TRIALS.csv'

        # Open trials file to write.
        with open(trialsFilename, mode='w') as trials_file:
            subject_writer = csv.writer(trials_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

            # Write column headers in order. Make sure this matches the order of data below in subject_writer.writerow([currentTrial["id"]....
            subject_writer.writerow(['trialNumber', 'block', 'staircase', 'wherelarger', 'dotdifference', 'int1', 'cj1', 'cor1', 'int2', 'cj2', 'cor2', 'trialType', 'whichAdvisor', 'advAnswer', 'advCorrect', 'advConfidence', 'rt1', 'rt2', 'ctcTime'])
            for f in range(0,len(trials)):
                currentTrial = trials[f]

                # We check the correctness of each trial manually by comparing ppt answer with correct answer.
                if currentTrial["initialAnswer"] is not None:
                    if currentTrial["initialAnswer"] == currentTrial["correctAnswer"]:
                        cor1 = 1
                    else:
                        cor1 = 0

                    # We don't have cor2 for the first few blocks where no advice is given.
                    if currentTrial["finalAnswer"] is None:
                        cor2 = None
                    elif currentTrial["finalAnswer"] == currentTrial["correctAnswer"]:
                        cor2 = 1
                    else:
                        cor2 = 0

                    # Response time calculations (from ms to seconds)
                    try:
                        rt1 = currentTrial["timeInitialResponse"]-currentTrial["timeInitialStimOff"]
                        rt1 = round((rt1/1000), 2)
                        rt2 = currentTrial["timeFinalResponse"]-currentTrial["timeFinalStart"]
                        rt2 = round((rt2/1000), 2)
                        ctcTime = currentTrial["timeFinalResponse"] - currentTrial["timeInitialResponse"]
                        ctcTime = round((ctcTime/1000), 2)
                    except:
                        rt2 = None
                        ctcTime = None

                    if currentTrial["advisorAnswer"] == currentTrial["correctAnswer"]:
                        advCorrect = 1
                    else:
                        advCorrect = 0

                    # Write our data one trial at a time to the row.
                    subject_writer.writerow([currentTrial["id"], currentTrial["block"]+1, currentTrial["practice"], currentTrial["correctAnswer"], currentTrial["dotDifference"], currentTrial["initialAnswer"], currentTrial["initialConfidence"], cor1, currentTrial["finalAnswer"], currentTrial["finalConfidence"], cor2, currentTrial["typeName"], currentTrial["advisorId"], currentTrial["advisorAnswer"], advCorrect, currentTrial["advisorConfidence"], rt1, rt2, ctcTime])

    except Exception as e:
        error = "Error in File: " + file
        logf.write(error)
        logf.write(str(e))
