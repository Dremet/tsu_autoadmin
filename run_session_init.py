
commands = [
]

with open("session_init_generated.src", "w", encoding="utf-8-sig") as file:
    file.write("\n".join(commands) + "\n")

