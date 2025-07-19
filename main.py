from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
import random

# Initialize the game
app = Ursina()

# Set up the scene
window.title = "Hidden Signs"
window.borderless = False
window.fullscreen = False
window.exit_button.visible = False
window.fps_counter.enabled = False

# Create the player
player = FirstPersonController()
player.position = (0, 0.5, -2)
player.cursor.visible = False

# Create apartment environment
# Floor
#collider='cube' value gives the object collision detection
floor = Entity(model='cube', collider='box', color=color.gray, scale=(20, 0.1, 20), position=(0, -0.5, 0))

# Walls
wall_north = Entity(model='cube', collider='box', color=color.white, scale=(20, 10, 0.5), position=(0, 4.5, 10))
wall_south = Entity(model='cube', collider='box', color=color.white, scale=(20, 10, 0.5), position=(0, 4.5, -10))
wall_east = Entity(model='cube', collider='box', color=color.white, scale=(0.5, 10, 20), position=(10, 4.5, 0))
wall_west = Entity(model='cube', collider='box', color=color.white, scale=(0.5, 10, 20), position=(-10, 4.5, 0))

# Ceiling
ceiling = Entity(model='cube', color=color.light_gray, scale=(20, 0.1, 20), position=(0, 9, 0))

# Furniture - Computer desk
desk = Entity(model='cube', color=color.brown, scale=(3, 0.1, 1.5), position=(7, 0.5, 5))
desk_legs = [
    Entity(model='cube', color=color.dark_gray, scale=(0.1, 1, 0.1), position=(6, 0, 4.5)),
    Entity(model='cube', color=color.dark_gray, scale=(0.1, 1, 0.1), position=(8, 0, 4.5)),
    Entity(model='cube', color=color.dark_gray, scale=(0.1, 1, 0.1), position=(6, 0, 5.5)),
    Entity(model='cube', color=color.dark_gray, scale=(0.1, 1, 0.1), position=(8, 0, 5.5))
]

# Computer monitor (this will be interactive)
monitor = Entity(model='cube', color=color.black, scale=(1.2, 0.8, 0.1), position=(7, 1.2, 5.2))
monitor_screen = Entity(model='cube', color=color.dark_gray, scale=(1.1, 0.7, 0.05), position=(7, 1.2, 5.25))

# Chair
chair = Entity(model='cube', color=color.red, scale=(0.8, 0.1, 0.8), position=(7, 0.3, 3.5))
chair_back = Entity(model='cube', color=color.red, scale=(0.8, 1.5, 0.1), position=(7, 1, 4))

# Bed
bed = Entity(model='cube', color=color.blue, scale=(2.5, 0.3, 4), position=(-6, 0.15, -4))
pillow = Entity(model='cube', color=color.white, scale=(1, 0.2, 0.8), position=(-6, 0.4, -6))

# Bookshelf
bookshelf = Entity(model='cube', color=color.brown, scale=(0.3, 3, 2), position=(-8, 1.5, 6))

# Add some books
for i in range(5):
    book = Entity(model='cube', color=color.random_color(), 
                 scale=(0.1, 0.3, 0.15), 
                 position=(-7.9, 1.2 + i*0.35, 5.5 + random.uniform(-0.3, 0.3)))

# Lighting
sun = DirectionalLight()
sun.look_at(Vec3(1, -1, -1))

# Add ambient light
AmbientLight(color=color.rgba(100, 100, 100, 0.1))

# Game state variables
game_state = {
    'computer_investigated': False,
    'file_found': False,
    'player_knows_truth': False
}

# UI elements
interaction_text = Text('', position=(-0.8, -0.4), scale=2, color=color.white)
story_text = Text('', position=(-0.8, 0.3), scale=1.5, color=color.yellow)
instructions = Text('WASD to move, Mouse to look, E to interact, ESC to quit', 
                   position=(-0.9, 0.45), scale=1, color=color.light_gray)

# Story content
story_content = {
    'intro': "You're in your apartment. Something feels off tonight...",
    'computer_prompt': "Press E to use the computer",
    'computer_first_use': "The computer boots up. Your desktop looks normal, but there's a file here you don't remember creating...",
    'file_discovery': "Strange... 'random_footage_2847.gif' - When did this get here? The timestamp shows it was created while you were asleep.",
    'file_contents': "The GIF shows blurry cellphone footage of people walking on a street. Nothing special, but... why is this on YOUR computer? Who put it here?",
    'growing_suspicion': "Your heart races. You didn't download this. Your computer has good security. How did someone access it remotely?"
}

def update():
    # Check for interactions
    if held_keys['escape']:
        quit()
    
    # Check distance to computer
    distance_to_computer = distance(player, monitor)
    
    if distance_to_computer < 3:
        if not game_state['computer_investigated']:
            interaction_text.text = 'Press E to investigate the computer'
            if held_keys['e']:
                investigate_computer()
        elif not game_state['file_found']:
            interaction_text.text = 'Press E to examine the strange file'
            if held_keys['e']:
                examine_file()
        else:
            interaction_text.text = 'The computer screen shows that mysterious GIF...'
    else:
        interaction_text.text = ''

def investigate_computer():
    game_state['computer_investigated'] = True
    story_text.text = story_content['computer_first_use']
    # Change monitor screen color to indicate it's on
    monitor_screen.color = color.blue
    
    # Add a mysterious file indicator
    file_indicator = Entity(model='cube', color=color.red, scale=(0.1, 0.1, 0.01), 
                           position=(7.3, 1.3, 5.26))
    
    invoke(lambda: setattr(story_text, 'text', story_content['file_discovery']), delay=3)

def examine_file():
    game_state['file_found'] = True
    story_text.text = story_content['file_contents']
    monitor_screen.color = color.green  # Show the "GIF" is playing
    
    invoke(lambda: setattr(story_text, 'text', story_content['growing_suspicion']), delay=4)
    invoke(lambda: setattr(story_text, 'text', 
           'This is just the beginning... [Press ESC to end demo]'), delay=8)

# Initial story text
story_text.text = story_content['intro']

# Run the game
app.run()