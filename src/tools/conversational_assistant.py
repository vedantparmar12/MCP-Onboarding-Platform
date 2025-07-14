from mcp import Tool
from typing import Any, Dict
import logging
import os
import sentry_sdk

logger = logging.getLogger(__name__)

class ConversationalOnboardingTool(Tool):
    def __init__(self):
        super().__init__(
            name="conversational_onboarding",
            description="Conversational assistant for onboarding using GenAI",
            inputSchema={
                "type": "object",
                "properties": {
                    "input_query": {
                        "type": "string",
                        "description": "User input query for conversational assistance"
                    }
                },
                "required": ["input_query"]
            }
        )

    async def execute(self, arguments: Dict[str, Any], user=None) -> Dict[str, Any]:
        """Execute conversational assistance with error handling."""
        try:
            input_query = arguments.get("input_query", "")

            if not input_query:
                return {"status": "error", "message": "No input query provided"}

            # Example GenAI response (stubbed)
            response = "Sample conversational response using GenAI"

            logger.info(f"Conversational response generated for query: {input_query}")
            return {
                "status": "success",
                "response": response
            }

        except Exception as e:
            logger.error(f"Conversational assistance failed: {str(e)}")
            sentry_sdk.capture_exception(e)
            return {"status": "error", "message": str(e)}

    def get_info(self) -> Dict[str, Any]:
        """Return tool information for MCP protocol."""
        return {
            "name": self.name,
            "description": self.description,
            "parameters": {
                "input_query": {
                    "type": "string",
                    "description": "User input query for conversational assistance",
                    "required": True
                }
            }
        }
