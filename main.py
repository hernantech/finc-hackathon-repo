from transcription.transcribe import transcribe_audio
import multiprocessing
def mainloop():
    #collect audio



class collect_and_pass:
    def __init__(self):
        #ping and pong buffers
        self.fivebufferone = []
        self.fivebuffertwo = []

    def start_processes(self):
        write = multiprocessing.Process(target=)
        read = multiprocessing.Process(target=)
    def capture_and_write(self):
        while True:


# Usage example
if __name__ == "__main__":
    audio_file_path = "test2.m4a"  # Can be mp3, mp4, mpeg, mpga, m4a, wav, or webm

    transcription = transcribe_audio(audio_file_path)
    print(f"Transcription: {transcription}")