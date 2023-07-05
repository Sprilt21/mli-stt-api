# Example filename: deepgram_test.py

from deepgram import Deepgram
import asyncio
import json
import copy
from itertools import zip_longest
import sys
#from config import *

# Mimetype for the file you want to transcribe
# Include this line only if transcribing a local file
# Example: audio/wav
MIMETYPE = 'audio/mp4'

FIRST_API_KEY = ''

async def main(lang1,lang2, FILE):

    
    # Initialize the Deepgram SDK
    deepgram = Deepgram(FIRST_API_KEY)
    
    # Check whether requested file is local or remote, and prepare source
    if FILE.startswith('http'):
        # file is remote
        # Set the source
        source = {
            'url': FILE
        }

    else:
        # file is local
        # Open the audio file
        audio = open(FILE, 'rb')

        # Set the source
        source = {
            'buffer': audio,
            'mimetype': MIMETYPE
        }
        
    #detectLang = await asyncio.create_task(
    #    deepgram.transcription.prerecorded(
    #        source,
    #         {
    #            'punctuate': True,
    #            'detect_language': True
    #        }
    #    )
    #)
    
    #domLang = detectLang['results']['channels'][0]['detected_language']
    
    #print(domLang)
    #if domLang == lang1:
        print('use more other lang')
        #return
    
    audio = open(FILE, 'rb')
    source = {
        'buffer': audio,
        'mimetype': MIMETYPE
    }
    # Send the audio to Deepgram and get the response
    response = await asyncio.create_task(
        deepgram.transcription.prerecorded(
            source,
            {   
                'model': 'phonecall',
                'tier': 'base',
                'punctuate': True,
                'language': lang1
            }
        )
    )
    print(json.dumps(response))
    words = response['results']['channels'][0]["alternatives"][0]['words']
    for word in words:
        print(word)
    print('---------------')
    # Write the response to the console
    #print(json.dumps(response, indent=4))
    
    audio = open(FILE, 'rb')
    source = {
            'buffer': audio,
            'mimetype': MIMETYPE
    }
    
    response2 = await asyncio.create_task(
        deepgram.transcription.prerecorded(
            source,
            {
                'model': 'phonecall',
                'tier': 'base',
                'punctuate': True,
                'language': lang2
            }
        )
    )
    words2 = response2['results']['channels'][0]["alternatives"][0]['words']
    for word in words2:
        print(word)
    # Write the response to the console
    #print(json.dumps(response2, indent=4))
    # Write only the transcript to the console
    # print(response["results"]["channels"][0]["alternatives"][0]["transcript"])
    
    combined = []
    languages = []
    
    secondIndex = 0
    
    for word in words:

        while secondIndex < len(words2) and word['start'] >= words2[secondIndex]['start']:
            
            combined.append(words2[secondIndex])
            languages.append(lang2)
            secondIndex += 1
        combined.append(word)
        languages.append(lang1)
    
    if secondIndex < len(words2):
        for i in range(secondIndex, len(words2)):
            combined.append(words2[i])
            languages.append(lang2)
    
    cleaned = []
    i = 0
    while i < len(combined)-1:
        
        #edit the logic of this
        if combined[i+1]['start'] - combined[i]['start'] < .1 and languages[i] != languages[i+1]:
            if combined[i+1]['confidence'] > combined[i]['confidence']:
                cleaned.append(combined[i+1])
            else:
                cleaned.append(combined[i])
            i = i+1
        else:
            cleaned.append(combined[i])
        i=i+1
    cleaned.append(combined[len(combined)-1])
    for word in cleaned:
        print(word['punctuated_word'], end=" ")

try:
    # If running in a Jupyter notebook, Jupyter is already running an event loop, so run main with this line instead:
    # await main()
    
    n = len(sys.argv)-1
    print("number of languages:",n)
    
    if n > 3:
        raise Exception("too many languages.")
    
    print("comfort lang:", sys.argv[1])
    if n > 2:
        
        print("learning lang:", sys.argv[2])
    
    asyncio.run(main(sys.argv[1],sys.argv[2], sys.argv[3]))
except Exception as e:
    exception_type, exception_object, exception_traceback = sys.exc_info()
    line_number = exception_traceback.tb_lineno
    print(f'line {line_number}: {exception_type} - {e}')
