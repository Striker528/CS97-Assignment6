import os
import sys
import zlib
import copy

#need regex to get the parent from the decompressed file
import re
from collections import deque

class CommitNode:
    def __init__(self, commit_hash):
        """
        :type commit_hash: str
        """
        self.commit_hash = commit_hash
        self.parents = set()
        self.children = set()

#Step 1
def get_git_directory():
    current_directory = os.getcwd()
    #testing
    #print("beginning directiory XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX" + current_directory)
    #print(current_directory)
    while ('/' != current_directory):
        if( os.path.exists(current_directory + "/.git")):
            going_in_git_directory = current_directory + "/.git"
            #testing
            #print("current_direcotyr: OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO" + going_in_git_directory)
            #print(current_directory)
            return going_in_git_directory
        else:
            if (os.path.exists(os.path.dirname(current_directory)) == False):
                exit(1)
            else:
                current_directory = os.path.dirname(current_directory)
    print("Not inside a git respository")
    exit(1)

#Step 2
def get_list_local_branches(git_dir, prefix = ''):

    #testing
    #print("current_directory: OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO" + git_dir)

    branchList= []
    contents_dir = os.listdir(git_dir)
    for content in contents_dir:
        namePath = git_dir + '/' + content
        isFile = os.path.isfile(namePath)
        if isFile == True:
            openFile = open(namePath, 'r')
            commitLine = openFile.readline().strip()
            branchList.append([prefix + content, commitLine])
        else:
            branchList.append(get_list_local_branches(namePath, prefix+ content +'/'))
    return branchList


    #Normal loop of getting all the directores in one list and looping through that. 
    #Get all the folders in the .git repo

    #go into /.git 's child directory of refs/heads
    os.chdir(git_dir + '/refs/heads')

    contents_dir = os.listdir(git_dir)
    #starts with the master or main branch (or the end of the commit history)
    local_branch_heads = []
    #Then loop through all the folders
    for content in contents_dir:
        #if there is a file
        if (os.path.isfile(content)):
            #In each folder, open up the file
            file = open(content, 'r')
            #read the first line from the file and append that to the branch heads
            #[branch, commit hash that branch points too]
            local_branch_heads.append[content, file.readline().strip()]
        #else, if the item is a directory
        else:
            #add the directory to the directory list
            contents_dir.append(content)
    return local_branch_heads

#Step 3
def build_commit_graph(git_dir, local_branch_heads): 
    #Represents your graph
    commit_nodes = {}
    visited = set()
    stack = local_branch_heads
    while stack:
        #Replace with Code - Get the next element from stack, store it in commit_hash, and remove it from stack
        #main or master or origin is the first element
        #need 2D array to get the second element of the first element
        commit_hash = stack[0][1]
        stack.remove(stack[0])

        if commit_hash in visited:
            #Replace with code - What do you do if the commit we’re on is already in visited?
            continue

        visited.add(commit_hash)
        if commit_hash not in commit_nodes:
            #Replace with code - Create a commit node and store it in the graph for later use
            new_commit_node = CommitNode(commit_hash)
            commit_nodes[commit_hash] = new_commit_node

        #Replace with Code - Using commit_hash, retrieve commit node object from graph
        commit = commit_nodes[commit_hash]

        #Replace with Code - Find commit_hash in the objects folder, decompress it, and get parent commits
        os.chdir(git_dir + '/objects')
        current_directory = os.getcwd()

        #testing
        #print("commmit_hash 888888888888888888888888888888888888: " + commit_hash)

        #to get the first two chars = [0:2]
        #to get the 3rd char to the end = [2:]
        commit_file = current_directory + '/' + commit_hash[0:2] + '/' + commit_hash[2:]
        compressed_contents = open(commit_file, 'rb').read()
        #.decode() to convert it to a string
        decompressed_contents = zlib.decompress(compressed_contents).decode()

        #testing
        print(decompressed_contents)


        #only way to get the parents is with regex
        #https://www.programiz.com/python-programming/regex
        # ^ : starts with
        # $ : ends with
        # .* : (*)zero or more occurances with (.)any characters
        # \s : matches where a string contains any whitespae character
        # \S : matches where a string contains any non-whitspace character
        # re.finall(pattern, string) : returns a list of strings containg all matches
        # re.search(pattern, string) : looks for the first location wehre the RegEx pattern produces a match
            #with the string
        parent_commit = re.findall("^parent\s .* \s$", decompressed_contents)

        #testing 
        print("parent_commit is " + parent_commit)


        commit.parents.append(parent_commit)
        for p in commit.parents:
            if p not in visited:
                #Replace with Code - What do we do if p isn’t in visited?
                visited.add(p)
            if p not in commit_nodes:
                #Replace with Code - What do we do if p isn’t in commit_nodes (graph)?    
                commit_nodes[p.commit_hash] = p
            
            #Replace with Code - Record that commit_hash is a child of commit node p
            commit_hash.parents.append(p)
            p.children.append(commit_hash)

    return commit_nodes

