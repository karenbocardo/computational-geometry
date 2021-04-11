## Python program to understand the usage of tabulate function for printing tables in a tabular format
from tabulate import tabulate
data = [[1, 'Liquid', 24, 12],
[2, 'Virtus.pro', 19, 14],
[3, 'PSG.LGD', 15, 19],
[4,'Team Secret', 10, 20]]
print(tabulate(data, headers=["Pos", "Team", "Win", "Lose"]))