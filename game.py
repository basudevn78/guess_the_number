from flask import Flask, render_template, request, redirect, url_for
import random

game = Flask(__name__)

# Initialize Global Variables
target = random.randint(1, 100)  # Random number between 1 and 100
attempts = 0                     # Number of attempts counting
high_score = None                # High score 

# Main Route: Game Logic
@game.route("/", methods=["GET", "POST"])
def index():
    global target, attempts, high_score
    message = ""

    if request.method == "POST":
        # If user clicks the Quit button
        if "quit" in request.form:
            message = f"____GAME OVER____ (Target was {target})"
            return render_template("index.html", message=message, game_over=True, attempts=attempts, high_score=high_score)
        
        # Handle Guess Submission
        choice = request.form.get("guess")
        if choice:
            attempts += 1
            choice = int(choice)

            if choice == target:
                # Correct Guess
                message = f"Correct Guess in {attempts} attempts!"
                # Update high score if needed
                if high_score is None or attempts < high_score:
                    high_score = attempts
                return render_template("index.html", message=message, game_over=True, attempts=attempts, high_score=high_score)
            elif choice < target:
                # Guess is too small
                message = "Your guess was too small. Take a bigger guess...."
            else:
                # Guess is too big
                message = "Your guess was too big. Take a smaller guess...."

    # Render the page with updated message and stats
    return render_template("index.html", message=message, game_over=False, attempts=attempts, high_score=high_score)

# Route to handle user feedback after game over
@game.route("/feedback", methods=["POST"])
def feedback():
    fb = request.form.get("feedback")
    print(f"Feedback Received: {fb}")
    # Reset the game after receiving feedback
    reset_game()
    return redirect(url_for('index'))

# Function to reset the game
def reset_game():
    global target, attempts
    target = random.randint(1, 100)  # Generate new random number
    attempts = 0                     # Reset attempt counter

# Run the Flask application
if __name__ == "__main__":
    game.run(debug=True)
