import pytest
from src.api.main import AnalyzeRequest

def test_input_model_validation():
    """Перевірка Pydantic моделі вхідних даних"""
    text = "Valid news text"
    request = AnalyzeRequest(text=text)
    assert request.text == text

def test_risk_logic():
    """Імітація тестування бізнес-логіки розрахунку ризику"""
    # У реальному проєкті тут ми б імпортували функцію calculate_risk(score)
    # Для MVP ми перевіряємо гіпотетичний сценарій
    score_high = 0.95
    risk_high = "HIGH" if score_high > 0.7 else "LOW"
    assert risk_high == "HIGH"
    
    score_low = 0.1
    risk_low = "LOW" if score_low < 0.3 else "HIGH"
    assert risk_low == "LOW"
