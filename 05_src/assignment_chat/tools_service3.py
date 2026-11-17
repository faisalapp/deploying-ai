from langchain.tools import tool


@tool
def convert_units(value: float, from_unit: str, to_unit: str) -> str:
    """Convert a numeric value between units.
    ALWAYS use this tool for any unit conversion question, even simple ones.
    Never convert units yourself — this tool is the single source of truth
    for all conversions. Supports km/mi, kg/lb, m/ft, cm/in, and Celsius/Fahrenheit.
    Requires a number, a source unit, and a target unit.
    """
    factors = {
        ("km", "mi"): 0.621,
        ("mi", "km"): 1.60934,
        ("kg", "lb"): 2.20462,
        ("lb", "kg"): 0.453592,
        ("m", "ft"): 3.28084,
        ("ft", "m"): 0.3048,
        ("cm", "in"): 0.393701,
        ("in", "cm"): 2.54

    }

    from_unit = from_unit.lower()
    to_unit = to_unit.lower()

    # Temperature is special: it's not multiply-only, it also shifts
    if from_unit in ("c", "celsius") and to_unit in ("f", "fahrenheit"):
        converted = value * 9 / 5 + 32
    elif from_unit in ("f", "fahrenheit") and to_unit in ("c", "celsius"):
        converted = (value - 32) * 5 / 9
    elif (from_unit, to_unit) in factors:
        converted = value * factors[(from_unit, to_unit)]
    else:
        return f"Unsupported conversion: {from_unit} -> {to_unit}. I handle km/mi, kg/lb, m/ft, cm/in, and C/F."

    return f"{value} {from_unit} = {round(converted, 2)} {to_unit}"