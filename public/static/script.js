let mediaRecorder;
let audioChunks = [];

const startStopButton = document.getElementById('startStopButton');
let isRecording = false;

startStopButton.addEventListener('click', async () => {
    if (!isRecording) {
        // 録音開始
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
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

                if (!response.ok) {
                    // HTTPステータスコードがエラーの場合（404, 500など）
                    const errorText = await response.text();
                    console.error('HTTPエラー:', response.status, errorText);
                    alert('アップロードに失敗しました（HTTPエラー）: ' + response.status);
                    return;
                }

                // 🎯 JSONとしてパースして、summaryだけ取り出してアラート表示
                const resultJson = await response.json();
                alert(resultJson.summary);

            } catch (error) {
                // ネットワークエラー(fetch自体が失敗したとき)
                console.error('fetch自体が失敗:', error);
                alert('アップロードに失敗しました（fetch失敗）: ' + error.message);
            }
        };

        audioChunks = []; // 新しい録音のためリセット
        mediaRecorder.start();
        isRecording = true;
        startStopButton.innerText = "録音停止";

    } else {
        // 録音停止
        mediaRecorder.stop();
        isRecording = false;
        startStopButton.innerText = "録音開始";
    }
});