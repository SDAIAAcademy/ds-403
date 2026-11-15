# /// script
# requires-python = ">=3.11"
# dependencies = ["numpy>=2.0", "pandas>=2.2", "scipy>=1.14", "statsmodels>=0.14", "matplotlib>=3.9"]
# ///

# %% [markdown]
# # Setup check
#
# Run this once before Day 1. It imports every library the labs use, reads the logs of Bunyan Building Permits Authority and prints what it finds. No model is called and no key is needed.

# %%
import os, sys, subprocess
from pathlib import Path

IN_COLAB = "google.colab" in sys.modules
if IN_COLAB:
    REPO_URL = "https://github.com/SDAIAAcademy/ds-403.git"
    if not Path("/content/ds-403").exists():
        subprocess.run(["git", "clone", "-q", REPO_URL, "/content/ds-403"], check=True)
    os.chdir("/content/ds-403/labs")
    subprocess.run([sys.executable, "-m", "pip", "install", "-q", "-r", "requirements-colab.txt"], check=True)
else:
    while not Path("_tools").exists() and Path.cwd() != Path.cwd().parent:
        os.chdir("..")  # solutions/ notebooks run from labs/
sys.path.insert(0, os.getcwd())

# %%
missing = []
for name in ("numpy", "pandas", "scipy", "statsmodels", "matplotlib"):
    try:
        mod = __import__(name)
        print(f"✅ {name} {mod.__version__}")
    except ImportError:
        missing.append(name)
        print(f"❌ {name} is missing: run uv sync in labs/, or the first cell again in Colab")
print("Python", sys.version.split()[0])

# %%
import bunyan as U

items = U.items()
results = U.load("results")
print(f"{len(items)} questions from {items.doc_id.nunique()} documents; languages {items.language.value_counts().to_dict()}")
print(f"{len(results)} graded answers; configurations {sorted(results.config.unique())}; temperatures {sorted(results.temperature.unique())}")
assert len(items) == 600 and items.doc_id.nunique() == 80
assert not missing, missing
print("✅ ready for Day 1" + (" (quick mode)" if U.QUICK else ""))
