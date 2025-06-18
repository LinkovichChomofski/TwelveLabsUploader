import streamlit as st
import os
import tempfile
import shutil
from dotenv import load_dotenv
from twelve_labs_client import TwelveLabsClient
from video_chunker import VideoChunker
import time

# Load environment variables
load_dotenv()

def init_session_state():
    """Initialize session state variables"""
    if 'client' not in st.session_state:
        st.session_state.client = None
    if 'upload_progress' not in st.session_state:
        st.session_state.upload_progress = []

def format_duration(seconds):
    """Format duration from seconds to human readable format"""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    seconds = int(seconds % 60)
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"

def main():
    st.set_page_config(
        page_title="Twelve Labs Video Uploader",
        page_icon="🎬",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Main header
    st.title("🎬 Twelve Labs Video Uploader")
    st.markdown("### Upload videos to Twelve Labs indexes with automatic chunking for large files")
    
    # Info section
    with st.expander("ℹ️ About this app"):
        st.markdown("""
        This app allows you to upload videos to Twelve Labs indexes with the following features:
        - **🚀 API v1.3 Compatible**: Uses the latest Twelve Labs API
        - **📹 Large File Support**: Automatically chunks videos longer than 1 hour
        - **🎯 Smart Defaults**: Pre-configured with Marengo 2.7 and Pegasus 1.2 models
        - **📊 Progress Tracking**: Real-time upload progress with detailed feedback
        
        **Getting Started:**
        1. Enter your Twelve Labs API key in the sidebar
        2. Choose to create a new index or use an existing one
        3. Upload your video file and watch the magic happen!
        """)
    
    # Initialize session state
    if 'client' not in st.session_state:
        st.session_state.client = None
    if 'upload_progress' not in st.session_state:
        st.session_state.upload_progress = []
    
    # Sidebar for API configuration
    with st.sidebar:
        st.header("🔧 Configuration")
        
        # API Key input
        api_key = st.text_input(
            "Twelve Labs API Key:",
            type="password",
            value=os.getenv("TWELVE_LABS_API_KEY", ""),
            help="Get your API key from the Twelve Labs Console"
        )
        
        if api_key:
            try:
                st.session_state.client = TwelveLabsClient(api_key)
                st.success("✅ API key configured successfully!")
            except Exception as e:
                st.error(f"❌ Invalid API key: {str(e)}")
                st.session_state.client = None
        else:
            st.warning("⚠️ Please enter your API key to continue")
            st.session_state.client = None
        
        # Divider
        st.divider()
        
        # Help section
        st.header("📚 Help & Resources")
        st.markdown("""
        **Need help?**
        - [Twelve Labs API Docs](https://docs.twelvelabs.io/)
        - [Get API Key](https://playground.twelvelabs.io/)
        - [Supported Formats](https://docs.twelvelabs.io/docs/supported-file-formats)
        """)
        
        # Current models info
        with st.expander("🤖 Default Models"):
            st.markdown("""
            **Marengo 2.7**
            - Advanced multimodal understanding
            - Best for complex video analysis
            
            **Pegasus 1.2**
            - Enhanced video and audio processing
            - Optimized for performance
            """)
        
        # Statistics
        if st.session_state.upload_progress:
            st.header("📊 Upload Statistics")
            completed = len([p for p in st.session_state.upload_progress if p.get('status') == 'completed'])
            total = len(st.session_state.upload_progress)
            st.metric("Uploads Completed", f"{completed}/{total}")
            
            if st.button("🗑️ Clear History"):
                st.session_state.upload_progress = []
                st.rerun()
    
    if not st.session_state.client:
        st.warning("Please configure your API key in the sidebar to continue.")
        return
    
    # Main content
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header("📁 Upload Video")
        
        # Index selection/creation
        st.subheader("Index Configuration")
        
        index_option = st.radio(
            "Choose an option:",
            ["Use existing index", "Create new index"]
        )
        
        index_id = None
        
        if index_option == "Use existing index":
            # Get existing indexes only if client is configured
            if st.session_state.client:
                try:
                    indexes = st.session_state.client.list_indexes()
                    if indexes:
                        # Handle different possible field names in API v1.3
                        index_options = {}
                        for idx in indexes:
                            # Try different possible field names
                            name = idx.get('name') or idx.get('index_name') or idx.get('title', 'Unnamed Index')
                            index_id_field = idx.get('_id') or idx.get('id') or idx.get('index_id')
                            
                            if index_id_field:
                                index_options[f"{name} ({index_id_field})"] = index_id_field
                        
                        if index_options:
                            selected_index = st.selectbox("Select an index:", list(index_options.keys()))
                            if selected_index:
                                index_id = index_options[selected_index]
                        else:
                            st.warning("Found indexes but couldn't parse them properly. Please use manual index ID input.")
                    else:
                        st.warning("No existing indexes found. Please create a new one.")
                    
                    # Manual index ID input
                    manual_index_id = st.text_input("Or enter index ID manually:")
                    if manual_index_id:
                        index_id = manual_index_id
                        
                except Exception as e:
                    st.error(f"Failed to load indexes: {str(e)}")
            else:
                st.warning("Please configure your API key first to load indexes.")
                # Still allow manual index ID input
                manual_index_id = st.text_input("Or enter index ID manually:")
                if manual_index_id:
                    index_id = manual_index_id
        
        else:  # Create new index
            new_index_name = st.text_input("New index name:")
            engines = st.multiselect(
                "Select engines:",
                ["marengo2.7", "pegasus1.2", "marengo2.6", "pegasus1"],
                default=["marengo2.7", "pegasus1.2"]
            )
            
            if st.button("Create Index") and new_index_name:
                try:
                    with st.spinner("Creating index..."):
                        result = st.session_state.client.create_index(new_index_name, engines)
                        index_id = result['_id']
                        st.success(f"✅ Index created successfully! ID: {index_id}")
                except Exception as e:
                    st.error(f"❌ Failed to create index: {str(e)}")
        
        # File upload
        if index_id:
            st.subheader("📤 Upload Video")
            
            uploaded_file = st.file_uploader(
                "Choose a video file",
                type=['mp4', 'avi', 'mov', 'mkv', 'wmv', 'flv'],
                help="Supported formats: MP4, AVI, MOV, MKV, WMV, FLV. Large file uploads are supported (up to 1TB).",
                accept_multiple_files=False
            )
            
            if uploaded_file:
                # Save uploaded file temporarily
                with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as tmp_file:
                    tmp_file.write(uploaded_file.read())
                    temp_file_path = tmp_file.name
                
                try:
                    # Analyze video
                    chunker = VideoChunker()
                    needs_chunking, chunk_count, duration = chunker.get_chunk_info(temp_file_path)
                    
                    # Display video info
                    st.info(f"📊 Video Duration: {format_duration(duration)}")
                    
                    if needs_chunking:
                        st.warning(f"⚠️ Video is longer than 1 hour and will be split into {chunk_count} chunks")
                    else:
                        st.success("✅ Video is under 1 hour - no chunking needed")
                    
                    # Upload button
                    if st.button("🚀 Upload Video"):
                        upload_chunks(st.session_state.client, temp_file_path, index_id, needs_chunking)
                
                except Exception as e:
                    st.error(f"❌ Failed to analyze video: {str(e)}")
                finally:
                    # Clean up temp file
                    if os.path.exists(temp_file_path):
                        os.unlink(temp_file_path)
    
    with col2:
        st.header("📊 Upload Progress")
        
        if st.session_state.upload_progress:
            for progress_item in st.session_state.upload_progress:
                with st.expander(f"🎬 {progress_item['name']}", expanded=True):
                    st.write(f"**Status:** {progress_item['status']}")
                    st.write(f"**Task ID:** {progress_item['task_id']}")
                    if progress_item['status'] == 'processing':
                        st.spinner("Processing...")
                    elif progress_item['status'] == 'ready':
                        st.success("✅ Complete")
                    elif progress_item['status'] == 'failed':
                        st.error("❌ Failed")
        else:
            st.info("No uploads in progress")

def upload_chunks(client, file_path, index_id, needs_chunking):
    """Handle video upload with chunking if needed"""
    
    if not needs_chunking:
        # Upload original file directly
        st.info("🎬 Uploading video...")
        try:
            result = client.upload_video(index_id, file_path)
            return result
        except Exception as e:
            raise Exception(f"Upload failed: {str(e)}")
    
    # Video needs chunking
    st.info("📹 Video is longer than 1 hour. Creating chunks...")
    
    try:
        chunker = VideoChunker(chunk_duration_hours=1.0)
        
        # Create chunks
        with st.spinner("Creating video chunks..."):
            chunk_paths = chunker.chunk_video(file_path)
        
        st.success(f"✅ Created {len(chunk_paths)} chunks")
        
        # Upload each chunk
        upload_results = []
        progress_bar = st.progress(0)
        
        for i, chunk_path in enumerate(chunk_paths):
            progress = (i + 1) / len(chunk_paths)
            progress_bar.progress(progress)
            
            chunk_name = os.path.basename(chunk_path)
            st.write(f"⬆️ Uploading chunk {i+1}/{len(chunk_paths)}: {chunk_name}")
            
            try:
                result = client.upload_video(index_id, chunk_path)
                upload_results.append(result)
                st.write(f"✅ Chunk {i+1} uploaded successfully")
                
            except Exception as e:
                st.error(f"❌ Failed to upload chunk {i+1}: {str(e)}")
                # Clean up remaining chunks
                for remaining_chunk in chunk_paths[i:]:
                    if os.path.exists(remaining_chunk) and remaining_chunk != file_path:
                        try:
                            os.remove(remaining_chunk)
                        except:
                            pass
                raise e
        
        # Clean up chunk files (but not the original)
        for chunk_path in chunk_paths:
            if chunk_path != file_path and os.path.exists(chunk_path):
                try:
                    os.remove(chunk_path)
                except:
                    pass
        
        st.success(f"🎉 All {len(chunk_paths)} chunks uploaded successfully!")
        return upload_results
        
    except Exception as e:
        raise Exception(f"Chunking/upload failed: {str(e)}")

if __name__ == "__main__":
    main()
