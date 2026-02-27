import os
from typing import Dict, Any

from langchain_groq import ChatGroq
from langchain_experimental.agents import create_pandas_dataframe_agent

from backend.data_loader import get_dataframe
from backend.tools import generate_chart

from dotenv import load_dotenv
import os

load_dotenv()  # This loads .env file


class TitanicAgent:
    def __init__(self):
        self.df = get_dataframe()

        self.llm = ChatGroq(
            temperature=0,
            model="llama-3.3-70b-versatile",
            api_key=os.getenv("GROQ_API_KEY")
        )

        self.agent = create_pandas_dataframe_agent(
            self.llm,
            self.df,
            verbose=False,
            allow_dangerous_code=True
        )

    def needs_chart(self, message: str) -> Dict[str, Any]:
        """
        Simple rule-based detection for visualization.
        """
        message_lower = message.lower()

        if "histogram" in message_lower:
            return {"type": "histogram"}
        if "bar" in message_lower:
            return {"type": "bar"}
        if "distribution" in message_lower:
            return {"type": "histogram"}
        return {}

    def extract_column_name(self, message: str) -> str:
        """
        Very simple column detection logic.
        """
        for col in self.df.columns:
            if col.lower() in message.lower():
                return col
        raise ValueError("No valid column detected in question.")

    def run(self, message: str) -> Dict[str, Any]:
        """
        Execute query and optionally generate chart.
        """
        chart_info = self.needs_chart(message)

        answer = self.agent.run(message)

        chart_image = None

        if chart_info:
            column = self.extract_column_name(message)
            chart_image = generate_chart(
                chart_type=chart_info["type"],
                column_name=column,
                df=self.df
            )

        return {
            "answer": answer,
            "chart": chart_image
        }