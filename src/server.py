"""
Onboarding Intelligence Hub - Main MCP Server
Production-ready server for financial services onboarding automation
"""

import os
import asyncio
import logging
from typing import Dict, Any, List, Optional
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Depends, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import sentry_sdk
from sentry_sdk.integrations.fastapi import FastApiIntegration
from sentry_sdk.integrations.sqlalchemy import SqlalchemyIntegration

from .tools.document_analyzer import DocumentAnalyzerTool
from .tools.compliance_validator import ComplianceValidatorTool
from .tools.risk_predictor import RiskPredictorTool
from .tools.conversational_assistant import ConversationalOnboardingTool
from .security.auth_manager import AuthManager
from .security.input_validator import InputValidator
from .monitoring.metrics import MetricsCollector
from .utils.cache import CacheManager
from .utils.database import DatabaseManager
from .utils.feature_flags import FeatureFlags
from .agents.multi_agent_system import MultiAgentSystem

# Initialize logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Sentry for error tracking
if os.getenv("SENTRY_DSN"):
    sentry_sdk.init(
        dsn=os.getenv("SENTRY_DSN"),
        integrations=[
            FastApiIntegration(auto_enabling=True),
            SqlalchemyIntegration(),
        ],
        traces_sample_rate=1.0,
        environment=os.getenv("NODE_ENV", "development"),
    )

