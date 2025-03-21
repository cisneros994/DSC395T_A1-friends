"""Assignment 1: Friend of a Friend

Please complete these functions, to answer queries given a dataset of
friendship relations, that meet the specifications of the handout
and docstrings below.

Notes:
- you should create and test your own scenarios to fully test your functions, 
  including testing of "edge cases"
"""

from py_friends.friends import Friends

"""
************** READ THIS ***************
************** READ THIS ***************
************** READ THIS ***************
************** READ THIS ***************
************** READ THIS ***************

If you worked in a group on this project, please type the EIDs of your groupmates below (do not include yourself).
Leave it as TODO otherwise.
Groupmate 1: TODO
Groupmate 2: TODO
"""

def load_pairs(filename):
    """
    Args:
        filename (str): name of input file

    Returns:
        List of pairs, where each pair is a Tuple of two strings

    Notes:
    - Each non-empty line in the input file contains two strings, that
      are separated by one or more space characters.
    - You should remove whitespace characters, and skip over empty input lines.
    """
    list_of_pairs = []
    with open(filename, 'rt') as infile:

# ------------ BEGIN YOUR CODE ------------
        # Read the filename and place lines into list object #test123
        lines = infile.readlines()

        for line in lines:
            # Remove whitespaces
            line = " ".join(line.split())
            # Split the names
            line = line.split()
            # Add potential edge cases where names have some other separator: tested - space, tab, multiple spaces/tabs
            # Edge Case: remove empty lines
            if len(line) == 2:
                # Convert the 2 line items into a Tuple()
                # Capitalize names
                # Add tuple to list
                list_of_pairs.append(((line[0]).upper(), (line[1]).upper()))

# ------------ END YOUR CODE ------------

    return list_of_pairs 

def make_friends_directory(pairs):
    """Create a directory of persons, for looking up immediate friends

    Args:
        pairs (List[Tuple[str, str]]): list of pairs

    Returns:
        Dict[str, Set] where each key is a person, with value being the set of 
        related persons given in the input list of pairs

    Notes:
    - you should infer from the input that relationships are two-way: 
      if given a pair (x,y), then assume that y is a friend of x, and x is 
      a friend of y
    - no own-relationships: ignore pairs of the form (x, x)
    """
    directory = dict()

    # ------------ BEGIN YOUR CODE ------------
    for name1, name2 in pairs:
        #Edge Case: Ignore own-pairs (name1 = name2)
        if name1 != name2:
        # Creates a new key of 'name1' if it doesn't exist prior
            if name1 not in directory:
                directory[name1] = set()
            # Adds 'name2' to Set object
            # Set object removes duplicates b/c sets have unique values
            directory[name1].add(name2)

            if name2 not in directory:
                directory[name2] = set()
            directory[name2].add(name1)
    # ------------ END YOUR CODE ------------

    return directory


def find_all_number_of_friends(my_dir):
    """List every person in the directory by the number of friends each has

    Returns a sorted (in decreasing order by number of friends) list 
    of 2-tuples, where each tuples has the person's name as the first element,
    the number of friends as the second element.
    """
    friends_list = []

    # ------------ BEGIN YOUR CODE ------------
    # Create list of Tuples(person, # friends)
    friends_list =[(key, len(values)) for key, values in my_dir.items()]

    # 1st sort: # of friends in descending order (-x[1]) (can't use reverse=true b/c of 2nd sort)
    # 2nd sort: ASCII order in ascending order (x[0])
    friends_list = sorted(friends_list, key =lambda x:(-x[1], x[0]))
    # ------------ END YOUR CODE ------------

    return friends_list


def make_team_roster(person, my_dir):
    """Returns str encoding of a person's team of friends of friends
    Args:
        person (str): the team leader's name
        my_dir (Dict): dictionary of all relationships

    Returns:
        str of the form 'A_B_D_G' where the underscore '_' is the
        separator character, and the first substring is the 
        team leader's name, i.e. A.  Subsequent unique substrings are 
        friends of A or friends of friends of A, in ASCII order
        and excluding the team leader's name (i.e. A only appears
        as the first substring)

    Notes:
    - Team is drawn from only within two circles of A -- friends of A, plus 
      their immediate friends only
    """
    assert person in my_dir
    label = person

    # ------------ BEGIN YOUR CODE ------------

    team = my_dir[person] # create team set

    for x in my_dir[person]: # for each friend of a person
        team = team.union(my_dir[x]) # combine friend's set of friends with 'person' set of friends

    team.discard(person) # remove team leader name from set (discard should do nothing if 'person' not in set)
    team = sorted(team) #convert to list and sort ASCII order #'sorted' automatically converts team from set to list
    team.insert(0, person) # add team leader to start of list
    label = '_'.join(team) # convert to string

    # ------------ END YOUR CODE ------------

    return label


def find_smallest_team(my_dir):
    """Find team with smallest size, and return its roster label str
    - if ties, return the team roster label that is first in ASCII order
    """
    smallest_teams = []

    # ------------ BEGIN YOUR CODE

    #roster_list = []
    roster_smallest = None
    team_length_smallest = float('inf')

    # Create list of Tuples(person, # team members)
    for key in my_dir:
        roster = make_team_roster(key, my_dir) # get roster str
        team_length = roster.count('_') # get roster length

        # More efficient way, smaller Big-O:
        # 1) Check if new team is smaller than the smallest team we've stored already
        # 2) If team length is the same size, check for smaller # for ASCII order. Initiate roster_smallest value with 1st key
        if team_length < team_length_smallest or (team_length == team_length_smallest and (roster_smallest is None or roster < roster_smallest)):
            #roster_list.append((roster, team_length)) # add tuple to list #delete
            team_length_smallest = team_length
            roster_smallest = roster

    # Edge Case: check if my_dir is empty
    if bool(my_dir):
        smallest_teams.insert(0, roster_smallest)
    # ------------ END YOUR CODE

    return smallest_teams[0] if smallest_teams else ""



if __name__ == '__main__':
    # To run and examine your function calls

    print('\n1. run load_pairs')
    my_pairs = load_pairs('2testfriends.txt')
    print(my_pairs)

    print('\n2. run make_directory')
    my_dir = make_friends_directory(my_pairs)
    print(my_dir) 

    print('\n3. run find_all_number_of_friends')
    print(find_all_number_of_friends(my_dir))
    '''
    print('\n4. run make_team_roster')
    my_person = 'HAN'   # test with this person as team leader
    team_roster = make_team_roster(my_person, my_dir)
    print(team_roster)
    '''
    print('\n5. run find_smallest_team')
    print(find_smallest_team(my_dir))

    print('\n6. run Friends iterator')

    # Corrections from Ed discussions named "possible small error in provided code"
    friends_iterator = Friends(my_dir)
    for num, pair in enumerate(friends_iterator):
        print(num, pair)
        if num == 50:
            break
    # print(len(list(friends_iterator)))
    # LC - I think the original length code was correct - the other one comes out as 0
    #print(len(list(friends_iterator)) + num + 1)
    print(len(list(friends_iterator)))