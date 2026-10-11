# Lab Programs Repository

Repository for lab experiments and programs organized by folders:
- 📁 **`dva/`**: For `.txt` files (e.g., Data Visualisation & Analytics / SQL queries / notes)
- 📁 **`ml/`**: For `.py` files (e.g., Machine Learning programs)

---

## 💻 On the Other Laptop (In Jupyter Notebook)

Open any Jupyter Notebook on the other laptop:

### Option 1: Using Git (Recommended)

#### 1. Setup / Update:
```python
!git pull
```
*(If cloning for the very first time on a new laptop: `!git clone https://github.com/thanoojchokkakula-dev/Lab.git` and `%cd Lab`)*

#### 2. View All Saved Codes (Shows both folders):
```python
import lab
lab.list()
```
Output:
```text
=== Available Codes (2 total) ===
--------------------------------------
[dva]
  [1] dva/experment-1.txt

[ml]
  [2] ml/p1.py

--------------------------------------
```

You can also filter by folder:
```python
lab.list('dva')   # Shows only dva files
lab.list('ml')    # Shows only ml files
```

#### 3. Print or Load Any Code:
- **By Number:**
  ```python
  lab.show(1)    # Prints program #1 (dva/experment-1.txt)
  lab.show(2)    # Prints program #2 (ml/p1.py)
  ```

- **By Name (searches automatically across all folders):**
  ```python
  lab.show('experment-1')  # Prints dva/experment-1.txt
  lab.show('p1')           # Prints ml/p1.py
  ```

- **Load Directly into Cell (Jupyter %load Magic):**
  ```python
  %load dva/experment-1.txt
  # or
  %load ml/p1.py
  ```
  *(Press **Shift + Enter**, and Jupyter replaces the cell with the full code!)*

---

### Option 2: Without Git (Direct 1-Liner from GitHub)

If git is not installed, fetch and print any file directly from GitHub:

```python
import urllib.request
# Fetch from dva folder:
print(urllib.request.urlopen("https://raw.githubusercontent.com/thanoojchokkakula-dev/Lab/main/dva/experment-1.txt").read().decode())

# Fetch from ml folder:
print(urllib.request.urlopen("https://raw.githubusercontent.com/thanoojchokkakula-dev/Lab/main/ml/p1.py").read().decode())
```

---

## 🚀 How to Add New Codes from this Laptop

1. Put your `.txt` files in the `dva/` folder and your `.py` files in the `ml/` folder.
2. Open terminal in this repository and run:
   ```bash
   git add .
   git commit -m "Added new lab codes"
   git push
   ```

3. On the other laptop in Jupyter, simply run:
   ```python
   !git pull
   lab.list()
   ```
