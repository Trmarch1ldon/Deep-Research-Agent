#!/usr/bin/env python3
"""
Troubleshooting script for OpenAI API connection issues
"""

import os
import asyncio
import httpx
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

async def test_connection():
    """Test various connection scenarios"""
    
    print("🔍 OpenAI Connection Troubleshooting")
    print("=" * 50)
    
    # 1. Check environment variables
    print("\n1. Environment Variables:")
    api_key = os.getenv("OPENAI_API_KEY")
    if api_key:
        print(f"   ✅ OPENAI_API_KEY found (ending in: ...{api_key[-4:]})")
    else:
        print("   ❌ OPENAI_API_KEY not found")
        return
    
    # 2. Test basic internet connectivity
    print("\n2. Internet Connectivity:")
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get("https://httpbin.org/get")
            if response.status_code == 200:
                print("   ✅ Basic internet connection working")
            else:
                print(f"   ❌ Internet test failed: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Internet connection failed: {e}")
        return
    
    # 3. Test OpenAI API endpoint
    print("\n3. OpenAI API Connectivity:")
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            }
            # Simple API test
            response = await client.get(
                "https://api.openai.com/v1/models",
                headers=headers
            )
            if response.status_code == 200:
                print("   ✅ OpenAI API connection successful")
                models = response.json()
                print(f"   📊 Available models: {len(models.get('data', []))}")
            else:
                print(f"   ❌ OpenAI API test failed: {response.status_code}")
                print(f"   Response: {response.text}")
    except httpx.ConnectError as e:
        print(f"   ❌ Connection error to OpenAI API: {e}")
        print("   💡 This suggests a network/firewall issue")
    except httpx.TimeoutException as e:
        print(f"   ❌ Timeout connecting to OpenAI API: {e}")
        print("   💡 Try increasing timeout or check network speed")
    except Exception as e:
        print(f"   ❌ OpenAI API test failed: {e}")
    
    # 4. Test with different timeout settings
    print("\n4. Testing with extended timeout:")
    try:
        from openai import AsyncOpenAI
        
        client = AsyncOpenAI(
            api_key=api_key,
            timeout=httpx.Timeout(60.0, connect=30.0)  # Extended timeouts
        )
        
        # Simple completion test
        response = await client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": "Hello"}],
            max_tokens=10
        )
        print("   ✅ OpenAI client with extended timeout successful")
        
    except Exception as e:
        print(f"   ❌ Extended timeout test failed: {e}")
    
    # 5. Suggestions
    print("\n💡 Troubleshooting Suggestions:")
    print("   • Check your internet connection and firewall settings")
    print("   • Verify your OpenAI API key is valid and has credits")
    print("   • Try running: uv sync --reinstall-package openai")
    print("   • Consider using a VPN if in a restricted region")
    print("   • Check OpenAI status: https://status.openai.com/")

if __name__ == "__main__":
    asyncio.run(test_connection()) 