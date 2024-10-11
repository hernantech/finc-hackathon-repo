import pyaudio
import wave
import os
from datetime import datetime


def record_usb_mic_segments(segment_duration=3, sample_rate=44100, channels=1, chunk_size=1024):
    p = pyaudio.PyAudio()

    # Find the index of the first USB microphone
    usb_mic_index = None
    for i in range(p.get_device_count()):
        device_info = p.get_device_info_by_index(i)
        if device_info['maxInputChannels'] > 0 and 'USB' in device_info['name']:
            usb_mic_index = i
            break

    if usb_mic_index is None:
        print("No USB microphone found.")
        return

    stream = p.open(format=pyaudio.paInt16,
                    channels=channels,
                    rate=sample_rate,
                    input=True,
                    input_device_index=usb_mic_index,
                    frames_per_buffer=chunk_size)

    print("Recording started. Press Ctrl+C to stop.")

    try:
        while True:
            frames = []
            for _ in range(0, int(sample_rate / chunk_size * segment_duration)):
                data = stream.read(chunk_size)
                frames.append(data)

            # Generate a unique filename using timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"audio_segment_{timestamp}.wav"

            # Write the audio segment to a file
            wf = wave.open(filename, 'wb')
            wf.setnchannels(channels)
            wf.setsampwidth(p.get_sample_size(pyaudio.paInt16))
            wf.setframerate(sample_rate)
            wf.writeframes(b''.join(frames))
            wf.close()

            print(f"Saved segment: {filename}")

    except KeyboardInterrupt:
        print("Recording stopped.")

    finally:
        stream.stop_stream()
        stream.close()
        p.terminate()


def combine_latest_recordings(num_files=3, output_filename="combined_audio.wav"):
    # Get all WAV files in the current directory
    wav_files = [f for f in os.listdir() if f.startswith("audio_segment_") and f.endswith(".wav")]

    # Sort files by creation time (most recent first)
    wav_files.sort(key=lambda x: os.path.getctime(x), reverse=True)

    # Take the latest num_files
    latest_files = wav_files[:num_files]

    # Sort these files chronologically (oldest first)
    latest_files.sort(key=lambda x: datetime.strptime(x, "audio_segment_%Y%m%d_%H%M%S.wav"))

    if not latest_files:
        print("No audio segments found.")
        return

    # Read the first file to get audio parameters
    with wave.open(latest_files[0], 'rb') as first_wave:
        params = first_wave.getparams()

    # Open the output file
    with wave.open(output_filename, 'wb') as output_wave:
        output_wave.setparams(params)

        # Concatenate audio data from each file
        for filename in latest_files:
            with wave.open(filename, 'rb') as w:
                output_wave.writeframes(w.readframes(w.getnframes()))

    print(f"Combined audio saved as: {output_filename}")
    print("Files combined (in order):")
    for file in latest_files:
        print(f"- {file}")



# Usage example
record_usb_mic_segments()