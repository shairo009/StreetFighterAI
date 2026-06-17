# 🥊 Street Fighter II AI

AI vs AI Street Fighter II gameplay using Reinforcement Learning!

## 🎮 What it does

- Trains an AI agent to play Street Fighter II
- Uses PPO (Proximal Policy Optimization) algorithm
- Creates GIF recordings of AI fights
- Fully automated via GitHub Actions

## 🚀 How to use

1. **Fork this repo**
2. **GitHub Actions runs automatically**
3. **Download video from Actions → Artifacts**

## 📁 Structure

```
StreetFighterAI/
├── .github/workflows/
│   └── fight.yml          # GitHub Actions workflow
├── roms/
│   └── StreetFighterIISpecialChampionEdition-Genesis/
│       └── rom.bin        # Game ROM (you provide)
├── train_and_test.py      # Main AI code
└── README.md
```

## 🔧 Setup

### Option 1: Use pre-trained model
Just push the code - it will use the included model.

### Option 2: Train from scratch
The AI trains for 50,000 timesteps automatically.

## 📊 Results

- AI learns to fight using health-based rewards
- Records fights as GIF animations
- Saves to `replays/` folder

## 🛠️ Tech Stack

- Python 3.10
- gym-retro (game environment)
- Stable Baselines3 (PPO algorithm)
- OpenCV (image processing)
- imageio (GIF creation)

## 📝 License

MIT License
