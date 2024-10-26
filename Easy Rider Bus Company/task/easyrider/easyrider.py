import json
import re


schema = {
    "bus_id": {"type": int, "required": True},
    "stop_id": {"type": int, "required": True},
    "stop_name": {"type": str, "required": True},
    "next_stop": {"type": int, "required": True},
    "stop_type": {"type": str, "required": False},
    "a_time": {"type": str, "required": True},
}


time_pattern = re.compile(r"^([0-1]\d|2[0-3]):[0-5]\d$")

json_data = input()
data = json.loads(json_data)

errors = {"bus_id": 0, "stop_id": 0, "stop_name": 0, "next_stop": 0, "stop_type": 0, "a_time": 0}
total_errors = 0

def validate_field(field_name, value, field_info):
    global total_errors
    if field_info["required"] and (value is None or value == ""):
        errors[field_name] += 1
        total_errors += 1
        return False
    if value and not isinstance(value, field_info["type"]):
        errors[field_name] += 1
        total_errors += 1
        return False
    if field_name == "stop_type" and value and len(value) > 1:
        errors[field_name] += 1
        total_errors += 1
        return False
    if field_name == "a_time" and not time_pattern.match(value):
        errors[field_name] += 1
        total_errors += 1
        return False
    return True

for record in data:
    for field_name, field_info in schema.items():
        value = record.get(field_name)
        validate_field(field_name, value, field_info)

print(f"Type and required field validation: {total_errors} errors")
for field, count in errors.items():
    print(f"{field}: {count}")