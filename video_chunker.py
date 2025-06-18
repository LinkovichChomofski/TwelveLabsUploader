import os
from moviepy.editor import VideoFileClip
from typing import List, Tuple
import tempfile
from moviepy.config import change_settings

class VideoChunker:
    def __init__(self, chunk_duration_hours: float = 1.0):
        self.chunk_duration_seconds = chunk_duration_hours * 3600
        
        # Set ffmpeg path explicitly to avoid subprocess issues
        try:
            change_settings({"FFMPEG_BINARY": "/opt/homebrew/bin/ffmpeg"})
        except:
            # If homebrew path doesn't work, try default paths
            for ffmpeg_path in ["/usr/local/bin/ffmpeg", "/usr/bin/ffmpeg"]:
                if os.path.exists(ffmpeg_path):
                    try:
                        change_settings({"FFMPEG_BINARY": ffmpeg_path})
                        break
                    except:
                        continue
    
    def get_video_duration(self, file_path: str) -> float:
        """Get video duration in seconds"""
        try:
            with VideoFileClip(file_path) as clip:
                return clip.duration
        except Exception as e:
            raise Exception(f"Failed to get video duration: {str(e)}")
    
    def needs_chunking(self, file_path: str) -> bool:
        """Check if video needs to be chunked (longer than 1 hour)"""
        duration = self.get_video_duration(file_path)
        return duration > self.chunk_duration_seconds
    
    def chunk_video(self, file_path: str, output_dir: str = None) -> List[str]:
        """
        Chunk video into segments of specified duration
        Returns list of chunk file paths
        """
        if output_dir is None:
            output_dir = tempfile.mkdtemp()
        
        os.makedirs(output_dir, exist_ok=True)
        
        video_name = os.path.splitext(os.path.basename(file_path))[0]
        chunk_paths = []
        
        try:
            # First, get the total duration
            duration = self.get_video_duration(file_path)
            
            if duration <= self.chunk_duration_seconds:
                # No chunking needed, return original file
                return [file_path]
            
            chunk_count = int(duration // self.chunk_duration_seconds) + 1
            
            # Create each chunk separately to avoid subprocess corruption
            for i in range(chunk_count):
                start_time = i * self.chunk_duration_seconds
                end_time = min((i + 1) * self.chunk_duration_seconds, duration)
                
                chunk_filename = f"{video_name}_chunk_{i+1:03d}.mp4"
                chunk_path = os.path.join(output_dir, chunk_filename)
                
                # Open video file fresh for each chunk to avoid subprocess issues
                try:
                    video = VideoFileClip(file_path)
                    chunk = video.subclip(start_time, end_time)
                    
                    chunk.write_videofile(
                        chunk_path,
                        codec='libx264',
                        audio_codec='aac',
                        verbose=False,
                        logger=None,
                        temp_audiofile=f'temp-audio-{i+1}.m4a',
                        remove_temp=True,
                        preset='fast'  # Use faster preset for quicker processing
                    )
                    
                    # Clean up immediately after each chunk
                    chunk.close()
                    video.close()
                    
                    chunk_paths.append(chunk_path)
                    
                except Exception as chunk_error:
                    # Clean up on chunk error
                    try:
                        if 'chunk' in locals():
                            chunk.close()
                        if 'video' in locals():
                            video.close()
                    except:
                        pass
                    
                    # Remove failed chunk file if it exists
                    if os.path.exists(chunk_path):
                        os.remove(chunk_path)
                    
                    raise chunk_error
            
            return chunk_paths
            
        except Exception as e:
            # Clean up any created chunks on error
            for chunk_path in chunk_paths:
                if os.path.exists(chunk_path):
                    try:
                        os.remove(chunk_path)
                    except:
                        pass
            raise Exception(f"Failed to chunk video: {str(e)}")
    
    def get_chunk_info(self, file_path: str) -> Tuple[bool, int, float]:
        """
        Get information about chunking requirements
        Returns: (needs_chunking, number_of_chunks, total_duration)
        """
        duration = self.get_video_duration(file_path)
        needs_chunking = duration > self.chunk_duration_seconds
        
        if needs_chunking:
            chunk_count = int(duration // self.chunk_duration_seconds) + 1
        else:
            chunk_count = 1
        
        return needs_chunking, chunk_count, duration
