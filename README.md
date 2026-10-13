# Lab Programs Repository

Repository for lab experiments and programs organized by folders:
- 📁 **`dva/`**: For `.txt` files (e.g., Data Visualisation & Analytics / SQL queries / notes)
- 📁 **`ml/`**: For `.py` files (e.g., Machine Learning programs)

---

## 💻 On the Other Laptop (In Jupyter Notebook)

### Browse the ML programs as a Python package

Once published on PyPI, install it with one command:

```python
%pip install --upgrade lab-ml-programs
```

Restart the notebook kernel after installation, then list and print programs:

```python
import ml

ml.list()
ml.show(1)  # Print the first program in the list
```

The scripts are installed inside Python's `site-packages` directory, not in
the notebook's current folder. Find that installed folder with:

```python
from pathlib import Path
print(Path(ml.__file__).resolve().parent)
```

You can also print a program by filename, without the `.py` extension:

```python
ml.show("linear_regression")
```

The distribution is named `lab-ml-programs` and imports as `ml` or `dva`.
Do not use `pip install ml`; that PyPI name belongs to an unrelated project.
After new programs are released, run the install command again to update.

#### First-time PyPI publishing setup

The PyPI project must be published before the short install command works.
The repository is configured to publish when a GitHub Release is published.
The repository owner must first configure a PyPI Trusted Publisher for:

- Owner: `thanoojchokkakula-dev`
- Repository: `Lab`
- Workflow: `publish-pypi.yml`
- Environment: `pypi`

Then create and publish a GitHub Release tagged `v0.3.0`. PyPI will receive
the package through GitHub Actions; no PyPI token needs to be stored in this
repository.

#### If installation is blocked on an older college computer

Download the repository ZIP from
https://github.com/thanoojchokkakula-dev/Lab/archive/refs/heads/main.zip and
extract it. In Jupyter, change the working directory to the extracted `Lab`
folder, or add that folder to Python's module path:

```python
import sys
sys.path.insert(0, r"C:\path\to\Lab")

import ml
ml.list()
ml.show(1)
```

This fallback does not install anything and does not need Git. To display the
code, Python only needs to be able to import the package. Running a displayed
program may additionally require that program's libraries (for example,
scikit-learn, pandas, or matplotlib).

### Browse both `dva/` and `ml/` with the `lab` helper

The same installation includes the DVA text files. Browse or print them with:

```python
import dva

dva.list()
dva.show(1)
```

To browse both folders through the `lab` helper:

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

3. Publish a GitHub Release with a new version tag to upload it to PyPI. On the
   other laptop in Jupyter, update with:
   ```python
   %pip install --upgrade lab-ml-programs
   import ml
   ml.list()
   ```
