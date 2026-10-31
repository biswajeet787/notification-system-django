
import re


def get_nested_value(data, path):
    """
    Get a value from nested dictionary data.

    Example:
    path = "user.name"
    data = {"user": {"name": "Biswajeet"}}
    result = "Biswajeet"
    """

    value = data

    for key in path.split("."):
        if not isinstance(value, dict) or key not in value:
            return ""

        value = value[key]

    return str(value) if value is not None else ""


def render_template(template_text, variable_mapping, context):
    """
    Replace template placeholders with actual values.

    Example:
    Template: "Hello {{name}}"
    Mapping: {"name": "user.name"}
    Context: {"user": {"name": "Biswajeet"}}
    Result: "Hello Biswajeet"
    """

    if not template_text:
        return ""

    variable_mapping = variable_mapping or {}
    context = context or {}

    def replace_variable(match):
        variable_name = match.group(1).strip()

        data_path = variable_mapping.get(variable_name)

        if not data_path:
            return match.group(0)

        value = get_nested_value(context, data_path)

        return value

    return re.sub(
        r"\{\{\s*(.*?)\s*\}\}",
        replace_variable,
        template_text
    )
