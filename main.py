from openai import OpenAI
import os


def transcribe_audio(audio_file_path: str) -> str:
    """
    Transcribe the given audio file using OpenAI's Whisper model via the OpenAI API.

    Args:
        audio_file_path (str): Path to the local audio file to be transcribed.
            Supports various formats including mp3, mp4, mpeg, mpga, m4a, wav, and webm.

    Returns:
        str: The transcribed text from the audio file.  
    """
    client = OpenAI(
        # This is the default and can be omitted
        api_key=os.environ.get("OPENAI_API_KEY"),
    )

    try:
        with open(audio_file_path, "rb") as audio_file:
            transcript = client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file
            )

        return transcript.text
    except Exception as e:
        return f"An error occurred: {str(e)}"


# Usage example
if __name__ == "__main__":
    audio_file_path = "test2.m4a"  # Can be mp3, mp4, mpeg, mpga, m4a, wav, or webm

    transcription = transcribe_audio(audio_file_path)
    print(f"Transcription: {transcription}")