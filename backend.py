from flask import Flask, request, jsonify, render_template
import xrpl
from xrpl.wallet import generate_faucet_wallet
from xrpl.models.transactions import Payment
from xrpl.transaction import autofill_and_sign, submit_and_wait
from xrpl.utils import xrp_to_drops
import json

# -----------------------
# XRPL TESTNET SETUP
# -----------------------
testnet_url = "https://s.altnet.rippletest.net:51234"
client = xrpl.clients.JsonRpcClient(testnet_url)

# Generate wallet
print("Getting a new account from the Testnet faucet...")
wallet = generate_faucet_wallet(client, debug=True)

SENDER_ADDRESS = wallet.classic_address
SENDER_SEED = wallet.seed
print(f"Sender Wallet Address: {SENDER_ADDRESS}")
print(f"Sender Wallet Seed: {SENDER_SEED}")

# Default destination
DEFAULT_DESTINATION = "rhZCMADKX5TN7tT6R7WGdRxKXZysxA6Xpa"

# -----------------------
# FLASK BACKEND
# -----------------------
backend = Flask(__name__)

# Detect QR type
QR_TYPES = {
    "NETS": "NETS",
    "PAYNOW": "PAYNOW",
    "PAYLAH": "PAYLAH",
    "WECHAT": "WECHAT",
    "ALIPAY": "ALIPAY",
}

def detect_qr_type(qr_data: str) -> str:
    qr_data = qr_data.strip().upper()
    for keyword, qr_type in QR_TYPES.items():
        if keyword in qr_data:
            return qr_type
    return "UNKNOWN"

# Send XRP function
def send_xrpl_payment(amount_xrp: float, destination: str = DEFAULT_DESTINATION) -> str:
    # Prepare transaction
    payment = Payment(
        account=wallet.classic_address,
        amount=xrp_to_drops(amount_xrp),
        destination=destination,
    )
    print("Payment object:", payment)

    # Sign transaction
    signed_tx = autofill_and_sign(payment, client, wallet)
    tx_id = signed_tx.get_hash()
    print(f"Signed transaction hash: {tx_id}")

    # Submit transaction
    try:
        tx_response = submit_and_wait(signed_tx, client)
    except xrpl.transaction.XRPLReliableSubmissionException as e:
        raise Exception(f"Submit failed: {e}")

    # Check transaction results
    print(json.dumps(tx_response.result, indent=4, sort_keys=True))
    return tx_id

# -----------------------
# Routes
# -----------------------

# API endpoint for payments
@backend.route("/pay", methods=["POST"])
def pay():
    data = request.json
    qr_data = data.get("qr", "")
    amount = float(data.get("amount", 1))
    destination = data.get("destination", DEFAULT_DESTINATION)

    qr_type = detect_qr_type(qr_data)
    tx_hash = send_xrpl_payment(amount_xrp=amount, destination=destination)

    return jsonify({
        "status": "success",
        "qr_type": qr_type,
        "xrpl_tx_hash": tx_hash,
        "amount_xrp": amount,
        "destination": destination,
        "message": f"Payment of {amount} XRP sent on XRPL Testnet",
        "explorer_link": f"https://testnet.xrpl.org/transactions/{tx_hash}"
    })

# -----------------------
if __name__ == "__main__":
    backend.run(debug=True)
