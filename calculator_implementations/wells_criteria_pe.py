import os
import json


def calculate_pe_wells(variables):
   clinical_dvt = variables.get('clinical_dvt', 'False')
   pe_diagnosis_likely = variables.get('pe_number_one', 'False')
   heart_rate = variables.get('heart_rate')[0]
   immobilization = variables.get('immobilization_for_3days', 'False')
   surgery_in_last_4_weeks = variables.get('surgery_in_past4weeks', 'False')
   previous_pe = variables.get('previous_pe', 'False')
   previous_dvt = variables.get('previous_dvt', 'False')
   hemoptysis = variables.get('hemoptysis', 'False')
   malignancy_or_palliative = variables.get('malignancy_with_treatment', 'False')

   score = 0
   
   if clinical_dvt:
      score += 3
   if pe_diagnosis_likely:
      score += 3
   if heart_rate > 100:
      score += 1.5
   if immobilization or surgery_in_last_4_weeks:
      score += 1.5
   if previous_pe or previous_dvt:
      score += 1.5
   if hemoptysis:
        score += 1
   if malignancy_or_palliative:
      score += 1

   return score 

def calculate_pe_wells_explanation(variables):

   explanation = "The Well's score for pulmonary embolism is currently 0.\n"

   score = 0

   if 'clinical_dvt' in variables:
      if variables['clinical_dvt']:
         explanation += f'Clinical signs and symptoms of DVT are reported to be present and so three points are added to the score, making the current total {score} + 3 = {score + 3}. '
         score += 3
      else:
         explanation += f'Clinical signs and symptoms of DVT are repoted to be absent and so the total score remains unchanged, keeping the total score at {score}. '
   else:
         explanation += f'Clinical signs and symptoms of DVT are not reported and so we assume that this is missing from the patient, keeping the current total at {score}. '
         
   if 'pe_number_one' in variables:
      if variables['pe_number_one']:
         explanation += f'Pulmonary Embolism is reported to be the #1 diagnosis or equally likely to be the #1 diagonsis and so we add 3 points to the score making the current total = {score} + 3 = {score + 3}.\n'
         score += 3
      else:
         explanation += f'Pulmonary Embolism is not reported to be the #1 diagnosis and so the total score remains unchanged, keeping the total score at {score}.\n'
   else:
      explanation += f'Whether Pulmonary Embolism is the #1 diagonsis or is equally likely to being the #1 diagnosis is not reported and so we assume this statement is false, keeping the total unchanged at {score}.\n'
      
   explanation += f"The patient's heart rate is {variables['heart_rate'][0]} beats per minute. " 
   if variables['heart_rate'][0] > 100:
      explanation += f'The heart rate is more than 100 bpm, and so the score is increased by 1.5, making the total score, {score} + 1.5 = {score + 1.5}.\n'
      score += 1.5
   else:
      explanation += f'The heart rate is less than 100 bpm, and so the score remains unchanged, keeping the total score at {score}.\n'

   if 'immobilization_for_3days' not in variables:
      explanation += f"The report does not give an indication on whether the patient has had an immobilization for at least 3 days and so we assume this to be false."
      variables['immobilization_for_3days'] = False

   if 'surgery_in_past4weeks' not in variables:
      explanation += f"The report does not give an indication on whether the patient has had a surgery for the past 4 weeks and so we assume this to be false."
      variables['surgery_in_past4weeks'] = False

   if not variables['immobilization_for_3days'] and not variables['surgery_in_past4weeks']: 
      explanation += f"Because the patient has not had an immobilization for at least 3 days, and the patient did not have a surgery in the past 4 weeks, the score remains at {score}.\n"
   elif not variables['immobilization_for_3days'] and variables['surgery_in_past4weeks']:
      explanation += f'Because the patient did not have an immobilization for at least 3 days but the patient had a surgery in the past 4 weeks, the score increases to {score} + 1.5 = {score + 1.5}.\n'
      score += 1.5
   elif variables['immobilization_for_3days'] and not variables['surgery_in_past4weeks']:
      explanation += f'Because the patient has had an immobilization for at least 3 days but the patient did not have a surgery in the past 4 weeks, the score increases to {score} + 1.5 = {score + 1.5}.\n'
      score += 1.5
   elif variables['immobilization_for_3days'] and variables['surgery_in_past4weeks']:
      explanation += f'Because the patient has had an immobilization for at least 3 days and the patient had a surgery in the past 4 weeks, the score increases to {score} + 1.5 =  {score + 1.5}.\n'
      score += 1.5


   if 'previous_pe' not in variables:
      explanation += f"The report does not give an indication on if the patient has previously had pulmonary embolism diagnosed and so we assume this to be false."
      variables['previous_pe'] = False

   if 'previous_dvt' not in variables:
      explanation += f"The report does not give an indication on if the patient has previously been diagnosed with deep vein thrombosis and so we assume this to be false."
      variables['previous_dvt'] = False

   if not variables['previous_pe'] and not variables['previous_dvt']: 
      explanation += f'Because the patient has no previous diagnosis of pulmonary embolism (PE) or deep vein thrombosis (DVT), the score remains at {score}.\n'
   elif not variables['previous_pe'] and variables['previous_dvt']:
      explanation += f'The patient not been diagnosed with pulmonary embolis (PE), but the patient has previously been diagnosed with deep vein thrombosis (DVT), we increase the current total by 1.5 so that {score} + 1.5 = {score + 1.5}.\n'
      score += 1.5
   elif variables['previous_pe'] and not variables['previous_dvt']:
      explanation += f'Because the patient has been previously diagnosed for pulmonary embolism (PE), but the patient has never been diagnosed for deep vein thrombosis (DVT), we increase the current total by 1.5 so that {score} + 1.5 = {score + 1.5}.\n'
      score += 1.5
   elif variables['previous_pe'] and variables['previous_dvt']:
      explanation += f'Because the patient has previously been diagnosed for pulmonary embolism (PE) and deep vein thrombosis (DVT), we increase the current total by 1.5 so that {score} + 1.5 = {score + 1.5}.\n'
      score += 1.5


   if 'hemoptysis' in variables:
      if variables['hemoptysis']:
         explanation += f'Hemoptysis is reported to be present and so one point is incremented to the score, making the current total {score} + 1 = {score + 1}.\n'
         score += 1
      else:
         explanation += f'Hemoptysis is reported to be absent and so the total score remains unchanged, keeping the total score at {score}.\n'
   else:
         explanation += f'Hemoptysis is not reported in the patient note and so we assume that it is missing from the patient, keeping the total score at {score}.\n'
         
   if 'malignancy_with_treatment' in variables:
      if variables['malignancy_with_treatment']:
         explanation += f'Malignany with treatment within 6 months or palliative is reported to be present and so one point is added to the score, making the total score {score} + 1 =  {score + 1}.\n'
         score += 1
      else:
         explanation += f'Malignany with treatment within 6 months or palliative is reported to be absent and so the total score remains unchanged, keeping the total score at {score}.\n'
   else:
         explanation += f'Malignany with treatment within 6 months or palliative is not reported in the patient note and so we assume that this is absent for the patient, keeping the score at {score}.\n'

   explanation += f"The patient's Well's score for pulmonary embolism is {score}.\n"

   return {"Explanation": explanation, "Answer": score, "Calculator Answer": calculate_pe_wells(variables)}


