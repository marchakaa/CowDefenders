# CowDefenders - Tower Defense Game
**CowDefenders** is a strategic tower defense game made with pygame where **cows** battle against waves of **slimes**! Inspired by traditional tower defense mechanics and games like **Teamfight Tactics (TFT)**, players must strategically buy, combine, and place different cows to defend their farm from relentless slime invaders.
## Instalation & Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/marchakaa/CowDefenders
2. Install requirements.txt:
   ```bash
   pip install -r requirements.txt
3. Run the game
   ```bash
   python main.py
## Game Mechanics
- **Cows**: Buy cows to defend from the slimes (keep in mind what you buy and place on the field, you can't sell or bench towers). Cows are separated in 5 tiers.
- **Upgrade**: Buying three times the same tower will upgrade the tower to level 2, combining 3 level 2 towers will make the tower level 3. Each level increases the strength of the tower.
- **Shop**: After each wave you are rewarded with gold. With gold you can buy towers from the shop or refresh the shop. The shop contains 5 random towers and as the game progresses you higher tier cows will appear in the shop.
- **Waves**: Each wave of slimes grow stronger. So you need to make sure you have strong enough towers to defend them!
- **Enemies**: Slimes have different strengths (some are with more hp, some are faster).
## How to Play
1. **Start the Game**: I mentioned above how to start the game.
2. **Main menu**: Main menu has 3 options: ("Start Game", "Continue Game", "Exit Game"). They are self explaining.
3. **Continue menu**: In this menu you can find your saved games and continue them or delete them.
3. **Game Start**: When the game begins prepare yourself and when you are ready start the waves by clicking SPACE.
## Cow Types
- **Moochine Gunner**: 1 cost. Shoots very fast. Rage Ability doubles the Moochine Gunner's attack speed.
- **Ice Cow**: 3 cost. Shoots fast and doesn't deal a lot of damage. IceNova Ability slows the enemies within 300 units. 
- **Sniper Cow**: 4 cost. Deals lots of damage, but shoots slow. Deadeye ability allows this tower to oneshot the 2 strongest enemies on the board.
- **Fire Cow**: 5 cost. This tower scales with the Blaze Ability. Each cast gives this tower attack damage reaching milestones gives it Burn effect on attacks and increases it's range.
## Upcomming Features
- **NEW Cows**: New Cows will be added into the game.
- **Traits**: Traits will be powerful buffs that requare combinations of cows.
- **NEW Enemies**: Enemies are quite simple for now, but they will have abilities in the future.
- **NEW Maps**: The players will be able to defend different fields.
- **Effects**: For now the game can't be playable with effects (audio and visual), but they will be added in the future.