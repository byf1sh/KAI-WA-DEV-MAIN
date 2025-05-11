import re

def extract_field(field, data):
        m = re.search(rf"{field}\s*:\s*(.*?)(?=\n\S.*|\Z)", data, re.DOTALL)
        return m.group(1).strip() if m else ""
