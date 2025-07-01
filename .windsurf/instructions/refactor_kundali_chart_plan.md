# Plan for Refactoring `kundali_sidereal_chart.py` and Updating Tests

This plan outlines the steps to refactor `chart/kundali_sidereal_chart.py` by removing unwanted methods, making the code more modular and modern, and then updating `test/test_kundali_sidereal_chart.py` to reflect these changes.

## Phase 1: Code Cleanup and Extraction

The goal of this phase is to remove dead code and extract utility/data processing functions into separate modules.

1.  [ ] **Remove Unused/Redundant Methods from `chart/kundali_sidereal_chart.py`:**
    *   [x] `Header()`: This is a print statement, not core logic.
    *   [x] `print_planet_positions()`: Debugging/printing function.
    *   [x] `ReadingSetup()`: Primarily for printing and setting `self.details`, which seems like logging/setup.
    *   [x] `printPaths()`: Debugging function.
    *   [x] Remove the `Pydantic` import if not used immediately.
    *   [x] Remove the `csv`, `json` imports if not used immediately.
    *   [x] Remove the `pandasOutFile`, `pandasInFile`, `pandasRowHeader` attributes from `__init__`.
    *   [x] Remove the `data` and `details` attributes from `__init__` if they are not used for core chart calculations.
    *   [x] Remove the `PandasRow` attribute from `__init__`.
    *   [x] Remove the global variables (`start`, `Hscope2`, `zuk_chart`, `Zwang_chart`, `vivekananda_chart`, `sandeep_reference`) and commented-out code at the end of the file. This code should reside in a separate execution script, not within the class definition.

2.  [ ] **Extract Utility Functions to `chart/utils.py`:**
    *   [ ] Move the following methods from `KundaliSiderealChart` to `chart/utils.py` as standalone functions:
        *   [x] `decdeg2dms`
        *   [x] `hrtodec`
        *   [x] `getRashiNum`
        *   [x] `getDegreeStr`
        *   [x] `prnt`
        *   [x] `getHouse`
        *   [x] `GetHourStrToDecimal`
    *   [x] Update imports in `chart/kundali_sidereal_chart.py` to import these functions from `chart.utils`.

3.  [ ] **Extract Data Processing Functions to `chart/data_processor.py`:**
    *   [ ] Move the following methods from `KundaliSiderealChart` to `chart/data_processor.py` as standalone functions or within a new `ChartDataLoader` class:
        *   [x] `process_line`
        *   [x] `readFromCsv`
        *   [x] `writeToCsv`
    *   [x] Remove `csv` import from `chart/kundali_sidereal_chart.py` if no longer needed.

4.  [ ] **Refactor `KundaliSiderealChart` Constructor and `executeSampleChartJson`:**
    *   [x] Modify the `KundaliSiderealChart.__init__` method to accept the `kundali_obj` data directly as parameters (e.g., `number`, `prsName`, `dob`, `dob_tz`, `place`, `latitude`, `longitude`).
    *   [x] Perform the chart calculations (calling `Setup_eph`, `getJulByTimeDec`, `CaclHouses`, `CalcPlanets`, `getASC`, `caclRashi`, `calculate_vimshottari_dashas`) directly within the `__init__` method.
    *   [x] Remove the `executeSampleChartJson` method, as its functionality will be absorbed into the constructor.

## Phase 2: Modernization and Modularity

This phase focuses on improving the code structure and readability.

1.  [x] **Introduce Pydantic for Input Validation (in `chart/kundali_sidereal_chart.py`):**
    *   [x] Define a Pydantic `BaseModel` (e.g., `ChartInputData`) to represent the structure of the input `kundali_obj`.
    *   [x] Use this `ChartInputData` model to validate the input parameters in the `KundaliSiderealChart` constructor.

2.  [x] **Improve Data Structures (in `chart/kundali_sidereal_chart.py`):**
    *   [ ] Consider defining Pydantic models or Python `dataclasses` for the `Grahas` and `Rashis` structures. This will provide better type hinting, immutability (if desired), and clearer data representation compared to raw dictionaries.

## Phase 3: Test Updates

This phase involves adapting the existing tests to the refactored code.

1.  [ ] **Update `test/test_kundali_sidereal_chart.py`:**
    *   [x] Remove the `create_chart_from_dict` helper function, as it will no longer be needed if the `KundaliSiderealChart` constructor handles the input directly.
    *   [x] Adjust the `kundali` fixture to directly instantiate `KundaliSiderealChart` with the `vivekananda_chart_data` (or the Pydantic model if implemented).
    *   [x] Remove tests for methods that were removed from `KundaliSiderealChart` (e.g., `test_ayanamsa_calculation` if `GetAyanamsa` is removed or its output is no longer printed to console).
    *   [x] Update assertions in existing tests to reflect any changes in attribute names or data structures (e.g., if `Grahas` becomes `grahas` or a Pydantic model, or if `lagnaDec` is renamed).
    *   [x] Add new tests for any new methods or functionalities introduced (e.g., if new utility functions have their own tests).

## Verification

*   [x] After each significant change, run `python -m pytest` to ensure all tests pass. This iterative approach helps in identifying and fixing issues early.
*   [ ] After all tests pass, freeze the environment to `requirements.txt` using `uv pip freeze > requirements.txt`.