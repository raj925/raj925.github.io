# aggregateData.py

# This script looks for all the inidividual participant data (csv) files generated by jsonConvert.py
# and then creates (and subsequently updates) an aggregate csv file with average data across participants
# This csv file can then be used for overall analysis such as ANOVAs.
# You can update the below code to add new fields to aggregate file derived from the individual data.
# If you need to add new inidividual participant data points, you will need to update jsonConvert.py.
# This only deals with aggregate analysis.
# If scheduling a cronjob to run both of these scripts, run this AFTER jonConvert.

# Author: Sriraj Aiyer

import json
import pandas as pd
import csv
import glob, os
import numpy as np
import fnmatch

# Set directory and filename to save csv file to.
os.chdir("./Trials")
aggregateFilename = "../allSubjects.csv"

logf = open("aggregateDataLog.txt", "w+")

with open(aggregateFilename, mode='w') as dataOut:
    
    csv_writer = csv.writer(dataOut, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    
    # Update the below row to change the column headers for aggregate data file.
    # Make sure the order and length matches the variables added on each row in the last line of this script (ie csv_writer.writerow([...]))
    csv_writer.writerow(['Participant ID', 'Gender', 'Age', 'Device Use', 'Final Dot Difference', 'Choice of Human', 'Choice of Algorithm', 'Preference Strength', 'Max Cj', 'Min Cj', 'Cj Range', 'Num of Unique Cj Values', 'Cj1 Mean Resolution', 'Cj2 Mean Resolution', 'Mean Cj1 Accuracy', 'Mean Cj2 Accuracy', 'Sway of Human Advice', 'Sway of Algor Advice', 'Mean RT1', 'Mean RT2', 'Mean CTC', 'AccQuant1', 'AccQuant2', 'AccQuant3', 'AccQuant4', 'AdvQuant1', 'AdvQuant2', 'AdvQuant3', 'AdvQuant4', 'CjQuant1', 'CjQuant2', 'CjQuant3', 'CjQuant4', 'Mean Cj1', 'Mean Cj2', 'Human Agreed %', 'Algor Agreed %', 'Algor Agreed % Diff', 'Human Agreed Conf Diff', 'Algor Agreed Conf Diff', 'Human Disagreed Conf Diff', 'Algor Disagreed Conf Diff', 'Algor Relative Influence'])

    # For all individual participant files (which jsonConvert names in the form TRIALS.csv)
    for file in glob.glob("*TRIALS.csv"):
        with open(file) as dataIn:
            try:
                filenameSplit = file.split("_")
                pid = filenameSplit[1]
                
                # Retrieve the data under the columns listed below. Refer to the trials file to see which columns are there (currently all listed below).
                df = pd.read_csv(dataIn, usecols=['trialNumber', 'block', 'staircase', 'wherelarger', 'dotdifference', 'int1', 'cj1', 'cor1', 'int2', 'cj2', 'cor2', 'trialType', 'whichAdvisor', 'advAnswer', 'advCorrect', 'advConfidence', 'rt1', 'rt2', 'ctcTime'])

                gender = "";
                age = 0;
                for subjectFile in os.listdir('../../private/Subjects'):
                    subjectName = '*' + pid + '_SUBJECT.csv'
                    if fnmatch.fnmatch(subjectFile, subjectName):
                        f = '../../private/Subjects/' + subjectFile
                        with open(f) as subjectDataIn:
                            subjectDf = pd.read_csv(subjectDataIn, usecols=['ID','date','gender','age','deviceUse'])
                            gender = subjectDf["gender"][0]
                            age = subjectDf["age"][0]
                            deviceUse = subjectDf["deviceUse"][0]
                        break    
                # We only want to pull trials after the practice/staricase trials for this script.
                # Remove this if you want to include these practice trials in analysis.
                df = df.loc[df["block"] > 3]
                df = df.loc[df["trialType"] != "forceblk4"]

                forcedTrials = df.loc[df["trialType"] == "force"]
                choiceTrials = df.loc[df["trialType"] == "choice"]
                forceNum = len(forcedTrials)
                choiceNum = len(choiceTrials)

                # Save the fields under each column as a sepearate dataframe variable (basically, a vector).
                int1 = df["int1"]
                int2 = df["int2"]
                cj1 = df["cj1"]
                cor1 = df["cor1"]
                cj2 = df["cj2"]
                cor2 = df["cor2"]
                whichAdvisor = df["whichAdvisor"]
                advCorrect = df["advCorrect"]
                rt1 = df["rt1"]
                rt2 = df["rt2"]
                ctcTime = df["ctcTime"]
                numOfTrials = len(df)
                dotdifference = df["dotdifference"]
                finalDD = dotdifference.iloc[numOfTrials-1]

                cj1Orig = cj1
                cj2Orig = cj2
                mask = (int1 == 0)
                mask2 = (int2 == 0)
                cj1Orig[mask] = (cj1Orig[mask])*-1
                cj2Orig[mask] = (cj2Orig[mask2])*-1

                # loc is the method in Python Pandas that allows you to pull a certain portion of data based on some filter.
                # So for below, we want to find the mean of advisor used only for choice trials in order to look at proportion of advisor chosen.
                # We subtract one here because the advisor ids in the trials files are 1 and 2 rather than 0 and 1.
                algorChoice = len(df.loc[(df["trialType"] == "choice") & (df["whichAdvisor"] == 1)])/choiceNum
                humanChoice = 1 - algorChoice

                maxCj = np.max(abs(cj1Orig));
                minCj = np.min(abs(cj1Orig));
                cjRange = maxCj - minCj;
                numOfCjVals = len(np.unique(abs(cj1Orig)))

                # Resolution is the difference in average confidence during correct and error trials.
                # Computer separately pre and post advice.
                resolution = np.mean(cj1.loc[df["cor1"] == 1]) - np.mean(cj1.loc[df["cor1"] == 0])
                resolution2 = np.mean(cj2.loc[df["cor2"] == 1]) - np.mean(cj2.loc[df["cor2"] == 0])
                meanCor1 = np.sum(cor1)/(choiceNum+forceNum)
                print(meanCor1)
                meanCor2 = np.mean(cor2)
                humanSway = np.mean(cj2Orig.loc[df["whichAdvisor"] == 1] - cj1Orig.loc[df["whichAdvisor"] == 1])
                algorSway = np.mean(cj2Orig.loc[df["whichAdvisor"] == 2] - cj1Orig.loc[df["whichAdvisor"] == 2])
                meanRt1 = np.mean(rt1)
                meanRt2 = np.mean(rt2)
                meanCtc = np.mean(ctcTime)
                meanCj1 = abs(np.mean(cj1Orig))
                meanCj2 = abs(np.mean(cj2Orig))
                
                humanAgreedPercent = len(df.loc[(df["int2"] == df["advAnswer"]) & (df["whichAdvisor"] == 1) & (df["trialType"] == "force")])/len(df.loc[(df["whichAdvisor"] == 1) & (df["trialType"] == "force")])
                algorAgreedPercent = len(df.loc[(df["int2"] == df["advAnswer"]) & (df["whichAdvisor"] == 2) & (df["trialType"] == "force")])/len(df.loc[(df["whichAdvisor"] == 2) & (df["trialType"] == "force")])
                agreedDiff = algorAgreedPercent - humanAgreedPercent
                humanAgreedConfDiff = np.mean(cj2Orig.loc[(df["int2"] == df["advAnswer"]) & (df["whichAdvisor"] == 1) & (df["trialType"] == "force")] - cj1Orig.loc[(df["int2"] == df["advAnswer"]) & (df["whichAdvisor"] == 1) & (df["trialType"] == "force")])
                algorAgreedConfDiff = np.mean(cj2Orig.loc[(df["int2"] == df["advAnswer"]) & (df["whichAdvisor"] == 2) & (df["trialType"] == "force")] - cj1Orig.loc[(df["int2"] == df["advAnswer"]) & (df["whichAdvisor"] == 2) & (df["trialType"] == "force")])
                humanDisagreedConfDiff = np.mean(cj2Orig.loc[(df["int2"] != df["advAnswer"]) & (df["whichAdvisor"] == 1) & (df["trialType"] == "force")] - cj1Orig.loc[(df["int2"] != df["advAnswer"]) & (df["whichAdvisor"] == 1) & (df["trialType"] == "force")])
                algorDisagreedConfDiff = np.mean(cj2Orig.loc[(df["int2"] != df["advAnswer"]) & (df["whichAdvisor"] == 2) & (df["trialType"] == "force")] - cj1Orig.loc[(df["int2"] != df["advAnswer"]) & (df["whichAdvisor"] == 2) & (df["trialType"] == "force")])
                algorRelativeInfluence = (algorAgreedConfDiff-algorDisagreedConfDiff) - (humanAgreedConfDiff-humanDisagreedConfDiff)

                # Quantiles below created using post-advice confidence.
                # We can see how these quantiles relate to accuracy and advisor choice.
                cj2Quant = df.cj2.quantile([0.25,0.5,0.75])

                accQuant1 = df.loc[(df["cj2"] < cj2Quant[0.25]), "cor2"]
                accQuant2 = df.loc[(df["cj2"] > cj2Quant[0.25]) & (df["cj2"] < cj2Quant[0.5]), "cor2"]
                accQuant3 = df.loc[(df["cj2"] > cj2Quant[0.5]) & (df["cj2"] < cj2Quant[0.75]), "cor2"]
                accQuant4 = df.loc[(df["cj2"] > cj2Quant[0.75]), "cor2"]
                
                advQuant1 = df.loc[(df["cj2"] < cj2Quant[0.25]), "whichAdvisor"]-1
                advQuant2 = df.loc[(df["cj2"] > cj2Quant[0.25]) & (df["cj2"] < cj2Quant[0.5]), "whichAdvisor"]-1
                advQuant3 = df.loc[(df["cj2"] > cj2Quant[0.5]) & (df["cj2"] < cj2Quant[0.75]), "whichAdvisor"]-1
                advQuant4 = df.loc[(df["cj2"] > cj2Quant[0.75]), "whichAdvisor"]-1

                # This gives you the distribution of cj2 indicated, so you can see how participants use the confidence scale.
                cjQuant1 = df.loc[(df["cj2"] < cj2Quant[0.25]), "cj2"]
                cjQuant2 = df.loc[(df["cj2"] > cj2Quant[0.25]) & (df["cj2"] < cj2Quant[0.5]), "cj2"]
                cjQuant3 = df.loc[(df["cj2"] > cj2Quant[0.5]) & (df["cj2"] < cj2Quant[0.75]), "cj2"]
                cjQuant4 = df.loc[(df["cj2"] > cj2Quant[0.75]), "cj2"]
                
                # Annoying bit below where we have to check if each quantile is empty, otherwise this messes up the table...
                if accQuant1.empty:
                    accQuant1 = 0
                else:
                    accQuant1 = np.nanmean(accQuant1)

                if accQuant2.empty:
                    accQuant2 = 0
                else:
                    accQuant2 = np.nanmean(accQuant2)

                if accQuant3.empty:
                    accQuant3 = 0
                else:
                    accQuant3 = np.nanmean(accQuant3)

                if accQuant4.empty:
                    accQuant4 = 0
                else:
                    accQuant4 = np.nanmean(accQuant4)

                if advQuant1.empty:
                    advQuant1 = 0
                else:
                    advQuant1 = np.nanmean(advQuant1)

                if advQuant2.empty:
                    advQuant2 = 0
                else:
                    advQuant2 = np.nanmean(advQuant2)

                if advQuant3.empty:
                    advQuant3 = 0
                else:
                    advQuant3 = np.nanmean(advQuant3)

                if advQuant4.empty:
                    advQuant4 = 0
                else:
                    advQuant4 = np.nanmean(advQuant4)

                if cjQuant1.empty:
                    cjQuant1 = 0
                else:
                    cjQuant1 = (cjQuant1.size)/numOfTrials

                if cjQuant2.empty:
                    cjQuant2 = 0
                else:
                    cjQuant2 = (cjQuant2.size)/numOfTrials

                if cjQuant3.empty:
                    cjQuant3 = 0
                else:
                    cjQuant3 = (cjQuant3.size)/numOfTrials

                if cjQuant4.empty:
                    cjQuant4 = 0
                else:
                    cjQuant4 = (cjQuant4.size)/numOfTrials

                # All of the above fields are rounded to 3 decimal places.
                algorChoice = round(algorChoice, 3)
                humanChoice = round(humanChoice, 3)
                resolution = abs(round(resolution, 3))
                resolution2 = abs(round(resolution2, 3))
                meanCor1 = round(meanCor1, 3)
                meanCor2 = round(meanCor2, 3)
                humanSway = abs(round(humanSway, 3))
                algorSway = abs(round(algorSway, 3))
                meanRt1 = round(meanRt1, 3)
                meanRt2 = round(meanRt2, 3)
                meanCtc = round(meanCtc, 3)
                accQuant1 = round(accQuant1, 3)
                accQuant2 = round(accQuant2, 3)
                accQuant3 = round(accQuant3, 3)
                accQuant4 = round(accQuant4, 3)
                advQuant1 = round(advQuant1, 3)
                advQuant2 = round(advQuant2, 3)
                advQuant3 = round(advQuant3, 3)
                advQuant4 = round(advQuant4, 3)
                cjQuant1 = round(cjQuant1, 3)
                cjQuant2 = round(cjQuant2, 3)
                cjQuant3 = round(cjQuant3, 3)
                cjQuant4 = round(cjQuant4, 3)
                preferenceStrength = round(abs(0.5 - algorChoice), 3)
                meanCj1 = round(meanCj1, 3)
                meanCj2 = round(meanCj2, 3)
                humanAgreedPercent = round(humanAgreedPercent, 3)
                algorAgreedPercent = round(algorAgreedPercent, 3)
                agreedDiff = round(agreedDiff, 3)
                humanAgreedConfDiff = round(humanAgreedConfDiff, 3)
                algorAgreedConfDiff = round(algorAgreedConfDiff, 3)
                humanDisagreedConfDiff = round(humanDisagreedConfDiff, 3)
                algorDisagreedConfDiff = round(algorDisagreedConfDiff, 3)
                algorRelativeInfluence = round(algorRelativeInfluence, 3)
                                                                                                                          
                csv_writer.writerow([pid, gender, age, deviceUse, finalDD, algorChoice, humanChoice, preferenceStrength, maxCj, minCj, cjRange, numOfCjVals, resolution, resolution2, meanCor1, meanCor2, humanSway, algorSway, meanRt1, meanRt2, meanCtc, accQuant1, accQuant2, accQuant3, accQuant4, advQuant1, advQuant2, advQuant3, advQuant4, cjQuant1, cjQuant2, cjQuant3, cjQuant4, meanCj1, meanCj2, humanAgreedPercent, algorAgreedPercent, agreedDiff, humanAgreedConfDiff, algorAgreedConfDiff, humanDisagreedConfDiff, algorDisagreedConfDiff, algorRelativeInfluence])

            except Exception as e:
                print(str(e))
                logf.write(str(e))
 
