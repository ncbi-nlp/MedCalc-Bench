from openai import AzureOpenAI
import pandas as pd
import json

def verify_medical_extraction(client, note, extracted_json, question):
    # Construct the prompt
    prompt = f"""
    Task: Verify if the extracted medical values match the patient note, focusing ONLY on values at admission/initial presentation before any treatment.

    Medical Note:
    {note}

    Extracted JSON Values:
    {extracted_json}

    Instructions:
    1. Review each attribute in the JSON against the patient note
    2. Only consider initial/admission values before any treatment
    3. For each attribute, verify if the extracted value matches the note
    4. If any value is incorrect, provide the correct value from the note

    Please provide your analysis in the following JSON format:
    {{
        "verification_results": {{
            "attribute_name": {{
                "is_correct": boolean,
                "extracted_value": "value from JSON",
                "correct_value": "value from note (if different)",
                "explanation": "brief explanation"
            }}
        }},
        "overall_assessment": "CORRECT/PARTIALLY_CORRECT/INCORRECT"
    }}

    Note: If you are not able to infer the correct value, mark it as "UNCERTAIN" in the explanation. If a value is not present in the note and the value is false, 
    """
    
    # Call Azure OpenAI
    response = client.chat.completions.create(
        model="gpt-4o", # or your deployed model name
        messages=[
            {"role": "system", "content": "You are a precise medical data verification assistant. Your task is to verify if extracted values match the source medical notes, focusing specifically on admission/initial values before treatment."},
            {"role": "user", "content": prompt}
        ],
        temperature=0,
        max_tokens=1000,
        response_format={ "type": "json_object" }
    )
    
    return response.choices[0].message.content

def process_dataset(file_path):
    # Initialize Azure OpenAI client
    client = AzureOpenAI(
        azure_endpoint="YOUR_AZURE_ENDPOINT",
        api_key="YOUR_API_KEY",
        api_version="2024-02-15-preview"
    )
    
    # Read your dataset
    df = pd.read_csv(file_path)
    
    def process_row(row):
        # Convert extracted values to JSON format
        extracted_json = {
            "lab_test": row['lab_test'],
            "value": row['extracted_value'],
            "unit": row['unit'] if 'unit' in row else None,
            # Add other relevant fields from your dataset
        }
        
        try:
            verification_result = verify_medical_extraction(
                client,
                row['patient_note'],
                json.dumps(extracted_json, indent=2),
                row['question']
            )
            return verification_result
        except Exception as e:
            return f"Error: {str(e)}"
    
    # Add verification results column
    df['verification_results'] = df.apply(process_row, axis=1)
    
    # Save results
    output_path = 'verified_medical_extractions.csv'
    df.to_csv(output_path, index=False)
    
    # Analyze results
    analyze_verification_results(df)

def analyze_verification_results(df):
    """Analyze and print summary of verification results"""
    try:
        # Convert JSON strings to dictionaries
        results = df['verification_results'].apply(json.loads)
        
        # Count overall assessments
        overall_counts = results.apply(lambda x: x['overall_assessment']).value_counts()
        
        print("\nVerification Summary:")
        print("=====================")
        print("\nOverall Assessment Counts:")
        print(overall_counts)
        
        # Analyze incorrect attributes
        print("\nDetailed Analysis of Incorrect Attributes:")
        for idx, result in results.items():
            if result['overall_assessment'] != 'CORRECT':
                print(f"\nRow {idx}:")
                for attr, details in result['verification_results'].items():
                    if not details['is_correct']:
                        print(f"- {attr}:")
                        print(f"  Extracted: {details['extracted_value']}")
                        print(f"  Correct: {details['correct_value']}")
                        print(f"  Explanation: {details['explanation']}")
                print("---")
    
    except Exception as e:
        print(f"Error in analysis: {str(e)}")

if __name__ == "__main__":
    process_dataset('your_dataset.csv')
