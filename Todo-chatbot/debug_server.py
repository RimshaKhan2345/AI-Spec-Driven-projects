import sys
import os
import traceback
from main import app
import uvicorn

def run_server_with_error_handling():
    try:
        # Enable debug mode to get more detailed error messages
        uvicorn.run(app, host="127.0.0.1", port=5001, reload=False, debug=True, log_level="info")
    except Exception as e:
        print(f"Error starting server: {e}")
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    run_server_with_error_handling()