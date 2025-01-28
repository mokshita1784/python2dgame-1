import tkinter as tk
import random

class CarRacingGame:
    def __init__(self, master):
        self.master = master
        self.master.title("Car Racing Game")
        self.canvas = tk.Canvas(master, width=400, height=600, bg="gray")
        self.canvas.pack()

        # Initialize road objects
        self.create_road()

        # Car body with wheels to make it look like a car
        self.car_body = self.canvas.create_rectangle(170, 500, 230, 550, fill="blue")
        self.car_wheel1 = self.canvas.create_oval(180, 540, 200, 560, fill="black")
        self.car_wheel2 = self.canvas.create_oval(220, 540, 240, 560, fill="black")

        self.obstacles = []
        self.score = 0
        self.game_over = False

        # Display score
        self.score_text = self.canvas.create_text(10, 10, anchor="nw", text="Score: 0", fill="white", font=("Arial", 14))

        # Bind keys for movement
        self.master.bind("<Left>", self.move_left)
        self.master.bind("<Right>", self.move_right)
        self.master.bind("<Up>", self.move_forward)
        self.master.bind("<Down>", self.move_backward)

        self.create_obstacles()  # Create initial obstacles
        self.update_game()

    def create_road(self):
        # Draw two parallel black rectangles to represent the road
        self.road1 = self.canvas.create_rectangle(50, 0, 350, 600, fill="black")  # Road part 1
        self.road2 = self.canvas.create_rectangle(50, -600, 350, 0, fill="black")  # Road part 2
        # Draw dashed lane lines
        self.create_lane_lines()

    def create_lane_lines(self):
        # Draw dashed lane lines on the road
        self.lane_lines = []
        for i in range(10, 600, 40):
            line = self.canvas.create_line(200, i, 200, i + 20, fill="white", dash=(5, 10))
            self.lane_lines.append(line)

    def move_left(self, event):
        if not self.game_over:
            car_coords = self.canvas.coords(self.car_body)
            if car_coords[0] > 50:  # Prevent moving off the left side
                self.canvas.move(self.car_body, -20, 0)
                self.canvas.move(self.car_wheel1, -20, 0)
                self.canvas.move(self.car_wheel2, -20, 0)

    def move_right(self, event):
        if not self.game_over:
            car_coords = self.canvas.coords(self.car_body)
            if car_coords[2] < 350:  # Prevent moving off the right side
                self.canvas.move(self.car_body, 20, 0)
                self.canvas.move(self.car_wheel1, 20, 0)
                self.canvas.move(self.car_wheel2, 20, 0)

    def move_forward(self, event):
        if not self.game_over:
            self.canvas.move(self.car_body, 0, -10)  # Move the car upwards (forward)
            self.canvas.move(self.car_wheel1, 0, -10)
            self.canvas.move(self.car_wheel2, 0, -10)

    def move_backward(self, event):
        if not self.game_over:
            self.canvas.move(self.car_body, 0, 10)  # Move the car downwards (backward)
            self.canvas.move(self.car_wheel1, 0, 10)
            self.canvas.move(self.car_wheel2, 0, 10)

    def create_obstacles(self):
        # Only create new obstacles if there are fewer than 4 on the screen
        if len(self.obstacles) < 4:
            num_obstacles = random.randint(1, 2)  # Create 1 or 2 obstacles at a time
            for _ in range(num_obstacles):
                x_position = random.randint(0, 370)
                color = random.choice(["red", "yellow", "green", "blue"])  # Random color selection
                speed = random.randint(12, 18)  # Random speed between 12 and 18
                # Create the car-like shape (body + wheels)
                body = self.canvas.create_rectangle(x_position, 0, x_position + 40, 30, fill=color)
                wheel1 = self.canvas.create_oval(x_position + 5, 25, x_position + 15, 35, fill="black")
                wheel2 = self.canvas.create_oval(x_position + 25, 25, x_position + 35, 35, fill="black")
                obstacle = {
                    "body": body, 
                    "wheel1": wheel1, 
                    "wheel2": wheel2, 
                    "speed": speed
                }
                self.obstacles.append(obstacle)

    def update_game(self):
        if not self.game_over:
            # Move road parts downward to simulate treadmill effect
            self.canvas.move(self.road1, 0, 10)
            self.canvas.move(self.road2, 0, 10)

            # Move lane lines
            for line in self.lane_lines:
                self.canvas.move(line, 0, 10)
                if self.canvas.coords(line)[1] > 600:
                    self.canvas.move(line, 0, -600)  # Reset the line to the top

            # Reposition road parts after they go off the screen
            if self.canvas.coords(self.road1)[1] > 600:
                self.canvas.coords(self.road1, 50, -600, 350, 0)
            if self.canvas.coords(self.road2)[1] > 600:
                self.canvas.coords(self.road2, 50, -600, 350, 0)

            # Update obstacles
            for obstacle in self.obstacles:
                self.canvas.move(obstacle["body"], 0, obstacle["speed"])  # Move body
                self.canvas.move(obstacle["wheel1"], 0, obstacle["speed"])  # Move wheel1
                self.canvas.move(obstacle["wheel2"], 0, obstacle["speed"])  # Move wheel2
                if self.check_collision(obstacle["body"]):
                    self.game_over = True
                    self.canvas.create_text(200, 300, text="Game Over!", fill="white", font=("Arial", 24))
                    return
                if self.canvas.coords(obstacle["body"])[1] > 600:  # If obstacle reaches bottom
                    self.canvas.delete(obstacle["body"])
                    self.canvas.delete(obstacle["wheel1"])
                    self.canvas.delete(obstacle["wheel2"])
                    self.obstacles.remove(obstacle)
                    self.score += 1
                    self.update_score()
                    self.create_obstacles()  # Create new obstacles when one goes off-screen

            self.master.after(80, self.update_game)  # Faster game loop (decreased delay)

    def check_collision(self, obstacle_body):
        car_coords = self.canvas.coords(self.car_body)
        obstacle_coords = self.canvas.coords(obstacle_body)
        # Check if the car and obstacle intersect
        return (car_coords[2] > obstacle_coords[0] and car_coords[0] < obstacle_coords[2] and
                car_coords[1] < obstacle_coords[3] and car_coords[3] > obstacle_coords[1])

    def update_score(self):
        self.canvas.itemconfig(self.score_text, text=f"Score: {self.score}")

if __name__ == "__main__":
    root = tk.Tk()
    game = CarRacingGame(root)
    root.mainloop()
