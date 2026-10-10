# Lab Programs Repository

Repository for lab experiments and programs (supports both `.py` and `.txt` files).

---

## 💻 On the Other Laptop (In Jupyter Notebook)

Open any Jupyter Notebook on the other laptop and paste these into code cells:

### Option 1: Using Git (Recommended)

#### 1. Setup / Update:
```python
!git pull
```
*(If opening for the very first time on a new laptop: `!git clone https://github.com/thanoojchokkakula-dev/Lab.git` and `%cd Lab`)*

#### 2. View All Saved Codes (Shows both `.py` and `.txt`):
```python
import lab
lab.list()
```
Output:
```text
=== Available Codes (2 total) ===
-----------------------------------
  [1] p1.py
  [2] p2.txt
-----------------------------------
```

#### 3. Print or Load Any Code:
- **By Number:**
  ```python
  lab.show(1)    # prints program #1
  lab.show(2)    # prints program #2
  ```

- **By Name:**
  ```python
  lab.show('p1')     # prints p1.py
  lab.show('p2')     # prints p2.txt
  ```

- **Load Directly into Cell (Jupyter %load Magic):**
  ```python
  %load p1.py
  # or
  %load p2.txt
  ```
  *(Press **Shift + Enter**, and Jupyter replaces the cell with the full code!)*

- **Jupyter File Listing Magic:**
  ```python
  %ls *.py *.txt
  ```
  *(Or on Windows: `!dir /b *.py *.txt`)*

---

### Option 2: Without Git (Direct 1-Liner from GitHub)

If git is not installed, fetch and print any file directly from GitHub:

```python
import urllib.request
# Fetch Python file:
print(urllib.request.urlopen("https://raw.githubusercontent.com/thanoojchokkakula-dev/Lab/main/p1.py").read().decode())

# Fetch Text file:
print(urllib.request.urlopen("https://raw.githubusercontent.com/thanoojchokkakula-dev/Lab/main/p2.txt").read().decode())
```

---

## 🚀 How to Add New Codes (.py or .txt) from this Laptop

Whenever you create or save new code files (e.g. `p3.py`, `p4.txt`, etc.):

1. Put the files in your `Lab` folder.
2. Open terminal in this folder and run:
   ```bash
   git add .
   git commit -m "Added new codes"
   git push
   ```

3. On the other laptop in Jupyter, simply run:
   ```python
   !git pull
   lab.list()
   ```
