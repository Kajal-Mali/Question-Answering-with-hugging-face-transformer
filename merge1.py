import os
import pandas as pd
import random
import json

# Define paths
dataset_path = r"E:\Data Science Project\IEMOCAP_full_release (1)\IEMOCAP_full_release"
squad_path = 'squad_20_entries.json'  # Path to the original SQuAD dataset
output_path = 'merged_squad_iamocap_2.json'

# Initialize an empty list to store the data
data = []

def extract_emotion(transcription_file, speaker):
    # Placeholder for emotion extraction logic
    # For this example, we'll use a random choice for demonstration purposes
    emotions = ['ang', 'hap', 'sad', 'neu']
    return random.choice(emotions)

# Define the emotions of interest
emotions_of_interest = {'ang', 'hap', 'sad', 'neu'}

# Function to generate questions and answers based on emotion
def generate_questions(context, emotion):
    questions = []
    emotion_dict = {
        'ang': 'anger',
        'hap': 'happiness',
        'sad': 'sadness',
        'neu': 'neutral'
    }

    # Emotion-related question
    questions.append({
        "id": str(random.randint(1, 10000)),
        "question": f"What emotion is expressed in the following statement: '{context}'?",
        "answers": [
            {
                "text": emotion_dict.get(emotion, emotion),
                "answer_start": 0
            }
        ]
    })

    # Context-based questions
    context_lower = context.lower()
    
    if "happy" in context_lower:
        questions.append({
            "id": str(random.randint(1, 10000)),
            "question": "Why is the speaker happy?",
            "answers": [
                {
                    "text": "Because they are expressing happiness.",
                    "answer_start": context_lower.find("happy")
                }
            ]
        })

    if "long time" in context_lower:
        questions.append({
            "id": str(random.randint(1, 10000)),
            "question": "How long has it been?",
            "answers": [
                {
                    "text": "It has been a long time.",
                    "answer_start": context_lower.find("long time")
                }
            ]
        })

    if "why did you do that" in context_lower:
        questions.append({
            "id": str(random.randint(1, 10000)),
            "question": "What is the speaker questioning?",
            "answers": [
                {
                    "text": "The reason for an action.",
                    "answer_start": context_lower.find("why did you do that")
                }
            ]
        })

    if "upset" in context_lower:
        questions.append({
            "id": str(random.randint(1, 10000)),
            "question": "What did the speaker not intend to do?",
            "answers": [
                {
                    "text": "Upset someone.",
                    "answer_start": context_lower.find("upset")
                }
            ]
        })

    return questions

# Process the IEMOCAP dataset
entry_count = 0
iemocap_data = {"data": [{"title": "IEMOCAP Dataset", "paragraphs": []}]}

for session in range(1, 6):
    session_path = os.path.join(dataset_path, f'Session{session}', 'dialog', 'transcriptions')
    
    # Loop through each transcription file in the session
    for transcription_file in os.listdir(session_path):
        if transcription_file.endswith('.txt'):
            with open(os.path.join(session_path, transcription_file), 'r') as file:
                lines = file.readlines()
                
                # Process each line in the transcription file
                for line in lines:
                    parts = line.strip().split(':')
                    if len(parts) >= 2:
                        speaker, text = parts[0].strip(), ':'.join(parts[1:]).strip()
                        
                        # Extract emotion based on the transcription file and speaker
                        emotion = extract_emotion(transcription_file, speaker)
                        
                        if emotion in emotions_of_interest:
                            # Generate questions based on the text and emotion
                            questions = generate_questions(text, emotion)
                            
                            # Append to the IEMOCAP data list in SQuAD format
                            paragraph = {
                                "context": text,
                                "qas": questions
                            }
                            iemocap_data["data"][0]["paragraphs"].append(paragraph)
                            entry_count += 1
                            if entry_count >= 20:
                                break
                if entry_count >= 20:
                    break
        if entry_count >= 20:
            break
    if entry_count >= 20:
        break

# Load the original SQuAD dataset
with open(squad_path, 'r') as f:
    squad_data = json.load(f)

# Merge the datasets
squad_data["data"].extend(iemocap_data["data"])

# Save the merged dataset
with open(output_path, 'w') as f:
    json.dump(squad_data, f, indent=2)

print(f"Data merged and saved to {output_path}.")
