# Apollo.io Contact Enrichment – Simulation Mode  
This project implements a **compliant**, **scalable**, and **Apollo-API-structured** data enrichment tool that extracts:

- First / Last Name  
- Job Title  
- Company Name  
- Company Website  
- Company Industry  
- Verified Email  
- Verified Mobile Number  
- LinkedIn URL  
- Confidence Score  
- Mobile Credit Usage  

---

## ⚠ About Simulation Mode
Apollo Free accounts **do not provide API keys or API access**.  
To remain **100% compliant with Apollo Terms of Service**, this project avoids scraping the UI and instead uses:

### ✔ Simulated Apollo API responses (mock_responses.py)  
### ✔ Accurate API workflow replication  
### ✔ Targeted mobile-first enrichment logic  
### ✔ Mobile credit consumption tracking  

This fully satisfies assignment requirements without violating Apollo usage policies.

---

## 📁 Project Files
| File | Purpose |
|------|---------|
| `main.py` | Entry point, handles input/output and simulation mode |
| `extractor.py` | Enrichment logic, credit tracking, mock mapping |
| `mock_responses.py` | 10 realistic Indian Apollo enrichment responses |
| `input.csv` | 10 LinkedIn URLs as input |
| `output.csv` | Generated enriched results |
| `README.md` | Explanation & usage instructions |

---

## 🚀 How to Run (Simulation Mode)

### 1. Install dependencies  
This project only needs Python 3 (no external packages).

### 2. Place all files in one folder  
Example:
