"""
🥊 AI vs AI Fighting Game - VISUAL VERSION
Two AI fighters with character sprites using Pillow!
"""

import random
import os
from PIL import Image, ImageDraw, ImageFont

# Constants
WIDTH = 800
HEIGHT = 600

# Colors
BLACK = (20, 20, 30)
RED = (220, 50, 50)
BLUE = (50, 50, 220)
GREEN = (50, 180, 50)
YELLOW = (255, 215, 0)
WHITE = (255, 255, 255)
GRAY = (100, 100, 100)
SKIN = (255, 200, 150)
DARK_BG = (30, 30, 40)

class Fighter:
    def __init__(self, name, color, x):
        self.name = name
        self.color = color
        self.x = x
        self.hp = 100
        self.max_hp = 100
        self.wins = 0
        self.special_cd = 0
        self.is_blocking = False
        self.attack_frame = 0
        self.attack_type = None
        
    def reset(self):
        self.hp = self.max_hp
        self.special_cd = 0
        self.is_blocking = False
        self.attack_frame = 0
        self.attack_type = None

class AI:
    def __init__(self, aggression):
        self.aggression = aggression
        
    def decide(self, fighter, opponent):
        if fighter.hp < 25:
            if random.random() < 0.4:
                return "block"
            elif fighter.special_cd <= 0 and random.random() < 0.3:
                return "special"
            return "punch"
        
        if random.random() < self.aggression:
            if fighter.special_cd <= 0 and random.random() < 0.15:
                return "special"
            return random.choice(["punch", "kick"])
        else:
            return random.choice(["block", "punch"])

def draw_stickman(draw, x, y, color, facing_right, attack_type, frame):
    d = 1 if facing_right else -1
    offset = 0
    
    if attack_type == "punch" and frame > 0:
        offset = 25 * d
    elif attack_type == "kick" and frame > 0:
        offset = 35 * d
    elif attack_type == "special" and frame > 0:
        offset = 45 * d
    
    # Head
    draw.ellipse([x-20, y-70, x+20, y-30], fill=SKIN, outline=color, width=2)
    # Eye
    draw.ellipse([x+6*d-3, y-58, x+6*d+3, y-52], fill=BLACK)
    # Body
    draw.line([x, y-30, x, y+30], fill=color, width=4)
    
    if attack_type == "block" and frame > 0:
        draw.line([x, y-20, x-15, y-40], fill=color, width=3)
        draw.line([x, y-20, x+15, y-40], fill=color, width=3)
    elif attack_type == "punch" and frame > 0:
        draw.line([x, y-20, x+offset, y-15], fill=color, width=3)
        draw.line([x, y-20, x-15*d, y+10], fill=color, width=3)
        draw.ellipse([x+offset-5, y-25, x+offset+8, y-10], fill=RED if color == RED else BLUE)
    elif attack_type == "kick" and frame > 0:
        draw.line([x, y-20, x+20*d, y-30], fill=color, width=3)
        draw.line([x, y-20, x-15*d, y+10], fill=color, width=3)
        draw.line([x, y+30, x+offset, y+50], fill=color, width=4)
    elif attack_type == "special" and frame > 0:
        draw.line([x, y-20, x+offset, y-20], fill=color, width=3)
        draw.line([x, y-20, x-15*d, y+10], fill=color, width=3)
        for i in range(3):
            sz = 12 - i*3
            draw.ellipse([x+offset+i*8*d-sz, y-32+i*5, x+offset+i*8*d+sz, y-22+i*5], fill=YELLOW)
    else:
        draw.line([x, y-20, x+25*d, y-30], fill=color, width=3)
        draw.line([x, y-20, x-15*d, y+10], fill=color, width=3)
    
    # Legs
    if attack_type != "kick" or frame == 0:
        draw.line([x, y+30, x-15, y+65], fill=color, width=4)
        draw.line([x, y+30, x+15, y+65], fill=color, width=4)

def draw_hp_bar(draw, x, y, hp, name, color):
    w = 200
    draw.rectangle([x, y, x+w, y+20], fill=GRAY)
    hw = int((hp/100)*w)
    draw.rectangle([x, y, x+hw, y+20], fill=color)
    draw.rectangle([x, y, x+w, y+20], outline=WHITE, width=1)
    draw.text((x+5, y+2), f"{name} {hp}HP", fill=WHITE)

