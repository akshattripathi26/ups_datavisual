# 📦 UPS Parcel Dataset Analysis (2025)

An exploratory data analysis (EDA) and reporting project built in Python using Google Colab. This repository processes, cleans, and analyzes the **UPS Parcel Dataset - 2025** to derive actionable insights regarding shipping costs, logistics performance, service usage, and invoice tracking.

---

## 📋 Table of Contents

- [Overview](#overview)
- [Key Features & Analytics](#key-features--analytics)
- [Dataset Structure](#dataset-structure)
- [Tech Stack & Dependencies](#tech-stack--dependencies)
- [Installation & Setup](#installation--setup)
- [Workflow](#workflow)
- [Future Enhancements](#future-enhancements)

---

## 📌 Overview

This project provides a structured pipeline for inspecting and analyzing UPS shipment records from 2025. By connecting to Google Drive, loading multi-row Excel headers, and leveraging Python data science libraries (`pandas`, `seaborn`, `matplotlib`), the notebook facilitates financial auditing, service-level evaluation, and temporal shipping trends.

---

## ⚡ Key Features & Analytics

- **Google Drive Integration**: Direct mounting to Google Drive for seamless dataset access in Google Colab.
- **Excel Data Cleaning**: Handles complex Excel formatted sheets (e.g., header offset parsing via `pd.read_excel(header=2)`).
- **Logistics Breakdown**: Analyses net charges across different carriers (`UPS Parcel`, `UPS Import`) and service types (`Next Day Air`, `Worldwide Express`).
- **Time-Series / Period Tracking**: Tracks shipping metrics across custom remittance weeks/months and ship weeks (`WK01`–`WK52`, `P01`–`P12`).
- **Data Visualization Ready**: Configured with `matplotlib` and `seaborn` for distribution analysis, cost tracking, and operational dashboards.

---

## 📊 Dataset Structure

The analysis centers around `UPS Parcel Dataset - 2025.xlsx`, which contains over 70 features covering logistical and financial dimensions. Key attributes include:

| Attribute | Description |
| :--- | :--- |
| `InvShipmentId` | Unique shipment identification number |
| `InvNbr` | Invoice tracking number |
| `CarrierShortNm` | Carrier category (e.g., `UPS Parcel`, `UPS IMPORT`) |
| `NetCharge` | Final billed charge for the shipment ($) |
| `InvDate` / `ShipDate` | Invoice issuance and package shipment dates |
| `ServiceTypeNm` | Specific shipping tier (e.g., `Next Day Air`, `Worldwide Express`) |
| `MOT` / `MOS` | Mode of Transport / Mode of Service (`Parcel`, `Expedite`, `Fees`) |
| `Ship Week` / `Ship Month` | Binned timeframes for seasonal and weekly aggregation |

---

## 🛠️ Tech Stack & Dependencies

- **Language**: Python 3
- **Environment**: Google Colab / Jupyter Notebook
- **Libraries**:
  - `pandas`: Data manipulation and tabular representation
  - `numpy`: Numerical operations
  - `matplotlib`: Core visualization engine
  - `seaborn`: Statistical graphics and visual enhancement
  - `openpyxl`: Excel file reading backend

---

## 🚀 Installation & Setup

1. **Clone or Download Notebook**: Load the `.ipynb` file into Google Colab or your local Jupyter environment.
2. **Dataset Location**: Place `UPS Parcel Dataset - 2025.xlsx` in your Google Drive at:
   ```text
   MyDrive/UPS Parcel Dataset - 2025.xlsx
   ```
3. **Install Requirements** (if running locally):
   ```bash
   pip install pandas numpy matplotlib seaborn openpyxl
   ```

---

## 🔄 Workflow

1. **Mount Drive**:
   ```python
   from google.colab import drive
   drive.mount('/content/drive')
   ```
2. **Import Libraries**:
   ```python
   import pandas as pd
   import numpy as np
   import matplotlib.pyplot as plt
   import seaborn as sns
   ```
3. **Load Data**: Skip top decorative rows using `header=2`:
   ```python
   url = '/content/drive/MyDrive/UPS Parcel Dataset - 2025.xlsx'
   df = pd.read_excel(url, header=2)
   display(df.head())
   ```

---

## 💡 Future Enhancements

- [ ] Add automated visualizations for total net charge by service type.
- [ ] Implement an on-time delivery rate analysis module.
- [ ] Add outlier detection for unexpectedly high shipping charges.
