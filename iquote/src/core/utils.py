from typing import Optional

from pydantic import PostgresDsn


class CustomPostgresDsn(PostgresDsn):
    @classmethod
    def build(
        cls,
        *,
        scheme: str,
        user: Optional[str] = None,
        password: Optional[str] = None,
        host: str,
        port: Optional[str] = None,
        path: Optional[str] = None,
        query: Optional[str] = None,
        fragment: Optional[str] = None,
        **_kwargs: str,
    ) -> str:
        parts = Parts(
            scheme=scheme,
            user=user,
            password=password,
            host=host,
            port=port,
            path=path,
            query=query,
            fragment=fragment,
            **_kwargs,  # type: ignore[misc]
        )

        url = scheme + "://"
        if user:
            url += user
        if password:
            url += ":" + password
        if user or password:
            url += "@"
        url += host
        if port and (
            "port" not in cls.hidden_parts
            or cls.get_default_parts(parts).get("port") != port
        ):
            url += ":" + port
        if path:
            url += path
        if query:
            url += "?" + query
        if fragment:
            url += "#" + fragment
        return url
