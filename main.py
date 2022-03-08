from PIL import Image
from tqdm import tqdm
import os, sys, getopt, numpy, json

def similar(data, history, scale, i):
	for j in range(0, i):
		similarity = 0

		for x in range(0,len(data)):
			if data[x] == history[j][x]:
				similarity += 1

		if similarity >= scale: return True

	return False

def generate(limit, scale, reroll_limit):
    features = open('layers.txt', 'r').read().splitlines()

    if scale < 1: 
        print('ERROR: Scale must be greater than zero.')
        sys.exit()
    if scale > len(features): 
        print('ERROR: Scale must be <= number of features.')
        sys.exit()

    history, elements, rerolls = numpy.zeros((limit, len(features)), dtype=int), [], 0

    for f in features:
        img_path = f'files/layers/{f}/'
        elements.append([f for f in os.listdir(img_path) if os.path.isfile(os.path.join(img_path, f))])

    total_combinations = len(numpy.array(numpy.meshgrid(numpy.array(elements))).flatten())
    if limit > total_combinations:
        print(f'ERROR: Limit ({limit}) cannot be greater than total number of combinations ({total_combinations}).')
        sys.exit()

    for i in tqdm(range(1, limit+1)):
        rerolls, combination = 0, []
        for e in elements: combination.append(numpy.random.randint(len(e)))

        while similar(combination, history, scale, i-1):
            rerolls += 1
            combination = []
            
            for e in elements: combination.append(numpy.random.randint(len(e)))

            if rerolls >= reroll_limit:
                print(f'WARN: Reroll limit of {rerolls}/{reroll_limit} reached. Stopping here.')
                sys.exit()

        history[i-1] = combination
        image, attrs = [], {}

        for j in range(len(features)):
            attrs[features[j]] = elements[j][combination[j]].replace('.png', '')
            image.append(Image.open(f'files/layers/{features[j]}/{elements[j][combination[j]]}'))

        # Create JSON attribtues file

        with open(f'files/results/{i}.json', 'w') as outfile:
            json.dump(attrs, outfile)

        # Create JPEG

        base_img = image.pop(0)

        for k in image: base_img.paste(k, (0, 0), k)
            
        base_img = base_img.convert('RGB')
        base_img.save(f'files/results/{i}.jpeg')

def main(argv):
    """
    Parses input arguments and runs program.
    @param argv command-line arguments
    """
    limit, scale, reroll_limit = 10000, 1, 1000
    opts, args = getopt.getopt(argv,"l:s:rr:",["limit=","scale=", "reroll_limit="])

    for opt, arg in opts:
        if opt in ("-l", "--limit"): limit = int(arg)
        if opt in ("-s", "--scale"): scale = int(arg)
        if opt in ("-rr", "--reroll_limit"): reroll_limit = int(arg)

    if opts == [] and args == []:
        print('No options specified.')
        print('Usage [short]: python main.py -l 10000 -s 1 -rr 1000')
        print('Usage [long]: python main.py --limit=10000 --scale=1 --reroll_limit=1000')
    else: generate(limit=limit, scale=scale, reroll_limit=reroll_limit)

if __name__ == "__main__":
    main(sys.argv[1:])
    