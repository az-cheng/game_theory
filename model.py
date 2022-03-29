"""
Annie Cheng, zc375
March 23, 2022
"""

from game_class import Game

class Model:
    """
    A class to represent the modeling of a game.
    """

    def __init__(self,lines=''):
        """
        Initializes a model with given input lines.
        If running directly from the main.py file, the program will ask input from the user by function run.

        Attribute lines: input lines to the model.
        Attribute g: object of class Game with input lines.
        """
        self.lines = lines
        if lines != '':
            self.g = Game(self.lines)


    def run(self):
        """
        This function runs the program by asking inputs from users.
        """
        lines = ""
        print('Enter multi-line input (one line at a time): ')
        while True:
            data = input()
            if data == "":
                break
            else:
                lines+=data+"\n"
        self.lines = lines
        self.g = Game(self.lines)

        # Q1: ask the user input for a player number to find the dominated strategies for that player
        Q1 = int(input('Input player number (1 or 2) to find dominated strategies: '))

        output, dominated,n_payoff = self.g.dominated_strategies(Q1, self.g.payoff)
        for i in output:
            print(i)

        # Q2: ask the user to input a player number and a strategy from her strategy set to find the set of best responses

        print('Find the set of best responses: ')
        Q2 = int(input('Player number: '))
        S = input('A strategy from her strategy set: ')

        print('Best responses: ')
        for i in self.g.best_resp(Q2,S):
            print(i)

        self.main()

    def main(self):
        """
        The main function of the model that outputs the IESDS strategies, rationalizable straties, as well as pure and mixed Nash equilibria.
        """
        # Q3: find IESDS strategies
        print('The set of IESDS strategies are: ')

        S1_final, S2_final = self.g.iesds()
        for i in S1_final:
            for j in S2_final:
                print(i+' '+j)

        # Q4: find the set of rationalizable strategies
        S1_best, S2_best = self.g.rationalizable()
        print('The set of rationalizable strategies are: ')

        for i in S1_best:
            for j in S2_best:
                print(i+' '+j)

        # Q5: find all pure_strategy Nash equilibria
        print('All pure_strategy Nash equilibria:')
        pure = self.g.pure_nash()
        for i in pure:
            st = ''
            for j in i:
                st = st+str(j)+' '
            print(st)

        # Q6: find all mixed_strategy Nash equilibria
        print('All mixed_strategy Nash equilibria:')
        st1, st2 = self.g.mixed_nash()
        print(st1)
        print(st2)

if __name__ == "__main__":
    Model().run()
