from src.youtube_handler import extract_video_id 
from src.youtube_handler import get_transcript_string
from src.ml_model import generate_summary 
from src.ml_model import text_to_speech , play_sound , text_to_speech_pyttsx3 
from os import getcwd
from src.file_handler import already_exist , write_summary , read_summary
import argparse 

def parse_arguments():
   parser = argparse.ArgumentParser(description="Provide the YouTube video link to process.")
   parser.add_argument("youtube_link", help="URL of the YouTube video.")
   parser.add_argument("-s", "--save", action="store_true", help="Save the summary as a voice file (optional).")
   return parser.parse_args()

def main():
   
   args = parse_arguments()
   url = args.youtube_link
   video_id = extract_video_id(url)
   

   LOW_LIMIT , UP_LIMIT = 3 , 30
   
   SOUND_PATH=f"{getcwd()}/summary_voice"
   TEXT_PATH = f"{getcwd()}/summary_text"
   
   voice_file = f"{video_id}.mp3"
   text_file = f"{video_id}.txt"
   
   voice_file_path = f"{SOUND_PATH}/{voice_file}"
   text_file_path = f"{TEXT_PATH}/{text_file}"
   
   if already_exist(TEXT_PATH,text_file) and already_exist(SOUND_PATH,voice_file):
      read_summary(text_file_path)
      play_sound(voice_file_path)
      return 
   
   content , duration = get_transcript_string(video_id)
   #print(content)
   # if duration of video is less than 30 min
   if LOW_LIMIT <= duration <= UP_LIMIT:
      summary = generate_summary(content)
      write_summary(TEXT_PATH , text_file , summary)
      print(summary)
      if args.save:
         text_to_speech(summary,voice_file_path)
      else:
         text_to_speech_pyttsx3(summary)
         
   else:
      print("[+] Invalid Youtube video length..")
   return 

if __name__ == '__main__':
   main()
   
