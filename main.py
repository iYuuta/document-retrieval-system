from src.handleDocs import addHandler
from src.handleQuery import queryHandler

def main():
    while True:
        cmd = input("Usage: Enter a command (add or query or exit)-> ")
        if cmd == "add":
            addHandler()
        elif cmd == "query":
            queryHandler()
        elif cmd == "exit":
            return
        else:
            print("Error: invalid command")
    
if __name__ == "__main__":
    main()