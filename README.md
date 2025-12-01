# **RetailX – Oracle to Databricks Migration (AWS + Databricks Architecture)**

![RetailX Architecture](soure_files/images/architecture.png)

---

## **📌 Overview**

RetailX is migrating operational data from an on-prem Oracle environment running inside AWS EC2 into Databricks using a modern Lakehouse design. The solution integrates **Lakeflow**, **Auto Loader**, **Unity Catalog**, **Delta Live Tables (DLT)**, and **Lakebridge** to deliver a scalable, production-grade pipeline.

---

## **🏗️ High-Level Architecture**

### **1. Source (AWS EC2 + Oracle in Docker)**

- Oracle DB hosted inside a Docker container on EC2.
- Python script extracts data from Oracle.
- Data paths:

  - **Orders → Lakeflow → UC Catalog**
  - **Customers → S3 → Auto Loader**

---

## **2. AWS S3 – Customer File Landing Zone**

- Customer CSV files are uploaded into S3 using Python + Boto3.
- This becomes the streaming ingestion zone for Databricks Auto Loader.

---

## **3. Databricks – Unified Ingestion, Storage, Transformation**

### **A. Lakeflow Connect (For Oracle → Orders Table)**

- Direct ingestion from Oracle to Databricks.
- Writes tables into **`retailx-onprem-catalog.orders`**.
- Exposed to the main catalog through UC views.

### **B. Auto Loader (For Customers → S3 → Databricks)**

- Watches S3 for new CSVs.
- Writes incrementally into Bronze with schema evolution.

---

## **4. Unity Catalog – Governance and Lineage**

Two catalogs are used:

| Catalog                    | Purpose                                                  |
| -------------------------- | -------------------------------------------------------- |
| **retailx-onprem-catalog** | Contains Lakeflow-synced Oracle tables (e.g., `orders`). |
| **retailx-catalog**        | Full Medallion pipeline (Bronze, Silver, Gold).          |

UC manages lineage, permissions, and secure access.

---

## **5. Medallion Architecture (retailx-catalog)**

### **Bronze**

- Raw ingested data from Lakeflow and Auto Loader.

### **Silver**

- Type standardization
- Deduplication
- Schema alignment
- Cleaned customer + order datasets

### **Gold**

Business-ready, aggregated, dimensional tables.

**Your Gold DLT tables included:**

---

## **📀 Gold Layer — Delta Live Tables (DLT)**

### **1️⃣ `retailx.gold.order_monthly_summary`**

Grain: **customer × month**

Aggregations:

- Total Revenue
- Order Count
- Average Order Value

---

### **2️⃣ `retailx.gold.customer_order_profile`**

Dimension-style enriched customer table with behavioral metrics.

Metrics:

- Last Order Date
- Lifetime Value (LTV)
- Total Orders

---

**These Gold tables serve the core business KPIs: revenue performance, customer LTV, churn analysis, and segmentation.**

---

## **6. Lakebridge Integration (Oracle Migration Automation)**

### **F1. Run Lakebridge Analyzer on Oracle scripts**

- Scans existing Oracle SQL & PL/SQL.
- Detects incompatibilities with Spark SQL.
- Generates a full compatibility + complexity report.
- Used to prioritize migration effort.

### **F2. Run Lakebridge Transpiler & integrate output**

- Automatically converts Oracle SQL to Databricks SQL/PySpark.
- Normalizes functions, datatypes, and expressions.
- Output is directly integrated into:

  - Silver transformation logic
  - Gold metrics
  - DLT pipelines

This significantly accelerates modernization while reducing errors.

---

## **📊 Data Flow Summary**

### **Orders**

1. Oracle → Python Extraction
2. Lakeflow → `retailx-onprem-catalog.orders`
3. Unity Catalog View → Bronze
4. DLT → Silver → Gold

### **Customers**

1. Python → S3 CSV
2. Auto Loader → Bronze
3. DLT → Silver → Gold

---

## **🛠️ Technology Stack**

| Layer        | Tools                                |
| ------------ | ------------------------------------ |
| Compute      | AWS EC2, Databricks                  |
| Storage      | Amazon S3, Unity Catalog             |
| Source DB    | Oracle (Dockerized)                  |
| Ingestion    | Python, Boto3, Lakeflow, Auto Loader |
| Transform    | Delta Live Tables, PySpark           |
| Migration    | Lakebridge Analyzer + Transpiler     |
| Governance   | Unity Catalog                        |
| Architecture | Medallion (Bronze/Silver/Gold)       |

```

```
