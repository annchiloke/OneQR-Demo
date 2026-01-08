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
