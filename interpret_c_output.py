

def read_output(fname: str):
    with open(fname, 'r') as f:
        lines = f.readlines()
        info = []
        for i in range(len(lines)):
            info.append(process_line(lines[i]))
        return info

def process_line(line: str):
    elements = line.split(";")
    ptr = 0
    res = dict()
    res["num_edges"] = int(elements[ptr])
    ptr += 1
    res["num_vertices"] = int(elements[ptr])
    ptr += 1
    res["total_distance"] = int(elements[ptr])
    ptr += 1
    res["average_distance"] = float(elements[ptr])
    ptr += 1
    res["max_diameter"] = int(elements[ptr])
    ptr += 1
    res["num_triangles"] = int(elements[ptr])
    ptr += 1
    res["typical_distance"] = [0]
    for i in range(res["max_diameter"]):
        res["typical_distance"].append(int(elements[ptr]))
        ptr += 1
    res["num_components"] = int(elements[ptr])
    ptr += 1

    res["components"] = []

    for i in range(res["num_components"]):
        comp = dict()
        comp["root_node"] = int(elements[ptr])
        ptr += 1
        comp["num_vertices"] = int(elements[ptr])
        ptr += 1
        comp["total_distance"] = int(elements[ptr])
        ptr += 1
        comp["average_distance"] = float(elements[ptr])
        ptr += 1
        comp["max_diameter"] = int(elements[ptr])
        ptr += 1
        comp["typical_distance"] = [0]
        for i in range(comp["max_diameter"]):
            comp["typical_distance"].append(int(elements[ptr]))
            ptr += 1

        res["components"].append(comp)

    return res

# info = read_output("/home/wouter/master/Complex Networks/edgestepgraphsinC/outputs/output20.csv")
# print(info)
# print()