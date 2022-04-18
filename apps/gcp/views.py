import io
import glob
import mimetypes
import os

from django.conf import settings as project_settings
from django.http import HttpResponse
from django.shortcuts import render
from google.cloud import speech_v1p1beta1, texttospeech


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
      local_file_name Name of local audio file, without extension, e.g. audio
    """

    client = speech_v1p1beta1.SpeechClient()

    # The language of the supplied audio
    language_code = "pl-PL"
    local_file_path = local_file_name + '.mp3'
    local_full_path = project_settings.MEDIA_ROOT + '/stt/' + local_file_path

    with io.open(local_full_path, "rb") as f:
        content = f.read()
    audio = {"content": content}

    config = speech_v1p1beta1.RecognitionConfig(
        encoding=speech_v1p1beta1.RecognitionConfig.AudioEncoding.MP3,
        sample_rate_hertz=16000,
        language_code=language_code,
    )

    # Detects speech in the audio file
    response = client.recognize(config=config, audio=audio)
    print(f"{response=}")

    for result in response.results:
        # First alternative is the most probable result
        alternative = result.alternatives[0]
        print(f"Transcript: {alternative.transcript}")
        print(f"Confidence: {alternative.confidence}")

    return render(
        request,
        "gcp/speech-to-text.html", {
            'local_file_name': local_file_name,
            'local_file_path': local_file_path,
            'transcript': alternative.transcript,
            'confidence': alternative.confidence
        }
    )


def voice_files(request):
    voice_files_list = []
    dir_path = project_settings.MEDIA_ROOT
    for full_path in glob.iglob(dir_path + '/stt/' + '*.mp3'):
        voice_files_list.append([os.path.basename(full_path), os.path.basename(full_path)[:-4]])
    return render(request, "gcp/voice-files.html", {'voice_files_list': voice_files_list})


def output_file(request, name):
    file_path = os.path.join(project_settings.MEDIA_ROOT) + "/stt/" + name + ".mp3"
    if os.path.exists(file_path):
        with open(file_path, "rb") as fh:
            mime_type, _ = mimetypes.guess_type(file_path)
            response = HttpResponse(fh.read(), content_type=mime_type)
            response["Content-Disposition"] = "inline; filename=" + os.path.basename(
                file_path
            )
            return response
    else:
        return render(request, "gcp/404.html")
