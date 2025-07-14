import asyncio
from typing import Dict, Any
from prometheus_client import Counter, Histogram, Gauge, generate_latest

class MetricsCollector:
    def __init__(self):
        # Initialize Prometheus metrics
        self.document_processed = Counter('documents_processed_total', 'Total documents processed')
        self.compliance_check = Counter('compliance_checks_total', 'Total compliance checks')
        self.risk_prediction = Counter('risk_predictions_total', 'Total risk predictions')
        self.chat_interaction = Counter('chat_interactions_total', 'Total chat interactions')
        
        self.processing_time = Histogram('processing_duration_seconds', 'Time to process requests')
        self.active_sessions = Gauge('active_onboarding_sessions', 'Currently active sessions')
        
        # Request metrics
        self.request_counter = Counter('http_requests_total', 'Total HTTP requests', ['method', 'endpoint', 'status_code'])
        self.request_duration = Histogram('http_request_duration_seconds', 'Request duration')

    def record_request(self, method: str, path: str, status_code: int, duration: float):
        """Record HTTP request metrics"""
        self.request_counter.labels(method=method, endpoint=path, status_code=str(status_code)).inc()
        self.request_duration.observe(duration)

    def get_metrics(self) -> str:
        """Get Prometheus metrics in text format"""
        return generate_latest()

    async def get_dashboard_data(self) -> Dict[str, Any]:
        """Get dashboard data for monitoring"""
        return {
            "documents_processed": self.document_processed._value.get(),
            "compliance_checks": self.compliance_check._value.get(),
            "risk_predictions": self.risk_prediction._value.get(),
            "chat_interactions": self.chat_interaction._value.get(),
            "active_sessions": self.active_sessions._value.get(),
            "avg_processing_time": self.get_avg_processing_time(),
            "success_rate": self.get_success_rate()
        }

    def get_avg_processing_time(self) -> float:
        """Calculate average processing time"""
        # This would typically be calculated from the histogram
        return 1.5  # placeholder

    def get_success_rate(self) -> float:
        """Calculate success rate"""
        # This would be calculated from request metrics
        return 0.99  # placeholder
