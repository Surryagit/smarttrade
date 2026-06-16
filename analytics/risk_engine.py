import numpy as np
import pandas as pd
import yfinance as yf

def get_stock_returns(symbol, period='1y'):
    """Download historical prices and calculate daily returns"""
    ticker = yf.Ticker(symbol)
    hist = ticker.history(period=period)
    if hist.empty:
        return None
    returns = hist['Close'].pct_change().dropna()
    return returns

def calculate_risk_metrics(symbol):
    """Calculate all risk metrics for a single stock"""
    returns = get_stock_returns(symbol)
    if returns is None or len(returns) == 0:
        return None

    # Annualized metrics (252 trading days in a year)
    avg_return = returns.mean() * 252
    volatility = returns.std() * np.sqrt(252)

    # Sharpe Ratio (return per unit of risk, risk free rate ~5%)
    risk_free_rate = 0.05
    sharpe_ratio = (avg_return - risk_free_rate) / volatility if volatility > 0 else 0

    # Maximum Drawdown (biggest drop from peak)
    cumulative = (1 + returns).cumprod()
    rolling_max = cumulative.cummax()
    drawdown = (cumulative - rolling_max) / rolling_max
    max_drawdown = drawdown.min()

    # Beta (how much stock moves vs market)
    market_returns = get_stock_returns('^GSPC')  # S&P 500
    if market_returns is not None:
        aligned = pd.concat([returns, market_returns], axis=1).dropna()
        if len(aligned) > 10:
            covariance = aligned.cov().iloc[0, 1]
            market_variance = aligned.iloc[:, 1].var()
            beta = covariance / market_variance if market_variance > 0 else 1
        else:
            beta = 1
    else:
        beta = 1

    # Risk Score (0-100, higher = riskier)
    risk_score = min(100, max(0,
        (volatility * 100 * 0.4) +
        (abs(max_drawdown) * 100 * 0.3) +
        (abs(beta - 1) * 20 * 0.3)
    ))

    # Risk Label
    if risk_score < 30:
        risk_label = 'Low'
    elif risk_score < 60:
        risk_label = 'Medium'
    else:
        risk_label = 'High'

    return {
        'symbol': symbol,
        'annual_return_pct': round(avg_return * 100, 2),
        'volatility_pct': round(volatility * 100, 2),
        'sharpe_ratio': round(sharpe_ratio, 2),
        'max_drawdown_pct': round(max_drawdown * 100, 2),
        'beta': round(beta, 2),
        'risk_score': round(risk_score, 2),
        'risk_label': risk_label,
    }

def analyze_portfolio_risk(symbols):
    """Analyze risk for entire portfolio"""
    results = []
    total_risk = 0

    for symbol in symbols:
        metrics = calculate_risk_metrics(symbol)
        if metrics:
            results.append(metrics)
            total_risk += metrics['risk_score']

    if not results:
        return None

    avg_risk = total_risk / len(results)

    if avg_risk < 30:
        portfolio_risk_label = 'Low Risk Portfolio'
        recommendation = 'Your portfolio is conservative and stable.'
    elif avg_risk < 60:
        portfolio_risk_label = 'Medium Risk Portfolio'
        recommendation = 'Your portfolio has moderate risk. Consider diversifying.'
    else:
        portfolio_risk_label = 'High Risk Portfolio'
        recommendation = 'Your portfolio is aggressive. Consider adding stable assets.'

    return {
        'stocks': results,
        'portfolio_risk_score': round(avg_risk, 2),
        'portfolio_risk_label': portfolio_risk_label,
        'recommendation': recommendation,
    }