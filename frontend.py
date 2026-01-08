import streamlit as st
import requests

BACKEND_PAY_URL = "http://127.0.0.1:5000/pay"

st.set_page_config(page_title="OneQR (Demo)", page_icon="💳", layout="centered")

st.title("💳 OneQR (Demo)")

# -----------------------
# 1) Get QR text (upload OR paste)
# -----------------------
qr_text = ""

tab_paste, tab_scan, tab_upload = st.tabs(["Paste QR Text", "Scan QR", "Upload QR Image"])

with tab_paste:
    pasted = st.text_area("Paste QR Payload (Text Inside QR)", value="PAYNOW123", height=120)
    if pasted.strip():
        qr_text = pasted.strip()

with tab_scan:
    st.info("The Scan tab is a work in progress. For now, please use the Paste tab instead.")

with tab_upload:
    st.info("The Upload tab is a work in progress. For now, please use the Paste tab instead.")
    uploaded = st.file_uploader("Upload QR image (PNG/JPG/JPEG)", type=["png", "jpg", "jpeg"])
    if uploaded is not None:
        try:
            from PIL import Image
            from pyzbar.pyzbar import decode

            img = Image.open(uploaded)
            st.image(img, caption="Uploaded QR", use_container_width=True)

            decoded = decode(img)
            if not decoded:
                st.error("No QR detected. Try a clearer/larger QR image.")
            else:
                qr_text = decoded[0].data.decode("utf-8", errors="ignore")
                st.success("QR detected ✅")
                st.code(qr_text, language="text")

        except Exception as e:
            st.error("QR decoding not available. Use the Paste tab instead.")
            st.caption(
                "If you want upload decoding: install zbar + pyzbar.\n"
                "macOS: `brew install zbar` then `python -m pip install pillow pyzbar`"
            )
            st.caption(str(e))

# -----------------------
# 2) Amount input
# -----------------------
st.subheader("Amount")
amount = st.number_input("Amount (XRP for Demo)", min_value=0.1, value=5.0, step=0.1)

# -----------------------
# 3) Pay button → call backend
# -----------------------
st.subheader("Pay")
pay_disabled = (not qr_text) or (amount <= 0)

if st.button("✅ Pay", disabled=pay_disabled):
    payload = {"qr": qr_text, "amount": float(amount)}  # ONLY {qr, amount}
    with st.spinner("Sending to backend..."):
        try:
            r = requests.post(BACKEND_PAY_URL, json=payload, timeout=30)
            data = r.json()

            if data.get("status") == "success":
                st.success(data.get("message", "Payment successful ✅"))
                st.write("**QR type:**", data.get("qr_type"))
                st.write("**Amount (XRP):**", data.get("amount_xrp"))

                tx = data.get("xrpl_tx_hash")
                if tx:
                    st.write("**Transaction hash:**")
                    st.code(tx, language="text")
                    st.write("**Explorer:**")
                    st.write(f"https://testnet.xrpl.org/transactions/{tx}")
            else:
                st.error("Payment failed ❌")
                st.json(data)

        except requests.exceptions.ConnectionError:
            st.error("Could not reach backend. Is `python app.py` running on port 5000?")
        except Exception as e:
            st.error("Something went wrong.")
            st.exception(e)

st.divider()
