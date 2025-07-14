import pytest
import os
import tempfile
from src.tools.document_analyzer import DocumentAnalyzerTool

@pytest.mark.asyncio
async def test_document_analysis():
    analyzer = DocumentAnalyzerTool()
    
    # Create a temporary file to test with
    with tempfile.NamedTemporaryFile(suffix='.txt', delete=False) as temp_file:
        temp_file.write(b"Sample document content for testing")
        temp_file_path = temp_file.name
    
    try:
        result = await analyzer.execute({
            "document_path": temp_file_path,
            "extraction_mode": "wealth_management"
        })
        
        assert result["status"] == "success"
        assert "analysis" in result
        assert result["analysis"] is not None
    finally:
        # Clean up the temporary file
        os.unlink(temp_file_path)

@pytest.mark.asyncio
async def test_document_analysis_file_not_found():
    analyzer = DocumentAnalyzerTool()
    
    result = await analyzer.execute({
        "document_path": "nonexistent_file.pdf",
        "extraction_mode": "wealth_management"
    })
    
    assert result["status"] == "error"
    assert "Document not found" in result["message"]
