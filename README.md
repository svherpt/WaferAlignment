Wafer Alignment Simulator - Python Bindings
===========================================

This project exposes the C++ Wafer Alignment Simulator as a Python module using **nanobind**. 
It allows controlling the simulator from Python for ML/RL experiments or other analysis workflows.

---

Requirements
------------

- Python 3.12 (Conda environment `wafer`)
- Conda: https://docs.conda.io/en/latest/miniconda.html
- C++ compiler supporting C++20
  - Windows: Visual Studio 2022
- Linux or macOS have not been tested
- CMake >= 3.18

Install Python dependencies using a conda environment

```bash
conda activate wafer
pip install -r requirements.txt
```

Or using the Conda environment file:

---

Project Structure
-----------------

```
WaferAlignment/
├─ simulator/                 # Core C++ library
│  ├─ simulator/              # Core source files (.h/.cpp)
│  ├─ simulator_tests/        # Unit tests for the simulator library using Google Test
│  ├─ bindings/               # Python bindings using nanobind
│  └─ simulator_app/          # Optional Visual Studio solution to run the core simulator
├─ python/                    # Python package, receives the .pyd module
├─ build/                     # Build artifacts (CMake output)
├─ requirements.txt
└─ environment.yml
```

---

Building the Python Module
--------------------------

1. From the project root, run:

```bash
conda activate wafer
cmake -S simulator -B build -G "Visual Studio 17 2022" -A x64
```

2. Build the library and module (Debug for development):

```bash
cmake --build build --config Debug
```

3. Build for performance (Release):

```bash
cmake --build build --config Release
```

- This builds the core simulator library (`simulator_lib`), the Python module (`wafer_simulator`), 
  and copies the `.pyd` to the `python/` folder.

---

Running the Python Module
-------------------------

1. Activate the environment:

```bash
conda activate wafer
```

2. Import the module:

```python
import python.wafer_simulator as ws

# Example usage (replace with actual functions)
result = ws.some_function()
print(result)
```

- The `python/` folder is a Python package because `__init__.py` is automatically created by CMake.

---

Running Unit Tests
------------------

- In Visual Studio, open `simulator_app/Simulator.sln`.
- Build the `simulator_tests` project.
- Run tests from Test Explorer.
- Alternatively, from command line (inside `build`):

```bash
ctest --config Debug
```

- Changes to core C++ files require rebuilding the library for tests and Python module.

---

Notes
-----

- Nanobind is used for efficient C++ ↔ Python bindings.
- Python module on Windows has extension `.pyd`; on Linux/macOS it is `.so`.

---

