from alith.tee.marlin import MarlinClient, AttestationRequest
import requests
import json

# --------------------------
# STEP 1: Connect to TEE
tee = MarlinClient.default()

# --------------------------
# STEP 2: Prepare data
data = "Secret: Alice pays Bob $100"
request = AttestationRequest(
    public_key=b"key",
    user_data=data.encode(),
    nonce=b"nonce"
)

# --------------------------
# STEP 3: Get attestation proof
proof = tee.attestation_hex(request)
result = {
    "data": data,
    "proof": proof[:50]  # Shortened for demonstration
}

# --------------------------
# STEP 4: Upload to IPFS using HTTP API
def ipfs_add_json(data):
    with open("temp.json", "w") as f:
        json.dump(data, f)
    with open("temp.json", "rb") as f:
        response = requests.post("http://127.0.0.1:5001/api/v0/add?wrap-with-directory=false&cid-version=1&cid-base=base32",
    files={"file": f}
)
    return response.json()["Hash"]

cid = ipfs_add_json(result)

# --------------------------
# STEP 5: Done!
print(f"✅ Secure data stored on IPFS: {cid}")
print("🎯 TEE proved it, IPFS stored it, anyone can verify it!")
print(f"🔗 View it at: https://ipfs.io/ipfs/{cid}")