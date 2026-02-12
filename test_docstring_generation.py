from modules.synthesis_engine import SynthesisEngine

def test_docstring_generation():
    engine = SynthesisEngine()

    # Test function 1: Simple function with args and returns
    signature1 = 'def add_numbers(a: int, b: int) -> int:'
    context1 = '''
    """Add two numbers."""
    return a + b
    '''
    print("Test 1: Simple function")
    for style in ['google', 'numpy', 'rest']:
        result = engine.generate_docstring(signature1, context1, style)
        print(f"{style.upper()} Style:")
        print(result['docstring'])
        print()

    # Test function 2: Function with raises
    signature2 = 'def divide_numbers(a: float, b: float) -> float:'
    context2 = '''
    """Divide two numbers."""
    if b == 0:
        raise ValueError('Cannot divide by zero')
    return a / b
    '''
    print("Test 2: Function with raises")
    for style in ['google', 'numpy', 'rest']:
        result = engine.generate_docstring(signature2, context2, style)
        print(f"{style.upper()} Style:")
        print(result['docstring'])
        print()

    # Test function 3: Function with no args, just returns
    signature3 = 'def get_pi() -> float:'
    context3 = '''
    """Return the value of pi."""
    return 3.14159
    '''
    print("Test 3: Function with no args")
    for style in ['google', 'numpy', 'rest']:
        result = engine.generate_docstring(signature3, context3, style)
        print(f"{style.upper()} Style:")
        print(result['docstring'])
        print()

if __name__ == "__main__":
    test_docstring_generation()
