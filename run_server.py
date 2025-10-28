"""
Quick server runner for Academic Debate Council
"""
import subprocess
import sys

print("=" * 80)
print("Starting Academic Debate Council - Chainlit Server")
print("=" * 80)
print("\nServer will be available at: http://localhost:8000")
print("\nPress Ctrl+C to stop the server")
print("=" * 80)
print()

try:
    subprocess.run([sys.executable, "-m", "chainlit", "run", "chainlit_app.py", "--port", "8000"])
except KeyboardInterrupt:
    print("\n\nServer stopped by user.")
except Exception as e:
    print(f"\nError: {e}")
