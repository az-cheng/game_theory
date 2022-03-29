"""
Annie Cheng, zc375
March 23, 2022
"""

import numpy as np
from scipy.optimize import linprog
import warnings
warnings.filterwarnings("ignore")

class Game(object):
    """
    A class to represent a game in Game Theory.
    """

    def __init__(self, lines):
        """
        Initializes a game with the given input lines.

        Attribute lines: a string
            •the first line of the input specifies the number of strategies for player 1
            •the second line contains the names of the strategies of player 1, separated by white space
            •the third line specifies the number of strategies for player 2
            •the fourth line contains the names of the strategies of player 2, separated by white space
            •the next lines specify the payoff as a bimatrix:
                – the first of these lines correspond to the first strategy for player 1, and will give the payoffs for
                player 1 and player 2 for all of the strategies of player 2
                – the payoffs of player 1 and player 2 are separated by a comma
                – the payoffs for the different strategies for player 1 and 2 are separated by white space.
            (above specifications copied from assignment)

        Attribute inp: a list contains each line from the input string
        Attribute N_S1: number of strategies for player 1 (first line)
        Attribute S1: names of the strategies of player 1 (second line)
        Attribute dict1: a dictionary contains strategies with indexes
        Attribute N_S2: number of strategies for player 2 (third line)
        Attribute S2: names of the strategies of player 2 (fourth line)
        Attribute dict2: a dictionary contains strategies with indexes
        Attribute payoff: the payoff matrix of the game
        Attribute S1_best: the set of best respones of player 1
        Attribute S2_best: the set of best respones of player 2
        Attribute pure_strategy: the pure strategy(ies) of the game
        """
        self.lines = lines
        self.inp = lines.split('\n')

        self.N_S1 = int(self.inp[0])
        self.S1 = self.inp[1].split(' ')
        self.dict1 = {}
        for i in range(self.N_S1):
            self.dict1[i] = self.S1[i]

        self.N_S2 = int(self.inp[2])
        self.S2 = self.inp[3].split(' ')
        self.dict2 = {}
        for i in range(self.N_S2):
            self.dict2[i] = self.S2[i]

        self.payoff = []
        for i in range(4,len(self.inp)-1):
            x = self.inp[i].split(' ')
            p = []
            for j in x:
                y = j.split(',')
                q = (float(y[0]),float(y[1]))
                p.append(q)
            self.payoff.append(p)

        self.S1_best = None
        self.S2_best = None
        self.S1_best, self.S2_best = self.rationalizable()
        self.pure_strategy = self.pure_nash()


    def is_s1_dominated(self, s, payy):
        """
        A function with an input s, denoting a strategy number of player 1, and a payoff matrix payy. Returns whether s is a dominated strategy as well as what it's dominated by.
        """
        l = list(range(len(payy)))
        l.pop(s)
        dominated_by = []
        for k in l:
            for j in range(len(payy[0])):
                if payy[s][j][0] >= payy[k][j][0]:
                    return False
            dominated_by.append(self.dict1[k])
        return dominated_by


    def is_s2_dominated(self, s, payy):
        """
        A function with an input s, denoting a strategy number of player 2, and a payoff matrix payy. Returns whether s is a dominated strategy as well as what it's dominated by.
        """
        l = list(range(len(payy[0])))
        l.pop(s)
        dominated_by = []
        for k in l:
            for j in range(len(payy)):
                if payy[j][s][1] >= payy[j][k][1]:
                    return False
            dominated_by.append(self.dict2[k])
        return dominated_by


    def dominated_strategies(self, n, payy):
        """
        Returns the dominated strategies for player n.
        """
        output = []
        dominated = []
        new_payoff = np.array(payy)

        if n == 1: # player 1
            for s in list(range(len(payy))):
                result = self.is_s1_dominated(s,payy)
                if result != False:
                    dominated.append(s)
                    new_payoff = np.delete(new_payoff, s, 0)
                    for i in result:
                        output.append(str(self.dict1[s]+' '+i))

        elif n == 2: # player 2
            for s in list(range(len(payy[0]))):
                result = self.is_s2_dominated(s, payy)
                if result != False:
                    dominated.append(s)
                    new_payoff = np.delete(new_payoff, s, 1)
                    for i in result:
                        output.append(str(self.dict2[s]+' '+i))

        return output, dominated, new_payoff


    def best_resp(self,n,S):
        """
        Returns a list of best responses given a player n and a strategy S
        """
        BR = []

        if n == 1: # player 1
            s = self.S1.index(S)
            responses = []
            for i in range(self.N_S2):
                responses.append(self.payoff[s][i][1])

            x = max(responses)
            for i in range(len(responses)):
                if responses[i] == x:
                    BR.append(self.dict2[i])

        elif n == 2: # player 2
            s = self.S2.index(S)
            responses = []
            for i in range(self.N_S1):
                responses.append(self.payoff[i][s][0])

            x = max(responses)
            for i in range(len(responses)):
                if responses[i] == x:
                    BR.append(self.dict1[i])

        return BR

    def iesds(self):
        """
        Returns a list each for player 1 and player 2 of their IESDS strategies.
        """
        n_payoff = np.array(self.payoff)
        deleted_1 = []
        deleted_2 = []

        while True:
            output, dominated_1, n_payoff = self.dominated_strategies(1, n_payoff)
            output, dominated_2, n_payoff = self.dominated_strategies(2, n_payoff)
            for i in dominated_1:
                deleted_1.append(i)
            for i in dominated_2:
                deleted_2.append(i)
            if (dominated_1 == [] and dominated_2 == []) or (len(n_payoff[0]) == 1 and len(n_payoff[0][0]==1)):
                break

        S1_final = self.S1
        S2_final = self.S2
        for index in sorted(deleted_1, reverse=True):
            del S1_final[index]
        for index in sorted(deleted_2, reverse=True):
            del S2_final[index]

        return S1_final, S2_final

    def rationalizable(self):
        """
        Returns lists of players' rationalizable strategies.
        """
        S2_best = []
        for i in self.S1:
            for j in self.best_resp(1,i):
                if j not in S2_best:
                    S2_best.append(j)
        self.S2_best = S2_best

        S1_best = []
        for i in self.S2:
            for j in self.best_resp(2,i):
                if j not in S1_best:
                    S1_best.append(j)
        self.S1_best = S1_best

        return S1_best, S2_best

    def pure_nash(self):
        """
        Returns a list of pure Nash equilibrium of the game.
        """
        pure_strategy = []
        for i in self.S1:
            for j in self.S2:
                if i in self.best_resp(2,j) and j in self.best_resp(1,i):
                    pure_strategy.append([i,j])
        self.pure_strategy = pure_strategy
        return pure_strategy

    def mixed_strategy(self,p,n_payoff,n1,n2):
        """
        Return the solution of linear programs to find a mixed strategy given:

        Parameter p: a player p
        Parameter n_payoff: a payoff matrix
        Parameter n1: the number of strategies for player 1
        Parameter n2: the number of strategies for player 2
        """
        # player 1
        if len(self.pure_strategy) == 1:
            return []

        if p == 1:
            obj = [1] * n2 + [0] * n1
            lhs_1 = np.identity(n2)
            lhs_2 = []
            for i in range(n2):
                a = []
                for j in range(n1):
                    a.append(-n_payoff[j][i][1])
                lhs_2.append(a)

            lhs_eq = np.concatenate((lhs_1, np.array(lhs_2).T), axis=1)

            if n1 == 2:
                x = 1
                lhs_3 = [[1,-1]+[0]*n1]
            elif n1 == 3:
                x = 3
                lhs_3 = [[1,-1,0]+[0]*n1,[1,0,-1]+[0]*n1,[0,1,-2]+[0]*n1]

            lhs_eq = np.concatenate((lhs_eq,np.array(lhs_3)),axis=0)
            lhs_eq = np.append(lhs_eq,[[0]*n2+[1]*n1],axis=0)

            rhs_eq = [0]*n2+[0]*x+[1]

            soln = linprog(c=obj, A_eq=lhs_eq, b_eq=rhs_eq,method="revised simplex")
            opt = soln.x
            return opt[n2:]

        # player 2
        if p == 2:
            obj = [1] * n1 + [0] * n2
            lhs_1 = np.identity(n1)
            lhs_2 = []
            for i in range(n1):
                a = []
                for j in range(n2):
                    a.append(-n_payoff[i][j][0])
                lhs_2.append(a)

            lhs_eq = np.concatenate((lhs_1, np.array(lhs_2).T), axis=1)

            if n1 == 2:
                x = 1
                lhs_3 = [[1,-1]+[0]*n2]
            elif n1 == 3:
                x = 3
                lhs_3 = [[1,-1,0]+[0]*n2,[1,0,-1]+[0]*n2,[0,1,-2]+[0]*n2]

            lhs_eq = np.concatenate((lhs_eq,np.array(lhs_3)),axis=0)
            lhs_eq = np.append(lhs_eq,[[0]*n1+[1]*n2],axis=0)

            rhs_eq = [0]*n1+[0]*x+[1]

            soln = linprog(c=obj, A_eq=lhs_eq, b_eq=rhs_eq,method="revised simplex")
            opt = soln.x
            return opt[n1:]

    def mixed_nash(self):
        """
        Returns the mixed Nash equilibrium of the game.
        """
        n1 = len(self.S1_best)
        n2 = len(self.S2_best)

        n_payoff = np.array(self.payoff)

        stay1 = []
        for i in self.S1_best:
            for key, value in self.dict1.items():
                if value == i:
                    stay1.append(key)

        for i in range(self.N_S1):
            if i not in stay1:
                n_payoff = np.delete(n_payoff, i, 0)

        stay2 = []
        for i in self.S2_best:
            for key, value in self.dict2.items():
                if value == i:
                    stay2.append(key)

        for i in range(self.N_S2):
            if i not in stay2:
                n_payoff = np.delete(n_payoff, i, 1)


        if len(self.pure_strategy) == 1:
            return '',''
        else:
            mixed1 =  list(self.mixed_strategy(1, n_payoff,n1,n2))
            st1 = ''
            for i in range(self.N_S1):
                if i not in stay1:
                    k = 0
                else:
                    k = round(mixed1[0],2)
                    mixed1.pop(0)
                st1 = st1+str(k)+' '

            mixed2 =  list(self.mixed_strategy(2, n_payoff,n1,n2))
            st2 = ''
            for i in range(self.N_S2):
                if i not in stay2:
                    k = 0
                else:
                    k = round(mixed2[0],2)
                    mixed2.pop(0)
                st2 = st2+str(k)+' '

            return st1, st2
