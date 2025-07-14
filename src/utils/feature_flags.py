import hashlib
from typing import Dict, Any

class FeatureFlags:
    def __init__(self):
        self.flags = {
            "genai_analysis": 1.0,  # 100% enabled
            "multi_agent_system": 0.1,  # 10% gradual rollout
            "conversational_ui": 0.5,  # 50% of users
            "batch_processing": 0.2,  # 20% of users
            "advanced_risk_scoring": 0.05,  # 5% beta testing
            "real_time_compliance": 0.3,  # 30% of users
        }
    
    def is_enabled(self, feature: str, user_id: str) -> bool:
        """Check if feature is enabled for a specific user"""
        if feature not in self.flags:
            return False
        
        # Get the rollout percentage for this feature
        rollout_percentage = self.flags[feature]
        
        # If 100% rollout, always enabled
        if rollout_percentage >= 1.0:
            return True
        
        # If 0% rollout, always disabled
        if rollout_percentage <= 0.0:
            return False
        
        # Use consistent hashing for gradual rollout
        hash_value = self._hash_user_feature(user_id, feature)
        return hash_value < rollout_percentage
    
    def _hash_user_feature(self, user_id: str, feature: str) -> float:
        """Generate consistent hash for user+feature combination"""
        combined = f"{user_id}:{feature}"
        hash_bytes = hashlib.md5(combined.encode()).digest()
        hash_int = int.from_bytes(hash_bytes[:4], byteorder='big')
        return hash_int / (2**32)  # Normalize to 0-1 range
    
    def update_flag(self, feature: str, percentage: float) -> bool:
        """Update feature flag percentage"""
        if 0.0 <= percentage <= 1.0:
            self.flags[feature] = percentage
            return True
        return False
    
    def get_all_flags(self) -> Dict[str, float]:
        """Get all feature flags"""
        return self.flags.copy()
    
    def get_user_flags(self, user_id: str) -> Dict[str, bool]:
        """Get all flags for a specific user"""
        return {
            feature: self.is_enabled(feature, user_id)
            for feature in self.flags
        }
