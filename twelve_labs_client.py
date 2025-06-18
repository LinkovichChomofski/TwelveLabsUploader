import requests
import os
import time
from typing import Dict, List, Optional
import json

class TwelveLabsClient:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.twelvelabs.io/v1.3"
        self.headers = {
            "x-api-key": api_key,
            "Content-Type": "application/json"
        }
    
    def create_index(self, name: str, engines: List[str] = None) -> Dict:
        """Create a new index"""
        if engines is None:
            engines = ["marengo2.7", "pegasus1.2"]
        
        # Build models array with proper structure for API v1.3
        models = []
        for engine in engines:
            models.append({
                "model_name": engine,
                "model_options": ["visual", "audio"]
            })
        
        payload = {
            "index_name": name,
            "models": models
        }
        
        response = requests.post(
            f"{self.base_url}/indexes",
            headers=self.headers,
            json=payload
        )
        
        if response.status_code == 201:
            return response.json()
        else:
            raise Exception(f"Failed to create index: {response.status_code} - {response.text}")
    
    def get_index(self, index_id: str) -> Dict:
        """Get index details"""
        response = requests.get(
            f"{self.base_url}/indexes/{index_id}",
            headers=self.headers
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Failed to get index: {response.status_code} - {response.text}")
    
    def list_indexes(self) -> List[Dict]:
        """List all indexes"""
        response = requests.get(
            f"{self.base_url}/indexes",
            headers=self.headers
        )
        
        if response.status_code == 200:
            response_data = response.json()
            
            # Handle different possible response structures
            if "data" in response_data:
                indexes = response_data["data"]
            else:
                indexes = response_data if isinstance(response_data, list) else []
            
            return indexes
        else:
            raise Exception(f"Failed to list indexes: {response.status_code} - {response.text}")
    
    def upload_video(self, index_id: str, file_path: str, video_title: str = None) -> Dict:
        """Upload a video to an index using API v1.3 direct upload"""
        if video_title is None:
            video_title = os.path.basename(file_path)
        
        # Prepare headers (no Content-Type for multipart/form-data - requests will set it)
        headers = {
            "x-api-key": self.api_key
        }
        
        # Prepare form data
        data = {
            "index_id": index_id
        }
        
        # Open file and upload directly
        with open(file_path, 'rb') as video_file:
            files = {
                'video_file': (video_title, video_file, 'video/mp4')
            }
            
            response = requests.post(
                f"{self.base_url}/tasks",
                headers=headers,
                data=data,
                files=files
            )
        
        if response.status_code in [200, 201]:
            result = response.json()
            return result
        else:
            raise Exception(f"Failed to upload video: {response.status_code} - {response.text}")
    
    def get_task_status(self, task_id: str) -> Dict:
        """Get the status of an upload task"""
        response = requests.get(
            f"{self.base_url}/tasks/{task_id}",
            headers=self.headers
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Failed to get task status: {response.status_code} - {response.text}")
    
    def wait_for_upload_completion(self, task_id: str, timeout: int = 3600) -> Dict:
        """Wait for upload task to complete"""
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            status = self.get_task_status(task_id)
            
            if status["status"] == "ready":
                return status
            elif status["status"] == "failed":
                raise Exception(f"Upload failed: {status.get('error', 'Unknown error')}")
            
            time.sleep(10)  # Wait 10 seconds before checking again
        
        raise Exception("Upload timeout")
