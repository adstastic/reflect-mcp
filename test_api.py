#!/usr/bin/env python3
"""Test script to verify all Reflect API endpoints."""

import asyncio
import httpx
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

ACCESS_TOKEN = os.getenv("REFLECT_ACCESS_TOKEN")
BASE_URL = "https://reflect.app/api"

if not ACCESS_TOKEN:
    print("Error: REFLECT_ACCESS_TOKEN environment variable not set")
    exit(1)

async def test_api():
    headers = {"Authorization": f"Bearer {ACCESS_TOKEN}"}
    
    async with httpx.AsyncClient() as client:
        # Test 1: List graphs
        print("1. Testing GET /graphs...")
        response = await client.get(f"{BASE_URL}/graphs", headers=headers)
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.json()}")
        print()
        
        if response.status_code == 200:
            graphs = response.json()
            if graphs and len(graphs) > 0:
                graph_id = graphs[0]["id"]
                print(f"   Using graph_id: {graph_id}")
                print()
                
                # Test 2: Get current user
                print("2. Testing GET /users/me...")
                response = await client.get(f"{BASE_URL}/users/me", headers=headers)
                print(f"   Status: {response.status_code}")
                print(f"   Response: {response.json()}")
                print()
                
                # Test 3: List books
                print(f"3. Testing GET /graphs/{graph_id}/books...")
                response = await client.get(f"{BASE_URL}/graphs/{graph_id}/books", headers=headers)
                print(f"   Status: {response.status_code}")
                print(f"   Response: {response.json()}")
                print()
                
                # Test 4: List links
                print(f"4. Testing GET /graphs/{graph_id}/links...")
                response = await client.get(f"{BASE_URL}/graphs/{graph_id}/links", headers=headers)
                print(f"   Status: {response.status_code}")
                links = response.json()
                print(f"   Response: {links[:2] if len(links) > 2 else links}")  # Show first 2
                print(f"   Total links: {len(links)}")
                print()
                
                # Test 5: Create a test note
                print(f"5. Testing POST /graphs/{graph_id}/notes...")
                note_data = {
                    "subject": f"Test Note - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
                    "content_markdown": "This is a test note created by the MCP server test script.\n\n## Test Section\n\n- Item 1\n- Item 2",
                    "pinned": False
                }
                response = await client.post(f"{BASE_URL}/graphs/{graph_id}/notes", headers=headers, json=note_data)
                print(f"   Status: {response.status_code}")
                print(f"   Response: {response.json()}")
                print()
                
                # Test 6: Append to daily note
                print(f"6. Testing PUT /graphs/{graph_id}/daily-notes...")
                append_data = {
                    "text": f"- Test entry from MCP server at {datetime.now().strftime('%H:%M')}",
                    "transform_type": "list-append",
                    "date": datetime.now().strftime('%Y-%m-%d')
                }
                response = await client.put(f"{BASE_URL}/graphs/{graph_id}/daily-notes", headers=headers, json=append_data)
                print(f"   Status: {response.status_code}")
                print(f"   Response: {response.json()}")
                print()
                
                # Test 7: Create a test link
                print(f"7. Testing POST /graphs/{graph_id}/links...")
                link_data = {
                    "url": "https://example.com/test",
                    "title": "Test Link from MCP Server",
                    "description": "This is a test link created to verify the API",
                    "highlights": ["Test highlight 1", "Test highlight 2"]
                }
                response = await client.post(f"{BASE_URL}/graphs/{graph_id}/links", headers=headers, json=link_data)
                print(f"   Status: {response.status_code}")
                print(f"   Response: {response.json()}")
                print()

if __name__ == "__main__":
    asyncio.run(test_api())