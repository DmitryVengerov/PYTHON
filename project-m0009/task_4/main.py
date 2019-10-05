from pydub import AudioSegment
from matplotlib import pyplot as plt
from numpy.lib import stride_tricks
from scipy import signal

import scipy.io.wavfile as wav
import warnings
import wave
import struct 
import numpy as np

class AudioGenerateService:
    def __init__(self):
        self.audio = []
        self.sample_rate = 44100
        self.freq_array = np.array([261.63, 293.66, 329.63, 349.23, 392.00, 440.00, 493.88])
    
    def generic_note(self, freq, duration = 1000, volume = 1.0, octave = 2):
        freq *= octave
        duration  *= 2
        for x in range(int(duration  * (self.sample_rate / 1000.0))):
            self.audio.append(volume * np.sin(2 * np.pi * freq * ( x / self.sample_rate))) 
    
    def generic_silence(self, duration  = 250):
        for x in range(int(duration  * ( self.sample_rate / 1000.0))):
            self.audio.append(.0)
        
    def save_wav(self, file_name):
        wav_file = wave.open(file_name, 'w')
        wav_file.setparams((1, 2, self.sample_rate, len(self.audio), 'NONE', 'not compressed'))
        
        for sample in self.audio:
            wav_file.writeframes(struct.pack('h', int(sample * 32767.0)))
        
        wav_file.close()
        pass
    
    def call(self):
        freq_array = self.freq_array
        for i in range(2):
            self.generic_note(freq=freq_array[1], duration = 150, octave = 1)
            self.generic_note(freq=freq_array[1], duration = 150, octave = 1)
            self.generic_note(freq=freq_array[1], duration = 150, octave = 1)
            self.generic_note(freq=freq_array[3], duration = 250, octave = 2)
            self.generic_note(freq=freq_array[5], duration = 350, octave = 2)
            self.generic_note(freq=freq_array[1], duration = 150, octave = 1)
            self.generic_note(freq=freq_array[1], duration = 150, octave = 1)
            self.generic_note(freq=freq_array[1], duration = 150, octave = 1)
            self.generic_note(freq=freq_array[3], duration = 250, octave = 2)
            self.generic_note(freq=freq_array[5], duration = 350, octave = 2)
            self.generic_note(freq=freq_array[1], duration = 150, octave = 1)
            self.generic_note(freq=freq_array[1], duration = 150, octave = 1)
            self.generic_note(freq=freq_array[1], duration = 150, octave = 1)
            self.generic_note(freq=freq_array[3], duration = 250, octave = 2)
            self.generic_note(freq=freq_array[4], duration = 350, octave = 2)
            self.generic_silence(duration = 250)
        self.save_wav('output.wav')
 
class AudioHistogram:
    def __init__(self):
        self.created_wav = AudioSegment.from_wav('output.wav')
        self.girei_wav = AudioSegment.from_wav('girei.wav')
        pass
        
    def combine(self):
        combine_wav = self.created_wav.overlay(self.girei_wav)
        combine_wav = combine_wav.fade_in(4000).fade_out(4000) 
        combine_wav.export('combine.wav', format = 'wav')
        pass        

    def create_frequency_spectrogram(self, audioPath):
        pass
        sampleRate, samples = wav.read(audioPath)
        frequencies, times, spectogram = signal.spectrogram(samples, sampleRate)
        plt.pcolormesh(times * 1000, frequencies, 10 * np.log10(spectogram))
        plt.ylabel('Frequency [Hz]')
        plt.xlabel('Time [Ms]')
        plt.show()
        pass

    def create_amplitude_spectogramm(self, audioPath):
        sample_rate, samples = wav.read(audioPath)

        samples = samples / (2. ** 15)
        sample_points = float(samples.shape[0])
        mono_audio = samples[:, 0]

        times = np.arange(0, sample_points, 1) / sample_rate * 1000

        plt.plot(times, mono_audio, color='R')
        plt.ylabel('Amplitude')
        plt.xlabel('Time [ms]')
        plt.show()

    def call(self):
        self.create_frequency_spectrogram("output.wav")
        self.create_amplitude_spectogramm("girei.wav")
        self.create_amplitude_spectogramm("combine.wav")

        pass

    
if __name__ == '__main__':
    # AudioGenerateService().call()
    AudioHistogram().call()
