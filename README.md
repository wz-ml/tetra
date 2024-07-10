# tetra
An adaptive human-like Tetris sparring partner.

## Setup
1. `git clone https://github.com/wz-ml/tetra.git`

2. Create a new conda environment:

```bash
conda create -n tetra python=3.11
conda activate tetra
```

3. Navigate to the `Tetra` directory and install the `tetra` package.

`pip install -e .`

Note: Avoid using `python setup.py` as it doesn't install the package in editable mode, which is required if you don't want to reinstall the package every time you update its files.