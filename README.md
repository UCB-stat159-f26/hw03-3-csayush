# Homework 3

In this homework, I made a package that gets a player's career matches from tennisabstract.com. Then, we plot the player's age against the age difference with each opponent (age - opponent_age).

`get_career_data()` downloads and cleans one player's matches. The input for it is a name in a potentially non-standard format like `"serena williams"`, `"Serena Williams"`, and `"SerenaWilliams"`. An invalid name like `"GastonSanchez"` raises an error. `plot_age_gap()` takes that data frame and draws the scatter plot. The axes for the plot are: player's age on x-axis, age difference is on y-axis, wins and losses are represented by different colors.

## Repo layout


src/tennis_career/data.py    download and clean the career data
src/tennis_career/plot.py    draw the scatter plot
src/tennis_career/__init__.py
tests/test_data.py           tests for cleaning the career files
tests/test_plot.py           tests for the plot
tests/fixtures/              mock women's and men's career files
pyproject.toml               package setup



## Returned data

| Column | Meaning |
| --- | --- |
| `date` | date of match |
| `tournament` | tournament name |
| `surface` | court surface (eg Clay) |
| `result` | `"W"` if the player won, `"L"` if they lost |
| `opponent` | opponent's name |
| `opponent_age` | opponent's age at that match |
| `player_age` | player's age at that match |
| `age_diff` | player's age minus the opponent's age |


## Reflection

The main thing I had to do was essentially figuring out that the career files are in different formats for every player. Initially I assumed that the format would be the same for every player and so my scripts did not differentiate based on gender. But then I realized from visual inspection that a women's file stores the opponent's birthday, while a men's file stores the opponent's age. As a result, I had to do code cleaning steps to convert them to a standard format. Also, this confused me at first when my script did not pick up the actual player's birthday. I later realized that the player's birthday is actually in a different file from the match list.

I also found unit tests to be very useful, since I could rely on something other than visual inspection. I also found it beneficial to write unit tests for features as I implemented them, instead of writing all tests towards the end. This allowed me to ensure every time I committed code, the feature was correctly built, and this helped me avoid writing all tests at the end and risk having many different failing tests towards the end. Also, initially I found the 20 line rule per function quite annoying, but I only later realized that it helped me split my code into smaller and more readable and easily testable functions.
