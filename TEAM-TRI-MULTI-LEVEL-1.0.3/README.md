##

# INFO 
Please run on windows, it seems there is an issue with OSX SDL Library which causes the game to lag with many sprites making playing it impossible

## Rubric


* Title Screen is present and contains the name of the game with instructions to go to the credits screen or start the game **(9 points) **

    * **YES, multiple title screens are present.**

* You can press a key to go to the credits screen 

    * **YES using a menu system**

* o You can press a different key to start the game 

    * **YES using a menu system**

* o You can press a different key to quit the game entirely

    * **YES using a menu system**

* Credits screen includes any necessary licensing information, along with author names and roles and instructions on how to play the game (9 points) 

    * **YES it’s a separate credit screen also includes GFX, SFX credits.**

    * **Separate help screen exists, from main menu**

* Classes in separate libraries include: GoodBlock, BadBlock, Player, Block, Music, Art, Level, CreditsLevel, TitleLevel, Main, GameLevel (33 points)

    * ALL of the above is present with some name changes. A more sophisticated framework was developed with proper transitions as well as level queues.

        * LevelManager with event handler and transitions

        * MusicManager includes facilities to play random songs depending on screen

        * Multiple Classes included including (Enemy, Animated enemy, solid blocks, Bullets, Blood, Collectible coins etc…)

        * Various interfaces facilitate menu and game logic

        * Lazy loading multiple levels

    * If you choose not to include a class from this list, you must include an indication of why in your final submission. 

        * **SEE ABOVE**

* - GoodBlocks and BadBlocks must move in slightly different ways. (3 points) 

    * **SEE ABOVE all done using OOP**

* - GoodBlocks, BadBlocks, and Player should have different images (3 points)

    * **SEE ABOVE + Yes coins etc… all present**

* There should be a sound effect when the Player collides with a GoodBlock and a different sound when colliding with a BadBlock (3 points) 

    * **Sound effects DEPEND on action taken, shooting, bullet colliding with enemy or player, coin is picked up**

* - There should be background music playin	g. (3 points) 		

    * **YES in every screen and it’s all different and randomly chosen depending on screen**

- The background music should be different between the Game and the Title/Credits screen. (3 points)

 - The background music should repeat after playing once. (3 points) 

* - The player should not be able to scroll off the screen. (3 points)

    * **Yes level design restricts player from going outside**

*  - When the player hits the border of the screen, a sound effect should play (and should only play once). (3 points) -

    * **NOT Needed given the design of the level and would take away from game, if the purpose of this is to learn how to use sound library then see bullets colliding with enemies :) There are MANY sounds used in this game**

*  Current score should be displayed on screen while playing the game. (3 points)

    * **YES there is a score on top right  in $$ and health bar top left**

*  - The player can press a key to quit the game and return to the title screen. (3 points) 

    * **YES DONE**

* - Uses descriptive variable names (3 points) 

    * Yes obviously

* - In your blackboard submission include: o The URL of your Git Repository, your final version should be in master - 1 point 

    * **Yep**

* o An explanation of why you did not include a particular class as described above (must indicate how your design is better and provides more flexibility / readability)

    * **Yep see above**

* Includes a class called File that loads files from disk indicating the art and sound assets in the game. (6 points)

    * **Sprite loading logic exists using manual loading**

    * **PyTMX library for loading TILED engine\**

    * **Music manager loads music etc….**

* For below files

    *  - Includes a file for Block object assets (3 points) 

        * **Yes spritesheets and stand alone assets are loaded**

    * - Includes a file for sound assets (3 point) 	

        * **Yes multiple files exist and loaded as needed**

* - 	Adds the ability for GoodBlocks and BadBlocks to give differing number of points depending on the object information in the file. (3 points)

    * Yes similar logic exists:

        * Each enemy has different HP, can fire bullets etc…

        * Collectibles also can represent this all have different values as set in map

