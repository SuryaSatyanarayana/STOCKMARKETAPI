while True:
    try:
        # Code that may raise an exception
        number = float(input("Enter a number: "))
        result = 10 / number
        print("Result:", result)
    except ZeroDivisionError:
        # Code to handle the ZeroDivisionError exception
        print("Error: Cannot divide by zero. Please try again.")
    except ValueError:
        # Code to handle the ValueError exception (if the input is not a valid number)
        print("Error: Please enter a valid number.")
    except Exception as e:
        # Code to handle any other exceptions
        print("An unexpected error occurred:", e)
        break  # Exit the loop if an unexpected error occurs
