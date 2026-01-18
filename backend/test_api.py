import requests
import json

BASE_URL = 'http://localhost:8000/api/v1'

def test_api():
    print("🧪 Testing RAG Chatbot API...s")
    
    # 1. Register user
    print("1️⃣  Registering user...")
    register_data = {
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'testpass123'
    }
    
    response = requests.post(f'{BASE_URL}/users/', json=register_data)
    if response.status_code == 201:
        print("✅ User registered successfully")
    else:
        print(f"❌ Registration failed: {response.text}")
        return
    
    # 2. Login
    print("Logging in...")
    login_data = {
        'username': 'testuser',
        'password': 'testpass123'
    }
    
    response = requests.post(f'{BASE_URL}/auth/login/', json=login_data)
    if response.status_code == 200:
        token = response.json()['token']
        print(f"✅ Login successful. Token: {token[:20]}...")
    else:
        print(f"❌ Login failed: {response.text}")
        return
    
    headers = {'Authorization': f'Token {token}'}
    
    # 3. Create collection
    print("Creating document collection...")
    collection_data = {
        'name': 'Test Collection',
        'description': 'My first RAG collection'
    }
    
    response = requests.post(
        f'{BASE_URL}/collections/',
        json=collection_data,
        headers=headers
    )
    
    if response.status_code == 201:
        collection = response.json()
        collection_id = collection['id']
        print(f"✅ Collection created: {collection_id}")
    else:
        print(f"❌ Collection creation failed: {response.text}")
        return
    
    # 4. Upload document (requires actual PDF file)
    print("Upload a PDF to test document upload")
    print(f"   POST {BASE_URL}/documents/")
    print(f"   Headers: Authorization: Token {token}")
    print(f"   Form-data: file=@your-file.pdf, collection={collection_id}")
    
    # 5. List collections
    print("Listing collections...")
    response = requests.get(f'{BASE_URL}/collections/', headers=headers)
    if response.status_code == 200:
        collections = response.json()
        print(f"✅ Found {collections['count']} collection(s)")
    
    # 6. Get user dashboard
    print("Getting user dashboard...")
    response = requests.get(f'{BASE_URL}/users/dashboard/', headers=headers)
    if response.status_code == 200:
        dashboard = response.json()
        print(f"✅ Dashboard data:")
        print(f"   User: {dashboard['user']['username']}")
        print(f"   Collections: {len(dashboard['recent_collections'])}")
    
    print("API test completed!")
    print("Full API documentation available at:")
    print(f"   {BASE_URL}/")

if __name__ == '__main__':
    test_api()