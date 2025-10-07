import random
import string

def generate_password(length):
    """Generate a random password of the specified length."""
    
    # Characters: uppercase, lowercase, digits, and symbols
    characters = string.ascii_letters + string.digits + string.punctuation
    
    # Create password using random choices
    password = ''.join(random.choice(characters) for _ in range(length))
    
    return password


def main():
    print("=== Python Password Generator ===")
    
    # Step 1: Get desired password length from user
    try:
        length = int(input("Enter the desired password length: "))
        
        if length <= 0:
            print("Please enter a positive number.")
            return
        
        # Step 2: Generate password
        password = generate_password(length)
        
        # Step 3: Display password
        print("\nYour Generated Password is:", password)
    
    except ValueError:
        print("Invalid input! Please enter a number.")


# Run the program
if __name__ == "__main__":
    main()
