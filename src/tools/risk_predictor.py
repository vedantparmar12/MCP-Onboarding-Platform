from mcp import Tool
from typing import Any, Dict, List
import joblib
import logging
import os
from sklearn.ensemble import RandomForestClassifier
import sentry_sdk

logger = logging.getLogger(__name__)

class RiskPredictorTool(Tool):
    def __init__(self):
        super().__init__(
            name="predict_risk",
            description="Predict financial risk based on client data",
            inputSchema={
                "type": "object",
                "properties": {
                    "client_profile": {
                        "type": "object",
                        "description": "Client profile data for risk assessment"
                    }
                },
                "required": ["client_profile"]
            }
        )
        self.model = self.load_or_train_model()
        self.feature_extractor = FeatureExtractor()
    
    def load_or_train_model(self) -> RandomForestClassifier:
        try:
            model = joblib.load('models/risk_model.pkl')
        except FileNotFoundError:
            model = RandomForestClassifier()
            # Train the model with historical data (example)
            logger.info("Training new RandomForest model.")
            # Create models directory if it doesn't exist
            os.makedirs('models', exist_ok=True)
            try:
                joblib.dump(model, 'models/risk_model.pkl')
            except Exception as e:
                logger.warning(f"Failed to save model: {e}")
        return model
    
    async def execute(self, arguments: Dict[str, Any], user=None) -> Dict[str, Any]:
        """Execute risk prediction with proper error handling."""
        try:
            client_profile = arguments.get("client_profile", {})
            
            if not client_profile:
                return {"status": "error", "message": "No client profile data provided"}
            
            features = self.feature_extractor.extract(client_profile)
            ml_risk_score = self.model.predict_proba([features])[0][1]
            genai_insights = await self.get_genai_risk_insights(client_profile)
            
            logger.info(f"Risk prediction completed successfully for profile: {client_profile}")
            return {
                "status": "success",
                "risk_score": ml_risk_score,
                "risk_level": self.categorize_risk(ml_risk_score),
                "genai_insights": genai_insights
            }
            
        except Exception as e:
            logger.error(f"Risk prediction failed: {str(e)}")
            sentry_sdk.capture_exception(e)
            return {"status": "error", "message": str(e)}

    async def get_genai_risk_insights(self, client_profile: Dict) -> Dict[str, Any]:
        # Call an LLM to enhance risk insights
        insights = "Insights based on GenAI analysis"
        return insights

    def categorize_risk(self, risk_score: float) -> str:
        # Classify risk level based on score
        if risk_score < 0.3:
            return "low"
        elif risk_score < 0.7:
            return "medium"
        else:
            return "high"

class FeatureExtractor:
    def extract(self, client_profile: Dict) -> List[float]:
        # Feature extraction logic for model
        return []  # Return list of extracted features
