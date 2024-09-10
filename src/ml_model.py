from psutil import cpu_percent
from openai import OpenAI
from gtts import gTTS 
from playsound import playsound 
import pyttsx3 
# Check CPU usage 
def cpu_use() -> int:
   """Return current CPU usage as an integer."""
   return int(cpu_percent(interval=1))

# Split text into chunks
def split_text(text: str, max_chunk_size: int = 5000) -> list[str]:
   """Split text into manageable chunks based on a maximum size."""
   chunks, current_chunk = [], ""
   for sentence in text.split("."):
      if len(current_chunk) + len(sentence) < max_chunk_size:
         current_chunk += f"{sentence}."
      else:
         chunks.append(current_chunk.strip())
         current_chunk = f"{sentence}."
   if current_chunk:
      chunks.append(current_chunk.strip())
   return chunks

# Load the summarization model
def load_summarizer_model():
   """Load the OpenAI API client for summarization."""
   return OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")

# Send a text chunk to the AI model for summarization
def send_to_ai(chunk: str, client, model:str , max_token: int) -> str:
   try:
      response = client.chat.completions.create(
            model=model,
            messages=[
               {
                  "role": "system",
                  "content": "You are a highly skilled AI trained in language comprehension and summarization. Please summarize the following text in less than 40 words."
               },
               {
                  "role": "user",
                  "content": chunk
               }
            ],
            temperature=0,
            max_tokens=max_token,
            top_p=1
      )
      return response.choices[0].message.content
   except Exception as e:
      return f"An error occurred: {e}"

# Process a text chunk using the summarization model
def process_chunk(chunk: str, client, model: str, max_token: int) -> str:
   return send_to_ai(chunk, client, model, max_token)

# Generate a summary of a large text input
def generate_summary(text: str, max_token: int = 2000, model: str = "TheBloke/Mistral-7B-Instruct-v0.2-GGUF") -> str:
   input_chunks = split_text(text)
   output_chunks = []
   
   if len(input_chunks) > 30:
      raise ValueError("Input Limit Exceeded")

   client = load_summarizer_model()

   for i, chunk in enumerate(input_chunks):
      print(f"Processing chunk {i+1}...")
      summary = process_chunk(chunk, client, model, max_token)
      output_chunks.append(summary.strip())

      if cpu_use() > 95:
         print("CPU usage exceeded its limit.")
         break
   
   return "\n".join(output_chunks)

# Convert text to speech and play it
def text_to_speech(summary: str, filepath: str) -> None:
   myobj = gTTS(text=summary, lang='en', slow=False)
   myobj.save(filepath)
   return 

def text_to_speech_pyttsx3(summary:str) -> None:
   # Initialize the pyttsx3 engine
   engine = pyttsx3.init()

   # Set properties (optional)
   engine.setProperty('rate', 150)    # Speed of speech
   engine.setProperty('volume', 1.0)  # Volume level (0.0 to 1.0)
   #speech to an audio file
   engine.say(summary)
   # Run the speech engine
   engine.runAndWait()
   return 
   
# Play a sound file
def play_sound(path: str) -> None:
   playsound(path)
