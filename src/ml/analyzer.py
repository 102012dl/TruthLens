"""
TruthLens - Main Analyzer Module
================================
ML/NLP Engine for credibility analysis

Author: 102012dl
Email: 102012dl@gmail.com
"""

import re
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any
from enum import Enum
import asyncio


class Sentiment(str, Enum):
    """Sentiment classification"""
    POSITIVE = "positive"
    NEGATIVE = "negative"
    NEUTRAL = "neutral"
    MIXED = "mixed"


class BiasType(str, Enum):
    """Types of detected bias"""
    POLITICAL_LEFT = "political_left"
    POLITICAL_RIGHT = "political_right"
    EMOTIONAL = "emotional"
    SENSATIONALIST = "sensationalist"
    NONE = "none"


class ManipulativeTechnique(str, Enum):
    """Types of manipulative techniques"""
    CLICKBAIT = "clickbait"
    EMOTIONAL_APPEAL = "emotional_appeal"
    FALSE_DICHOTOMY = "false_dichotomy"
    APPEAL_TO_FEAR = "appeal_to_fear"
    CHERRY_PICKING = "cherry_picking"
    MISLEADING_STATISTICS = "misleading_statistics"
    AD_HOMINEM = "ad_hominem"
    STRAWMAN = "strawman"
    BANDWAGON = "bandwagon"
    APPEAL_TO_AUTHORITY = "appeal_to_authority"


@dataclass
class FactCheck:
    """Fact check result"""
    claim: str
    verdict: str  # "true", "false", "partially_true", "unverified"
    confidence: float
    sources: List[str] = field(default_factory=list)
    explanation: str = ""


@dataclass
class AnalysisResult:
    """Complete analysis result"""
    # Core scores
    credibility_score: int  # 0-100
    verdict: str  # "credible", "likely_true", "uncertain", "likely_false", "false"
    
    # Sentiment analysis
    sentiment: Sentiment
    sentiment_score: float  # -1.0 to 1.0
    
    # Bias detection
    bias_level: str  # "none", "low", "medium", "high"
    bias_score: float  # 0.0 to 1.0
    bias_types: List[BiasType] = field(default_factory=list)
    
    # Manipulative techniques
    manipulative_techniques: List[ManipulativeTechnique] = field(default_factory=list)
    manipulation_score: float = 0.0
    
    # Fact checking
    fact_checks: List[FactCheck] = field(default_factory=list)
    
    # Source analysis
    source_credibility: Optional[float] = None
    source_name: Optional[str] = None
    
    # Key findings and recommendations
    key_findings: List[str] = field(default_factory=list)
    recommendations: List[str] = field(default_factory=list)
    
    # Metadata
    language: str = "en"
    processing_time_ms: int = 0
    model_version: str = "1.0.0"


