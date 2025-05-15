from StaticError import *
from Symbol import *
from functools import *

def simulate(list_of_commands):
    """
    Executes a list of commands and processes them sequentially.

    Args:
        list_of_commands (list[str]): A list of commands to be executed.

    Returns:
        list[str]: A list of return messages corresponding to each command.
    """
    scope = [[]]  # Danh sách các env (mỗi env là một danh sách các Symbol)
    block_level = 0
    block_stack = [0] # Stack để theo dõi các block đang mở

    def findSymbol(name, env):
        # Tìm kiếm symbol trong env hiện tại và các env cha
        if not env:
            return None, -1
        
        def search(current_env, level):
            if not current_env:
                return None, -1
            local = current_env[-1]
            found_symbol = findSymbolLocal(name, local)
            if found_symbol:
                return found_symbol, level
            return search(current_env[:-1], level - 1)

        return search(env, len(env) - 1)
    
    def findSymbolLocal(name, envLocal):
        # Tìm kiếm symbol trong env hiện tại
        if not envLocal:
            return None
        return next((sym for sym in envLocal if isinstance(sym, Symbol) and sym.name == name), None)
    
    def print(mode, env):
        def printSymbol(idList, levelList, current_env, level):
            # In danh sách các symbol trong toàn bộ tầm vực 
            if not current_env:
                return idList, levelList
            envLocal = current_env[-1]
            idListLocal, levelListLocal = printSymbolLocal(idList, levelList, envLocal, level)
            return printSymbol(idListLocal, levelListLocal, current_env[:-1], level - 1)
        
        def printSymbolLocal(idList, levelList, current_env, level):
        # In danh sách các symbol trong tầm vực hiện tại
            if not current_env:
                return idList, levelList
            item = current_env[-1]
            if isinstance(item, Symbol) and item.name not in idList:
                idList += [item.name]
                levelList += [level]
            return printSymbolLocal(idList, levelList, current_env[:-1], level)
        
        def printForward(idList, levelList):
            return " ".join(f"{id}//{level}" for id, level in zip(idList, levelList))

        def printBackward(idList, levelList):
            return " ".join(f"{id}//{level}" for id, level in zip(reversed(idList), reversed(levelList)))
        
        idResultList, levelResultList = printSymbol([], [], env, len(env) - 1)
        if not idResultList: 
            return ""
        return printForward(idResultList, levelResultList) if mode == 0 else printBackward(idResultList, levelResultList)
   
        
    def checkCommandSpace(command, pos = 0):
        if pos == len(command) - 1:
            return True
        elif command[pos] == " " and command[pos - 1] == " ":
            raise InvalidInstruction(command)
        else: 
            return checkCommandSpace(command, pos + 1)

    def checkWord(wordCheck, word):
        def checkID(char):
            if not char:
                return True
            if all(c.isalnum() or c == "_" for c in char):
                return True
            return False

        def checkNumber(char):
            if not char:
                return False
            if all(c.isdigit() for c in char):
                return True
            return False
        
        def checkString(char):
            if not char:
                return True
            if all(c.isalnum() for c in char):
                return True
            return False

        if wordCheck == "checkID":
            return word[0].isalpha() and word[0].islower() and checkID(word[1:])

        if wordCheck == "checkString":
            return word[0] == "'" and word[-1] == "'" and checkString(word[1: -1])

        if wordCheck == "checkNumber":
            return checkNumber(word)
        
        return False
        
    def checkINSERT(command, env):
        partsBEGIN = command.split(" ")
        varNameBegin, varType = partsBEGIN[1], partsBEGIN[2]
        if not checkWord("checkID", varNameBegin):
            raise InvalidInstruction(command)
        symbol = findSymbolLocal(varNameBegin, env[-1])
        if symbol is not None:
            raise Redeclared(command)
        if varType not in ["number", "string"]:
            raise InvalidInstruction(command)
        env[-1] += [Symbol(varNameBegin, varType)]
        return env

    def checkASSIGN(command, env):
        partsASSIGN = command.split(" ")
        varNameASSIGN, varValue = partsASSIGN[1], partsASSIGN[2] 
        if not checkWord("checkID", varNameASSIGN):
            raise InvalidInstruction(command)
        symbol, _ = findSymbol(varNameASSIGN, env)
        if not symbol:
            raise Undeclared(command)
        if checkWord("checkNumber", varValue):
            if symbol.typ != "number":
                raise TypeMismatch(command)
        elif checkWord("checkString", varValue):
            if symbol.typ != "string":
                raise TypeMismatch(command)
        elif checkWord("checkID", varValue):
            symbol2, _ = findSymbol(varValue, env)
            if not symbol2: 
                raise Undeclared(command)
            elif symbol.typ != symbol2.typ:
                raise TypeMismatch(command)
        else:
            raise InvalidInstruction(command)
        return env

    def checkBEGIN(env, blBEGIN, bsBEGIN):
        newblBEGIN = blBEGIN + 1
        return env + [[]], newblBEGIN, bsBEGIN + [newblBEGIN]

    def checkEND(env, blEND, bsEND):
        if not bsEND or len(bsEND) <= 1: # Luôn có block 0 (global)
            raise UnknownBlock()
        closed_level = bsEND[-1]

        if closed_level != blEND:
            raise UnclosedBlock(closed_level)
        
        if not env:
            raise UnknownBlock()
        
        return env[:-1], blEND - 1, bsEND[:-1]

    def checkLOOKUP(command, env):
        partsLOOKUP = command.split(" ")
        varNameLOOKUP = partsLOOKUP[1]
        if not checkWord("checkID", varNameLOOKUP):
            raise InvalidInstruction(command)
        symbol, level = findSymbol(varNameLOOKUP, env)
        if not symbol:
            raise Undeclared(command)
        return str(level)

    def checkPRINT(env):
        return print(1, env)

    def checkRPRINT(env):
        return print(0, env)

    def checkCommand(command, env, blockLevelCommand, blockStackCommand):
        if len(command) == 0:
            raise InvalidInstruction("Invalid command")
        if command[0] == " ":  #Check command space 
            raise InvalidInstruction("Invalid command")
        checkCommandSpace(command)
        partsCommand = command.split(" ")
        keyWord = partsCommand[0]

        if keyWord == "INSERT":
            if len(partsCommand) == 3:
                return checkINSERT(command, env), "success", blockLevelCommand, blockStackCommand
            else:
                raise InvalidInstruction(command)
        elif keyWord == "ASSIGN":
            if len(partsCommand) == 3:
                return checkASSIGN(command, env), "success", blockLevelCommand, blockStackCommand
            else:
                raise InvalidInstruction(command)
        elif keyWord == "BEGIN":
            if len(partsCommand) == 1:
                envCommand, blCommand, bsCommand = checkBEGIN(env, blockLevelCommand, blockStackCommand)
                return envCommand, None, blCommand, bsCommand
            else:
                raise InvalidInstruction(command)
        elif keyWord == "END":
            if len(partsCommand) == 1:
                envCommand, blCommand, bsCommand =  checkEND(env, blockLevelCommand, blockStackCommand)
                return envCommand, None, blCommand, bsCommand
            else:
                raise InvalidInstruction(command)
        elif keyWord == "LOOKUP":
            if len(partsCommand) == 2:
                return env, checkLOOKUP(command, env), blockLevelCommand, blockStackCommand
            else:
                raise InvalidInstruction(command)
        elif keyWord == "PRINT":
            return env, checkPRINT(env), blockLevelCommand, blockStackCommand
        elif keyWord == "RPRINT":
            return env, checkRPRINT(env), blockLevelCommand, blockStackCommand
        else:
            raise InvalidInstruction("Invalid command")

    def traverseCommandList(commandList, env, results, blockLevel, blockStack):
        if not commandList:
            return results
        command = commandList[0]
        env, result, newBlockLevel, newBlockStack = checkCommand(command, env, blockLevel, blockStack)
        if result is not None:
            results += [result]
        if len(commandList) == 1:
            return results, newBlockLevel
        return traverseCommandList(commandList[1:], env, results, newBlockLevel, newBlockStack)
    
    if not list_of_commands:
        return []

    results, block_level = traverseCommandList(list_of_commands, scope, [], block_level, block_stack)

    if block_level > 0:
        raise UnclosedBlock(str(block_level))

    return results