from pydantic import AnyHttpUrl, field_validator
from typing import Optional

def validate_http_url(value: Optional[str]) -> Optional[str]:
    if value:
        AnyHttpUrl.validate(value)
        return value
