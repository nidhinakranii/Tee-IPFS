# simple_agent.py
import requests

def run(user_data: bytes) -> bytes:
    """
    This function is run inside the TEE.
    It receives user_data (expected to be an IPFS CID in bytes),
    fetches the content from IPFS, transforms it (e.g., uppercase),
    and returns the result as bytes.
    """
    try:
        cid = user_data.decode("utf-8")
        url = f"https://ipfs.io/ipfs/{cid}"
        response = requests.get(url)
        response.raise_for_status()
        content = response.text.strip()
        print("Fetched from IPFS:", content)
        result = content.upper()
        return result.encode("utf-8")
    except Exception as e:
        return f"Error in agent: {str(e)}".encode("utf-8")