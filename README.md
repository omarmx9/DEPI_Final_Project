# DEPI_Final_Project
ASR-TTS
This project is a combination of speechtotext and text to speech, utilizing pretrained wav2vec for speechtotext and tacotron2 for text to speech, at first we have tried multiple approaches using modified pre trained models to our dataset whether being tacotron, tacotron 2, fastspeech, glowtts and coqui tts however it has proved that there were compatibility issues and would lead to many failures, hence usage of a pretrained model was needed.

We first started with loading the data which is LJSpeech dataset that contains 13,100 audio files with their own transcription, the dataset was loaded then preprocessed and resampled to 16,000 Hz for speech to text and 22,050 Hz for text to speech , once the audio was resampled, we then converted them into a mel-spectogram graphs to get a general idea on how they look like to compare once we make the generated mel-spectograms.

After preprocessing was done it was time to make and choose the model we wanted to use and train the data with, we started with tacotron and from the very beginning it started to have issues being initiated and deployed which 
