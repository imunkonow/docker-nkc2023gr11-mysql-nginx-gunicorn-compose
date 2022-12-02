function synthesizeSpeech() {
    const regionText = 'japanwest';
    phraseText = document.getElementById("phraseText").value;

    let speechConfig = SpeechSDK.SpeechConfig.fromSubscription(`{{key}}`, regionText);
    speechConfig.speechSynthesisLanguage = "ja-JP";
    speechConfig.speechSynthesisVoiceName = "ja-JP-NanamiNeural";

    const synthesizer = new SpeechSDK.SpeechSynthesizer(speechConfig);
    synthesizer.speakTextAsync(
        phraseText,
        function (result) {
            console.log(result);
            synthesizer.close();
            synthesizer = undefined;
        }, function (err) {
            console.log(err);
            synthesizer.close();
            synthesizer = undefined;
        }
    )
}

{/* <script
src="https://cdn.jsdelivr.net/npm/microsoft-cognitiveservices-speech-sdk@latest/distrib/browser/microsoft.cognitiveservices.speech.sdk.bundle-min.js">
</script> */}