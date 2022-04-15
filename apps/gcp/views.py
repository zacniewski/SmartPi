import io
import mimetypes
import os

from django.conf import settings as project_settings
from django.http import HttpResponse
from django.shortcuts import render
from google.cloud import speech, texttospeech


def text_to_speech(request):
    """ Convert text from the form into MP3 file"""
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
    with open(file_path + "/tts/" + name_of_speech_file + ".mp3", "wb") as out_file:
        # Write the response to the output file.
        out_file.write(response.audio_content)
        print(f"Audio content written to file {name_of_speech_file}.mp3")
    return render(request, 'gcp/text-to-speech.html')


def speech_to_text(request, local_file_name):
    """
    Transcribe a short audio file using synchronous speech recognition
    Args:
      local_file_path Path to local audio file, e.g. /path/audio.wav
    """

    client = speech.SpeechClient()

    # local_file_path = 'resources/brooklyn_bridge.raw'

    # The language of the supplied audio
    language_code = "pl-PL"

    # Sample rate in Hertz of the audio data sent
    sample_rate_hertz = 24000  # było 16000

    # Encoding of audio data sent. This sample sets this explicitly.
    # This field is optional for FLAC and WAV audio formats.
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=sample_rate_hertz,
        language_code=language_code,
    )

    local_full_path = project_settings.MEDIA_ROOT + '/stt/' + local_file_name
    local_file_name = local_file_name[:-4]
    with io.open(local_full_path, "rb") as f:
        content = f.read()
    audio = {"content": content}

    response = client.recognize(config, audio)
    for result in response.results:
        # First alternative is the most probable result
        alternative = result.alternatives[0]
        print(u"Transcript: {}".format(alternative.transcript))
        print(u"Confidence: {}".format(alternative.confidence))

    return render(
        request,
        "gcp/speech-to-text.html",
        {"text": alternative.transcript,
         'confidence': alternative.confidence,
         'local_file_name': local_file_name},
    )


def output_file(request, text):
    file_path = os.path.join(project_settings.MEDIA_ROOT) + "/stt/" + text + ".mp3"
    if os.path.exists(file_path):
        with open(file_path, "rb") as fh:
            mime_type, _ = mimetypes.guess_type(file_path)
            response = HttpResponse(fh.read(), content_type=mime_type)
            response["Content-Disposition"] = "inline; filename=" + os.path.basename(
                file_path
            )
            return response
        raise Http404("Nie ma takiego pliku!")
    else:
        return render(request, "gcp/404.html")
