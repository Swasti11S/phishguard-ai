# feature_extraction.py
# ---------------------
# This module extracts numerical features from a URL
# that help the ML model determine if it's phishing or safe.

import re

# Keywords commonly found in phishing URLs
SUSPICIOUS_KEYWORDS = [
    'login', 'signin', 'verify', 'secure', 'account', 'update',
    'confirm', 'banking', 'password', 'credential', 'suspend',
    'alert', 'urgent', 'free', 'prize', 'winner', 'claim',
    'paypal', 'amazon', 'apple', 'microsoft', 'google', 'netflix',
    'ebay', 'bank', 'refund', 'invoice', 'payment', 'wallet'
]

def has_ip_address(url):
    """Check if the URL contains an IP address instead of a domain name."""
    # IPv4 pattern: matches strings like 192.168.1.1
    ip_pattern = re.compile(
        r'(([01]?\d\d?|2[0-4]\d|25[0-5])\.){3}([01]?\d\d?|2[0-4]\d|25[0-5])'
    )
    return 1 if ip_pattern.search(url) else 0

def count_dots(url):
    """Count the number of dots in the URL (more dots = more suspicious)."""
    return url.count('.')

def has_at_symbol(url):
    """Check for @ symbol — used in phishing to redirect browsers."""
    return 1 if '@' in url else 0

def is_https(url):
    """Check if the URL uses HTTPS (safe sites usually do)."""
    return 1 if url.startswith('https://') else 0

def url_length(url):
    """Return the length of the URL (long URLs are often phishing)."""
    return len(url)

def count_suspicious_keywords(url):
    """Count how many suspicious keywords appear in the URL."""
    url_lower = url.lower()
    return sum(1 for keyword in SUSPICIOUS_KEYWORDS if keyword in url_lower)

def count_hyphens(url):
    """Count hyphens — phishing domains often use hyphens."""
    return url.count('-')

def count_subdomains(url):
    """Count the number of subdomains (more subdomains = more suspicious)."""
    # Remove protocol prefix before counting
    stripped = re.sub(r'https?://', '', url)
    domain_part = stripped.split('/')[0]
    parts = domain_part.split('.')
    # Subtract 2 for the main domain + TLD
    return max(0, len(parts) - 2)

def extract_features(url):
    """
    Main function: Extract all features from a URL and return as a list.
    This list is fed directly into the ML model for prediction.
    """
    features = [
        url_length(url),           # Feature 1: URL length
        has_ip_address(url),       # Feature 2: IP address present?
        count_dots(url),           # Feature 3: Number of dots
        has_at_symbol(url),        # Feature 4: @ symbol present?
        is_https(url),             # Feature 5: Uses HTTPS?
        count_suspicious_keywords(url),  # Feature 6: Suspicious keyword count
        count_hyphens(url),        # Feature 7: Number of hyphens
        count_subdomains(url),     # Feature 8: Number of subdomains
    ]
    return features
