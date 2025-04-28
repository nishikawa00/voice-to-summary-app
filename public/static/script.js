const startStopButton = document.getElementById('recordButton');  // ✅ ここ！

let mediaRecorder;
let audioChunks = [];
let isRecording = false;

startStopButton.addEventListener('click', async () => {
    if (!isRecording) {
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        const options = { mimeType: 'audio/webm' }; 

        mediaRecorder = new MediaRecorder(stream);

        mediaRecorder.ondataavailable = event => {
            if (event.data.size > 0) {
                audioChunks.push(event.data);
            }
        };

        mediaRecorder.onstop = async () => {
            const audioBlob = new Blob(audioChunks, { type: 'audio/webm' });
            const formData = new FormData();
            formData.append('file', audioBlob, 'recording.webm');

            try {
                const response = await fetch('/upload', {
                    method: 'POST',
                    body: formData
                });
                const result = await response.text();
                // alert(result);
            } catch (error) {
                alert('アップロードに失敗しました: ' + error.message);
            }
        };

        mediaRecorder.start();
        isRecording = true;
        startStopButton.innerText = "録音停止";
    } else {
        mediaRecorder.stop();
        isRecording = false;
        startStopButton.innerText = "録音開始";
    }
});