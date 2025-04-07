# 📊 FRI-Calculator

## 🎯 Project Objective
Develop a **user-friendly graphical interface (GUI)** for calculating **descriptive statistics** and **partition measures** (quartiles, quintiles, deciles, and percentiles) from grouped frequency data. The goal is to provide an efficient tool for statistical analysis with clear visualization and customizable calculations.

---

## 🛠 Key Features
✔ **Frequency Distribution Table**  
   - Computes absolute frequency (`fi`), relative frequency (`fri`), cumulative frequency (`Fi`)  
   - Percentage conversions and angular degrees for pie charts  

✔ **Central Tendency Measures**  
   - **Mean (ME)**, **Mode (MO)**, **Median (MD)** calculations  

✔ **Partition Measures**  
   - Quartiles (Q1, Q2, Q3)  
   - Quintiles (K1-K4)  
   - Deciles (D1-D9)  
   - Custom percentiles (e.g., P5, P95)  

✔ **Interactive Table**  
   - Scrollable Treeview with 12 columns of computed data  
   - Dynamic formatting (removes trailing `.00` for integers)  

✔ **One-Click Export**  
   - Copy table data as TSV (tab-separated values) to clipboard  

✔ **Responsive UI**  
   - Adapts to window resizing  
   - Smart scrolling for large datasets  

---

## 💻 Tech Stack
| Component       | Technology Used           |
|-----------------|---------------------------|
| Core Language   | Python 3                  |
| GUI Framework   | Tkinter (ttk widgets)     |
| Table Display   | `ttk.Treeview` + Scrollbar|
| Math Logic      | Custom algorithms for:<br>• Class interpolation<br>• Modal class detection<br>• Percentile positioning |

---

## ⚙️ How It Works
1. **Input Phase**  
   ```python
   Enter k (classes): 5
   Set h (amplitude): 10
   Define Li (initial): 0
   Input fi values: [5, 10, 15, 8, 2]

![image](https://github.com/user-attachments/assets/39d135c4-5648-47df-a0b7-393efae97d55)

```bash
# Clone repository
git clone https://github.com/KauaZao0o/FRI-Calculator.git

# Run application
cd FRI-Calculator
python main.py
```

> [!NOTE]  
> Requires Python 3.6+ with Tkinter (usually included in standard library)

<div align="center"> <sub>©KauaZao0o</sub> | <a href="https://github.com/KauaZao0o/FRI-Calculator/issues">Report Bug</a> | <a href="https://github.com/KauaZao0o/FRI-Calculator/pulls">Contribute</a> </div>