class TruthLensAnalyzer:
    """
    Main analyzer class for TruthLens platform.
    
    Combines multiple ML/NLP models for comprehensive 
    credibility analysis of text content.
    
    Components:
    - Sentiment Analysis (TextBlob/BERT)
    - Bias Detection (Custom classifier)
    - Manipulative Technique Detection
    - Fact Checking (RAG-based)
    - Source Verification
    """
    
    # Emotional/sensational words
    EMOTIONAL_WORDS = {
        'shocking', 'unbelievable', 'incredible', 'amazing', 'terrifying',
        'horrifying', 'devastating', 'explosive', 'breaking', 'urgent',
        'scandal', 'exposed', 'revealed', 'secret', 'hidden', 'banned',
        'miracle', 'stunning', 'outrageous', 'disgusting', 'horrific'
    }
    
    # Clickbait patterns
    CLICKBAIT_PATTERNS = [
        r"you won't believe",
        r"what happens next",
        r"\d+ reasons why",
        r"this is why",
        r"here's what",
        r"the truth about",
        r"\?\!+$",
        r"!!!+",
        r"doctors hate",
        r"one weird trick"
    ]
    
    # Known reliable sources
    RELIABLE_SOURCES = {
        'reuters.com': 0.95,
        'apnews.com': 0.95,
        'bbc.com': 0.90,
        'bbc.co.uk': 0.90,
        'nytimes.com': 0.85,
        'theguardian.com': 0.85,
        'washingtonpost.com': 0.85,
        'nature.com': 0.95,
        'science.org': 0.95,
        'who.int': 0.95,
        'cdc.gov': 0.95,
        'un.org': 0.90
    }
    
    # Known unreliable sources
    UNRELIABLE_SOURCES = {
        'infowars.com': 0.1,
        'naturalnews.com': 0.15,
        'beforeitsnews.com': 0.1
    }
    
    def __init__(self, use_gpu: bool = False):
        """Initialize the analyzer."""
        self.use_gpu = use_gpu
        self._models_loaded = False
        self._llm_client = None
    
    async def load_models(self):
        """Load ML models (lazy loading)."""
        if self._models_loaded:
            return
        
        # In production, load actual models here:
        # - transformers for BERT
        # - spacy for NLP
        # - custom trained models
        
        self._models_loaded = True
    
    async def analyze(self, text: str, url: Optional[str] = None) -> AnalysisResult:
        """
        Perform comprehensive credibility analysis.
        
        Args:
            text: Text content to analyze
            url: Optional source URL
            
        Returns:
            AnalysisResult with all analysis components
        """
        import time
        start_time = time.time()
        
        # Preprocess text
        cleaned_text = self._preprocess(text)
        
        # Run all analysis components
        sentiment, sentiment_score = self._analyze_sentiment(cleaned_text)
        bias_level, bias_score, bias_types = self._detect_bias(cleaned_text)
        techniques, manipulation_score = self._detect_manipulation(cleaned_text)
        
        # Source analysis
        source_cred = None
        source_name = None
        if url:
            source_cred, source_name = self._analyze_source(url)
        
        # Calculate credibility score
        credibility_score = self._calculate_credibility(
            sentiment_score=sentiment_score,
            bias_score=bias_score,
            manipulation_score=manipulation_score,
            source_credibility=source_cred
        )
        
        # Determine verdict
        verdict = self._get_verdict(credibility_score)
        
        # Generate findings and recommendations
        key_findings = self._generate_findings(
            credibility_score, sentiment, bias_level, techniques
        )
        recommendations = self._generate_recommendations(
            credibility_score, bias_level, techniques
        )
        
        processing_time = int((time.time() - start_time) * 1000)
        
        return AnalysisResult(
            credibility_score=credibility_score,
            verdict=verdict,
            sentiment=sentiment,
            sentiment_score=sentiment_score,
            bias_level=bias_level,
            bias_score=bias_score,
            bias_types=bias_types,
            manipulative_techniques=techniques,
            manipulation_score=manipulation_score,
            source_credibility=source_cred,
            source_name=source_name,
            key_findings=key_findings,
            recommendations=recommendations,
            processing_time_ms=processing_time
        )
    
    def _preprocess(self, text: str) -> str:
        """Preprocess text for analysis."""
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        return text
    
    def _analyze_sentiment(self, text: str) -> tuple[Sentiment, float]:
        """Analyze sentiment of text."""
        text_lower = text.lower()
        
        # Simple keyword-based sentiment (replace with BERT in production)
        positive_words = {'good', 'great', 'excellent', 'positive', 'success', 
                         'achievement', 'progress', 'improve', 'benefit'}
        negative_words = {'bad', 'terrible', 'fail', 'crisis', 'disaster',
                         'problem', 'danger', 'threat', 'fear', 'death'}
        
        words = set(text_lower.split())
        pos_count = len(words & positive_words)
        neg_count = len(words & negative_words)
        
        total = pos_count + neg_count or 1
        score = (pos_count - neg_count) / total
        
        if score > 0.2:
            return Sentiment.POSITIVE, score
        elif score < -0.2:
            return Sentiment.NEGATIVE, score
        elif pos_count > 0 and neg_count > 0:
            return Sentiment.MIXED, score
        else:
            return Sentiment.NEUTRAL, score
    
    def _detect_bias(self, text: str) -> tuple[str, float, List[BiasType]]:
        """Detect bias in text."""
        text_lower = text.lower()
        bias_types = []
        bias_score = 0.0
        
        # Check for emotional language
        emotional_count = sum(1 for word in self.EMOTIONAL_WORDS 
                             if word in text_lower)
        if emotional_count > 3:
            bias_types.append(BiasType.EMOTIONAL)
            bias_score += 0.3
        
        # Check for sensationalism
        if any(re.search(pattern, text_lower) for pattern in self.CLICKBAIT_PATTERNS):
            bias_types.append(BiasType.SENSATIONALIST)
            bias_score += 0.3
        
        # Normalize score
        bias_score = min(bias_score, 1.0)
        
        # Determine level
        if bias_score < 0.2:
            level = "none"
        elif bias_score < 0.4:
            level = "low"
        elif bias_score < 0.7:
            level = "medium"
        else:
            level = "high"
        
        return level, bias_score, bias_types
    
    def _detect_manipulation(self, text: str) -> tuple[List[ManipulativeTechnique], float]:
        """Detect manipulative techniques in text."""
        techniques = []
        text_lower = text.lower()
        
        # Clickbait detection
        if any(re.search(p, text_lower) for p in self.CLICKBAIT_PATTERNS):
            techniques.append(ManipulativeTechnique.CLICKBAIT)
        
        # Emotional appeal
        emotional_count = sum(1 for w in self.EMOTIONAL_WORDS if w in text_lower)
        if emotional_count >= 2:
            techniques.append(ManipulativeTechnique.EMOTIONAL_APPEAL)
        
        # Appeal to fear
        fear_words = {'danger', 'threat', 'risk', 'warning', 'alert', 'emergency'}
        if sum(1 for w in fear_words if w in text_lower) >= 2:
            techniques.append(ManipulativeTechnique.APPEAL_TO_FEAR)
        
        # Calculate manipulation score
        score = len(techniques) * 0.2
        return techniques, min(score, 1.0)
    
    def _analyze_source(self, url: str) -> tuple[Optional[float], Optional[str]]:
        """Analyze source credibility."""
        from urllib.parse import urlparse
        
        try:
            domain = urlparse(url).netloc.lower()
            domain = domain.replace('www.', '')
            
            # Check known sources
            if domain in self.RELIABLE_SOURCES:
                return self.RELIABLE_SOURCES[domain], domain
            elif domain in self.UNRELIABLE_SOURCES:
                return self.UNRELIABLE_SOURCES[domain], domain
            else:
                return 0.5, domain  # Unknown source
        except:
            return None, None
    
    def _calculate_credibility(self, sentiment_score: float, bias_score: float,
                               manipulation_score: float, 
                               source_credibility: Optional[float]) -> int:
        """Calculate overall credibility score."""
        # Base score
        base_score = 70
        
        # Adjust for bias (high bias reduces credibility)
        base_score -= int(bias_score * 20)
        
        # Adjust for manipulation
        base_score -= int(manipulation_score * 25)
        
        # Adjust for source credibility
        if source_credibility is not None:
            if source_credibility > 0.8:
                base_score += 15
            elif source_credibility > 0.5:
                base_score += 5
            elif source_credibility < 0.3:
                base_score -= 20
        
        # Clamp to 0-100
        return max(0, min(100, base_score))
    
    def _get_verdict(self, score: int) -> str:
        """Get verdict based on credibility score."""
        if score >= 80:
            return "credible"
        elif score >= 60:
            return "likely_true"
        elif score >= 40:
            return "uncertain"
        elif score >= 20:
            return "likely_false"
        else:
            return "false"
    
    def _generate_findings(self, score: int, sentiment: Sentiment,
                          bias_level: str, techniques: List) -> List[str]:
        """Generate key findings."""
        findings = []
        
        if score >= 70:
            findings.append("Content appears to be credible")
        elif score >= 50:
            findings.append("Content has mixed credibility indicators")
        else:
            findings.append("Content shows signs of misinformation")
        
        if bias_level in ['medium', 'high']:
            findings.append(f"Detected {bias_level} level of bias")
        
        if techniques:
            tech_names = [t.value.replace('_', ' ') for t in techniques[:3]]
            findings.append(f"Manipulative techniques detected: {', '.join(tech_names)}")
        
        if sentiment == Sentiment.NEGATIVE:
            findings.append("Content has predominantly negative tone")
        
        return findings
    
    def _generate_recommendations(self, score: int, bias_level: str,
                                  techniques: List) -> List[str]:
        """Generate recommendations for user."""
        recs = []
        
        if score < 60:
            recs.append("Verify information from multiple reliable sources")
            recs.append("Check official sources for confirmation")
        
        if bias_level in ['medium', 'high']:
            recs.append("Be aware of potential bias in the content")
            recs.append("Seek alternative perspectives on this topic")
        
        if techniques:
            recs.append("Be cautious of emotional manipulation in the text")
        
        if not recs:
            recs.append("Information appears reliable")
            recs.append("Continue to verify important claims")
        
        return recs


# Factory function
def create_analyzer(use_gpu: bool = False) -> TruthLensAnalyzer:
    """Create and return a TruthLens analyzer instance."""
    return TruthLensAnalyzer(use_gpu=use_gpu)
