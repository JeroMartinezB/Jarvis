let speechMode = false;
const modeButton = document.querySelector('#modeButton');
const container = document.querySelector('#mode');
container.innerHTML = '<button id="startButton">Start Listening</button><button id="stopButton">Stop</button>';
document.addEventListener('DOMContentLoaded', interaction);
modeButton.addEventListener('click', interaction);

function interaction() {
    speechMode = !speechMode;
    if (speechMode) {
        console.log("Welcome to speech mode");
        container.innerHTML = '<button id="startButton">Start Listening</button><button id="stopButton">Stop</button>';
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
    } else {
        console.log("Welcome to chat mode");
        container.innerHTML = '<p>Welcome to chat mode</p> <br> <textarea id="textInput"></textarea><br><button id="chatButton">Send</button>';

        const textInput = document.querySelector('#textInput');
        const chatButton = document.querySelector('#chatButton');

        chatButton.addEventListener('click', async function() {
            const prompt = textInput.value;
            const response = await fetch("/prompt", {
                method: "POST",
                body: prompt
            });

            const data = await response.text();
            document.querySelector('#chatbox').textContent = data;
            textInput.value = '';
        });
    }
}

function customVoice (text) {
    const speech = new SpeechSynthesisUtterance(text);

    function setVoice() {
        const voices = window.speechSynthesis.getVoices();
        const selectedVoice = voices.find(voice => voice.name === 'Google UK English Male');

        if (selectedVoice) {
            speech.voice = selectedVoice;
            speech.rate = 1.27;
        }

        window.speechSynthesis.speak(speech);
    }

    const voices = window.speechSynthesis.getVoices();

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