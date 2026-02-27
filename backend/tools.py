import io
import base64
import matplotlib.pyplot as plt
import pandas as pd


def generate_chart(chart_type: str, column_name: str, df: pd.DataFrame) -> str:
    """
    Generate a chart and return base64 encoded image string.
    """
    plt.figure()

    if column_name not in df.columns:
        raise ValueError(f"Column '{column_name}' not found in dataset.")

    if chart_type == "histogram":
        df[column_name].dropna().hist()
        plt.title(f"Histogram of {column_name}")
    elif chart_type == "bar":
        df[column_name].value_counts().plot(kind="bar")
        plt.title(f"Bar Chart of {column_name}")
    else:
        raise ValueError("Unsupported chart type")

    buffer = io.BytesIO()
    plt.savefig(buffer, format="png")
    buffer.seek(0)
    image_base64 = base64.b64encode(buffer.read()).decode("utf-8")
    plt.close()

    return image_base64