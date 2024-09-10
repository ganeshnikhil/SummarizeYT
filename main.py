from src.youtube_handler import extract_video_id, get_transcript_string
from src.ml_model import generate_summary, text_to_speech, text_to_speech_pyttsx3
from os import getcwd
from src.file_handler import already_exist, write_summary, read_summary
import gradio as gr

def process_youtube_video(url, save=False):
    video_id = extract_video_id(url)
    print(f"[DEBUG] Video ID: {video_id}")  # Debugging

    LOW_LIMIT, UP_LIMIT = 0, 30
    
    SOUND_PATH = f"{getcwd()}/summary_voice"
    TEXT_PATH = f"{getcwd()}/summary_text"
    
    voice_file = f"{video_id}.mp3"
    text_file = f"{video_id}.txt"
    
    voice_file_path = f"{SOUND_PATH}/{voice_file}"
    text_file_path = f"{TEXT_PATH}/{text_file}"

    
    # Check if the summary and audio already exist
    if already_exist(TEXT_PATH, text_file) and already_exist(SOUND_PATH, voice_file):
        summary = read_summary(text_file_path)
        print(f"[DEBUG] Returning existing summary and audio file.")  # Debugging
        return text_file_path, voice_file_path  # Return the text file path and the audio file path
    
    # Check if the text file exists and audio is not to be saved
    if already_exist(TEXT_PATH, text_file) and not save:
        return text_file_path , None
    
    if already_exist(TEXT_PATH, text_file) and save:
        summary = read_summary(text_file_path)
        text_to_speech(summary, voice_file_path)
        return text_file_path , voice_file_path 
    
    # Get transcript and duration
    content, duration = get_transcript_string(video_id)
    print(f"[DEBUG] Video Duration: {duration}")  # Debugging
    print(f"[DEBUG] Transcript Content: {content[:100]}...")  # Debugging (first 100 chars)

    # Check if the video duration is within the limits
    if LOW_LIMIT <= duration <= UP_LIMIT:
        summary = generate_summary(content)
        print(f"[DEBUG] Generated Summary: {summary}")  # Debugging
        write_summary(TEXT_PATH, text_file, summary)

        # Save or play the generated summary
        if save:
            text_to_speech(summary, voice_file_path)  # Save the summary as an audio file
            print(f"[DEBUG] Saved audio file at: {voice_file_path}")  # Debugging
            return text_file_path, voice_file_path  # Return the text file path and the saved audio file path
        else:
            text_to_speech_pyttsx3(summary)  # Play the summary without saving audio
            return text_file_path, None  # Return the text file path without audio
    else:
        return "Invalid video length", None  # Return None if the video length is invalid

# Gradio interface function
def gradio_interface(youtube_link, save_audio):
    text_file_path, audio_file_path = process_youtube_video(youtube_link, save_audio)
    print(f"[DEBUG] Gradio Return Values: Text Path: {text_file_path}, Audio Path: {audio_file_path}")  # Debugging
    return text_file_path, audio_file_path

# Create Gradio interface
gradio_ui = gr.Interface(
    fn=gradio_interface,
    inputs=[
        gr.Textbox(label="YouTube Video Link"),  # Input for the YouTube link
        gr.Checkbox(label="Save as audio?")  # Optional checkbox to save audio
    ],
    outputs=[
        gr.File(label="Text File"),  # Output file component for the summary text file
        gr.Audio(label="Audio", type="filepath")  # Output audio component to provide the file
    ]
)

# Launch Gradio interface
if __name__ == '__main__':
    gradio_ui.launch()
# unchecked save mode -> you get text file only
# checked save mode -> you get both text and audio file
