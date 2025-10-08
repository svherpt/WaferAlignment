# Wafer Alignment Simulator - Python Bindings

This project exposes the C++ Wafer Alignment Simulator as a Python module using **nanobind**. It allows controlling the simulator from Python for ML/RL experiments or other analysis workflows.

---

## Requirements

- Python 3.12 (Conda environment `wafer`)
- Conda: [https://docs.conda.io/en/latest/miniconda.html](https://docs.conda.io/en/latest/miniconda.html)
- C++ compiler supporting C++20
  - Windows: Visual Studio 2022
- Linux or macOS have not been tested
- CMake >= 3.18

Install Python dependencies:

```bash
conda activate wafer
pip install -r requirements.txt
```

Or using the Conda environment file:

```bash
conda env create -f environment.yml
conda activate wafer
```

---

## Building the Python module

1. Create a build directory:

```bash
mkdir build
cd build
```

2. Build with CMake:

```bash
cmake -S simulator -B build -G "Visual Studio 17 2022" -A x64
cmake --build build --config Debug
```

```bash
cmake --build build --config Release
```


- This builds the core simulator library (`simulator_lib`) and the Python module (`wafer_simulator`).
- The resulting Python extension is automatically copied to the `python/` folder.

---

## Using the Python module

1. Ensure you are in the project root so that `python/` is on the Python path:

```bash
conda activate wafer
python
```

2. Import the module:

```python
import python.wafer_simulator as ws

# Example usage (replace with actual functions)
result = ws.some_function()
print(result)
```

- The `python/` folder is a package because `__init__.py` is automatically created by CMake.

---

## Notes

- Changes to the core C++ simulator files (`simulator/simulator/`) require rebuilding the Python module.
- Nanobind is used for efficient C++ ↔ Python bindings.
- On Windows, the Python module has extension `.pyd`; on Linux/macOS, it is `.so`.
- For local development, you can optionally install the Python package in editable mode:

```bash
pip install -e python/
```

This allows importing and testing changes without rebuilding every time.

---

Maintainer: Simen van Herpt
