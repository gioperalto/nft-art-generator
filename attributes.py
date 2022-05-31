from unicodedata import name

import os, sys, getopt, numpy, json

if __name__ == "__main__":
    features = open('layers.txt', 'r').read().splitlines()
    i, total, distribution = 1, 0, {}


    while i != -1:

        json_path = f'files/results/{i}.json'

        try:
            with open(json_path) as json_file:
                data = json.load(json_file)
                
                for f in features:
                    if f in data: 
                        if not f in distribution: 
                            distribution[f] = {}

                        if not data[f] in distribution[f]: distribution[f][data[f]] = 0
                        
                        distribution[f][data[f]] += 1

                i += 1
                total += 1
 
        except FileNotFoundError:
            print(f'Sorry, the file "{json_path}" does not exist.')
            i = -1

    for layer in distribution:
        print(f'\n{layer}')
        for attr in distribution[layer]:
            print(f"{attr}: {'{0:.4g}%'.format(distribution[layer][attr] / total * 100)}")

    print('Distribution:', distribution)