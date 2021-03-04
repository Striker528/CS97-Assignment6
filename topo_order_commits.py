#testing:
#directory: 
    #topo-ordered-commits-test-suite/tests/repo_fixture/example-repo-1
#command:
    #python3 ../../../../topo_ordered_commits.py

#Had to remove all the spaces as they were not configured correctly

#git log --all --graph --oneline

import os
import sys
import zlib
import copy

#need regex to get the parent from the decompressed file
#import re
from collections import deque

class CommitNode:
    def __init__(self, commit_hash):
        """
        :type commit_hash: str
        """
        self.commit_hash = commit_hash
        #making parents and children lists instead of set()
        self.parents = []
        self.children = []

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

    branch_list= []
    contents_dir = os.listdir(git_dir)
    for content in contents_dir:
        name_path = git_dir + '/' + content
        is_file = os.path.isfile(name_path)
        if is_file == True:
            open_file = open(name_path, 'r')
            commit_line = open_file.readline().strip()
            branch_list.append([prefix + content, commit_line])
        else:
            #print(f"get_list_local_branches: {get_list_local_branches(name_path, prefix + content +'/')}")
            #[0]: made a list, but jsut grap the first element from tat list
            # stoping the contious nesting
            branch_list.append(get_list_local_branches(name_path, prefix + content +'/')[0])
    return branch_list

#Step 2.5
def converting_to_head_to_branches(local_branch_heads):
    #converting local_branch_heads to head_to_branches
    #head_to_branches: dict {key(hash):value(list of any branches that point to it)}
    head_to_branches = {}

    #print(f"local_branch_head: {local_branch_heads}")

    for item in local_branch_heads:
        if item[1] in head_to_branches:
            head_to_branches[item[1]].append(item[0])
        else:
            head_to_branches[item[1]] = [item[0]] 

    #print(f"head_to_branches: {head_to_branches}")
    return head_to_branches

#Step 3
def build_commit_graph(git_dir, local_branch_heads): 
    #Represents your graph
    commit_nodes = {}
    visited = set()

    stack = []
    for item in local_branch_heads:
        stack.append(item[1])
        #torubles from old double list, as some commits were not [][], so just need the commits
        #print('item: 0000000000' + item[1])


    while stack:
        #Replace with Code - Get the next element from stack, store it in commit_hash, and remove it from stack
        #main or master or origin is the first element
        #need 2D array to get the second element of the first element

        #print(f'stack: OOOOOOOOOOOOOOO {stack}')
        commit_hash = stack[0]
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

        #to get the first two chars = [0:2], to get the 3rd char to the end = [2:]
        commit_file = current_directory + '/' + commit_hash[0:2] + '/' + commit_hash[2:]
        compressed_contents = open(commit_file, 'rb').read()
        #.decode() to convert it to a string
        decompressed_contents = zlib.decompress(compressed_contents).decode()

        #testing
        #print(decompressed_contents)

        split_file = decompressed_contents.split()

        #if there are multiple parents
        current_loc = 0
        for file in split_file:
            if (file == "parent"):
                commit.parents.append(split_file[current_loc + 1])
                current_loc = current_loc + 1
            else:
                current_loc = current_loc + 1


        #parent_commit = split_file[4]

        #testing 
        #print("parent_commit is " + parent_commit)
        #print("parent_commit in list is ")
        #for item in commit.parents:
            #print(item)

        #commit.parents.append(parent_commit)
        #print(f'commit.parents is {commit.parents}')
        for p in commit.parents:
            if p not in visited:
                #Replace with Code - What do we do if p isn’t in visited?
                #Need to add hash to processing list
                stack.append(p)

            if p not in commit_nodes:
                #Replace with Code - What do we do if p isn’t in commit_nodes (graph)?
                #Need to create a parent node and add it to the graph
                new_parent_commit_node = CommitNode(p)
                commit_nodes[p] = new_parent_commit_node
            
            #Replace with Code - Record that commit_hash is a child of commit node p
            parent_commit = commit_nodes[p]
            parent_commit.children.append(commit_hash)

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
            no_children.append(commit_hash)

    #Loop through until all commits are processed
    while len(no_children) > 0:
        commit_hash = no_children.popleft()
        result.append(commit_hash)
        # Now that we are processing commit, remove all connecting edges to parent commits
        # And add parent to processing set if it has no more children after
        for parent_hash in list(copy_graph[commit_hash].parents):
            # Replace with code - Remove parent hash from current commit parents
            # need to get the commit_hash object from the graph (commit_nodes)
            # to access the parent
            copy_graph[commit_hash].parents.remove(parent_hash)

            # Replace with code - Remove child hash from parent commit children
            # need to get the commit_hash object from the graph (commit_nodes)
            # to access the parent
            copy_graph[parent_hash].children.remove(commit_hash)

            # Replace with code - How do we check if parent has no children
            # need to get the commit_hash object from the graph (commit_nodes)
            # to access the parent
            if(len(copy_graph[parent_hash].children) == 0):
                no_children.append(parent_hash)

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

    #step 2.5
    #converting local_branch_heads to dict {key(hash):value(list of any branches that point to it)}
    #to head_to_branches
    head_to_branches = converting_to_head_to_branches(local_branch_heads)

    #Step 3
    #Build the commit graph (can be helper function)
    commit_nodes = build_commit_graph(git_dir, local_branch_heads)

    #Step 4
    #Topologically sort the commit graph (can be helper fnction)
    topo_ordered_commits = topological_sort(commit_nodes)

    #testing
    #print(f'topo_order_commits: llllllllllllllllllllllllllll {topo_ordered_commits}')

    #Step 5
    #Print the sorted order (can be helper function)
    print_topo_ordered_commits_with_branch_names(commit_nodes, topo_ordered_commits, head_to_branches)


if __name__ == '__main__':
    topo_order_commits()

#strace

#ran (strace -f -o topo-test.tr pytest) in the topo ordered commits file and got everything back green and good