class OnboardingMCPServer:
    """Main MCP Server for Onboarding Intelligence Hub"""
    
    def __init__(self):
        self.app = FastAPI(
            title="Onboarding Intelligence Hub",
            description="AI-powered financial services onboarding automation",
            version="1.0.0",
            docs_url="/docs",
            redoc_url="/redoc"
        )
        
        # Initialize core components
        self.auth_manager = AuthManager()
        self.input_validator = InputValidator()
        self.metrics = MetricsCollector()
        self.cache = CacheManager()
        self.db = DatabaseManager()
        self.feature_flags = FeatureFlags()
        self.multi_agent_system = MultiAgentSystem()
        
        # Initialize tools
        self.tools = {
            "document_analyzer": DocumentAnalyzerTool(),
            "compliance_validator": ComplianceValidatorTool(),
            "risk_predictor": RiskPredictorTool(),
            "conversational_assistant": ConversationalOnboardingTool(),
        }
        
        self.setup_middleware()
        self.setup_routes()
        
    def setup_middleware(self):
        """Setup FastAPI middleware"""
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],  # Configure for production
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
        
        # Add metrics middleware
        @self.app.middleware("http")
        async def metrics_middleware(request, call_next):
            start_time = asyncio.get_event_loop().time()
            response = await call_next(request)
            process_time = asyncio.get_event_loop().time() - start_time
            
            self.metrics.record_request(
                method=request.method,
                path=request.url.path,
                status_code=response.status_code,
                duration=process_time
            )
            
            return response
    
    def setup_routes(self):
        """Setup API routes"""
        
        @self.app.get("/health")
        async def health_check():
            """Health check endpoint"""
            return {
                "status": "healthy",
                "version": "1.0.0",
                "timestamp": asyncio.get_event_loop().time()
            }
        
        @self.app.post("/mcp/tools/analyze_document")
        async def analyze_document(
            request: Dict[str, Any],
            background_tasks: BackgroundTasks,
            auth: HTTPAuthorizationCredentials = Depends(HTTPBearer())
        ):
            """Analyze onboarding documents using GenAI"""
            try:
                # Authenticate user
                user = await self.auth_manager.authenticate(auth.credentials)
                
                # Validate input
                self.input_validator.validate_document_analysis_request(request)
                
                # Check feature flag
                if not self.feature_flags.is_enabled("genai_analysis", user.id):
                    raise HTTPException(status_code=403, detail="Feature not enabled")
                
                # Process with caching
                cache_key = f"doc_analysis:{hash(str(request))}"
                result = await self.cache.get_or_compute(
                    cache_key,
                    lambda: self.tools["document_analyzer"].execute(request, user),
                    ttl=3600
                )
                
                # Record metrics
                self.metrics.document_processed.inc()
                
                return result
                
            except Exception as e:
                logger.error(f"Document analysis failed: {str(e)}")
                sentry_sdk.capture_exception(e)
                raise HTTPException(status_code=500, detail="Analysis failed")
        
        @self.app.post("/mcp/tools/validate_compliance")
        async def validate_compliance(
            request: Dict[str, Any],
            auth: HTTPAuthorizationCredentials = Depends(HTTPBearer())
        ):
            """Validate regulatory compliance"""
            try:
                user = await self.auth_manager.authenticate(auth.credentials)
                self.input_validator.validate_compliance_request(request)
                
                result = await self.tools["compliance_validator"].execute(request, user)
                
                self.metrics.compliance_check.inc()
                return result
                
            except Exception as e:
                logger.error(f"Compliance validation failed: {str(e)}")
                sentry_sdk.capture_exception(e)
                raise HTTPException(status_code=500, detail="Validation failed")
        
        @self.app.post("/mcp/tools/predict_risk")
        async def predict_risk(
            request: Dict[str, Any],
            auth: HTTPAuthorizationCredentials = Depends(HTTPBearer())
        ):
            """Predict onboarding risk using ML and GenAI"""
            try:
                user = await self.auth_manager.authenticate(auth.credentials)
                self.input_validator.validate_risk_prediction_request(request)
                
                # Use multi-agent system for comprehensive analysis
                if self.feature_flags.is_enabled("multi_agent_system", user.id):
                    result = await self.multi_agent_system.analyze_risk(request, user)
                else:
                    result = await self.tools["risk_predictor"].execute(request, user)
                
                self.metrics.risk_prediction.inc()
                return result
                
            except Exception as e:
                logger.error(f"Risk prediction failed: {str(e)}")
                sentry_sdk.capture_exception(e)
                raise HTTPException(status_code=500, detail="Prediction failed")
        
        @self.app.post("/mcp/tools/chat")
        async def conversational_interface(
            request: Dict[str, Any],
            auth: HTTPAuthorizationCredentials = Depends(HTTPBearer())
        ):
            """Conversational onboarding assistant"""
            try:
                user = await self.auth_manager.authenticate(auth.credentials)
                
                if not self.feature_flags.is_enabled("conversational_ui", user.id):
                    raise HTTPException(status_code=403, detail="Feature not enabled")
                
                self.input_validator.validate_chat_request(request)
                
                result = await self.tools["conversational_assistant"].execute(request, user)
                
                self.metrics.chat_interaction.inc()
                return result
                
            except Exception as e:
                logger.error(f"Chat interaction failed: {str(e)}")
                sentry_sdk.capture_exception(e)
                raise HTTPException(status_code=500, detail="Chat failed")
        
        @self.app.get("/mcp/tools")
        async def list_tools(
            auth: HTTPAuthorizationCredentials = Depends(HTTPBearer())
        ):
            """List available MCP tools"""
            try:
                user = await self.auth_manager.authenticate(auth.credentials)
                
                tools_info = []
                for tool_name, tool in self.tools.items():
                    if hasattr(tool, 'get_info'):
                        tools_info.append({
                            "name": tool_name,
                            "description": tool.get_info().get("description", ""),
                            "parameters": tool.get_info().get("parameters", {}),
                            "enabled": self.feature_flags.is_enabled(tool_name, user.id)
                        })
                
                return {"tools": tools_info}
                
            except Exception as e:
                logger.error(f"Failed to list tools: {str(e)}")
                raise HTTPException(status_code=500, detail="Failed to list tools")
        
        @self.app.get("/metrics")
        async def get_metrics():
            """Prometheus metrics endpoint"""
            return self.metrics.get_metrics()
        
        @self.app.get("/dashboard")
        async def get_dashboard():
            """Real-time monitoring dashboard"""
            return await self.metrics.get_dashboard_data()

# Global server instance
server = OnboardingMCPServer()
app = server.app

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "src.server:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
