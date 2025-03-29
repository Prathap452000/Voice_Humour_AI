# Voice Conversation AI Humor

A real-time voice conversation application that uses AI to generate witty and humorous responses. The application features voice input/output capabilities and real-time communication using WebSocket technology.

## Features

- 🎤 Voice Input: Speak to the AI using your microphone
- 🔊 Voice Output: AI responses are converted to speech
- 🤖 AI-Powered: Uses Google's Generative AI for witty responses
- ⚡ Real-time: WebSocket-based communication for instant responses
- 🎨 Modern UI: Clean and intuitive user interface
- 🔒 Secure: Environment variable-based configuration for sensitive data

## Prerequisites

- Python 3.11 or higher
- Working microphone
- Speakers or headphones
- Google API key for Generative AI

## Installation

1. Clone the repository:
```bash
git clone https://github.com/Prathap452000/Voice_Humour_AI.git
cd Voice_Humour_AI
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
# On Windows
venv\Scripts\activate
# On Unix or MacOS
source venv/bin/activate
```

3. Install required packages:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the project root with the following variables:
```
GOOGLE_API_KEY=your_api_key_here
FLASK_SECRET_KEY=your_secret_key_here
```

## Usage

1. Start the Flask server:
```bash
python app.py
```

2. Open your web browser and navigate to:
```
http://localhost:5000
```

3. Click the "Start Listening" button to begin voice interaction with the AI.

## Project Structure

```
Voice_Humour_AI/
├── app.py              # Main Flask application
├── requirements.txt    # Python dependencies
├── static/            # Static files (CSS, JS)
│   └── style.css      # Application styles
├── templates/         # HTML templates
│   └── index.html     # Main application page
└── .env              # Environment variables (create this)
```

## Technical Details

- **Backend**: Flask with Flask-SocketIO for real-time communication
- **AI**: Google's Generative AI for response generation
- **Voice Processing**: 
  - SpeechRecognition for voice-to-text
  - gTTS for text-to-speech
  - Pygame for audio playback
- **Frontend**: HTML, CSS, JavaScript with Socket.IO client

## Dependencies

- Flask 3.0.2
- google-generativeai 0.3.2
- python-dotenv 1.0.1
- SpeechRecognition 3.10.0
- gTTS 2.4.0
- playsound 1.3.0
- pydub 0.25.1
- sounddevice 0.4.6
- flask-socketio 5.3.6
- python-engineio 4.9.0
- python-socketio 5.11.2
- requests 2.31.0
- numpy 1.26.4

## Troubleshooting

1. **Microphone Issues**:
   - Ensure your microphone is properly connected and set as default
   - Check if PyAudio is correctly installed
   - Try restarting the application

2. **Audio Playback Issues**:
   - Check if your speakers/headphones are working
   - Ensure no other application is using the audio device
   - Try refreshing the page

3. **AI Response Issues**:
   - Verify your Google API key is valid
   - Check your internet connection
   - Ensure the API key has proper permissions

## Contributing

Feel free to submit issues and enhancement requests!


## Acknowledgments

- Google Generative AI for providing the AI capabilities
- Flask and Flask-SocketIO communities for the excellent frameworks
