let mediaRecorder;
let audioChunks = [];

document.getElementById('recordButton').addEventListener('click', async () => {
  if (!mediaRecorder || mediaRecorder.state === 'inactive') {
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    mediaRecorder = new MediaRecorder(stream);
    mediaRecorder.ondataavailable = e => audioChunks.push(e.data);
    mediaRecorder.onstop = async () => {
      const audioBlob = new Blob(audioChunks, { type: 'audio/webm' });
      const formData = new FormData();
      formData.append('file', audioBlob);
      const res = await fetch('/upload', { method: 'POST', body: formData });
      const data = await res.json();
      alert('要約完了: ' + data.summary);
      audioChunks = [];
    };
    mediaRecorder.start();
  } else {
    mediaRecorder.stop();
  }
});