test_outputs = [{'clinical_dvt': False, 
                 "pe_number_one": False, 
                 "heart_rate": [90, "beats per minute"], 
                 'immobilization_for_3days': False,
                 'surgery_in_past4weeks': False, 
                 'previous_pe': False, 
                 'previous_dvt': False, 
                 'hemoptysis':False, 
                 'malignancy_with_treatment': False}, 

               {'clinical_dvt': True, 
                 "pe_number_one": True, 
                 "heart_rate": [110, "beats per minute"], 
                 'immobilization_for_3days': True,
                 'surgery_in_past4weeks': True, 
                 'previous_pe': True, 
                 'previous_dvt': True, 
                 'hemoptysis': True, 
                 'malignancy_with_treatment': True}, 

               {'clinical_dvt': True, 
                 "pe_number_one": True, 
                 "heart_rate": [100, "beats per minute"], 
                 'immobilization_for_3days': True,
                 'surgery_in_past4weeks': False, 
                 'previous_pe': True, 
                 'previous_dvt': False, 
                 'hemoptysis': True, 
                 'malignancy_with_treatment': True}, 

               {"heart_rate": [100, "beats per minute"]}, 

                ]

outputs = {}

text = ""

for i in range(len(test_outputs)):
    text += "Explantion:\n" + calculate_pe_wells_explanation(test_outputs[i])["Explanation"] + "\n"


file_name = "explanations/wells_critera_pe.txt"

with open(file_name, 'w') as file:
   file.write(text)

'''
os.makedirs(os.path.dirname(file_name), exist_ok=True)

with open(file_name, 'w') as file:
    json.dump(outputs, file, indent=4)
'''