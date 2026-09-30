
from tkinter import *
import random



WIDTH = 500
HEIGHT = 600

root = Tk()
root.title("Fruit Catch Game")
root.resizable(False, False)

canvas = Canvas(
    root,
    width=WIDTH,
    height=HEIGHT,
    bg="purple"
)
canvas.pack()




apple = PhotoImage(file="apple.png").subsample(8, 8)
banana = PhotoImage(file="banana.png").subsample(8, 8)
strawberry = PhotoImage(file="strawberry.png").subsample(38, 38)
basket_img = PhotoImage(file="basket.png").subsample(5, 5)

bomb = PhotoImage(file="bomb.png").subsample(12, 12)
star = PhotoImage(file="star.png").subsample(12, 12)




score = 0
high_score = 0
lives = 3
level = 1
speed = 5

game_running = True
paused = False

fruit = None
fruit_value = 0
fruit_type = ""




score_text = canvas.create_text(
    60,
    20,
    text="Score: 0",
    font=("Arial", 14, "bold"),
    fill="white"
)

high_score_text = canvas.create_text(
    175,
    20,
    text="High Score: 0",
    font=("Arial", 14, "bold"),
    fill="white"
)

level_text = canvas.create_text(
    280,
    20,
    text="Level: 1",
    font=("Arial", 14, "bold"),
    fill="yellow"
)

lives_text = canvas.create_text(
    430,
    20,
    text="Lives: 3",
    font=("Arial", 14, "bold"),
    fill="white"
)


# -----------------------------
# BASKET
# -----------------------------

basket = canvas.create_image(
    250,
    560,
    image=basket_img
)




def left(event):
    if not game_running or paused:
        return

    x, y = canvas.coords(basket)

    if x > 40:
        canvas.move(basket, -20, 0)


def right(event):
    if not game_running or paused:
        return

    x, y = canvas.coords(basket)

    if x < 460:
        canvas.move(basket, 20, 0)


root.bind("<Left>", left)
root.bind("<Right>", right)



def create_fruit():
    global fruit
    global fruit_value
    global fruit_type

    # Normal fruits
    choices = [
        (apple, 1, "fruit"),
        (banana, 2, "fruit"),
        (strawberry, 3, "fruit")
    ]

    # Add bomb
    choices.append((bomb, 0, "bomb"))

    # Add bonus star
    choices.append((star, 5, "bonus"))

    img, fruit_value, fruit_type = random.choice(choices)

    x = random.randint(40, 460)

    fruit = canvas.create_image(
        x,
        40,
        image=img
    )




def update_level():
    global level
    global speed

    new_level = score // 10 + 1

    if new_level > level:

        level = new_level

        # Increase speed
        speed = 5 + (level - 1) * 2

        canvas.itemconfig(
            level_text,
            text=f"Level: {level}"
        )




def update_high_score():
    global high_score

    if score > high_score:
        high_score = score

        canvas.itemconfig(
            high_score_text,
            text=f"High Score: {high_score}"
        )




def fall():

    global score
    global lives
    global game_running
    global fruit

    if not game_running:
        return

    if paused:
        root.after(40, fall)
        return

    # Move object
    canvas.move(
        fruit,
        0,
        speed
    )

    # Get positions
    fx, fy = canvas.coords(fruit)
    bx, by = canvas.coords(basket)


    
    if abs(fx - bx) < 45 and abs(fy - by) < 30:

       

        if fruit_type == "bomb":

            lives -= 1

            canvas.itemconfig(
                lives_text,
                text=f"Lives: {lives}"
            )

        

        elif fruit_type == "bonus":

            score += 5

            canvas.itemconfig(
                score_text,
                text=f"Score: {score}"
            )

       

        else:

            score += fruit_value

            canvas.itemconfig(
                score_text,
                text=f"Score: {score}"
            )


        # Update high score
        update_high_score()

        # Remove object
        canvas.delete(fruit)


        # Check level
        update_level()


        # Check lives
        if lives <= 0:

            game_over()

            return


        # Create next object
        create_fruit()


    

    elif fy > HEIGHT:

        # Only fruits and bonus objects
        # reduce lives when missed.
        if fruit_type != "bomb":

            lives -= 1

            canvas.itemconfig(
                lives_text,
                text=f"Lives: {lives}"
            )


        canvas.delete(fruit)


        if lives <= 0:

            game_over()

            return


        create_fruit()


    # Continue game
    root.after(
        40,
        fall
    )




def pause_game(event=None):

    global paused

    if not game_running:
        return

    paused = not paused

    if paused:

        canvas.create_text(
            250,
            280,
            text="PAUSED",
            font=("Arial", 30, "bold"),
            fill="yellow",
            tag="pause_text"
        )

        canvas.create_text(
            250,
            320,
            text="Press P to Resume",
            font=("Arial", 15),
            fill="white",
            tag="pause_text"
        )

    else:

        canvas.delete("pause_text")


root.bind("p", pause_game)
root.bind("P", pause_game)




def game_over():

    global game_running

    game_running = False

    canvas.create_rectangle(
        80,
        220,
        420,
        400,
        fill="black",
        outline="white",
        width=2,
        tag="game_over"
    )

    canvas.create_text(
        250,
        260,
        text="GAME OVER",
        font=("Arial", 28, "bold"),
        fill="red",
        tag="game_over"
    )

    canvas.create_text(
        250,
        305,
        text=f"Final Score: {score}",
        font=("Arial", 18),
        fill="white",
        tag="game_over"
    )

    canvas.create_text(
        250,
        340,
        text=f"Level Reached: {level}",
        font=("Arial", 16),
        fill="yellow",
        tag="game_over"
    )

    canvas.create_text(
        250,
        370,
        text=f"High Score: {high_score}",
        font=("Arial", 16),
        fill="white",
        tag="game_over"
    )

    # Restart button
    restart_button = Button(
        root,
        text="RESTART",
        font=("Arial", 12, "bold"),
        command=restart_game
    )

    canvas.create_window(
        250,
        430,
        window=restart_button,
        tag="game_over"
    )


# -----------------------------
# RESTART GAME
# -----------------------------

def restart_game():

    global score
    global lives
    global level
    global speed
    global game_running
    global paused
    global fruit

    # Delete game over screen
    canvas.delete("game_over")
    canvas.delete("pause_text")

    # Reset values
    score = 0
    lives = 3
    level = 1
    speed = 5

    game_running = True
    paused = False

    # Update display
    canvas.itemconfig(
        score_text,
        text="Score: 0"
    )

    canvas.itemconfig(
        lives_text,
        text="Lives: 3"
    )

    canvas.itemconfig(
        level_text,
        text="Level: 1"
    )

    # Move basket back to center
    canvas.coords(
        basket,
        250,
        560
    )

    # Delete old fruit if it exists
    if fruit is not None:
        canvas.delete(fruit)

    # Create new fruit
    create_fruit()

    # Start game
    fall()



create_fruit()
fall()

root.mainloop()

