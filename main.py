from models import build_model
import torch
from kokoro import generate
from openai import OpenAI
import SpeechRecognition as sr
from playsound import playsound
import tempfile
import os
from dotenv import dotenv_values
from fpdf import FPDF
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

config = dotenv_values(".env")

device = 'cpu'
VOICE_MODEL = build_model('kokoro-v0_19.pth', device)
VOICENAME = "af"
VOICEPACK = torch.load(f'voices/{VOICENAME}.pt', weights_only=True).to(device)
print(f'Loaded voice: {VOICENAME}')

client = OpenAI(
    base_url = 'http://localhost:11434/v1',
    api_key='ollama',
)
TEXT_MODEL = "deepseek-r1:1.5b"

def say(text):
    print(text)
    audio, out_ps = generate(VOICE_MODEL, text, VOICEPACK, lang=VOICENAME[0])
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio:
        temp_audio.write(audio)
        temp_audio_path = temp_audio.name
    playsound(temp_audio_path)
    os.remove(temp_audio_path)

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)
    try:
        print("Recognizing...")    
        query = r.recognize_google(audio, language ='en-in')
        print(f"User said: {query}\n")
    except Exception as e:
        print(e)    
        say("Unable to Recognize your voice.")  
        return "None"
    return query

def email_content(grade, topic, type):
    ls = os.listdir(os.getcwd())
    if f"{grade}_{topic}_{type}.pdf" in ls:
        # Create a multipart message
        msg = MIMEMultipart()
        msg["Subject"] = f"{type.capitalize()} on {topic.capitalize()}"
        msg["From"] = config["SENDER_EMAIL"]
        msg["To"] = config["RECIPIENT"]

        # Add body to email
        body = "Sent from your local Gnome system."
        msg.attach(MIMEText(body, 'plain'))

        try:
            # Create SMTP session
            with smtplib.SMTP('smtp.gmail.com', 587) as server:
                server.starttls()  # Enable security
                server.login(config["SENDER_EMAIL"], config["PASSWORD"])
                
                # Send email
                server.send_message(msg)
            
            print("Message sent!")
            say("The email has been sent.")
        
        except Exception as e:
            print(f"Error sending email: {e}")
    else:
        generate_content(grade, topic, type)
        email_content(grade, topic, type)

def generate_content(grade_level, topic, content_type):
    prompt = f"Create a {content_type} for {grade_level}th grade students on the topic of {topic}. Provide clear and engaging content tailored to their level."
    try:
        response = client.chat.completions.create(
            model=TEXT_MODEL,
            messages=[
                {"role": "system", "content": "You are a helpful assistant specialized in creating educational materials."},
                {"role": "user", "content": prompt}
            ]
        )
        content = response.choices[0].message.content
        filename = f"{grade_level}_{topic}_{content_type}.pdf"
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.multi_cell(0, 10, content)
        pdf.output(filename)

        return f"PDF saved as {filename}"
    except Exception as e:
        return f"Error: {e}"

def main_loop():
    print("Gnome is ready. Say 'gnome' to activate.")
    say("Gnome is ready. Say 'gnome' to activate.")

    while True:
        command = takeCommand().lower()
        
        if "gnome" in command:
            say("Yes, how can I assist you?")
            user_input = takeCommand()

            # Ask the LLM separately for classification
            try:
                classification_prompt = f"Is this a question or a content request? Answer with 'question' or 'content request': {user_input}"
                classification_response = client.chat.completions.create(
                    model=TEXT_MODEL,
                    messages=[
                        {"role": "system", "content": "You are an assistant that classifies user input."},
                        {"role": "user", "content": classification_prompt}
                    ]
                )

                classification = classification_response.choices[0].message.content.strip().lower()

                if classification == "question":
                    # Answer the question using the model
                    try:
                        answer_prompt = f"Answer this question: {user_input}"
                        answer_response = client.chat.completions.create(
                            model=TEXT_MODEL,
                            messages=[
                                {"role": "system", "content": "You are a knowledgeable assistant."},
                                {"role": "user", "content": answer_prompt}
                            ]
                        )
                        answer = answer_response.choices[0].message.content.strip()
                        say(answer)
                    except Exception as e:
                        say("I couldn't answer the question. Please try again later.")
                        print(f"Error answering question: {e}")
                elif classification == "content request":
                    # Generate content
                    try:
                        say("Please specify the grade, topic, and type of content, such as quiz or notes.")
                        
                        # Ask separately for grade, topic, and content type
                        grade_prompt = f"Extract the grade level (as a number) from this input: {user_input} \n<exampleresponse>9</exampleresponse>"
                        grade_response = client.chat.completions.create(
                            model=TEXT_MODEL,
                            messages=[
                                {"role": "system", "content": "You extract the grade level as a number."},
                                {"role": "user", "content": grade_prompt}
                            ]
                        )
                        grade = grade_response.choices[0].message.content.strip()

                        topic_prompt = f"Extract the topic (1-2 words) from this input: {user_input} \n<exampleresponse>Protists</exampleresponse>"
                        topic_response = client.chat.completions.create(
                            model=TEXT_MODEL,
                            messages=[
                                {"role": "system", "content": "You extract the topic as 1-2 words."},
                                {"role": "user", "content": topic_prompt}
                            ]
                        )
                        topic = topic_response.choices[0].message.content.strip()

                        content_type_prompt = f"Extract the content type (e.g., quiz, notes) from this input: {user_input} \n  \n<exampleresponse>quiz</exampleresponse>"
                        content_type_response = client.chat.completions.create(
                            model=TEXT_MODEL,
                            messages=[
                                {"role": "system", "content": "You extract the content type as one word."},
                                {"role": "user", "content": content_type_prompt}
                            ]
                        )
                        content_type = content_type_response.choices[0].message.content.strip()

                        if not grade or not topic or not content_type:
                            say("I couldn't extract all details. Please provide grade, topic, and content type.")
                            say("What is the grade level?")
                            grade = takeCommand().lower()
                            say("What is the topic?")
                            topic = takeCommand().lower()
                            say("What type of content? For example, quiz or notes.")
                            content_type = takeCommand().lower()

                        say("Generating your content. Please wait.")
                        result = generate_content(grade, topic, content_type)
                        say(result)
                    except Exception as e:
                        say("I couldn't generate the content. Please try again later.")
                        print(f"Error generating content: {e}")
                else:
                    say("I couldn't understand your request. Please try again.")
            except Exception as e:
                say("I'm having trouble understanding. Please try again later.")
                print(f"Error classifying input: {e}")

if __name__ == "__main__":
    main_loop()

if __name__ == "__main__":
    main_loop()


if __name__ == "__main__":
    main_loop()
