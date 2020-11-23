# -*- coding: utf-8 -*-
"""
Created on Sat Oct  3 17:27:41 2020

@author: ivan_
"""
#Libraries
import pandas as pd
import uuid
import os

#Variables
medArray = [] 
encounterArray = []
conditionArray = []

#Functions
def getPatientId(data):
    for entry in data['entry']:
        if entry['resource']['resourceType'] == 'Patient':
            patientId = entry['resource']['identifier'][1]['value']
            return patientId

def getMedicationData(data,patientParam):       
    for entry in data['entry']:
        entryMedArray = []
        if entry['resource']['resourceType'] == 'MedicationRequest':        
            entryMedArray.append(str(uuid.uuid1())) #Add Primary Key
            entryMedArray.append(entry['resource']['context']['reference'])
            entryMedArray.append(entry['resource']['medicationCodeableConcept']['coding'][0]['code'])
            entryMedArray.append(entry['resource']['medicationCodeableConcept']['coding'][0]['display'])
            #entryMedArray.append(entry['resource']['authoredOn'])   
            entryMedArray.append(patientParam)   
            medArray.append(entryMedArray)


def getEncounterData(data,patientParam):  
    for entry in data['entry']:
        if entry['resource']['resourceType'] == 'Encounter':
            entryEncArray = []
            entryEncArray.append(str(uuid.uuid1())) #Add Primary Key
            entryEncArray.append(entry['fullUrl'])
            entryEncArray.append(entry['resource']['type'][0]['coding'][0]['code'])
            entryEncArray.append(entry['resource']['type'][0]['text'])
            entryEncArray.append(entry['resource']['period']['start'])
            entryEncArray.append(entry['resource']['period']['end'])
            entryEncArray.append(patientParam)
            encounterArray.append(entryEncArray)

def getConditionData(data,patientParam):   
    for entry in data['entry']:
        if entry['resource']['resourceType'] == 'Condition':
            entryCondArray = []
            entryCondArray.append(str(uuid.uuid1())) #Add Primary Key
            entryCondArray.append(entry['resource']['context']['reference'])
            entryCondArray.append(entry['resource']['code']['coding'][0]['code'])
            entryCondArray.append(entry['resource']['code']['coding'][0]['display'])            
            entryCondArray.append(entry['resource']['onsetDateTime'])
            #entryCondArray.append(entry['resource']['recordedDate'])
            entryCondArray.append(patientParam)
            conditionArray.append(entryCondArray)

#Define Data
path = 'C:\\Users\\ivan_\\Documents\\Synthea\\synthea_2017_02_27.tar\\synthea_2017_02_27\\synthea_1m_fhir_1_8\\output_1_20170223T225016.tar\\output_1_20170223T225016\\output_1\\fhir'
directories = os.listdir(path)


#Create Dataframes
for subdir in directories:
    path2 = path + '\\' + subdir
    directories2 = os.listdir(path2)
    print('Starting ' + subdir)
    for subdir2 in directories2:
        path3 = path2 + '\\' + subdir2
        directories3 = os.listdir(path3)
        for file in directories3:
            fullPath = path3 + '\\' + file
            medRecData = pd.read_json(fullPath)
            patient = getPatientId(medRecData)          
            getEncounterData(medRecData,patient)
            getMedicationData(medRecData,patient)
            getConditionData(medRecData,patient)
        

#Modify Dataframes
medDataframe = pd.DataFrame(medArray)
medDataframe.columns = ['recordId','relatedEncounter','rxNormCode','rxNormName','patientKey']
encDataframe = pd.DataFrame(encounterArray)
encDataframe.columns = ['recordId','encounter','encounterTypeCode','encounterTypeName','startDate','endDate','patientKey']
condDataframe = pd.DataFrame(conditionArray)
condDataframe.columns = ['recordId','encounterreference','conditionCode','conditionName','onsetTime','patientKey']

#Combine Dataframes
diagDrugDataframe = condDataframe.merge(medDataframe, how='left',left_on='patientKey',right_on = 'patientKey',suffixes=('_diag','_med'))

#Write File
diagDrugDataframe.to_csv('C:\\Users\\ivan_\\Documents\\School\\MSDS_434\\HL7DataOutput.csv')