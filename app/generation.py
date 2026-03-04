from __future__ import annotations

from typing import Optional
from pydantic.dataclasses import dataclass
from app.prompts import build_messages, FALLBACK_IDE
from app.llm import call_openai_chat

@dataclass
class GenerationConfig:
    provider: str = "openai"
    model: str = "gpt-4o-mini"
    temperature: float = 0.0
    max_tokens: int = 500
    max_context_chars: int = 12000
    empty_context_fallback: str = "I donot know based on the context provided."


class AnswerGenerator:

    def __init__(self, config: Optional[GenerationConfig] = None):
        """ Loads config parameters"""
        self.cofig = config or GenerationConfig()
    
    def _normalize_text(self, s: str) -> str:
        """ensures not empty"""
        return (s or "").strip()
    
    def _truncate_context(self, context: str) -> str:
        """Truncates beyond max tokens permitted"""
        context = self._normalize_text(context)
        if len(context) <= self.cofig.max_context_chars:
            return context
        return context[: self.cofig.max_context_chars].rstrip() + "\n\n[Context Truncated]"
    
    def generate_answer(self, question: str, context: str) -> str:
        """Gathers parameters, context, question and attach to prmopt, finally sends to openai. Returns answer unless empty."""
        question = self._normalize_text(question)
        if not question:
            raise ValueError("Question canot be empty.")
        
        context = self._truncate_context(context)
        if not context:
            return self.cofig.empty_context_fallback
        
        messages = build_messages(question=question, context=context)

        answer = call_openai_chat(messages=messages,
                                  model=self.cofig.model,
                                  temperature=self.cofig.temperature,
                                  max_tokens=self.cofig.max_tokens)
        
        
        answer = self._normalize_text(answer)
        return answer or self.cofig.empty_context_fallback

# if __name__ == "__main__":
#     gen = AnswerGenerator()
#     fake_context = "RAG stands for Retrieval-Augmented Generation."
#     ans = gen.generate_answer("What does RAG stand for?", fake_context)
#     print("Answer:", ans)

#     ans2 = gen.generate_answer("What is the CEO name?", "")
#     print("Empty-context answer:", ans2)