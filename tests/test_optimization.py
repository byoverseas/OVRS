from app.analytics.schemas import CampaignIn
from app.analytics.services import compute_metrics, get_optimization_tips


def test_high_cpa_tip():
    data = CampaignIn(platform="google", impressions=1000, clicks=100, spend=1000, revenue=1000, conversions=5)
    metrics = compute_metrics(data)
    tips = get_optimization_tips(metrics)
    assert any("High CPA" in tip for tip in tips)


def test_low_ctr_tip():
    data = CampaignIn(platform="tiktok", impressions=1000, clicks=5, spend=10, revenue=20, conversions=1)
    metrics = compute_metrics(data)
    tips = get_optimization_tips(metrics)
    assert any("Low CTR" in tip for tip in tips)
