"""
🥊 Street Fighter II AI - Train & Test
Trains AI using PPO and creates fight video
"""

import retro
from gym import Env
from gym.spaces import Discrete, Box, MultiBinary
import numpy as np
import os
import imageio

# Custom Environment
class StreetFighter(Env):
    def __init__(self):
        super().__init__()
        self.observation_space = Box(low=0, high=255, shape=(84, 84, 1), dtype=np.uint8)
        self.action_space = MultiBinary(12)
        self.game = retro.make(
            game='StreetFighterIISpecialChampionEdition-Genesis', 
            use_restricted_actions=retro.Actions.FILTERED
        )
        self.previous_health = None
        self.previous_enemy_health = None
        
    def step(self, action):
        obs, reward, done, info = self.game.step(action)
        obs = self.preprocess(obs)
        
        # Custom reward: health difference
        if self.previous_health is not None:
            reward = (self.previous_enemy_health - info['enemy_health']) - (self.previous_health - info['health'])
        else:
            reward = 0
            
        self.previous_health = info['health']
        self.previous_enemy_health = info['enemy_health']
        
        return obs, reward, done, info
    
    def reset(self):
        obs = self.game.reset()
        self.previous_health = None
        self.previous_enemy_health = None
        return self.preprocess(obs)
    
    def render(self, mode='rgb_array'):
        return self.game.render(mode)
    
    def close(self):
        self.game.close()
    
    def preprocess(self, obs):
        # Convert to grayscale and resize
        gray = np.mean(obs, axis=2).astype(np.uint8)
        gray = np.expand_dims(gray, axis=2)
        return gray

def main():
    print("🥊 Street Fighter II AI - Starting...")
    print("=" * 50)
    
    # Create environment
    env = StreetFighter()
    print("✅ Game loaded!")
    
    # Check if pre-trained model exists
    model_path = 'latest_model.zip'
    
    if os.path.exists(model_path):
        print(f"📦 Loading pre-trained model: {model_path}")
        from stable_baselines3 import PPO
        model = PPO.load(model_path, env=env)
    else:
        print("🏋️ Training new AI model...")
        from stable_baselines3 import PPO
        
        # Train for a few episodes (quick training for demo)
        model = PPO('CnnPolicy', env, verbose=1, learning_rate=3e-5, n_steps=1024, batch_size=128, gamma=0.9)
        
        # Quick training (increase timesteps for better results)
        model.learn(total_timesteps=50000)
        model.save(model_path)
        print("✅ Training complete!")
    
    # Test the AI
    print("\n🎮 Running test fights...")
    
    os.makedirs('replays', exist_ok=True)
    
    for game_num in range(1, 4):  # 3 test games
        print(f"\n--- Game {game_num} ---")
        
        obs = env.reset()
        done = False
        total_reward = 0
        frames = []
        steps = 0
        
        while not done:
            # Get frame
            frame = env.render(mode='rgb_array')
            if frame is not None:
                frames.append(frame)
            
            # AI action
            action, _ = model.predict(obs)
            obs, reward, done, info = env.step(action)
            total_reward += reward
            steps += 1
            
            if steps % 50 == 0:
                print(f"  Step {steps}: HP={info['health']}, Enemy HP={info['enemy_health']}")
        
        # Save as GIF
        if frames:
            gif_path = f'replays/game_{game_num}.gif'
            imageio.mimsave(gif_path, frames, fps=24)
            print(f"  📹 Saved: {gif_path}")
        
        # Result
        if info['health'] > info['enemy_health']:
            print(f"  🏆 AI WINS! (HP: {info['health']})")
        else:
            print(f"  💀 AI LOSES! (Enemy HP: {info['enemy_health']})")
        
        print(f"  Total reward: {total_reward:.2f}")
    
    env.close()
    print("\n✅ All done! Check replays/ folder for videos!")

if __name__ == "__main__":
    main()
