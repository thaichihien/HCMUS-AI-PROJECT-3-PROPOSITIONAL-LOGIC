
from propositional_logic import PropositionalLogic,PropositionalResolution

def ReadFile(source_file):
    file = open(source_file)
    resource = file.read().splitlines()
    file.close()
    alpha = resource[0]
    if int(resource[1]) > 0:
        KB = resource[2:]

    return alpha,KB


def WriteFile(source_file,resolutions):
    file = open(source_file,'w')

    for clauses in resolutions:
        if clauses == None:
            file.write('0\nNO')
            return
        
        file.write('{0}\n'.format(len(clauses)))
        file.writelines(clauses)
        
    file.write('YES')
    file.close()



#main
alpha,KB = ReadFile('Input.txt')
PL = PropositionalLogic()
alpha = PL.convertToClause(alpha)
KB = PL.convertKB(KB)

algorithm = PropositionalResolution()

result,resolutions = algorithm.Resolution(KB,PL.Not(alpha))

WriteFile('Output.txt',resolutions)

if result:
    print('YES')
else:print('NO')







