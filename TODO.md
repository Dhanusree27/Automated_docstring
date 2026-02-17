# Fix Plan: Docstring Generation for Entire File

## Problem
When selecting NumPy or reST style, only 1 function gets docstrings instead of all functions/classes in the file. Google style works correctly.

## Root Cause
The `synthesis_engine.generate_docstring()` method is designed for a single function, not the entire file. The prompt says "Generate a docstring for the following Python function" which doesn't work for file-level generation.

## Solution Plan

### Step 1: Add `generate_file_docstrings()` method in `synthesis_engine.py`
- Create new method that handles entire file
- Build prompt that explicitly asks for ALL functions and classes
- Parse and return combined docstrings

### Step 2: Modify `app.py` to use new method
- Change the "Generate Docstrings for Entire File" button to call `generate_file_docstrings()` instead of `generate_docstring()`

## Files to Edit
1. `modules/synthesis_engine.py` - Add new method
2. `app.py` - Update generation logic
