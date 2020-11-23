import pandas as pd
pd.set_option('display.max_columns', None)

path = 'C:\\Users\\ivan_\\Downloads\\synthea_1m_fhir_3_0_May_24\\csv'

medFile = 'C:\\Users\\ivan_\\Downloads\\synthea_1m_fhir_3_0_May_24\\csv\\medications.csv'
condFile = 'C:\\Users\\ivan_\\Downloads\\synthea_1m_fhir_3_0_May_24\\csv\\conditions.csv'
encFile = 'C:\\Users\\ivan_\\Downloads\\synthea_1m_fhir_3_0_May_24\\csv\\encounters.csv'

medData = pd.read_csv(medFile)
conData = pd.read_csv(condFile)
encData = pd.read_csv(encFile)

encDrugDataframe = encData.merge(medData, how='inner',left_on='ID',right_on = 'ENCOUNTER',suffixes=('_enc','_med'))

allDrugDataframe = encDrugDataframe.merge(conData, how='inner',left_on='ID',right_on = 'ENCOUNTER')

allDrugDataframe = allDrugDataframe[['CODE_med','DESCRIPTION_med','CODE','DESCRIPTION']]

allDrugDataframe.to_csv('C:\\Users\\ivan_\\Documents\\School\\MSDS_434\\CombinedMedicalData.csv')
