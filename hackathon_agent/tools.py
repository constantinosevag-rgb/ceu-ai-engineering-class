# Custom tools for the hackathon agent

def simple_calculator(expression: str) -> str:
    try:
        result = eval(expression, {"__builtins__": {}})
        return f"Result: {result}"
    except Exception as e:
        return f"Error: {e}"
