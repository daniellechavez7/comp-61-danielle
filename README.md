# Extra Credit Game

Demo Video 
https://youtu.be/txsAzYKMOGo 

Setup:
  pip install pygame
  cd path/to/FrogHop
python main.py
go to Frog Hops folder and run with main.py

Game Overview 
- Game title: 
  Frog Hop
- Game Summary
  In Frog Hop, you play as a frog hopping along a river on lilypads. Hop across the lily pads in order to gain points, collect food, and reach stars to advance to the next level. As the levels increase, the rewards double but the levels are more challenging with less lily pads to hop on. Help the frog navigate through the water and get a new high score!
- Core Gameplay Loop
  The player controls the frog using arrow keys to hop between lilypads. Player is given 3 lives and must hop around in attempt to collect food for bonus points and reach the star to advance to the next level. As the levels increase, there will be less lily pads and less food. Missing a lily pad or jumping into the water will cause the player to lose a life. As soon as all 3 lives are gone, the game is over. 

Gameplay Mechanics 
- Controls:
  Arrows Keys - Move in four directions 
  R - Restart game (when the game is over)
  I for Instructions
  Q to Quit 
- Core Mechanics:
  Hopping: Movement allowed in grid steps and gives points for every successful move
  Moving Platforms: lily pads move to different locations after every hop
  Collectibles: Food items for bonus points
  Level Stars: Collect to advance to next level
  Lives: Lose a life if you land in water 
- Level Progression: 
  Each level increases difficulty (less lilypads)
  Lilypad layout changes with every hop
  Points earned are doubled per level
  Game is not over until all lives are lost 
- Win/Loss Conditions
  Win: Progress through levels by collecting stars and get a new high      score
  Loss: Lose all 3 lives by falling into the water

  





