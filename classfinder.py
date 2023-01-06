import json
import re
from operator import itemgetter
import requests

# finds the most similar list
# master = [] with n items
# candidates = [[],[],[],...] each nested list with n items
# original_candidates = [{}, {}, {},...]
def best_similarity(master, candidates, originalcandidates):
    counts = [0] * len(candidates)
    for i, masterval in enumerate(master):
        for ci, c in enumerate(candidates):
            counts[ci] += masterval == c[i] #True is numerically 1
    candidate_scores = zip(counts, originalcandidates)
    # returns a map
    return max(candidate_scores, key=itemgetter(0))[1]

# sorts a list alphabetically and adds padding (empty strings) so it can be used in the best_similarity function
def list_sort(list, padding):
    return sorted(list) + [''] * (padding - len(list))

def main():

    old = requests.get("https://discord.com/assets/454210598d8beed381ab.js")._content.decode("utf8")
    new = requests.get("https://canary.discord.com/assets/782c119d5f878e08f08e.js")._content.decode("utf8")
    
    # jsonifies the source files
    replacements = [[r"\n", ""], [r"\},\d+.*?s=", ","], [r"\}{2,}.*", "}]"], [r"^.*\{,", "["], [r"(?<=\{|,)\b", "\""], [":", "\":"],["\"+", "\""]]
    for r in replacements:
        old = re.sub(r[0], r[1], old)
        new = re.sub(r[0], r[1], new)
    old = json.loads(old)
    new = json.loads(new)

    output = open("output.md", "w+")

    # turns the new element map into a nested list
    new_as_list = [list_sort(list(new_element_map), 100) for new_element_map in new]

    for element_map in old:

        element_list = list_sort(list(element_map.keys()), 100)
        match = best_similarity(element_list, new_as_list, new)

        for element in list(element_map.keys()):

            # checks if element contains a number as the first character, or a parenthesis
            # -> gets rid of elements such as "calc(...)" or "24px"
            if element in match and re.search(r"^\d|\(|\)", match[element]):
                print(f"Discarding {element}")
            else:
                try:
                    # splits elements with multiple classes into multiple lines
                    for substring in zip(element_map[element].split(' '), match[element].split(' ')):
                        output.write(f"{substring[0]} = {substring[1]}\n")
                    print(f"Found {element_map[element]}")
                except:
                    print(f"Couldn't find {element}")

    print("Finished")
    output.close()

main()