# Eco-Acoustic Health Monitor: Intelligent Forest Soundscape Analysis

An intelligent web-based application designed for eco-acoustic analysis of forest soundscapes. The platform processes uploaded environmental audio recordings to extract acoustic metadata, compute Mel Spectrograms, execute pretrained Audio Spectrogram Transformer (AST) sound classification, extract 46-dimensional Librosa acoustic feature vectors, and provide a downloadable CSV summary report.

---

## 🌿 Domain & Background

Bioacoustics and passive acoustic monitoring (PAM) enable non-invasive tracking of biodiversity, animal vocalizations, and anthropogenic threats (such as chainsaws, gunshots, or motorized vehicle operations) in forest environments.

---

## 🛠️ Technology Stack

- **User Interface & Web Engine**: Streamlit (Python-based interactive GUI)
- **Deep Learning Model**: PyTorch & Hugging Face Transformers (`MIT/ast-finetuned-audioset-10-10-0.4593`)
- **Audio Processing**: Librosa, SoundFile, Mutagen
- **Machine Learning & Feature Analytics**: Scikit-Learn (RandomForest Classifier), NumPy
- **Data Visualization & Analytics**: Plotly Express, Pandas, Matplotlib

---

## 🧩 Implemented System Architecture & Modules

The application is structured into four core processing modules:

### Module 1: Audio Upload & Metadata Extraction
- Multi-format audio file loader supporting WAV and MP3 formats.
- Safe filename sanitization and local disk persistence.
- Metadata extraction using Mutagen and Wave (format, sample rate, channels, bitrate, duration, file size).

### Module 2: Signal Preprocessing & Mel Spectrogram
- Resampling audio signals to a standardized 16,000 Hz.
- Single-channel mono conversion and peak amplitude normalization (`[-1.0, 1.0]`).
- Log-scale decibel Mel Spectrogram computation (128 Mel frequency bins) visualized interactively using Plotly.

### Module 3: AudioSpectrogramTransformer (AST) Classification
- Pretrained Hugging Face AST model inference for general AudioSet event classification.
- Audio max-pooling across 10-second chunks to safely process long recordings.
- Top-5 class detection probabilities and rule-based threat evaluation (detecting chainsaw, gunshot, or motorized vehicle signatures).

### Module 4: Wildlife Acoustic Analysis & Feature Profiling
- 46-dimensional Librosa acoustic feature extraction (20 MFCC means, 20 MFCC stds, Spectral Centroid Mean/Std, Spectral Bandwidth Mean, Spectral Rolloff Mean, Zero Crossing Rate Mean, RMS Energy Mean).
- Local RandomForest Classifier integration with dataset subfolder auto-discovery (`dataset/<species_name>/*.wav`).

---

## ⚠️ Important Academic & Technical Scope Limitations

1. **AudioSpectrogramTransformer (AST) Model Scope**:
   - The AST model (`MIT/ast-finetuned-audioset`) is a general AudioSet environmental event classifier trained on 527 broad sound classes. It is **not** a specialized fine-tuned forest wildlife species classifier.

2. **Wildlife Classifier Status & Dataset Requirement**:
   - Module 4 species classification relies on a local RandomForest classifier. When no labeled species subfolders exist in `dataset/`, the model status is explicitly displayed as **"Not Trained (Dataset Required)"**. It does not invent species predictions when untrained.

3. **Ecosystem Acoustic Score (Heuristic)**:
   - The Ecosystem Acoustic Score is a project-specific heuristic metric derived from AST classification confidence and threat status flags. It is **not** a scientifically validated ecological health index.

4. **Local Audio Handling & Reports**:
   - Audio processing and file saving occur locally on the host machine. Report export currently generates a structured **CSV summary** (`eco_acoustic_analysis_summary.csv`) containing active analysis metrics.

5. **Demo / Illustrative Screens**:
   - Certain screens (Dashboard stats, Forest Ecosystem Health Overview, Historical Records, and Environmental Alerts) display explicitly labeled **demo/illustrative data** and do not represent live IoT sensor streams or persistent database records.

---

## 📦 Installation & Setup

### Prerequisites
- Python 3.9+ (Python 3.10 / 3.11 recommended)

### 1. Clone & Setup Virtual Environment
```bash
git clone <repository_url>
cd Eco-Acoustic
python -m venv venv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the Application
```bash
streamlit run app/main.py
```

The application will launch in your browser at `http://localhost:8501`.

---

## 📄 License & Usage Notice

This project was developed for academic research and demonstration purposes. It does not claim production readiness, real-time IoT network integration, database persistence, or scientifically validated ecological auditing.
