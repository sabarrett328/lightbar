import board
import digitalio
import rotaryio
import pwmio

# Constants
PWM_FREQ = 1000  # PWM frequency in Hz
PWM_MAX = 65535  # Maximum PWM duty cycle
PWM_HALF = PWM_MAX // 2  # 50% brightness step
ENCODER_STEP = 100  # Step size for brightness adjustment

# Define PWM outputs for LED strings
led1 = pwmio.PWMOut(board.D5, frequency=PWM_FREQ, duty_cycle=0)
led2 = pwmio.PWMOut(board.D6, frequency=PWM_FREQ, duty_cycle=0)

# Rotary encoders
encoder1 = rotaryio.IncrementalEncoder(board.D2, board.D3)
encoder2 = rotaryio.IncrementalEncoder(board.D4, board.D7)

# Encoder pushbuttons
button1 = digitalio.DigitalInOut(board.D8)
button1.switch_to_input(pull=digitalio.Pull.UP)
button2 = digitalio.DigitalInOut(board.D9)
button2.switch_to_input(pull=digitalio.Pull.UP)

# State variables
brightness = {"led1": 0, "led2": 0}
toggle_state = {"led1": False, "led2": False}
last_position = {"encoder1": encoder1.position, "encoder2": encoder2.position}

# Function to update brightness
def update_brightness(encoder, last_pos, led, key):
    position = encoder.position
    if position != last_pos:
        brightness[key] = max(0, min(PWM_MAX, brightness[key] + (position - last_pos) * ENCODER_STEP))
        led.duty_cycle = brightness[key]
    return position

# Function to handle button press
def handle_button(button, led, key):
    if not button.value:
        time.sleep(0.05)  # Simple debounce delay
        if not button.value:  # Check if still pressed
            toggle_state[key] = not toggle_state[key]
            if toggle_state[key]:
                last_brightness[key] = brightness[key]
                led.duty_cycle = PWM_HALF  # Set to 50% brightness
            else:
                led.duty_cycle = 0  # Turn off
            while not button.value:  # Wait for button release
                pass

while True:
    last_position["encoder1"] = update_brightness(encoder1, last_position["encoder1"], led1, "led1")
    last_position["encoder2"] = update_brightness(encoder2, last_position["encoder2"], led2, "led2")
    
    handle_button(button1, led1, "led1")
    handle_button(button2, led2, "led2")
