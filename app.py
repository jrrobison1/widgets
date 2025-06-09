"""Application entry point"""

import os
from src.widgets.main import app

if __name__ == "__main__":
    import uvicorn
    # Use environment variable for host, default to localhost for security
    host = os.getenv("HOST", "127.0.0.1")
    port = int(os.getenv("PORT", "8000"))
    uvicorn.run(app, host=host, port=port) 