"""Custom exceptions for Search Agent."""

class SearchAgentError(Exception):
    """Base exception class for Search Agent."""
    pass

class RateLimitError(SearchAgentError):
    """Raised when rate limit is hit."""
    def __init__(self, message="Rate limit exceeded. Please try again later.", retry_after=None):
        self.retry_after = retry_after
        super().__init__(message)

class SearchError(SearchAgentError):
    """Raised when search operation fails."""
    def __init__(self, message="Search operation failed.", original_error=None):
        self.original_error = original_error
        super().__init__(message)

class ConfigurationError(SearchAgentError):
    """Raised when configuration is invalid."""
    pass
