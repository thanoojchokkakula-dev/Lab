# Lab Programs Repository

Repository for lab experiments and programs organized by folders:
- 📁 **`dva/`**: For `.txt` files (e.g., Data Visualisation & Analytics / SQL queries / notes)
- 📁 **`ml/`**: For `.py` files (e.g., Machine Learning programs)

---

## 💻 On the Other Laptop (In Jupyter Notebook)

### Browse the ML programs as a Python package

Install the latest version directly from this public GitHub repository:

```python
%pip install --upgrade git+https://github.com/thanoojchokkakula-dev/Lab.git
```

Then list and print programs:

```python
import ml

ml.list()
ml.show(1)  # Print the first program in the list
```

You can also print a program by filename, without the `.py` extension:

```python
ml.show("linear_regression")
```

When new programs are pushed to GitHub, run the install command again to update
the package on the other laptop. The PyPI name `ml` is already used by an
unrelated project, so install this repository from GitHub rather than running
`pip install ml`.

### Browse both `dva/` and `ml/` with the `lab` helper

The existing `lab` helper can also list files from both folders. Install this
repository in the notebook environment as above, then use:

```python
import lab
lab.list()
```

You can also filter by folder:
```python
lab.list('dva')   # Shows only dva files
lab.list('ml')    # Shows only ml files
```

Print code by number or name:
- **By Number:**
  ```python
  lab.show(1)
  ```

- **By Name (searches automatically across all folders):**
  ```python
  lab.show('linear_regression')
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
   %pip install --upgrade git+https://github.com/thanoojchokkakula-dev/Lab.git
   import ml
   ml.list()
   ```
