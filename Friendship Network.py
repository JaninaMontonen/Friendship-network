"""
COMP.CS.100 Programming 1
StudentId: 050015443
Firstname Lastname: Janina Montonen
Email: janina.montonen@tuni.fi
Project 3, Friendship Network

A tool program for analyzing friendship networks

In this program I have made my own codes and functions and inputted them to a
prepared code template given by a lecturer. I have marked the codes and
functions, which have been given ready at the template, with comments. All
functions have been named and commented by a lecturer. This program uses a text
file named "friendships.txt", which was given by a lecturer.
"""


DEFAULT_FILENAME = "friendships.txt"


# This function was given ready, but I have initialized a variable named
# "network" myself, as an empty dictionary.
def read_friendship_network(filename):
    """
    Read a friendship network description file which must contain
    lines in the following format:

        name;friend_1;friend_2;...;friend_n

    At least one friend (i.e. friend_1) must be present on every line
    of the file, but there is no upper limit to how many friends a line
    can contain.

    :param filename: str, Name of the friendship network file to be read.
    :return: The data structure containing the friendship network
             information or None in the case of an error.
    """

    network = {}

    try:
        file = open(filename, mode="r")

        for line in file:
            line = line.rstrip()

            # Any line in the input file which begins with # is
            # considered a comment line and is skipped.  You can
            # therefore add # characters in the beginning of the
            # lines to temporarily ignore some lines for testing
            # purposes.
            if len(line) > 0 and line[0] == "#":
                continue

            fields = line.split(";")

            if len(fields) < 2:
                print(f"Fatal Error: line '{line}' has too few fields.")
                return None

            for name in fields:
                if not name.isalpha():
                    print(f"Fatal Error: '{name}' is not a valid name.")
                    return None

            who = fields[0]
            for friend in fields[1:]:
                # Remember: add_friendship automatically records the
                # friendships in two ways: <friend> will be <who>'s friend,
                # and <who> will be <friend>'s friend.
                add_friendship(network, who, friend)

        file.close()

        return network

    except OSError:
        print(f"Fatal Error: opening '{filename}' failed.")
        return None


# This function was given ready.
def user_interface(network):
    """
    Implements a simple user interface for the friendship network analyzer.

    The errors resulting from faulty user inputs are not fatal errors
    and the program will continue working after printing an error message.
    Most of the error messages are printed in the command functions as this
    leaves the user interface function very clear and easy to understand.

    :param network: The data structure containing the information about
                    who is friends with whom.
    :return: None
    """

    while True:
        print()
        print("Enter one of the commands "
              "[Pp]rint/[Aa]dd/[Ff]riends/[Cc]ommon/[Qq]uit")
        print("followed by one or more names if needed.")
        fields = input("Enter command: ").strip().split()

        if len(fields) == 0:
            print("Error: an empty line is not a valid command.")
            continue

        command = fields[0]
        rest = fields[1:]

        if command in ["P", "p"]:
            print_command(network, rest)

        elif command in ["A", "a"]:
            add_command(network, rest)

        elif command in ["F", "f"]:
            friends_command(network, rest)

        elif command in ["C", "c"]:
            common_friends_command(network, rest)

        elif command in ["Q", "q"]:
            print("Farewell cruel world...")
            return

        else:
            print(f"Error: unknown command '{command}'.")


def add_friendship(network, name1, name2):
    """
    Adds a friendship between name1 and name2.

    There are two situations which are not considered as errors
    but the function just doesn't do anything:

    - name1 is the same as name2
    - name1 and name2 are already friends.

    If name1 or name2 is not a name (i.e. it contains other
    characters than letters) an error message is printed and
    network is not modified.

    The friendship relation is always a two way relation:
    name1 will be registered as a friend of name2, and name2
    will be registered as a friend of name1.

    :param network: Data structure containing the friendship network.
                    This parameter will be modified to include the
                    new two way friendship.
    :param name1: str, Person 1's name
    :param name2: str, Person 2's name
    :return: None
    """

    # This error check is not necessary here since both
    # read_friendship_network and add_command functions (i.e. the only two
    # functions who call this function) already make sure that names only
    # contain letters.  It won't hurt anything to keep this check here
    # anyway, just in case.
    for name in [name1, name2]:
        if not name.isalpha():
            print("Error: '{name}' is not a valid name: friendship not added.")
            return
    # The error check above and its comments was given ready.

    # This if structure is a sanity check to make sure no one can be added as
    # his or her own friend.
    if name1 == name2:
        return

    # This if structure adds information about <name1> being <name2>'s friend
    # and other way round, into the parameter data structure (dictionary)
    # <network>. Payloads are presented as lists. If both names are already
    # known to be friends, nothing needs to be done.
    if name1 not in network:
        network[name1] = [name2]
    elif name2 not in network[name1]:
        network[name1].append(name2)
    else:
        pass

    if name2 not in network:
        network[name2] = [name1]
    elif name1 not in network[name2]:
        network[name2].append(name1)
    else:
        pass


