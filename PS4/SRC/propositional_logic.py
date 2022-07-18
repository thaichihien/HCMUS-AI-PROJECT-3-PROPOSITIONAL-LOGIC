'''
Data structure used for the resolution algorithm:
+ literal :          'A'               <=> 65                       (ascii value)
+ clause:          'A OR B'            <=> (65,66)                  (a tuple)
+ KB:       {'A OR B','-B OR C','-A'}  <=> [(65,66),(-66,67),(-65)] (a list)
'''



class PropositionalLogic:
    def convertKB(self,KB : list[str]) -> list: 
        '''
        Convert string KB list to number format for logical processing
        Ex: ['A OR B','-B OR C','-A']  ==> [(65,66),(-66,67),(-65)]

        '''

        clauses = []
        for line in KB:
            line = line.split(' AND ')
            if len(line) > 1:
                KB += line[1:]
            clause = self.convertToClause(line[0])
            clauses.append(clause)

        return clauses


    def convertToClause(self,line : str) -> tuple:
        '''
        Converts a string clause to a numeric tuple
        Ex: 'A OR B' ==> (65,66)
        
        '''

        literals = line.split(' OR ')
        clause = []
        for literal in literals:
            literal = literal.strip()
            if literal.startswith('-'):
                clause.append(ord(literal[1:])*-1)
            else:clause.append(ord(literal))

        return tuple(clause)

    
    def convertToString(self,clause : tuple) -> str:
        '''
        Converts a numeric tuple to a string clause
        Ex: (65,66) ==> 'A OR B\n'
            'empty' ==> '{}\n'

        '''

        if clause == (0,):
            return '{}\n'
        literals = []
        for literal in clause:
            temp = self.convertLiteralToString(literal)
            literals.append(temp)
        result = ' OR '.join(literals)
        result = result + '\n'
        return result


    def convertLiteralToString(self,value : int) -> str:
        '''
        Convert a number to a string literal
        Ex: 65 ==> 'A'
            -66 ==> '-B'

        '''

        literal = chr(abs(value))
        if value < 0:
            return '-{0}'.format(literal)
        else:return literal

    def Not(self,clause : tuple) -> list:
        '''
        Ex: > Not((65))
            > [(-65)]
            > Not((65,-66))
            > [(-65),(66)]
        '''
        result = []
        for literal in clause:
            value = [literal*-1]
            temp = tuple(value)
            result.append(temp)
        return result


class PropositionalResolution:
    def __init__(self) -> None:
        self.PL = PropositionalLogic()
        self.savefile = []


    def Resolution(self,KB : list,alpha : list)->bool:
        '''
        Propositional-logic resolution
        return result if  KB entails alpha or not
        Some additional things:
        + Due to project requirements, the inference condition will be checkd at the end of each loop
        + The returned results include the answer result if KB entails alpha 
          and the list of clauses will be written to file Output.txt
        
        '''


        clauses = list(KB)
        clauses += alpha
        new = []
        finish = False

        while True:
            n = len(clauses)
            for i in range(n):
                for j in range(i+1,n):
                    resolvents = self.Resolve(clauses[i],clauses[j])
                    if resolvents == None:continue
                    new.append(resolvents)

            temp = []               #to check the clause before adding to KB
            temp_file = []          #to save to the output file
            for clause in new:
                if clause not in clauses and clause not in temp:
                    if clause == (0,):finish = True
                    temp.append(clause)
                    line = self.PL.convertToString(clause)
                    temp_file.append(line)

            if len(temp) == 0 and not finish:
                self.savefile.append(None)
                return False,self.savefile

            self.savefile.append(temp_file)
            if finish: return True,self.savefile
            clauses += temp



    def Resolve(self,C1 : tuple,C2 : tuple):
        '''
        Return a clause by resolving 2 clauses
        Ignore clauses like 'A OR -B OR B'
        Ex : > Resolve('A OR -B','B OR C')
             > ('A OR C')
             > Resolve('A OR -B','C')
             > None
             > Resolve('-B','B')
             > ()
        
        '''

        infer_basis = findSameLiteral(C1,C2)
        if len(infer_basis) == 1:
            same_literal = infer_basis[0]
            clauses = combineClause(C1,C2,same_literal)
        else:
            return None
        if len(clauses) == 0:clauses = [0] 
        return tuple(clauses)



def findSameLiteral(C1:tuple,C2:tuple) -> list:
    '''
    Find complementary literals between two clauses
    Ex: > findSameLiteral('A OR B','-B OR C')
        > ['B']
        > findSameLiteral('A OR -B','-A OR B OR C')
        > ['A','B']

    '''

    result = list()
    c1 = set(C1)

    for value in C2:
        if 0 - value in c1:
            result.append(abs(value))

    return result


def combineClause(C1: tuple,C2 : tuple,_except=None):
    '''
    Combine two clauses in alphabetical order of literals 
    and ignore literal _except 
    '''
    n = len(C1)
    m = len(C2)
    i = 0
    j = 0

    result = []
    while i < n and j < m:
        if abs(C1[i]) < abs(C2[j]):
            if _except != None and abs(C1[i]) != _except and C1[i] not in result:
                result.append(C1[i])
            i += 1
        else:
            if _except != None and abs(C2[j]) != _except and C2[j] not in result:
                result.append(C2[j])
            j += 1

    while i < n:
        if _except != None and abs(C1[i]) != _except and C1[i] not in result:
            result.append(C1[i])
        i += 1
    while j < m:
        if _except != None and abs(C2[j]) != _except and C2[j] not in result:
            result.append(C2[j])
        j += 1

    return result