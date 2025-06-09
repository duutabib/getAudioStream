# Audio Stream Capture

A Python package for capturing and processing audio streams with support for real-time data handling and file recording.

## Features
- Real-time audio capture from microphone
- Configurable audio parameters (sample rate, channels, blocksize)
- Threaded implementation for non-blocking operations
- File recording support
- Real-time data queue for processing

## Prerequisites
- Python 3.8+
- PortAudio (required by sounddevice)
- System audio input device

## Installation

### Using pip (recommended)
```bash
# Clone the repository
git clone <repository-url>
cd getAudioStream

# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install the package in development mode with all dependencies
pip install -e ".[dev]"
```

### Using conda
```bash
# Create and activate conda environment
conda env create -f environment.yml
conda activate getAudioStream
```

## Usage

### Basic Usage
```python
from src.script import audioCapture

# Start audio capture
audio, dqueue, filename, thread = audioCapture(
    mode='get',  # 'get' for real-time data, 'save' to record to file
    record=True,  # Set to True to start recording immediately
    blocksize=1024,  # Audio block size
    channels=1,  # Number of audio channels
    samplerate=44100  # Sample rate in Hz
)

try:
    # Process audio data from the queue
    while True:
        if not dqueue.empty():
            data = dqueue.get()
            # Process your audio data here
            print(f"Got {len(data)} samples")
except KeyboardInterrupt:
    print("Stopping...")
```

### Command Line
```bash
python main.py
```

## Configuration

### Audio Parameters
You can configure the following parameters in the `audioCapture` function:
- `mode`: 'get' for real-time data, 'save' to record to file
- `record`: Boolean to start/stop recording
- `blocksize`: Number of frames per buffer
- `channels`: Number of audio channels (1=mono, 2=stereo)
- `samplerate`: Sample rate in Hz
- `filename`: Output filename (only used in 'save' mode)

## Development

### Dependencies
All dependencies are specified in `pyproject.toml`.


### Code Formatting
This project uses Black and isort for code formatting:
```bash
black .
isort .
```

## License
MIT

## Authors
- Abib Duut (k.aduut@gmail.com)
- Chris Parsons (chris.parsons@cjp.email)