#Step 4
def topological_sort(commit_nodes):
    # commits we have processed and are now sorted
    result = []

    # commits we can process now
    no_children = deque()

    # Copy graph so we don't erase info
    copy_graph = copy.deepcopy(commit_nodes)

    # If the commit has no children, we can process it
    for commit_hash in copy_graph:
        if len(copy_graph[commit_hash].children) == 0:
            no_children.append(commit)

    #Loop through until all commits are processed
    while len(no_children) > 0:
        commit_hash = no_children.popleft()
        result.append(commit_hash)
        # Now that we are processing commit, remove all connecting edges to parent commits
        # And add parent to processing set if it has no more children after
        for parent_hash in list(copy_graph[commit_hash].parents):
            # Replace with code - Remove parent hash from current commit parents
            commit_hash.parents.remove(parent_hash)

            # Replace with code - Remove child hash from parent commit children
            parent_hash.children.remove(commit_hash)


            # Replace with code - How do we check if parent has no children
            if(parent_hash.children.len == 0):
                no_children.append(parent)

    # Error check at the end
    if len(result) < len(commit_nodes):
        raise Exception("cycle detected")
    return result

#Step 5
def print_topo_ordered_commits_with_branch_names(commit_nodes, topo_ordered_commits, head_to_branches):
    jumped = False
    for i in range(len(topo_ordered_commits)):
        commit_hash = topo_ordered_commits[i]
        if jumped:
            jumped = False
            sticky_hash = ' '.join(commit_nodes[commit_hash].children)
            print(f'={sticky_hash}')
        branches = sorted(head_to_branches[commit_hash]) if commit_hash in head_to_branches else []
        print(commit_hash + (' ' + ' '.join(branches) if branches else ''))
        if i+1 < len(topo_ordered_commits) and topo_ordered_commits[i+1] not in commit_nodes[commit_hash].parents:
            jumped = True
            sticky_hash = ' '.join(commit_nodes[commit_hash].parents)
            print(f'{sticky_hash}=\n')


def topo_order_commits():
    #Step 1
    #Get git directory (can be helper function)
    git_dir = get_git_directory()
    #print("get_dir: 66666666666666666666666666666666666666666666666666666666666666666" + get_dir)
    #print(get_dir)

    #for Step 2 going into /refs/heads
    git_dir_refs_heads = git_dir + "/refs/heads"

    #Step 2 
    #Get list of local branch names (can be helper function)
    local_branch_heads = get_list_local_branches(git_dir_refs_heads)

    #Step 3
    #Build the commit graph (can be helper function)
    commit_nodes = build_commit_graph(git_dir, local_branch_heads)

    #Step 4
    #Topologically sort the commit graph (can be helper fnction)
    topo_ordered_commits = topological_sort(commit_nodes)

    #Step 5
    #Print the sorted order (can be helper function)
    print_topo_ordered_commits_with_branch_names(commit_nodes, topo_ordered_commits, local_branch_heads)


if __name__ == '__main__':
    topo_order_commits()