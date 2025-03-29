from flask import Flask, render_template, request, jsonify, session
from flask_socketio import SocketIO, emit
import google.generativeai as genai
from gtts import gTTS
import os
import tempfile
from datetime import datetime
from dotenv import load_dotenv
import pygame
import threading
import speech_recognition as sr

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "fallback-secret-key")

# Initialize SocketIO
socketio = SocketIO(app, cors_allowed_origins="*")

# Initialize Pygame mixer (once at startup)
pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)

# Configure Gemini
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel('gemini-1.5-flash')

# Global conversation history
conversation_history = []

def speak_response(text):
    """Convert text to speech using gTTS and play with Pygame"""
    tts = gTTS(text=text, lang='en')
    temp_file_path = None
    
    try:
        # Create temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_audio_file:
            tts.save(temp_audio_file.name)
            temp_file_path = temp_audio_file.name
        
        # Load and play audio
        pygame.mixer.music.load(temp_file_path)
        pygame.mixer.music.play()

        # Wait for playback to finish
        clock = pygame.time.Clock()
        while pygame.mixer.music.get_busy():
            clock.tick(30)  # Check 30 times per second
            
    except Exception as e:
        print(f"Error playing audio: {e}")
        emit('error', {'message': f'Audio playback error: {str(e)}'})
    finally:
        # Clean up with a small delay to ensure file is not in use
        if temp_file_path and os.path.exists(temp_file_path):
            try:
                pygame.mixer.music.unload()  # Unload the music before deleting
                pygame.time.wait(100)  # Wait 100ms to ensure file is released
                os.remove(temp_file_path)
            except Exception as e:
                print(f"Error cleaning up audio file: {e}")

def generate_witty_response(user_input):
    """Generate humorous response with conversation context"""
    global conversation_history
    
    # Add to history
    conversation_history.append({
        'time': datetime.now().strftime("%H:%M:%S"),
        'user': user_input
    })
    
    # Create context prompt
    prompt = f"""You are a stand-up comedian AI. Reply playfully to this in 1-2 sentences:
    
    User: "{user_input}"
    
    Your hilarious response:"""
    
    # Get Gemini response
    response = model.generate_content(prompt)
    ai_text = response.text
    
    # Add to history
    conversation_history.append({
        'time': datetime.now().strftime("%H:%M:%S"),
        'ai': ai_text
    })
    
    return ai_text

@app.route("/")
def home():
    return render_template("index.html")

@socketio.on('start_listening')
def handle_listening():
    """Handle voice input via SocketIO"""
    recognizer = sr.Recognizer()
    
    try:
        with sr.Microphone() as source:
            emit('listening_status', {'status': 'active'})
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
            
            # Speech to text
            user_input = recognizer.recognize_google(audio)
            emit('user_input', {'text': user_input})
            
            # Get AI response
            ai_response = generate_witty_response(user_input)
            emit('ai_response', {'text': ai_response})
            
            # Play audio in background thread
            threading.Thread(
                target=speak_response,
                args=(ai_response,),
                daemon=True
            ).start()
            
    except sr.WaitTimeoutError:
        emit('error', {'message': 'No speech detected'})
    except sr.UnknownValueError:
        emit('error', {'message': 'Could not understand audio'})
    except Exception as e:
        emit('error', {'message': f'Error: {str(e)}'})
    finally:
        emit('listening_status', {'status': 'inactive'})

if __name__ == "__main__":
    socketio.run(app, debug=True, host='0.0.0.0', port=5000)