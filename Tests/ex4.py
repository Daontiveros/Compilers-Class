import json
import sys
from collections import OrderedDict
from collections import deque

TERMINATORS = 'jmp', 'br', 'ret'


# get the key depending on the label
def getKey(instrs, label):
    for i, instr in enumerate(instrs):
        if instr.get('label') == label:
            return i


# get path
def pathLengths(cfg, entry):
    lengths = {entry: 0}
    queue = deque([entry])

    while queue:
        node = queue.popleft()
        for child in cfg.get(node, []):
            # only if we have not visited the node
            # otherwise it will loop
            if child not in lengths: 
                lengths[child] = lengths[node] + 1
                #print(child) no
                queue.append(child)

    return lengths


def reversePostorder(cfg, entry):
    visited = set()
    postorder = []

    def dfs(node):
        if node in visited:
            #print(visited)
            return
        visited.add(node)
        for succ in cfg.get(node, []):
            dfs(succ)
        postorder.append(node)
    dfs(entry)
    listNodes = []
    for x in postorder[::-1]:
        listNodes.append(x)
    #print(listNodes)
    return listNodes 


def backEdges(graph, entry):
    # visited nodes
    visited = set()
    recStack = set()
    # cycle
    backEdges2 = []

    
    def dfs(node):
        # add node to set
        visited.add(node)
        recStack.add(node)

        # nodes
        for neighbor in graph.get(node, []):
            # recursion over not visited nodes
            if neighbor not in visited:
                # dfs(node)
                dfs(neighbor)
            elif neighbor in recStack:
                #print(node)
                #print(neighbor)
                backEdges2.append((node, neighbor))
        #
        recStack.remove(node)

    for node in graph:
        if node not in visited:
            dfs(node)

    return backEdges2

def computeDominators(cfg, startNode):
    allNodes = set(cfg.keys())
    #print(allNodes)
    for successors in cfg.values():
        allNodes.update(successors)
    allNodes = list(allNodes)

    
    dominators = {node: set(allNodes) for node in allNodes}
    #print(dominators)
    dominators[startNode] = {startNode}
    #print(dominators)
    changed = True
    while changed:
        changed = False
        for node in allNodes:
            #print(node)
            if node == startNode:
                continue
            #print(startNode)
            predecessors = [pred for pred in allNodes if node in cfg.get(pred, [])]
            if not predecessors:
                continue
            newDoms = set(allNodes)
            #print(newDoms)
            for pred in predecessors:
                newDoms &= dominators[pred]
            newDoms.add(node)  
            if newDoms != dominators[node]:
                dominators[node] = newDoms
                changed = True
            #print(node)

    return dominators


def isReducible(cfg, startNode):
    dominators = computeDominators(cfg, startNode)
    #print(dominators)
    backEdges3 = backEdges(cfg, startNode)
    for (source, target) in backEdges3:
        #print(target)
        #print(source)
        if target not in dominators[source]:
            return False
    return True



def mycfg():
    prog = json.load(sys.stdin)

    # cleaning the dictionary until we only have the instructions
    instrs = prog['functions'][0]['instrs']
    
    # dictionary where cfg will be 0:[successors]... and so on
    cleanCfg = {}

    # create the clean cfg 
    for i, instr in enumerate(instrs):
            # put successors here
            successors = []
            op = instr.get('op')
            # from op get the instruction
            if op == 'jmp': 
                labels = instr['labels'][0]
                successors.append(getKey(instrs, labels))
            elif op == 'br': 
                trueLabel, falseLabel = instr['labels']
                successors.append(getKey(instrs, trueLabel))
                successors.append(getKey(instrs, falseLabel))
            elif op == 'ret': 
                successors = []
            else:
                if i + 1 < len(instrs):
                    successors.append(i + 1)
            # put successors on values
            cleanCfg[i] = successors

    print("CFG: ", cleanCfg)

    # call path_lengths
    entry = 0 
    print(pathLengths(cleanCfg, entry))

    # call reverse_postorder
    print(reversePostorder(cleanCfg, entry))

    # the back edges so a cycle
    print(backEdges(cleanCfg, entry))

    # reducible like a tree
    print("Is reducible?", isReducible(cleanCfg, entry))
    

if __name__ == '__main__':
    mycfg()