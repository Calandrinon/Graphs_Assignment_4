class DisjointSet:

    def __init__(self, nodes):
        self.parent_list = [i for i in range(0, nodes)]
        
    
    def find_set(self, node):
        if self.parent_list[node] == node:
            return node
        parent = self.find_set(self.parent_list[node])
        self.parent_list[node] = parent 
        return parent


    def merge_sets(self, set_a, set_b):
        self.parent_list[self.find_set(set_a)] = self.find_set(set_b)


    def get_number_of_sets(self):
        myset = set()

        for i in range(0, len(self.parent_list)):
            myset.add(self.find_set(i))

        return len(myset)