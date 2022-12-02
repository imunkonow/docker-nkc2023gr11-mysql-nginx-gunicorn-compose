function speechtoText2() {
    // for html
    const downloadLink = document.getElementById('download');
    const stopButton = document.getElementById('stop');
    const time = Number(document.getElementById('time').value)*1000;
    console.log(time);

    // for audio
    let audio_sample_rate = null;
    let scriptProcessor = null;
    let audioContext = null;

    // audio data
    let audioData = [];
    let bufferSize = 1024;

    let saveAudio = function () {
      downloadLink.href = exportWAV(audioData);
      downloadLink.download = 'test.wav';
      downloadLink.style = "";
      downloadLink.click();

      audioContext.close().then(function () {
        // stopButton.setAttribute('disabled', 'disabled');
      });
    }

    // export WAV from audio float data
    let exportWAV = function (audioData) {

      let encodeWAV = function (samples, sampleRate) {
        let buffer = new ArrayBuffer(44 + samples.length * 2);
        let view = new DataView(buffer);

        let writeString = function (view, offset, string) {
          for (let i = 0; i < string.length; i++) {
            view.setUint8(offset + i, string.charCodeAt(i));
          }
        };

        let floatTo16BitPCM = function (output, offset, input) {
          for (let i = 0; i < input.length; i++ , offset += 2) {
            let s = Math.max(-1, Math.min(1, input[i]));
            output.setInt16(offset, s < 0 ? s * 0x8000 : s * 0x7FFF, true);
          }
        };

        writeString(view, 0, 'RIFF');  // RIFFヘッダ
        view.setUint32(4, 32 + samples.length * 2, true); // これ以降のファイルサイズ
        writeString(view, 8, 'WAVE'); // WAVEヘッダ
        writeString(view, 12, 'fmt '); // fmtチャンク
        view.setUint32(16, 16, true); // fmtチャンクのバイト数
        view.setUint16(20, 1, true); // フォーマットID
        view.setUint16(22, 1, true); // チャンネル数
        view.setUint32(24, sampleRate, true); // サンプリングレート
        view.setUint32(28, sampleRate * 2, true); // データ速度
        view.setUint16(32, 2, true); // ブロックサイズ
        view.setUint16(34, 16, true); // サンプルあたりのビット数
        writeString(view, 36, 'data'); // dataチャンク
        view.setUint32(40, samples.length * 2, true); // 波形データのバイト数
        floatTo16BitPCM(view, 44, samples); // 波形データ

        return view;
      };

      let mergeBuffers = function (audioData) {
        let sampleLength = 0;
        for (let i = 0; i < audioData.length; i++) {
          sampleLength += audioData[i].length;
        }
        let samples = new Float32Array(sampleLength);
        let sampleIdx = 0;
        for (let i = 0; i < audioData.length; i++) {
          for (let j = 0; j < audioData[i].length; j++) {
            samples[sampleIdx] = audioData[i][j];
            sampleIdx++;
          }
        }
        return samples;
      };

      let dataview = encodeWAV(mergeBuffers(audioData), audio_sample_rate);
      let audioBlob = new Blob([dataview], { type: 'audio/wav' });
      console.log(dataview);

      let myURL = window.URL || window.webkitURL;
      let url = myURL.createObjectURL(audioBlob);
      return url;
    };

    // stop button
    // stopButton.addEventListener('click', function () {
    //   saveAudio('../sound/record.wav');
    //   console.log('saved wav');
    // });

    // save audio data
    var onAudioProcess = function (e) {
      var input = e.inputBuffer.getChannelData(0);
      var bufferData = new Float32Array(bufferSize);
      for (var i = 0; i < bufferSize; i++) {
        bufferData[i] = input[i];
      }

      audioData.push(bufferData);
    };

    // getusermedia
    let handleSuccess = function (stream) {
      audioContext = new AudioContext();
      audio_sample_rate = audioContext.sampleRate;
      console.log(audio_sample_rate);
      scriptProcessor = audioContext.createScriptProcessor(bufferSize, 1, 1);
      var mediastreamsource = audioContext.createMediaStreamSource(stream);
      mediastreamsource.connect(scriptProcessor);
      scriptProcessor.onaudioprocess = onAudioProcess;
      scriptProcessor.connect(audioContext.destination);

      console.log('record start?');

      // when time passed without pushing the stop button
      setTimeout(function () {
        console.log("10 sec");
        saveAudio();
        // if (stopButton.disabled == false) {
        //   saveAudio();
        //   console.log("saved audio");
        // }
      }, time);
    };

    // getUserMedia
    navigator.mediaDevices.getUserMedia({ audio: true, video: false })
      .then(handleSuccess);

}