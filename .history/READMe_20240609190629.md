# MedCalc-Bench

## MedCalc-Bench Dataset

To download the MedCalc-Bench Dataset CSV, either download the file, , from in this repository or from HuggingFace at .



## Reproducing Main Results 




## License 

Depending on the calculator, our dataset consists of notes that were either designed from templated-based functions implemented in Python, handwritten by clinicians, or taken from our data Open-Patients. 

Open-Patients is an aggregated dataset of 180k patient notes coming from three different sources. We have authorization to use the dataset from all three sources. The first source is the USMLE questions from MedQA which is released under the MIT License. 
The second source of our dataset are the Trec Clinical Decision Support and Trec Clinical Trial which are available for redistribution because they are both government-owned datasets released to the public. Lastly, PMC-Patients is released under the CC-BY-SA 4.0 license and so we have permission to incorporate PMC-Patients inside Open-Patients and MedCalc-Bench, but the dataset must be released under the same lisense. Hence, our source of notes, Open-Patients, and the dataset curated from it, MedCalc-Bench, are both released under the CC-BY-SA 4.0 license. 

Based on the justification of license rules, both Open-Patients and MedCalc-Bench comply with the license CC-BY-SA 4.0, but the authors of this paper will bear all responsibility in case of violation of rights. 


## Acknowledgments and Disclosure of Funding

This research was supported by the NIH Intramural Research Program, National Library of Medicine. Additionally, the contributions made by Soren Dunn were done using the Delta advanced computing and data resource which is supported by the National Science Foundation (award OAC tel:2005572) and the State of Illinois. Delta is a joint effort of the University of Illinois Urbana-Champaign (UIUC) and its National Center for Supercomputing Applications (NCSA).


## Ethics Statement
For curating the patient notes in MedCalc-Bench, we only use publicly available patient notes from published case report articles in PubMed Central and clinician-generated anonymous patient vignettes. As such, no identifiable personal health information is revealed in this study. While MedCalc-Bench is designed to evaluate the medical calculation capabilities of LLMs, it should be noted that the dataset is not intended for direct diagnostic use or medical decision-making
without review and oversight by a clinical professional. Individuals should not change their health
behavior solely on the basis of our study.


## Broader Impacts 

As described in Sec 1, medical calculators are commonly used in the clinical setting. With the rapidly growing interest in using LLMs for domain-specific applications, healthcare practitioners might directly prompt chatbots like ChatGPT to perform medical calculation tasks. However, the capabilities of LLMs in these tasks are currently unknown. Since healthcare is a high-stakes domain and wrong medical calculations can lead to severe consequences, including misdiagnosis, inappropriate treatment plans, and potential harm to patients, it is crucial to thoroughly evaluate the performance of LLMs in
medical calculations. Surprisingly, the evaluation results on our MedCalc-Bench dataset show that all the studied LLMs struggle in the medical calculation tasks. The most capable model GPT-4 achieves only 50% accuracy with one-shot learning and chain-of-thought prompting. As such, our study indicates that current LLMs are not yet ready to be used for medical calculations. It should be noted that while high scores on MedCalc-Bench do not guarantee excellence in medical calculation tasks, failing in this dataset indicates that the models must not be considered for such purposes at all. In other words, we believe that passing MedCalc-Bench should be a necessary (but not sufficient) condition for a model to be used for medical calculation

## Maintenance and Responsibility 

Any additional new notes for new or existing calculators, will be updated both on this Github under the ground_truth_csv and the HuggingFace link. 
