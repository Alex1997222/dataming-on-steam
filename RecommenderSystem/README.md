# Recommender System

We can build an recommender system based on the idea of "Collaborative Filtering". Though we cannot use it directly, we can still modify it to build one.

## Data Analyze

Firstly, we need to merge `user_table.csv` and `game_table.csv` into `user_game.csv`.  
Through data analyzing, we know that for one user, only one item of game is stored in the data table. So we cannot directly perform "Collaborative Filtering", since it requires one user have multiple lines.  


## Building the recommender system


### step 1  

We can recommend games to user according to their favorite game labels. We firstly analyze their favorite game labels, then we store these games which have similar labels.   

### step 2 

We check the attitude of the users of these stored games, if most of the comments are positive, we recommend these games to the candidate, and we recommend these users to the candidate.  



