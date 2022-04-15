from django.conf import settings as project_settings
from django.shortcuts import render
from google.cloud import texttospeech


def text_to_speech(request):
    # Instantiates a client
    client = texttospeech.TextToSpeechClient()

    # Set the text input to be synthesized
    text_to_convert = request.GET.get("text_to_speech", "Witaj Arturze!")
    name_of_speech_file = request.GET.get("name_of_speech_file", "Witaj Arturze!")

    synthesis_input = texttospeech.SynthesisInput(text=text_to_convert)

    # Build the voice request, select the language code ("en-US") and the ssml
    # voice gender ("neutral")
    voice = texttospeech.VoiceSelectionParams(
        language_code="pl-PL", ssml_gender=texttospeech.SsmlVoiceGender.MALE
    )

    # Select the type of audio file you want returned
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    # Perform the text-to-speech request on the text input with the selected
    # voice parameters and audio file type
    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    # The response's audio_content is binary.
    file_path = project_settings.MEDIA_ROOT
    with open(file_path + "/" + name_of_speech_file + ".mp3", "wb") as out_file:
        # Write the response to the output file.
        out_file.write(response.audio_content)
        print('Audio content written to file "output.mp3"')
    return render(request, 'gcp/text-to-speech.html')
