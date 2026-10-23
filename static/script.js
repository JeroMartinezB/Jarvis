const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;

    if (!SpeechRecognition) {
        alert("Your browser does not support the API");
    } else {
        const recognition = new SpeechRecognition();
    

        // Config
        recognition.continuous = true;
        recognition.interimResults = true;
        recognition.lang = 'en-US';

        const startButton = document.querySelector('#startButton');
        const stopButton = document.querySelector('#stopButton');
        const output = document.querySelector('#output');

        startButton.addEventListener('click', () => {
            recognition.start();
            output.innerText = "Listening";
        });

        stopButton.addEventListener('click', () => {
            recognition.stop();
        });

        // Handle the transcription
        let prompt = '';

        recognition.onresult = (event) => {

            let finalTranscript = '';

            // Loop through
            for (let i = event.resultIndex; i < event.results.length; i++) {
                const transcript = event.results[i][0].transcript;
                if (event.results[i].isFinal) {
                    //prompt += transcript + ' ';
                    finalTranscript += transcript + ' ';
                }
                
            }

            if (finalTranscript) {
                prompt = finalTranscript;
                output.innerText = finalTranscript;
            }
        };
        recognition.onerror = (event) => {
            console.error("Speech recognition error", event.error);
        };
        stopButton.addEventListener("click", async function() {
            const response = await fetch("/prompt", {
                method: "POST",
                body: prompt
            });

            const data = await response.text();
            customVoice(data);
            
            document.querySelector('#chatbox').textContent = data;
        });
    }

function customVoice (text) {
    const speech = new SpeechSynthesisUtterance(text);

    function setVoice() {
        const voices = window.speechSynthesis.getVoices();
        const selectedVoice = voices.find(voice => voice.name === 'Google UK English Male');

        if (selectedVoice) {
            speech.voice = selectedVoice;
        }

        window.speechSynthesis.speak(speech);
    }

    const voices = window.speechSynthesis.getVoices();
    console.log(voices);

    if (voices.length > 0) {
        setVoice();
    } else {
        window.speechSynthesis.addEventListener(
            'voiceschanged',
            setVoice,
            { once: true}
        );
    }
}