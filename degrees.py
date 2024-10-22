import csv
import sys

from util import Node, StackFrontier, QueueFrontier

# Maps names to a set of corresponding person_ids
names = {}

# Maps person_ids to a dictionary of: name, birth, movies (a set of movie_ids)
people = {}

# Maps movie_ids to a dictionary of: title, year, stars (a set of person_ids)
movies = {}

def load_data(directory):
    """
    Load data from CSV files into memory.
    """
    # Load people
    with open(f"{directory}/people.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            people[row["id"]] = {
                "name": row["name"],
                "birth": row["birth"],
                "movies": set()
            }
            if row["name"].lower() not in names:
                names[row["name"].lower()] = {row["id"]}
            else:
                names[row["name"].lower()].add(row["id"])

    # Load movies
    with open(f"{directory}/movies.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            movies[row["id"]] = {
                "title": row["title"],
                "year": row["year"],
                "stars": set()
            }

    # Load stars
    with open(f"{directory}/stars.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                people[row["person_id"]]["movies"].add(row["movie_id"])
                movies[row["movie_id"]]["stars"].add(row["person_id"])
            except KeyError:
                pass


def main():

    directory = sys.argv[1] if len(sys.argv) == 2 else "large"

    print("argz ", sys.argv)

    # Load data from files into memory
    print("Loading data...")
    load_data(directory)
    print("Data loaded.")

    #source = person_id_for_name(input("Name: "))
    source = person_id_for_name(sys.argv[2])

    if source is None:
        sys.exit("Person not found.")
    #target = person_id_for_name(input("Name: "))
    target = person_id_for_name(sys.argv[3])

    print("Using this data source: ", directory)
    print("Using this Person A: ", sys.argv[2])
    print("Using this Person B: ", sys.argv[3])
    
    if target is None:
        sys.exit("Person not found.")

    path = shortest_path(source, target)

    if path is None:
        print("Not connected.")
    else:
        degrees = len(path)
        print(f"{degrees} degrees of separation.")
        path = [(None, source)] + path
        for i in range(degrees):
            person1 = people[path[i][1]]["name"]
            person2 = people[path[i + 1][1]]["name"]
            movie = movies[path[i + 1][0]]["title"]
            print(f"{i + 1}: {person1} and {person2} starred in {movie}")

class PathNode:
    def __init__(self, person_id: str, movie_id: str, parent: 'PathNode' = None):
        self.person_id = person_id
        self.movie_id = movie_id
        self.parent = parent

    # Equality check based on person_id and movie_id
    def __eq__(self, other):
        if isinstance(other, PathNode):
            return self.person_id == other.person_id and self.movie_id == other.movie_id
        return False

    # Hashing based on person_id and movie_id
    def __hash__(self):
        return hash((self.person_id, self.movie_id))

    # Optional: for better debugging and printing
    def __repr__(self):
        return f"PathNode(person_id={self.person_id}, movie_id={self.movie_id}, parent={self.parent})"

def shortest_path(source, target):
    """
    Returns the shortest list of (movie_id, person_id) pairs
    that connect the source to the target.

    If no possible path, returns None.
    """

    print("Finding shotest path from ", source, " to ", target)

    frontier = QueueFrontier()

    start_node = PathNode(source, movie_id=None, parent=None)

    frontier.add(start_node)

    visited_person_id_set = set()
    visited_person_id_set.add(source)

    print("AAA, AAA, AAA")
    while frontier.empty() == False:
        popped_node = frontier.remove()
        print("BBB, BBB, BBB, Popped node is ", popped_node)

        neighbors = neighbors_for_person(popped_node.person_id)
        print("neighbors = ", neighbors)

        for neighbor in neighbors:
            neighbor_person_id = neighbor[1]
            neighbor_movie_id = neighbor[0]

            print("neighbor_person_id = ", neighbor_person_id)
            print("neighbor_movie_id = ", neighbor_movie_id)
            
    


    print(people[source])
    print(people[target])
    


    return [("93779", "914612"), ("112384", "1697")]

'''
class StackFrontier():
    def __init__(self):
        self.frontier = []

    def add(self, node):
        self.frontier.append(node)

    def contains_state(self, state):
        return any(node.state == state for node in self.frontier)

    def empty(self):
        return len(self.frontier) == 0

    def remove(self):
        if self.empty():
            raise Exception("empty frontier")
        else:
            node = self.frontier[-1]
            self.frontier = self.frontier[:-1]
            return node
'''


def person_id_for_name(name):
    """
    Returns the IMDB id for a person's name,
    resolving ambiguities as needed.
    """
    person_ids = list(names.get(name.lower(), set()))
    if len(person_ids) == 0:
        return None
    elif len(person_ids) > 1:
        print(f"Which '{name}'?")
        for person_id in person_ids:
            person = people[person_id]
            name = person["name"]
            birth = person["birth"]
            print(f"ID: {person_id}, Name: {name}, Birth: {birth}")
        try:
            person_id = input("Intended Person ID: ")
            if person_id in person_ids:
                return person_id
        except ValueError:
            pass
        return None
    else:
        return person_ids[0]


def neighbors_for_person(person_id):
    """
    Returns (movie_id, person_id) pairs for people
    who starred with a given person.
    """
    movie_ids = people[person_id]["movies"]
    neighbors = set()
    for movie_id in movie_ids:
        for person_id in movies[movie_id]["stars"]:
            neighbors.add((movie_id, person_id))
    return neighbors


if __name__ == "__main__":
    main()