def print_command(network, namelist):
    """
    The function neatly prints out the friendship network.
    All the names and friends' names are printed in alphabetical order.
    Friends' names are printed under the name of the person whose friends
    they are. In front of the every friend's name there is "- "
    (minus and space) character combination.

    The parameter namelist must be an empty list, otherwise an error message
    will be printed and function will return back to user interface which
    will continue normally.

    :param network: Contains the friendship network to be printed.
    :param namelist: list, This parameter should be an empty list since
                           print command doesn't require any names after it.
                           It is passed as a parameter only for error checking
                           purposes.
    :return: None
    """

    # This error check was given ready.
    if len(namelist) != 0:
        print("Error: there was extra text after [Pp]rint command.")
        return

    # This for structure prints all friendships in alphabetical order.
    for help_name1 in sorted(network):
        print(help_name1)
        for help_name2 in sorted(network[help_name1]):
            print("-", help_name2)


# This function was given ready.
def add_command(network, namelist):
    """
    Adds a friendship between the first element of the namelist
    and the rest of its elements.

    The friendships are automatically considered to be a two way relationship,
    therefore, if A has B added as his friend, B will also have A added
    as her friend.

    Any errors happening during a call to this functions are not fatal
    errors.  The function will print an error message and return back
    to the user interface which will continue normally.

    In case of any error, network will be left unmodified.

    :param network: The friendship network data structure which will
                    be modified as a result of the call to this function.
    :param namelist: list, This list must have at least two elements.
                     The first one is the name of the person to
                     whom we want to add friends.  The rest of the
                     elements are the names of the friends to be added.
    :return: None
    """

    if len(namelist) < 2:
        print("Error: [Aa]dd command requires minimum two names.")
        return

    for name in namelist:
        if not name.isalpha():
            print(f"Error: '{name}' is not a valid name.")
            return

    for friend in namelist[1:]:
        # Remember, add_friendship function is supposed to automatically
        # add a two way relationship.  Therefore one call to it is enough.
        add_friendship(network, namelist[0], friend)


def friends_command(network, namelist):
    """
    Print out, in aplhabetical order, all the friends of the person whose
    name is the only element in the namelist parameter.

    An error message is printed if the namelist doesn't contain exactly
    one element which is a string of letters.

    An error message is also printed if the name in the namelist does not
    exist in the friendship network.

    These error conditions are not fatal errors. The program will continue
    normally after printing an error message and returning to the
    user interface.

    :param network: Data structure containing the friendship information.
    :param namelist: list, List containing one element: the name of the
                           person whose friends are we interested in printing.
    :return: None
    """

    # These two if structures were given ready.
    if len(namelist) != 1:
        print("Error: [Ff]riends command requires exactly one name.")
        return

    name = namelist[0]
    if not name.isalpha():
        print(f"Error: {name} is not a valid name.")
        return

    # This if structure checks, if <name> is an unknown person. If so it prints
    # an error message and stops.
    if namelist[0] not in network:
        print(f"Error: '{name}' is an unknown name.")
        return

    # Below <name>'s friends are printed in alphabetical order.
    for name_of_a_friend in sorted(network[namelist[0]]):
        print(name_of_a_friend)


def common_friends_command(network, namelist):
    """
    Prints, in alphabetical order, the common friends of the two persons whose
    names are in the namelist.

    The following error conditions are possible:

    - There are more or less than two names in the namelist.
    - Either of the names in the namelist contains some other
      characters than letters.
    - Either of the names in namelist does not exist in the network.

    All these errors cause an error message to printed but they are not
    fatal errors: the program will return to user interface and continue
    normally after printing the error message.

    :param network: Data structure containing the friendship information.
    :param namelist: list, A list containing exactly two names.
    :return: None
    """

    if len(namelist) != 2:
        print("[Cc]ommon command requires exactly two names.")
        return

    for name in namelist:
        if not name.isalpha():
            print(f"Error: {name} is not a valid name.")
            return

    for name in namelist:
        # This if structure checks, if <name> is an unknown person. If so it
        # prints an error message and stops.
        if name not in network:
            print(f"Error: '{name}' is an unknown name.")
            return

    name1 = namelist[0]
    name2 = namelist[1]
    # The code above was given ready.

    # Below is another sanity check to make sure that a person does not have
    # common friends with him/herself.
    if name1 == name2:
        print(f"{name1} has no common friends with him/herself.")
        return

    # Below the common friends of <name1> and <name2> are printed. If they
    # don't have any common friends, an error message is printed. The common
    # friends are putted into <help_list>.
    help_list = []
    for name_to_search1 in network[name1]:
        for name_to_search2 in network[name2]:
            if name_to_search2 == name_to_search1:
                help_list.append(name_to_search2)
            else:
                pass

    if len(help_list) == 0:
        print(f"{name1} and {name2} have no common friends.")
    else:
        for name in sorted(help_list):
            print(name)


# This main function was given ready.
def main():

    filename = input("Enter the name of the input file: ")

    # If the user inputs an empty filename let's use the default file.
    if filename == "":
        filename = DEFAULT_FILENAME

    net = read_friendship_network(filename)

    if net is None:
        return
    else:
        print(f"File {filename} successfully read.")

    user_interface(net)


if __name__ == "__main__":
    main()