import os
import sys
import shutil
from fastapi.testclient import TestClient

# Ensure parent directory is in the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from main import app

client = TestClient(app)

def test_reset():
    print("Resetting test environment (completely purging all existing documents)...")
    # Clean up all PDF files in uploaded_docs via our delete API
    if os.path.exists("uploaded_docs"):
        for filename in os.listdir("uploaded_docs"):
            if filename.endswith(".pdf"):
                print(f"Purging pre-existing document: {filename}")
                client.delete(f"/api/documents/{filename}")
                file_path = os.path.join("uploaded_docs", filename)
                if os.path.exists(file_path):
                    try:
                        os.remove(file_path)
                    except Exception:
                        pass
            
    print("[SUCCESS] Test environment fully reset!")
    print("-" * 50)

def test_root():
    print("Testing root endpoint '/'...")
    response = client.get("/")
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    data = response.json()
    assert data["status"] == "healthy", f"Expected status healthy, got {data}"
    print("[SUCCESS] Root endpoint verified successfully!")
    print(data)
    print("-" * 50)

def test_document_routes():
    print("Testing documents listing and upload...")
    
    # 1. List documents initially (should be 0 since we reset)
    response = client.get("/api/documents")
    assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text}"
    docs_before = response.json()
    print(f"Documents count before: {len(docs_before)}")
    assert len(docs_before) == 0, f"Expected 0 documents after reset, found {len(docs_before)}"

    # 2. Upload sample.pdf
    pdf_path = "sample.pdf"
    if not os.path.exists(pdf_path):
        print(f"[WARNING] {pdf_path} not found. Skipping upload test.")
        return

    print(f"Uploading and processing '{pdf_path}'...")
    with open(pdf_path, "rb") as f:
        response = client.post(
            "/api/documents/upload",
            files={"file": (pdf_path, f, "application/pdf")}
        )
    
    assert response.status_code == 201, f"Expected 201, got {response.status_code}: {response.text}"
    upload_data = response.json()
    assert upload_data["filename"] == "sample.pdf"
    assert upload_data["pages_processed"] > 0
    assert upload_data["chunks_created"] > 0
    print("[SUCCESS] Upload and processing verified successfully!")
    print(upload_data)

    # 3. List documents after upload (should be 1)
    response = client.get("/api/documents")
    assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text}"
    docs_after = response.json()
    print(f"Documents count after: {len(docs_after)}")
    assert len(docs_after) == 1, f"Expected 1 document, found {len(docs_after)}"
    assert any(doc["filename"] == "sample.pdf" for doc in docs_after), "Uploaded file not in list"
    print("[SUCCESS] Document list verified successfully!")
    print("-" * 50)

def test_chat_route():
    print("Testing chat /api/chat endpoint...")
    payload = {
        "message": "What is the primary methodology discussed in this research?",
        "history": [
            {"role": "user", "content": "Hi, I am interested in understanding the methodology."},
            {"role": "assistant", "content": "Sure, I can help you with that. Which paper or aspect are you asking about?"}
        ]
    }
    
    response = client.post("/api/chat", json=payload)
    assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text}"
    chat_data = response.json()
    
    assert "answer" in chat_data
    assert "standalone_query" in chat_data
    assert "citations" in chat_data
    
    print("[SUCCESS] Chat endpoint verified successfully!")
    print(f"Standalone Query: {chat_data['standalone_query']}")
    print(f"Citations: {chat_data['citations']}")
    print(f"Answer snippet: {chat_data['answer'][:200]}...")
    print("-" * 50)

def test_deletion_and_filtering():
    print("Testing document deletion and metadata-based filtering...")
    
    # 1. Create a clone.pdf locally
    shutil.copy("sample.pdf", "clone.pdf")
    assert os.path.exists("clone.pdf"), "Failed to create local clone.pdf"
    
    try:
        # 2. Upload clone.pdf
        print("Uploading clone.pdf...")
        with open("clone.pdf", "rb") as f:
            response = client.post(
                "/api/documents/upload",
                files={"file": ("clone.pdf", f, "application/pdf")}
            )
        assert response.status_code == 201, f"Expected 201 for clone upload, got {response.status_code}: {response.text}"
        print("[SUCCESS] clone.pdf uploaded and embedded successfully!")

        # 3. List documents to confirm both are present
        response = client.get("/api/documents")
        docs = response.json()
        filenames = [d["filename"] for d in docs]
        assert "sample.pdf" in filenames, "sample.pdf missing from list"
        assert "clone.pdf" in filenames, "clone.pdf missing from list"
        print(f"Current documents in inventory: {filenames}")

        # 4. Perform a filtered chat query scoped ONLY to sample.pdf
        print("Performing chat query filtered only to 'sample.pdf'...")
        payload = {
            "message": "What methodology was proposed in the paper?",
            "history": [],
            "filenames": ["sample.pdf"]
        }
        response = client.post("/api/chat", json=payload)
        assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text}"
        chat_data = response.json()
        print(f"Citations returned for filtered query: {chat_data['citations']}")
        
        # Verify that all cited files are strictly "sample.pdf"
        for citation in chat_data["citations"]:
            assert citation["filename"] == "sample.pdf", f"Unexpected citation of {citation['filename']} when query was filtered to sample.pdf"
        print("[SUCCESS] Scoped context filtering verified successfully!")

        # 5. Delete clone.pdf
        print("Deleting clone.pdf...")
        response = client.delete("/api/documents/clone.pdf")
        assert response.status_code == 200, f"Expected 200 on delete, got {response.status_code}: {response.text}"
        delete_data = response.json()
        assert delete_data["filename"] == "clone.pdf"
        print("[SUCCESS] Delete endpoint verified successfully!")

        # 6. Verify clone.pdf is deleted from directory
        response = client.get("/api/documents")
        docs_after = response.json()
        filenames_after = [d["filename"] for d in docs_after]
        assert "clone.pdf" not in filenames_after, "clone.pdf still present after deletion"
        print(f"Updated inventory post-deletion: {filenames_after}")
        print("[SUCCESS] Inventory cleanup verified successfully!")
        print("-" * 50)

    finally:
        # Cleanup local cloned copy if still here
        if os.path.exists("clone.pdf"):
            os.remove("clone.pdf")
            print("Cleaned up local clone.pdf file.")

if __name__ == "__main__":
    print("Running InsightAI API integration tests...\n")
    # Let exceptions propagate naturally to get full traceback and line numbers in logs!
    test_reset()
    test_root()
    test_document_routes()
    test_chat_route()
    test_deletion_and_filtering()
    print("[SUCCESS] ALL TESTS PASSED SUCCESSFULLY!")
