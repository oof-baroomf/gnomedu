curl -fsSL https://ollama.com/install.sh | sh
git lfs install
git clone https://huggingface.co/hexgrad/Kokoro-82M
cd Kokoro-82M
sudo apt-get -qq -y install espeak-ng > /dev/null 2>&1
pip install -q phonemizer torch transformers scipy munch openai SpeechRecognition playsound python-dotenv fpdf
ollama serve &
python main.py &