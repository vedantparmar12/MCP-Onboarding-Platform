import os
from typing import Dict, Any
from fastapi import HTTPException

class InputValidator:
    MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
    ALLOWED_FILE_TYPES = ['.pdf', '.jpg', '.png', '.jpeg']

    def validate_file(self, file_path: str) -> bool:
        """Validate file type and size"""
        if not any(file_path.endswith(ext) for ext in self.ALLOWED_FILE_TYPES):
            raise HTTPException(status_code=400, detail="Invalid file type")
        
        if os.path.getsize(file_path) > self.MAX_FILE_SIZE:
            raise HTTPException(status_code=400, detail="File too large")
        
        return True

    def validate_document_analysis_request(self, request: Dict[str, Any]) -> None:
        """Validate document analysis request"""
        if 'document_path' not in request:
            raise HTTPException(status_code=400, detail="Document path is required")
        
        self.validate_file(request['document_path'])

    def validate_compliance_request(self, request: Dict[str, Any]) -> None:
        """Validate compliance validation request"""
        if 'client_data' not in request:
            raise HTTPException(status_code=400, detail="Client data is required")
        
        if 'jurisdictions' not in request:
            raise HTTPException(status_code=400, detail="Jurisdictions are required")

    def validate_risk_prediction_request(self, request: Dict[str, Any]) -> None:
        """Validate risk prediction request"""
        if 'client_profile' not in request:
            raise HTTPException(status_code=400, detail="Client profile is required")

    def validate_chat_request(self, request: Dict[str, Any]) -> None:
        """Validate chat request"""
        if 'message' not in request:
            raise HTTPException(status_code=400, detail="Message is required")
        
        if 'client_id' not in request:
            raise HTTPException(status_code=400, detail="Client ID is required")
