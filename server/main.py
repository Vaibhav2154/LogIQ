from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
from datetime import datetime
from core import Config, logger
from model import HealthCheck, ErrorResponse, DatabaseStats
from routers import auth, users



@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application lifespan - startup and shutdown events."""
    logger.info("Starting ForensIQ API server...")
    # Place startup initialization here (DB connections, clients, etc.)
    try:
        # yield control back to FastAPI so the app can start
        yield
    finally:
        # cleanup / shutdown tasks
        logger.info("Shutting down ForensIQ API server...")

app = FastAPI(
    title="ForensIQ - MITRE ATT&CK Log Analysis API",
    description="AI-powered system log analysis with MITRE ATT&CK technique matching using Gemini AI and ChromaDB RAG",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*","localhost:3000"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(users.router)

@app.get("/", response_model=dict)
async def root():
    """Root endpoint with API information."""
    return {
        "message": "ForensIQ - MITRE ATT&CK Log Analysis API",
        "version": "1.0.0",
        "description": "AI-powered system log analysis with MITRE ATT&CK technique matching",
        "docs": "/docs",
        "health": "/health",
        "timestamp": datetime.utcnow().isoformat()
    }

@app.get("/health", response_model=HealthCheck)
async def health_check():
    """Health check endpoint to verify all services are running."""
    try:
        services_status = {}
        # Check Gemini service
        if gemini_service:
            services_status["gemini_ai"] = "healthy"
        else:
            services_status["gemini_ai"] = "not_initialized"
            
        # Check AWS Bedrock service
        if aws_bedrock_service:
            services_status["aws_bedrock"] = "healthy"
        else:
            services_status["aws_bedrock"] = "not_initialized"
        if chromadb_service:
            try:
                stats = await chromadb_service.get_collection_stats()
                if "error" in stats:
                    services_status["chromadb"] = f"error: {stats['error']}"
                else:
                    services_status["chromadb"] = "healthy"
                    db_stats = DatabaseStats(
                        total_techniques=stats.get('total_techniques', 0),
                        collection_name=stats.get('collection_name', 'unknown'),
                        embedding_model=stats.get('embedding_model', 'unknown')
                    )
            except Exception as e:
                services_status["chromadb"] = f"error: {str(e)}"
                db_stats = None
        else:
            services_status["chromadb"] = "not_initialized"
            db_stats = None
        # Determine overall status
        overall_status = "healthy" if all(
            status == "healthy" for status in services_status.values()
        ) else "degraded"
        return HealthCheck(
            status=overall_status,
            services=services_status,
            database_stats=db_stats
        )
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        return HealthCheck(
            status="unhealthy",
            services={"error": str(e)}
        )

@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler for unhandled errors."""
    logger.error(f"Unhandled exception: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content=ErrorResponse(
            error="Internal server error",
            detail=str(exc)
        ).dict()
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=Config.HOST,
        port=Config.PORT,
        log_level=Config.LOG_LEVEL.lower()
    )