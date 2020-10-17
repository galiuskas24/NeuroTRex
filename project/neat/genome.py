class Genome:

    def __init__(self):
        self.nodes_dict = {}
        self.connections_dict = {}

    @property
    def nodes_count(self):
        return len(self.node_ids)

    def contains_node(self, node_id):
        return node_id in self.nodes_dict

    def get_node(self, node_id):
        assert self.contains_node(node_id), f"Node with id: {node_id} does not exist."
        return self.nodes_dict[node_id]

    def add_node(self, node):
        assert not self.contains_node(node.id), f"Duplicate node id: {node.id}."
        self.nodes_dict[node.id] = node

    @property
    def node_ids(self):
        return self.nodes_dict.keys()

    @property
    def nodes(self):
        return list(self.nodes_dict.values())

    @property
    def connections_count(self):
        return len(self.connections_dict)

    def contains_connection(self, in_node_id, out_node_id):
        key = in_node_id, out_node_id
        return key in self.connections_dict

    def get_connection(self, in_node_id, out_node_id):
        assert self.contains_connection(in_node_id, out_node_id), \
               f"Connection with in_node_id={in_node_id} and out_node_id={out_node_id} does not exist."
        return self.connections_dict[(in_node_id, out_node_id)]

    def add_connection(self, connection):
        in_node_id = connection.in_node_id
        out_node_id = connection.out_node_id
        assert self.contains_node(in_node_id), f"Input node with id: {in_node_id} does not exist."
        assert self.contains_node(out_node_id), f"Output node with id: {out_node_id} does not exist."
        assert not self.contains_connection(in_node_id, out_node_id), \
               f"Connection with in_node_id={in_node_id} and out_out_id={out_node_id} already exists."
        self.connections_dict[(in_node_id, out_node_id)] = connection

    @property
    def connection_ids(self):
        return self.connections_dict.keys()

    @property
    def connections(self):
        return list(self.connections_dict.values())

    def __str__(self):
        string = "Nodes:\n"
        string += "\n".join([str(node) for node in self.nodes])
        string += "\n"
        string += "Connections:\n"
        string += "\n".join([str(connection) for connection in self.connections])
        return string