def create_frame(f1, f2, rnd, log, frame_n, winner=None):
    img = Image.new('RGB', (WIDTH, HEIGHT), DARK_BG)
    draw = ImageDraw.Draw(img)
    
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 20)
        font_sm = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 14)
    except:
        font = ImageFont.load_default()
        font_sm = font
    
    # Title
    draw.text((WIDTH//2-80, 15), f"ROUND {rnd}", fill=YELLOW, font=font)
    
    # HP bars
    draw_hp_bar(draw, 30, 50, f1.hp, f1.name, RED)
    draw_hp_bar(draw, WIDTH-230, 50, f2.hp, f2.name, BLUE)
    
    # Ground
    draw.rectangle([0, 420, WIDTH, 440], fill=GRAY)
    
    # Fighters
    draw_stickman(draw, 200, 350, RED, True, f1.attack_type, f1.attack_frame)
    draw_stickman(draw, 600, 350, BLUE, False, f2.attack_type, f2.attack_frame)
    
    # Log
    y = 460
    draw.text((30, y), "BATTLE LOG:", fill=WHITE, font=font_sm)
    y += 22
    for entry in log[-5:]:
        draw.text((30, y), entry[:65], fill=GRAY, font=font_sm)
        y += 18
    
    # Frame counter
    draw.text((WIDTH-90, HEIGHT-25), f"Frame: {frame_n}", fill=GRAY, font=font_sm)
    
    # Winner banner
    if winner:
        draw.rectangle([WIDTH//2-130, HEIGHT//2-30, WIDTH//2+130, HEIGHT//2+30], fill=BLACK, outline=YELLOW, width=2)
        draw.text((WIDTH//2-100, HEIGHT//2-15), f"{winner} WINS!", fill=YELLOW, font=font)
    
    return img

def main():
    os.makedirs("frames", exist_ok=True)
    
    f1 = Fighter("RYU", RED, 200)
    f2 = Fighter("KEN", BLUE, 600)
    ai1 = AI(0.55)
    ai2 = AI(0.65)
    
    frame_n = 0
    frames = []
    
    print("🥊 AI FIGHT GAME - Starting!")
    
    for rnd in range(1, 6):
        f1.reset()
        f2.reset()
        log = [f"Round {rnd} - FIGHT!"]
        winner = None
        
        while f1.hp > 0 and f2.hp > 0:
            # Save frame
            img = create_frame(f1, f2, rnd, log, frame_n)
            img.save(f"frames/frame_{frame_n:04d}.png")
            frames.append(img)
            frame_n += 1
            
            # AI decisions
            a1 = ai1.decide(f1, f2)
            a2 = ai2.decide(f2, f1)
            
            # Execute
            for fighter, opp, ai_act, c in [(f1, f2, a1, RED), (f2, f1, a2, BLUE)]:
                if ai_act == "block":
                    fighter.is_blocking = True
                    fighter.attack_type = "block"
                    fighter.attack_frame = 1
                    log.append(f"{fighter.name} BLOCKS!")
                elif ai_act == "special" and fighter.special_cd <= 0:
                    dmg = random.randint(25, 40)
                    if opp.is_blocking:
                        dmg = dmg // 3
                    opp.hp = max(0, opp.hp - dmg)
                    fighter.special_cd = 3
                    fighter.attack_type = "special"
                    fighter.attack_frame = 1
                    log.append(f"{fighter.name} SPECIAL! -{dmg}HP")
                elif ai_act == "punch":
                    dmg = random.randint(8, 15)
                    if opp.is_blocking:
                        dmg = dmg // 3
                    opp.hp = max(0, opp.hp - dmg)
                    fighter.attack_type = "punch"
                    fighter.attack_frame = 1
                    log.append(f"{fighter.name} PUNCH! -{dmg}HP")
                elif ai_act == "kick":
                    dmg = random.randint(12, 22)
                    if opp.is_blocking:
                        dmg = dmg // 3
                    opp.hp = max(0, opp.hp - dmg)
                    fighter.attack_type = "kick"
                    fighter.attack_frame = 1
                    log.append(f"{fighter.name} KICK! -{dmg}HP")
            
            # Attack animation frames
            for _ in range(3):
                img = create_frame(f1, f2, rnd, log, frame_n)
                img.save(f"frames/frame_{frame_n:04d}.png")
                frames.append(img)
                frame_n += 1
            
            # Reset
            f1.is_blocking = False
            f2.is_blocking = False
            f1.attack_frame = 0
            f2.attack_frame = 0
            f1.attack_type = None
            f2.attack_type = None
            f1.special_cd = max(0, f1.special_cd-1)
            f2.special_cd = max(0, f2.special_cd-1)
        
        if f1.hp > 0:
            f1.wins += 1
            winner = f1.name
            log.append(f"Round {rnd}: {f1.name} WINS!")
        else:
            f2.wins += 1
            winner = f2.name
            log.append(f"Round {rnd}: {f2.name} WINS!")
        
        # Winner frames
        for _ in range(10):
            img = create_frame(f1, f2, rnd, log, frame_n, winner)
            img.save(f"frames/frame_{frame_n:04d}.png")
            frames.append(img)
            frame_n += 1
        
        print(f"Round {rnd}: {f1.name} {f1.wins} - {f2.wins} {f2.name}")
    
    # Final winner
    final_winner = f1.name if f1.wins > f2.wins else f2.name if f2.wins > f1.wins else "DRAW"
    for _ in range(15):
        img = Image.new('RGB', (WIDTH, HEIGHT), BLACK)
        draw = ImageDraw.Draw(img)
        try:
            font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 36)
            font_sm = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 20)
        except:
            font = ImageFont.load_default()
            font_sm = font
        draw.text((WIDTH//2-150, HEIGHT//2-50), f"CHAMPION: {final_winner}!", fill=YELLOW, font=font)
        draw.text((WIDTH//2-100, HEIGHT//2+10), f"{f1.name}: {f1.wins} | {f2.name}: {f2.wins}", fill=WHITE, font=font_sm)
        img.save(f"frames/frame_{frame_n:04d}.png")
        frames.append(img)
        frame_n += 1
    
    print(f"\n🏆 CHAMPION: {final_winner}")
    print(f"Total frames: {frame_n}")
    
    # Save GIF
    if frames:
        frames[0].save("AI_Fight.gif", save_all=True, append_images=frames[1:], duration=125, loop=0)
        print("✅ GIF saved: AI_Fight.gif")

if __name__ == "__main__":
    main()
