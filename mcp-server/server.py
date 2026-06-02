from __future__ import annotations

import re
from pathlib import Path
from typing import List

from mcp.server.fastmcp import FastMCP

ROOT = Path(__file__).resolve().parents[1]
README = ROOT / "README.md"

mcp = FastMCP("free-for-dev")


def _read_readme() -> str:
    if not README.exists():
        raise FileNotFoundError(f"README.md not found at {README}")
    return README.read_text(encoding="utf-8", errors="ignore")


def _slug(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r"[^a-z0-9\s-]", "", text)
    text = re.sub(r"\s+", "-", text)
    return text


def _sections() -> dict[str, str]:
    content = _read_readme()
    matches = list(re.finditer(r"^##\s+(.+?)\s*$", content, flags=re.MULTILINE))
    sections: dict[str, str] = {}
    for i, match in enumerate(matches):
        title = match.group(1).strip()
        start = match.start()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(content)
        sections[title] = content[start:end].strip()
    return sections


@mcp.tool()
def list_categories() -> List[str]:
    """List all free-for-dev README categories."""
    return list(_sections().keys())


@mcp.tool()
def get_category(category: str) -> str:
    """Return the full Markdown content for a matching category."""
    sections = _sections()
    wanted = category.lower().strip()

    for title, body in sections.items():
        if wanted == title.lower() or wanted == _slug(title):
            return body

    matches = [title for title in sections if wanted in title.lower()]
    if not matches:
        return f"No category found for: {category}"

    return "\n\n".join(sections[title] for title in matches[:3])


@mcp.tool()
def search_services(query: str, limit: int = 20) -> str:
    """Search the free-for-dev list and return matching service lines with category context."""
    query_clean = query.lower().strip()
    if not query_clean:
        return "Please provide a search query."

    results: list[str] = []
    for title, body in _sections().items():
        for line in body.splitlines():
            if query_clean in line.lower():
                clean_line = line.strip()
                if clean_line:
                    results.append(f"[{title}] {clean_line}")
            if len(results) >= limit:
                break
        if len(results) >= limit:
            break

    if not results:
        return f"No services found for: {query}"

    return "\n".join(results)


@mcp.tool()
def recommend_free_services(use_case: str, limit: int = 10) -> str:
    """Recommend free developer services by searching relevant keywords in the README."""
    keywords = [word.lower() for word in re.findall(r"[a-zA-Z0-9+#.-]{3,}", use_case)]
    if not keywords:
        return "Please describe your use case, for example: deploy a Python API for free."

    scored: list[tuple[int, str, str]] = []
    for title, body in _sections().items():
        for line in body.splitlines():
            lower = line.lower()
            score = sum(1 for keyword in keywords if keyword in lower)
            if score > 0 and line.strip().startswith("*"):
                scored.append((score, title, line.strip()))

    scored.sort(key=lambda item: item[0], reverse=True)
    if not scored:
        return f"No recommendation found for: {use_case}"

    return "\n".join(f"[{title}] {line}" for _, title, line in scored[:limit])


if __name__ == "__main__":
    mcp.run()
