# SmartTrade - AI-Powered Stock Portfolio Analyzer

A full-stack FinTech application built with **Django**, **Django REST Framework**, **WebSockets**, and **Machine Learning**.

## 🎯 Features
- JWT Authentication & Registration
- Portfolio Management (Add/Edit/Delete stocks)
- Live Stock Prices via Yahoo Finance
- AI Risk Analysis Engine
- WebSocket Real-time Updates
- Beautiful Dark Dashboard with Charts

## 📊 Results
- Portfolio Risk: 22.24/100 (Low Risk)
- AAPL: +$1,209 profit (+68.9%)
- GOOGL: +$1,146 profit (+163.8%)

## 🛠️ Tech Stack
- Django 6.0, DRF, Django Channels
- yfinance, NumPy, Pandas, scikit-learn
- WebSockets, Chart.js

## 🚀 Quick Start
```bash
git clone https://github.com/Surryagit/smarttrade.git
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```