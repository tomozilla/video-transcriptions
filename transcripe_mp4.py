import os
import whisper

# Directories
INPUT_DIR = "mp4"
OUTPUT_DIR = "transcripts"

# Ensure output directory exists
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Load Whisper model (choose 'tiny', 'base', 'small', 'medium', or 'large')
model = whisper.load_model("base")

def transcribe_folder(input_dir: str, output_dir: str):
    while True:
        # Get list of files in input directory
        files = [f for f in os.listdir(input_dir) if f.lower().endswith((".mp4", ".m4a"))]
        
        if not files:
            print("No more files to process. Exiting...")
            break
            
        # Process the first file in the list
        fname = files[0]
        input_path = os.path.join(input_dir, fname)
        print(f"Transcribing {input_path}...")
        
        try:
            # Transcribe without timestamps
            result = model.transcribe(input_path, word_timestamps=False)
            text = result.get("text", "").strip()

            # Write transcript to .txt file
            base_name = os.path.splitext(fname)[0]
            out_path = os.path.join(output_dir, f"{base_name}.txt")
            with open(out_path, "w", encoding="utf-8") as f:
                f.write(text)
            print(f"Saved transcript to {out_path}")

            # Delete the original file after successful transcription
            os.remove(input_path)
            print(f"Deleted original file: {input_path}\n")
        except Exception as e:
            print(f"Error processing {input_path}: {str(e)}\n")

if __name__ == "__main__":
    print("Starting transcription process...")
    transcribe_folder(INPUT_DIR, OUTPUT_DIR)
    print("All files have been processed.")

# Usage:
# 1. pip install git+https://github.com/openai/whisper.git
# 2. Ensure ffmpeg is installed on your system.
# 3. Place your .mp4 or .m4a files into the 'mp4' folder.
# 4. Run: python transcribe_mp4.py
# 5. The script will process all files in the 'mp4' folder one by one.
# 6. Transcripts will be saved as .txt files in the 'transcripts' folder.
# 7. Original files will be deleted after successful transcription.
# 8. The script will exit when all files are processed.
