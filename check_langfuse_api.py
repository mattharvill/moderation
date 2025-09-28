#!/usr/bin/env python3
"""
Check available Langfuse API methods
"""
import os
from dotenv import load_dotenv
from langfuse import Langfuse

load_dotenv()

langfuse = Langfuse(
    public_key=os.getenv("LANGFUSE_PUBLIC_KEY"),
    secret_key=os.getenv("LANGFUSE_SECRET_KEY"),
    host=os.getenv("LANGFUSE_HOST")
)

print("Available methods in Langfuse client:")
methods = [method for method in dir(langfuse) if not method.startswith('_')]
for method in sorted(methods):
    print(f"  - {method}")