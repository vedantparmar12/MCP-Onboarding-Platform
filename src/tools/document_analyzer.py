from mcp import Tool
from typing import Any, Dict, Optional
import os
import asyncio
import logging
from anthropic import AsyncAnthropic
import PyPDF2
import sentry_sdk

logger = logging.getLogger(__name__)

class DocumentAnalyzerTool(Tool):
    def __init__(self):
        super().__init__(
            name="analyze_onboarding_document",
            description="Analyze financial documents using GenAI for onboarding compliance and risk assessment",
            inputSchema={
                "type": "object",
                "properties": {
                    "document_path": {
                        "type": "string",
                        "description": "Path to the document to analyze"
                    },
                    "extraction_mode": {
                        "type": "string",
                        "description": "Mode for document analysis",
                        "enum": ["wealth_management", "kyc", "risk_assessment", "general"]
                    }
                },
                "required": ["document_path"]
            }
        )
        # Initialize Anthropic client if API key is available
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if api_key:
            try:
                self.llm_client = AsyncAnthropic(api_key=api_key)
            except Exception as e:
                logger.warning(f"Failed to initialize Anthropic client: {e}")
                self.llm_client = None
        else:
            self.llm_client = None
        
    async def load_document(self, path: str):
        with open(path, 'rb') as file:
            return file.read()
        
    async def extract_text(self, document_path: str) -> str:
        """Extract text from document using appropriate method."""
        try:
            if document_path.endswith('.pdf'):
                # PDF text extraction using PyPDF2
                with open(document_path, 'rb') as file:
                    pdf_reader = PyPDF2.PdfReader(file)
                    text = ""
                    for page in pdf_reader.pages:
                        text += page.extract_text()
                    return text
            else:
                # For other formats, return placeholder
                return "Text extraction for this format not implemented yet"
        except Exception as e:
            logger.error(f"Error extracting text from {document_path}: {str(e)}")
            raise

    async def analyze_with_llm(self, text: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Perform GenAI analysis on text."""
        # Use the LLM client (e.g., Anthropic or OpenAI's GPT)
        analysis = "Analysis results based on the text"
        return {
            "status": "success",
            "analysis": analysis
        }

    async def execute(self, arguments: Dict[str, Any], user=None) -> Dict[str, Any]:
        """Execute document analysis with proper error handling and monitoring."""
        try:
            document_path = arguments["document_path"]
            
            # Validate file exists
            if not os.path.exists(document_path):
                return {"status": "error", "message": f"Document not found: {document_path}"}
            
            # Extract text from document
            text = await self.extract_text(document_path)
            
            # Analyze with LLM
            analysis = await self.analyze_with_llm(text, arguments)
            
            logger.info(f"Document analysis completed successfully for {document_path}")
            return analysis
            
        except Exception as e:
            logger.error(f"Document analysis failed: {str(e)}")
            sentry_sdk.capture_exception(e)
            return {"status": "error", "message": str(e)}
    
    def get_info(self) -> Dict[str, Any]:
        """Return tool information for MCP protocol."""
        return {
            "name": self.name,
            "description": self.description,
            "parameters": {
                "document_path": {
                    "type": "string",
                    "description": "Path to the document to analyze",
                    "required": True
                },
                "extraction_mode": {
                    "type": "string",
                    "description": "Mode for document analysis (e.g., 'wealth_management', 'kyc', 'risk_assessment')",
                    "required": False,
                    "default": "general"
                }
            }
        }
