# OneQR: A Global QR Payment Routing Demo

**Project Repository for NUS Fintech Summit 2026**

**OneQR** is a global payment abstraction layer that routes QR payments through country or platform-specific rails.

**Problem**: QR payment systems vary by country, e.g.
- **Singapore**: Multiple QR systems exist (e.g. NETS, PayLah!, PayNow), but some merchants may only accept one type.
- **China**: Popular services like Alipay and WeChat Pay sometimes only work for locals, or charge extra fees for foreign users, making payments difficult.

**Goal**: Build a system where users can pay with their preferred method, while merchants receive funds via their existing rails.

## Project Overview

This project demonstrates a universal QR payment system using:
- **Flask** for backend API handling payments
- **Streamlit** for frontend UI (paste QR, scan QR, upload QR)
- **XRP Ledger** for interacting with the XRPL Testnet

The backend generates a sender wallet automatically on startup for demo payments. 

A fixed test destination wallet is used for consistent demonstration purposes.
- Generated using `create_wallet.py`

## XRPL Features

### 1. Cross-Country Payments
- While QR payment systems differ by country, XRPL provides a neutral, borderless ledger for value transfer.
- This demo simulates cross-country QR payments by routing country-specific QR formats to a unified backend.
- QR formats are detected via `detect_qr_type`, while settlement is performed via `send_xrpl_payment` (see `backend.py`).

### 2. Native XRP Payments
- Payments are executed as XRPL Payment transactions on the XRPL Testnet.
- Transactions are signed, submitted and validated on-ledger.
- Each payment returns a verifiable transaction hash and explorer link.

### 3. XRPL Testnet and Wallet Creation
- Sender wallets are generated and funded using the XRPL Testnet faucet.
- Enables safe testing without real funds.

## Setup

### 1. Create a virtual environment

### 2. Install dependencies
- `pip install -r requirements.txt`

## Running the Project

### 1. Start the Flask backend
- Open a terminal
- Run: `python backend.py`

### 2. Start the Streamlit frontend
- Open a **new** terminal
- Run: `streamlit run frontend.py`

## Authors
- [Loke Ann Chi](https://github.com/annchiloke)
- [Lim Ze Yan](https://github.com/zyyy22)
- [Kwek Jia Qi](https://github.com/JiaQiK05)
