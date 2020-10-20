from PIL import Image, ImageDraw


class PngExporter:

    def __init__(self,
                 width=800,
                 height=600,
                 abs_max_weight=1.0,
                 abs_min_weight=0.1,
                 connection_width_part=0.01,
                 show_disabled=False,
                 node_size_part=0.05,
                 node_outline_width_part=0.05,
                 rescale_factor=0.95,
                 background_color=(255, 255, 255),
                 negative_weight_color=(255, 0, 0),
                 positive_weight_color=(0, 255, 0),
                 disabled_weight_color=(192, 192, 192),
                 input_node_fill_color=(90, 90, 90),
                 hidden_node_fill_color=(150, 150, 150),
                 output_node_fill_color=(230, 230, 230),
                 node_outline_color=(0, 0, 0)):
        self.width = width
        self.height = height
        self.abs_max_weight = abs_max_weight
        self.abs_min_weight = abs_min_weight
        self.connection_width_part = connection_width_part
        self.show_disabled = show_disabled
        self.node_size_part = node_size_part
        self.node_outline_width_part = node_outline_width_part
        self.rescale_factor = rescale_factor
        self.background_color = background_color
        self.negative_weight_color = negative_weight_color
        self.positive_weight_color = positive_weight_color
        self.disabled_weight_color = disabled_weight_color
        self.input_node_fill_color = input_node_fill_color
        self.hidden_node_fill_color = hidden_node_fill_color
        self.output_node_fill_color = output_node_fill_color
        self.node_outline_color = node_outline_color

    def _separate_layers(self, genome):
        layers = {}
        for node in genome.nodes:
            layer = node.layer
            if layer not in layers:
                layers[layer] = []
            layers[layer].append(node)
        for layer in layers:
            layers[layer].sort(key=lambda n: n.id)
        return layers

    def _determine_weight_color(self, connection):
        if not connection.enabled:
            return self.disabled_weight_color
        return self.positive_weight_color if connection.weight > 0 else self.negative_weight_color

    def _determine_node_color(self, node, layers):
        first_layer = 0
        last_layer = len(layers) - 1
        if node.layer == first_layer:
            return self.input_node_fill_color
        elif node.layer == last_layer:
            return self.output_node_fill_color
        else:
            return self.hidden_node_fill_color

    def _resolution_error(self, message):
        raise Exception(f"Resolution is too small. {message}")

    def _create_image(self, genome):
        image = Image.new("RGB", (self.width, self.height), color=self.background_color)
        d = ImageDraw.Draw(image)

        default_node_size = int(self.width * self.node_size_part)
        if default_node_size < 1:
            self._resolution_error("Default node size is not visible.")
        max_connection_width = int(self.width * self.connection_width_part)
        if max_connection_width < 1:
            self._resolution_error("Maximal connection width is not visible.")

        offset_x = default_node_size
        layers = self._separate_layers(genome)
        layers_distance = (self.width - 2 * offset_x) // (len(layers) - 1)
        if layers_distance < 1:
            self._resolution_error("Distance between layers is not visible.")

        node_data = {}
        for layer in layers:
            current_x = offset_x + layer * layers_distance
            current_nodes = layers[layer]
            for i, node in enumerate(current_nodes):
                nodes_distance = self.height // (len(current_nodes) + 1)
                if nodes_distance < 1:
                    self._resolution_error("Distance between nodes is not visible.")
                current_node_size = min(default_node_size, layers_distance, nodes_distance)
                if current_node_size < default_node_size:
                    current_node_size = int(current_node_size * self.rescale_factor)
                if current_node_size < 1:
                    self._resolution_error("Nodes are not visible.")
                node_data[node.id] = (current_x, (i+1) * nodes_distance, current_node_size)

        for connection in genome.connections:
            if not connection.enabled and not self.show_disabled: continue
            in_node_x, in_node_y, _ = node_data[connection.in_node_id]
            out_node_x, out_node_y, _ = node_data[connection.out_node_id]
            points = [(in_node_x, in_node_y), (out_node_x, out_node_y)]
            bounded_weight = min(max(abs(connection.weight), self.abs_min_weight), self.abs_max_weight)
            width = int(bounded_weight / self.abs_max_weight * max_connection_width)
            color = self._determine_weight_color(connection)
            d.line(points, width=width, fill=color)

        for node_id in node_data:
            node_x, node_y, size = node_data[node_id]
            radius = size // 2
            points = [(node_x - radius, node_y - radius), (node_x + radius, node_y + radius)]
            width = int(size * self.node_outline_width_part)
            color = self._determine_node_color(genome.get_node(node_id), layers)
            d.ellipse(points, outline=self.node_outline_color, fill=color, width=width)

        return image

    def show(self, genome, title=""):
        self._create_image(genome).show(title)

    def save(self, genome, name):
        self._create_image(genome).save(name)
