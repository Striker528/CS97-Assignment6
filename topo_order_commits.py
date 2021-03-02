import os
import sys
import zlib
import copy
from collections import deque

class CommitNode:
    def __init__(self, commit_hash):
        """
        :type commit_hash: str
        """
        self.commit_hash = commit_hash
        self.parents = set()
        self.children = set()


def get_git_directory():
    current_directory = os.getcwd()
    while ('/' != current_directory):
        if( os.path.exists(current_directory + "/.git")):
            return current_directory
        else:
            if (os.path.exists() == False):
                exit(1)
            else:
                current_directory = os.path.dirname(current_directory)
    print("Not inside a git respository")
    exit(1)


def get_list_local_branches(git_dir):
    #Normal loop of getting all the directores in one list and looping through that. 
    #Get all the folders in the .git repo
    contents_dir = os.listdir(git_dir)
    local_branch_heads = []
    #Then loop through all the folders
    for content in contents_dir:
        #if there is a file
        if (os.path.isfile(conent)):
            #In each folder, open up the file
            file = open(content, 'r')
            #read the first line from the file and append that to the branch heads
            local_branch_heads.append[content, file.readline().strip()]
        #else, if the item is a directory
        else:
            #add the directory to the directory list
            contents_dir.append(content)
    return local_branch_heads


def build_commit_graph(git_dir, local_branch_heads):
    #Represents your graph
    commit_nodes = {} 
    visited = set() 
    stack = local_branch_heads
    while stack:
        #Replace with Code - Get the next element from stack, store it in commit_hash, and remove it from stack
        commit_hash = 

        if commit_hash in visited:
            #Replace with code - What do you do if the commit we’re on is already in visited?

        visited.add(commit_hash)
        if commit_hash not in commit_nodes:
            #Replace with code - Create a commit node and store it in the graph for later use



        #Replace with Code - Using commit_hash, retrieve commit node object from graph
        commit = 

        #Replace with Code - Find commit_hash in the objects folder, decompress it, and get parent commits
        commit.parents =

        for p in commit.parents:
            if p not in visited:
                #Replace with Code - What do we do if p isn’t in visited?
            

            if p not in commit_nodes:
                #Replace with Code - What do we do if p isn’t in commit_nodes (graph)?    
            
            
            #Replace with Code - Record that commit_hash is a child of commit node p
            
    
    return commit_nodes


def topological_sort(commit_nodes):
    # commits we have processed and are now sorted
    result = []

    # commits we can process now
    no_children = deque()

    # Copy graph so we don't erase info
    copy_graph = copy.deepcopy(commit_nodes)


    # If the commit has no children, we can process it
    for commit_hash in copy_graph:
        if len(copy_graph[commit_hash].children) == 0:
            no_children.append(commit)

    #Loop through until all commits are processed
    while len(no_children) > 0:
        commit_hash = no_children.popleft()
        result.append(commit_hash)
        # Now that we are processing commit, remove all connecting edges to parent commits
        # And add parent to processing set if it has no more children after
        for parent_hash in list(copy_graph[commit_hash].parents):
            # Replace with code - Remove parent hash from current commit parents


            # Replace with code - Remove child hash from parent commit children


            # Replace with code - How do we check if parent has no children
                
                
                no_children.append(parent)
    # Error check at the end
    if len(result) < len(commit_nodes):
        raise Exception("cycle detected")
    return result


def print_topo_ordered_commits_with_branch_names(commit_nodes, topo_ordered_commits, head_to_branches):
    jumped = False
    for i in range(len(topo_ordered_commits)):
        commit_hash = topo_ordered_commits[i]
        if jumped:
            jumped = False
            sticky_hash = ' '.join(commit_nodes[commit_hash].children)
            print(f'={sticky_hash}')
        branches = sorted(head_to_branches[commit_hash]) if commit_hash in head_to_branches else []
        print(commit_hash + (' ' + ' '.join(branches) if branches else ''))
        if i+1 < len(topo_ordered_commits) and topo_ordered_commits[i+1] not in commit_nodes[commit_hash].parents:
            jumped = True
            sticky_hash = ' '.join(commit_nodes[commit_hash].parents)
            print(f'{sticky_hash}=\n')


def topo_order_commits():
    #Get git directory (can be helper function)
    get_dir = get_git_directory()

    #Get list of local branch names (can be helper function)
    local_branch_heads = get_list_local_branches(get_dir)

    #Build the commit graph (can be helper function)
    commit_nodes = build_commit_graph(git_dir, local_branch_heads)

    #Topologically sort the commit graph (can be helper fnction)
    topo_ordered_commits = topological_sort(commit_nodes)

    #Print the sorted order (can be helper function)
    print_topo_ordered_commits_with_branch_names(commit_nodes, topo_ordered_commits, head_to_branches)


if __name__ == '__main__':
    topo_order_commits()