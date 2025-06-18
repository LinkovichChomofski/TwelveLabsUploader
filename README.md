# Twelve Labs Video Uploader 

A powerful Streamlit application for uploading videos to Twelve Labs indexes with automatic chunking for large files. Built with Twelve Labs API v1.3 compatibility.

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://your-app-url.streamlit.app)

## Features

- **API v1.3 Compatible**: Uses the latest Twelve Labs API v1.3 for reliable uploads
- **Large File Support**: Automatically chunks videos longer than 1 hour into manageable segments
- **Smart Defaults**: Pre-configured with Marengo 2.7 and Pegasus 1.2 models
- **Index Management**: Create new indexes or select from existing ones
- **Progress Tracking**: Real-time upload progress with detailed feedback
- **Auto Cleanup**: Automatic cleanup of temporary files and chunks
- **Error Handling**: Robust error handling with user-friendly messages

## Use Cases

- **Content Creators**: Upload long-form videos for AI-powered analysis
- **Media Companies**: Batch upload video content to searchable indexes
- **Developers**: Test Twelve Labs API integration with large video files
- **Researchers**: Upload video datasets for multimodal AI research

## Quick Start

### Prerequisites

1. **Twelve Labs API Key**: Get your API key from [Twelve Labs Console](https://playground.twelvelabs.io/)
2. **Python 3.8+**: Required for running the application
3. **FFmpeg**: Required for video processing (installed automatically on most systems)

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/twelve-labs-video-uploader.git
   cd twelve-labs-video-uploader
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**:
   ```bash
   streamlit run app.py
   ```

### Configuration

You can configure your API key in two ways:

1. **Via UI**: Enter your API key in the sidebar when running the app
2. **Via Environment File**: Create a `.env` file:
   ```env
   TWELVE_LABS_API_KEY=your_api_key_here
   ```

## How to Use

### 1. Configure API Key
- Enter your Twelve Labs API key in the sidebar
- The app will validate your credentials automatically

### 2. Manage Indexes
Choose between:
- **Create New Index**: Create a fresh index with default models (Marengo 2.7, Pegasus 1.2)
- **Use Existing Index**: Select from your existing indexes or enter an index ID manually

### 3. Upload Videos
- **Small Videos** (< 1 hour): Upload directly without chunking
- **Large Videos** (> 1 hour): Automatically chunked into 1-hour segments
- Monitor progress with real-time updates

### 4. Track Progress
- View upload status in real-time
- Get detailed feedback for each chunk
- Automatic cleanup of temporary files

## Architecture

### Core Components

- **`app.py`**: Main Streamlit application with UI logic
- **`twelve_labs_client.py`**: Twelve Labs API v1.3 client wrapper
- **`video_chunker.py`**: Video chunking logic using MoviePy
- **`requirements.txt`**: Python dependencies
- **`.streamlit/config.toml`**: Streamlit configuration for large file uploads

### API Integration

The app uses Twelve Labs API v1.3 with:
- **Direct Upload**: Multipart form-data upload to `/v1.3/tasks`
- **Index Management**: Create and list indexes via `/v1.3/indexes`
- **Task Tracking**: Monitor upload progress via task IDs

### Video Processing

- **Chunking Algorithm**: Splits videos into 1-hour segments
- **Format Support**: MP4, AVI, MOV, and other common formats
- **Quality Preservation**: Maintains original video quality during chunking
- **Resource Management**: Efficient memory usage with immediate cleanup

## Technical Details

### Supported Video Formats
- MP4 (recommended)
- AVI
- MOV
- WMV
- FLV
- And more via MoviePy

### File Size Limits
- **Individual Files**: Up to 100GB per file
- **Chunking**: Automatic for videos > 1 hour
- **API Limits**: Respects Twelve Labs API constraints

### Models Used
- **Marengo 2.7**: Advanced multimodal understanding
- **Pegasus 1.2**: Enhanced video and audio processing
- **Options**: Visual and audio analysis enabled

## Development

### Project Structure
```
twelve-labs-video-uploader/
├── app.py                 # Main Streamlit app
├── twelve_labs_client.py  # API client
├── video_chunker.py       # Video processing
├── requirements.txt       # Dependencies
├── .streamlit/
│   └── config.toml       # Streamlit config
├── .env.example          # Environment template
└── README.md             # This file
```

### Local Development

1. **Clone and install**:
   ```bash
   git clone <repo-url>
   cd twelve-labs-video-uploader
   pip install -r requirements.txt
   ```

2. **Set up environment**:
   ```bash
   cp .env.example .env
   # Edit .env with your API key
   ```

3. **Run locally**:
   ```bash
   streamlit run app.py
   ```

### Testing Large Files

To test with large files:
1. Use a video longer than 1 hour
2. Monitor the chunking process in the UI
3. Check that all chunks upload successfully
4. Verify cleanup of temporary files

## Deployment

### Streamlit Community Cloud

1. **Push to GitHub**: Ensure your code is in a public GitHub repository
2. **Connect to Streamlit**: Link your GitHub repo to Streamlit Community Cloud
3. **Set Secrets**: Add your `TWELVE_LABS_API_KEY` in the Streamlit secrets
4. **Deploy**: Your app will be live at `https://your-app-name.streamlit.app`

### Environment Variables

For production deployment, set:
```env
TWELVE_LABS_API_KEY=your_production_api_key
```

## Requirements

- Python 3.8+
- Streamlit 1.28+
- MoviePy 1.0+
- Requests 2.31+
- FFmpeg (for video processing)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [Twelve Labs](https://twelvelabs.io/) for their powerful video understanding API
- [Streamlit](https://streamlit.io/) for the amazing web app framework
- [MoviePy](https://zulko.github.io/moviepy/) for video processing capabilities

## Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/twelve-labs-video-uploader/issues)
- **Twelve Labs API**: [Documentation](https://docs.twelvelabs.io/)
- **Streamlit**: [Documentation](https://docs.streamlit.io/)

---

Built with  using Streamlit and Twelve Labs API
