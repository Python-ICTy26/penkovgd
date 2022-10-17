def get_greeting(name: str) -> str:
    greeting = "Hello, %s!" % name
    return greeting


if __name__ == "__main__":
    message = get_greeting("World")
    print(message)
