"""
Streamlit Chat Interface (UI Prototype & Placeholder).

This module provides the frontend chat interface for the university assistant.
Currently running in placeholder mode with a mock backend adapter adhering to the
contract specified in `ui/README.md`.
"""

from __future__ import annotations

import time
from typing import Any, Dict, List, TypedDict
import streamlit as st


class ChatMessage(TypedDict):
    """Schema for stored chat history items."""
    role: str
    content: str
    sources: List[str]


class BackendClient:
    """
    Adapter client handling communication between UI and Backend service.
    
    In future iterations, this will execute HTTP requests to the backend 
    endpoint (e.g., POST /chat). Currently returns placeholder mock data.
    """

    @staticmethod
    def send_message(message: str) -> Dict[str, Any]:
        """
        Simulate sending a message payload to the backend service.

        Args:
            message (str): The raw text submitted by the user.

        Returns:
            Dict[str, Any]: JSON payload containing 'reply' and 'sources'.
        """
        # Simulated network latency for realistic UX
        time.sleep(0.4)

        # Standard response contract as defined in ui/README.md
        return {
            "reply": (
                f"This is a placeholder response for: \"{message}\". "
                "Backend services (office lookup & AI query engine) will be connected soon."
            ),
            "sources": [
                "docs/ui-mockup.png",
                "ui/README.md",
            ],
        }


def initialize_session_state() -> None:
    """Initialize necessary Streamlit session state keys if not already set."""
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {
                "role": "assistant",
                "content": (
                    "Hello! I am your University Campus Assistant. "
                    "How can I help you find departments, offices, or services today?"
                ),
                "sources": [],
            }
        ]


def render_sidebar() -> None:
    """Render sidebar information, status indicators, and control buttons."""
    with st.sidebar:
        st.header("⚙️ System Status")
        st.status("UI Placeholder Mode Active", state="complete")
        
        st.markdown(
            """
            **Component Info:**
            - **Target Framework:** Streamlit
            - **Contract:** JSON over `POST /chat`
            - **Backend Status:** Mock Adapter
            """
        )

        st.divider()

        if st.button("🗑️ Clear Conversation", use_container_width=True):
            st.session_state.messages = []
            initialize_session_state()
            st.rerun()


def render_chat_history() -> None:
    """Iterate and display previous messages and citations in the chat container."""
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            if message.get("sources"):
                with st.expander("📚 Sources & References", expanded=False):
                    for src in message["sources"]:
                        st.caption(f"• `{src}`")


def main() -> None:
    """Main entry point for running the Streamlit chat application."""
    st.set_page_config(
        page_title="Campus Assistant - Chat",
        page_icon="💬",
        layout="centered",
        initial_sidebar_state="auto",
    )

    initialize_session_state()
    render_sidebar()

    st.title("💬 University Assistant")
    st.caption("Interactive chat placeholder for campus queries, offices, and rules.")

    render_chat_history()

    # User Input box
    if prompt := st.chat_input("Ask a question about campus offices or services..."):
        # 1. Render and store user message
        st.session_state.messages.append(
            {"role": "user", "content": prompt, "sources": []}
        )
        with st.chat_message("user"):
            st.markdown(prompt)

        # 2. Query the backend adapter
        with st.chat_message("assistant"):
            with st.spinner("Processing request..."):
                backend_response = BackendClient.send_message(prompt)
                reply_text = backend_response.get("reply", "")
                sources = backend_response.get("sources", [])

                st.markdown(reply_text)
                if sources:
                    with st.expander("📚 Sources & References", expanded=False):
                        for src in sources:
                            st.caption(f"• `{src}`")

        # 3. Persist assistant reply to history
        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": reply_text,
                "sources": sources,
            }
        )


if __name__ == "__main__":
    main()