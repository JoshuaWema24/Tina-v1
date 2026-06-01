def build_response(parts: list) -> str:

    cleaned = []

    for part in parts:

        if not part:
            continue

        if isinstance(part, str):
            cleaned.append(part.strip())

        elif isinstance(part, dict):
            reply = part.get("reply")

            if reply:
                cleaned.append(reply.strip())

    return "\n\n".join(cleaned).strip()
