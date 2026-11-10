"""Formatting and structural checks for Goldbach certificates."""


def format_witness(n: int, p: int, q: int) -> str:
    """Serialize one decomposition as it appears in the certificate."""
    return f"{n} = {p} + {q}"


def is_ordered_pair(n: int, p: int, q: int) -> bool:
    """Check ordering and the sum invariant; primality is checked by the caller."""
    return p >= 2 and q >= p and p + q == n


def format_interval(lo: float, hi: float, digits: int = 6) -> str:
    """Render a certified interval for the report."""
    return f"[{lo:.{digits}f}, {hi:.{digits}f}]"


def short_digest(digest: str, length: int = 16) -> str:
    """Shorten a hexadecimal digest for display."""
    if length <= 0:
        raise ValueError("digest length must be positive")
    return digest[:length]
