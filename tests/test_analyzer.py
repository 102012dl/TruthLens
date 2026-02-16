"""
TruthLens - Analyzer Unit Tests
===============================
Author: 102012dl
"""

import pytest
import asyncio
from src.ml.analyzer import (
    TruthLensAnalyzer,
    create_analyzer,
    Sentiment,
    BiasType,
    ManipulativeTechnique,
    AnalysisResult
)


class TestTruthLensAnalyzer:
    """Test suite for TruthLensAnalyzer"""
    
    @pytest.fixture
    def analyzer(self):
        """Create analyzer instance."""
        return create_analyzer()
    
    @pytest.mark.asyncio
    async def test_analyzer_creation(self, analyzer):
        """Test analyzer can be created."""
        assert analyzer is not None
        assert isinstance(analyzer, TruthLensAnalyzer)
    
    @pytest.mark.asyncio
    async def test_analyze_credible_text(self, analyzer):
        """Test analysis of credible text."""
        text = """
        According to a study published in Nature, researchers have found 
        evidence of a new treatment for cancer. The study was conducted 
        at Harvard Medical School and peer-reviewed by independent experts.
        """
        
        result = await analyzer.analyze(text)
        
        assert result is not None
        assert isinstance(result, AnalysisResult)
        assert 0 <= result.credibility_score <= 100
        assert result.verdict in ['credible', 'likely_true', 'uncertain', 
                                   'likely_false', 'false']
    
    @pytest.mark.asyncio
    async def test_analyze_suspicious_text(self, analyzer):
        """Test analysis of suspicious text."""
        text = """
        SHOCKING!!! You won't believe what doctors don't want you to know!
        This miracle cure has been BANNED by the government! 
        Scientists EXPOSED for hiding the truth!!!
        """
        
        result = await analyzer.analyze(text)
        
        assert result is not None
        # Should detect manipulative techniques
        assert len(result.manipulative_techniques) > 0
        # Should have high bias
        assert result.bias_level in ['medium', 'high']
        # Score should be lower
        assert result.credibility_score < 70
    
    @pytest.mark.asyncio
    async def test_sentiment_analysis(self, analyzer):
        """Test sentiment analysis."""
        positive_text = "Great news! Excellent progress has been made."
        negative_text = "Terrible disaster caused massive problems."
        
        pos_result = await analyzer.analyze(positive_text)
        neg_result = await analyzer.analyze(negative_text)
        
        assert pos_result.sentiment == Sentiment.POSITIVE
        assert neg_result.sentiment == Sentiment.NEGATIVE
    
    @pytest.mark.asyncio
    async def test_source_analysis(self, analyzer):
        """Test source credibility analysis."""
        text = "Test article content"
        
        # Test with reliable source
        result_reliable = await analyzer.analyze(
            text, url="https://www.reuters.com/article"
        )
        assert result_reliable.source_credibility is not None
        assert result_reliable.source_credibility > 0.8
        
        # Test with unknown source
        result_unknown = await analyzer.analyze(
            text, url="https://random-news-site.com/article"
        )
        assert result_unknown.source_credibility == 0.5
    
    @pytest.mark.asyncio
    async def test_clickbait_detection(self, analyzer):
        """Test clickbait detection."""
        clickbait = "You won't believe what happens next! 10 reasons why this is shocking!"
        
        result = await analyzer.analyze(clickbait)
        
        assert ManipulativeTechnique.CLICKBAIT in result.manipulative_techniques
    
    @pytest.mark.asyncio
    async def test_key_findings_generated(self, analyzer):
        """Test that key findings are generated."""
        text = "This is a sample news article about recent events in technology."
        
        result = await analyzer.analyze(text)
        
        assert len(result.key_findings) > 0
        assert len(result.recommendations) > 0
    
    @pytest.mark.asyncio
    async def test_processing_time_recorded(self, analyzer):
        """Test that processing time is recorded."""
        text = "Sample text for analysis."
        
        result = await analyzer.analyze(text)
        
        assert result.processing_time_ms >= 0
    
    def test_preprocess_text(self, analyzer):
        """Test text preprocessing."""
        text = "  Multiple   spaces    and\n\nnewlines  "
        cleaned = analyzer._preprocess(text)
        
        assert "  " not in cleaned
        assert cleaned == "Multiple spaces and newlines"
    
    def test_verdict_mapping(self, analyzer):
        """Test verdict mapping based on score."""
        assert analyzer._get_verdict(85) == "credible"
        assert analyzer._get_verdict(70) == "likely_true"
        assert analyzer._get_verdict(50) == "uncertain"
        assert analyzer._get_verdict(30) == "likely_false"
        assert analyzer._get_verdict(10) == "false"


class TestAnalysisResultDataclass:
    """Test AnalysisResult dataclass."""
    
    def test_result_creation(self):
        """Test creating AnalysisResult."""
        result = AnalysisResult(
            credibility_score=75,
            verdict="likely_true",
            sentiment=Sentiment.NEUTRAL,
            sentiment_score=0.0,
            bias_level="low",
            bias_score=0.2
        )
        
        assert result.credibility_score == 75
        assert result.verdict == "likely_true"
        assert result.sentiment == Sentiment.NEUTRAL
    
    def test_result_defaults(self):
        """Test AnalysisResult default values."""
        result = AnalysisResult(
            credibility_score=50,
            verdict="uncertain",
            sentiment=Sentiment.NEUTRAL,
            sentiment_score=0.0,
            bias_level="none",
            bias_score=0.0
        )
        
        assert result.manipulative_techniques == []
        assert result.fact_checks == []
        assert result.key_findings == []
        assert result.recommendations == []
        assert result.language == "en"
        assert result.model_version == "1.0.0"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
