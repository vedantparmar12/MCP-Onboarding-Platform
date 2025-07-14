from mcp import Tool
from typing import Any, Dict, List
import logging
import sentry_sdk

logger = logging.getLogger(__name__)

class ComplianceValidatorTool(Tool):
    def __init__(self):
        super().__init__(
            name="validate_compliance",
            description="Validate regulatory compliance using preset frameworks for financial services onboarding",
            inputSchema={
                "type": "object",
                "properties": {
                    "jurisdictions": {
                        "type": "array",
                        "items": {
                            "type": "string",
                            "enum": ["MAS", "HKMA", "SEC"]
                        },
                        "description": "List of jurisdictions to validate against"
                    },
                    "client_data": {
                        "type": "object",
                        "description": "Client data to validate"
                    }
                },
                "required": ["jurisdictions", "client_data"]
            }
        )
        self.frameworks = {
            "MAS": MASComplianceChecker(),
            "HKMA": HKMAComplianceChecker(),
            "SEC": SECComplianceChecker()
        }

    async def execute(self, arguments: Dict[str, Any], user=None) -> Dict[str, Any]:
        """Execute compliance validation with proper error handling."""
        try:
            jurisdictions = arguments.get("jurisdictions", [])
            client_data = arguments.get("client_data", {})
            
            if not jurisdictions:
                return {"status": "error", "message": "No jurisdictions specified"}
            
            results = []
            for jurisdiction in jurisdictions:
                checker = self.frameworks.get(jurisdiction)
                if checker:
                    result = await checker.check(client_data)
                    results.append(result)
                else:
                    logger.warning(f"Unsupported jurisdiction: {jurisdiction}")
            
            consolidated_result = self.consolidate_results(results)
            
            logger.info(f"Compliance validation completed for jurisdictions: {jurisdictions}")
            return {"status": "success", "results": consolidated_result}
            
        except Exception as e:
            logger.error(f"Compliance validation failed: {str(e)}")
            sentry_sdk.capture_exception(e)
            return {"status": "error", "message": str(e)}

    def consolidate_results(self, results: List[Dict]) -> Dict[str, Any]:
        # Consolidate results from various checkers
        consolidated = {}
        for result in results:
            consolidated.update(result)
        return consolidated

class MASComplianceChecker:
    async def check(self, client_data: Dict) -> Dict[str, Any]:
        # Logic for MAS compliance check
        return {"MAS": "compliant"}

class HKMAComplianceChecker:
    async def check(self, client_data: Dict) -> Dict[str, Any]:
        # Logic for HKMA compliance check
        return {"HKMA": "compliant"}

class SECComplianceChecker:
    async def check(self, client_data: Dict) -> Dict[str, Any]:
        # Logic for SEC compliance check
        return {"SEC": "compliant"}
