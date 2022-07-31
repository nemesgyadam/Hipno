"""Synthesizes speech from the input string of text or ssml.
Make sure to be working in a virtual environment.

Note: ssml must be well-formed according to:
    https://www.w3.org/TR/speech-synthesis/
"""

# B -> nem rosz természetes, férfi
# C -> nem rosz, komoly, női
# D -> nem rosz kicsit gépies, férfi
# F -> szimpi, női

import os
from google.cloud import texttospeech
from config.default import config
from utils.parser import text2short


client = texttospeech.TextToSpeechClient()
voice = texttospeech.VoiceSelectionParams(
    language_code=config["language_code"], ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
)




def text2mp3(text, speed, pitch):
    
    file_name = text2short(text)
    file_name = file_name+'p'+str(pitch)+'_s'+str(speed)+'.mp3'
    file_name = os.path.join(config['path'], file_name)
    
    synthesis_input = texttospeech.SynthesisInput(text=text)
    
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3,
        pitch = pitch,
        speaking_rate = speed
    )
    response = client.synthesize_speech(
        input=synthesis_input, voice=config['voice'], audio_config=audio_config
    )


    with open(file_name, "wb") as out:
        # Write the response to the output file.
        out.write(response.audio_content)
        print(f'Audio content written to file {file_name}')
        
        
for text in config['texts']:
    for speed in config['speed_rates']:
        for pitch in config['pitch_rates']:
            text2mp3(text, speed, pitch)