import sys

sites = {}
for filename in sys.argv[1:]:
    for line in open(filename):
        # each line may refer to any number of web sites
        index = 0
        while True:
            site = None
            index = line.find("http://", index)
            if index > -1:  # Return -1 on failure
                index += len("http://")  # increment index by the length of "http://"
                for j in range(index, len(line)):
                    if not (line[j].isalnum() or line[j] in ".-"):  # until one that isn't valid for a web site's name
                        site = line[index:j].lower()
                        break
                if site and "." in site:
                    sites.setdefault(site, set()).add(filename)
                index = j
            else:
                break

for site in sorted(sites):
    print("{0} is referred to in:".format(site))
    for filename in sorted(sites[site], key=str.lower):
        print("    {0}".format(filename))
