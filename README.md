# Lab Programs Repository

Repository for lab experiments and programs.

---

## 💻 On the Other Laptop (In Jupyter Notebook)

Open any Jupyter Notebook on the other laptop. You can use any of the options below:

### Option 1: Using Git (Recommended)

#### 1. Clone repository into Jupyter (run in a cell once):
```python
!git clone https://github.com/thanoojchokkakula-dev/Lab.git
%cd Lab
```

#### 2. Print or Load the Code:
- **To print the code in cell output:**
  ```python
  import lab
  lab.show('p1')
  ```
  *(Or: `print(open('p1.py').read())`)*

- **To load the code into the cell to run/edit (Jupyter magic):**
  ```python
  %load p1.py
  ```
  *(Press `Shift + Enter`, and Jupyter will replace the cell with the full code of `p1.py`)*

- **To list all available programs:**
  ```python
  import lab
  lab.list_programs()
  ```

---

### Option 2: Without Git (Direct 1-Liner from GitHub)

If git is not installed or you don't want to clone the repo, run this in any Jupyter cell:

```python
import urllib.request
print(urllib.request.urlopen("https://raw.githubusercontent.com/thanoojchokkakula-dev/Lab/main/p1.py").read().decode())
```

To fetch any other file later, simply replace `p1.py` with `p2.py`, `p3.py`, etc.

---

## 🚀 How to Add New Codes from this Laptop

Whenever you create new code files (e.g. `p2.py`, `p3.py`):

1. Put the files in this folder.
2. Open terminal in this folder and run:
   ```bash
   git add .
   git commit -m "Added new lab programs"
   git push
   ```

3. On the other laptop in Jupyter, simply run:
   ```python
   !git pull
   ```
   Now you can print or load the new programs:
   ```python
   lab.show('p2')
   # or %load p2.py
   ```
