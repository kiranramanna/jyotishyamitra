# Instructions to Run Tests

First, ensure you have `uv` installed. If not, you can install it with:
```bash
brew install uv
```

1.  **Create Virtual Environment:** Create a new virtual environment using `uv` with Python 3.11. This will create a `.venv` directory in your project root.
    ```bash
    uv venv --python 3.11
    ```

2.  **Activate Virtual Environment:** Activate the newly created environment.
    *   **macOS/Linux:**
        ```bash
        source .venv/bin/activate
        ```
    *   **Windows:**
        ```bash
        .venv\Scripts\activate
        ```

3.  **Install Dependencies:** Compile `requirements.in` to `requirements.txt` (which will pin package versions) and then install the required libraries using `uv pip`.
    ```bash
    uv pip compile requirements.in -o requirements.txt
    uv pip install -r requirements.txt
    ```

4.  **Run Tests:** Execute the test suite using the `pytest` command from the project root directory.
    ```bash
    python -m pytest
    ```

5.  **Freeze Environment:** After tests pass, freeze the installed packages to `requirements.txt`.
    ```bash
    uv pip freeze > requirements.txt
    ```