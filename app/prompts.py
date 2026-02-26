

def build_rag_prompt(question: str, context: str) -> str:
    """instruction: “answer only from context; if missing say I don’t know”"""
    pass

def build_system_message() -> str:
    """(optional if using chat format)"""
    pass

def build_user_message(question: str, context: str) -> str:
    pass

def guardrail_text() -> str:
    pass