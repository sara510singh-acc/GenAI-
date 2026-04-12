import streamlit as st
import requests
import numpy as np
import sounddevice as sd
import io
from scipy.io.wavfile import write
import wave
import openai
from openai import OpenAI
client = OpenAI(api_key="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")



def speech_to_text(file_path):
    audio_file= open(file_path, "rb")
    transcription = client.audio.transcriptions.create(
      model="whisper-1",
      file=audio_file
    )
    print("transcript:")
    print(transcription.text)
    return transcription.text

def generate_ai_ml_image():
    prompt = """ Based on Artificial Intelligence and Machine Learning concepts,
    easy to recognize visualizations.
    """
    response = client.images.generate(
        model="dall-e-2",
        prompt=prompt,
        size="1024x1024"
    )

    image_url = response.data[0].url
    print("Image URL:", image_url)
    return image_url

def describe_image(image_url):
    response = client.chat.completions.create(
      model="gpt-4o",
      messages=[
        {
          "role": "user",
          "content": [
            {"type": "text", "text": "describe this image like an AI and ML student"},
            {
              "type": "image_url",
              "image_url": {
                "url": image_url,
              },
            },
          ],
        }
      ],
      max_tokens=300,
    )
    print("Chat GPT:")
    print(response.choices[0].message.content)
    return response.choices[0].message.content



def compare_descriptions(model_desc, user_desc):
    st.write(f" Description: {model_desc}")
    st.write(f"Your Description: {user_desc}")
    completion = client.chat.completions.create(
      model="gpt-3.5-turbo",
      messages=[
      {"role": "system", "content": "You are a Computer Science Professor in AI and ML. You have a predefined description of an image, and also a user written dscription. you just have to judge the knowledge and concepts clearance of the user provided description. keep in mind that the user is a beginner so be supportive and helpful."},
      {"role": "user", "content": f"Description: {model_desc},user Description: {user_desc}. based on these two respond what all the user can improve in their description of the image "}
      ]
    )

    print(completion.choices[0].message.content)
    st.subheader('Feedback')
    st.write(f"Analysis: {completion.choices[0].message.content.strip()}")


def app():
    st.header('Image Comprehension')
    st.write('Learn to understand and explain about the concepts with fluent understanding This task focuses on improving your speaking skills.')

    if 'image_shown' not in st.session_state:
        st.session_state.image_shown = False
    if 'recording_started' not in st.session_state:
        st.session_state.recording_started = False

    # Start button to display the image
    if st.button('Start'):
        st.session_state.image_shown = True
        st.session_state.image_generated = False

    if st.session_state.image_shown:
        # Display the image
        print(st.session_state.image_generated)
        if st.session_state.image_generated == False:
           if st.session_state.image_generated == False:
            image_url = generate_ai_ml_image()
            st.session_state.image_url = image_url
            st.session_state.image_generated = True
            st.session_state.image_url=image_url
            st.session_state.image_generated = True
            print(st.session_state.image_generated)
        st.image(st.session_state.image_url, caption='Describe this image.')
        st.subheader('You have to analyze and talk about what you see in the image. Take your time look and analyse the image think about what you want to say and then start.\n You will have 30 seconds to speak about it. Focus on rich decription fluid speech.')

        if st.button('Start Talking'):
            st.session_state.recording_started = True
            duration = 30  # seconds
            sample_rate = 44100  # Sample rate
            st.write('Recording started... speak now!')
            myrecording = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1, dtype='int16')
            sd.wait()  # Wait until recording is finished
            st.write('Recording Done!')
            st.session_state.recording_started = False
            # Convert the NumPy array to audio file
            st.write('Recording stopped.')
            output_file = "output2.wav"
            with wave.open(output_file, 'w') as wf:
                wf.setnchannels(1)  # Stereo
                wf.setsampwidth(2)  # Sample width in bytes
                wf.setframerate(sample_rate)
                wf.writeframes(myrecording.tobytes())

            print(f"Audio saved to {output_file}")
            user_description = speech_to_text("output2.wav")
            model_description = describe_image(st.session_state.image_url)
            compare_descriptions(model_description, user_description)


