"""Main application module for {project_name}."""

from fastapi import FastAPI

app = FastAPI(title="{project_name}", description="{project_description}")

@app.get("/")
async def root():
    """Root endpoint."""
    return {"message": "Welcome to {project_name}!"}

@app.get("/health")
async def health():
    """Health check endpoint."""
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
