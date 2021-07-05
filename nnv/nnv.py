import numpy as np
from matplotlib.patches import Circle
from matplotlib.collections import PatchCollection
import matplotlib.lines as lines
import matplotlib.pyplot as plt



class Element:
    def __init__(self, top, left, width, height, color):
        self.top = top
        self.left = left
        self.width = width
        self.height = height
        self.color = color

    def get_center_x(self):
        return self.left + self.width / 2

    def get_center_y(self):
        return self.top - self.height / 2

    def get_bottom(self):
        return self.top - self.height

    def move_y(self, delta):
        self.top += delta


class Node(Element):
    def __init__(self, top, left, radius, color="gray"):
        Element.__init__(self, top, left, radius*2, radius*2, color=color)
        self.radius = radius

    def get_radius(self):
        return self.radius

    def get_edge_out_position(self):
        return [self.left + self.width, self.top - self.height*0.5]

    def get_edge_in_position(self):
        return [self.left, self.top - self.height*0.5]

    def render(self, m_ax):
        circle = Circle((self.get_center_x(), self.get_center_y()), self.get_radius(), color=self.color, zorder=10)
        m_ax.add_patch(circle)
        return circle


def get_edge_positions(from_node, to_node):
    o = from_node.get_edge_out_position()
    d = to_node.get_edge_in_position()
    return ([o[0], d[0]], [o[1], d[1]])

def connect_nodes(node1, node2, ax, edges_color, edges_width):
    (a,b) = get_edge_positions(node1, node2)
    l1 = lines.Line2D(a,b, color=edges_color, linewidth=edges_width)
    ax.add_line(l1)



class Layer():
    def __init__(self, left, num_nodes, node_radius, title=None, spacing_nodes = 1, max_num_nodes_visible=None, color="gray", font_size=36, edges_color="lightGray", edges_width=4):
        self.nodes = []
        self.top = 0
        self.title = title
        self.font_size = font_size
        self.edges_color = edges_color
        self.edges_width = edges_width
        top = 0

        self.three_dots = None
        three_dots_index = -1
        restart_index = -1
        if (max_num_nodes_visible is not None) and (max_num_nodes_visible < num_nodes):
            three_dots_index = (max_num_nodes_visible // 2)
            restart_index = num_nodes - three_dots_index
        for i in range(num_nodes):
            if i > three_dots_index and i < restart_index:
                continue
            if i == three_dots_index:
                self.three_dots = ThreeDots(top, x = left + node_radius, dot_radius = max(min(4,node_radius*0.5),1), spacing = 2)
                top = self.three_dots.get_bottom() - spacing_nodes
            else:
                node = Node(top, left, radius = node_radius, color = color)
                self.nodes.append(node)
                top = node.get_bottom() - spacing_nodes
        self.bottom = top

    def set_top(self, top):
        delta = top - self.top
        for n in self.nodes:
            n.move_y(delta)
        self.top += delta
        self.bottom += delta


    def get_left(self):
        return self.nodes[0].left

    def get_width(self):
        return self.nodes[0].width

    def get_center_x(self):
        return self.get_left() + self.get_width() /2

    def get_right(self):
        return self.get_left() + self.get_width()

    def get_height(self):
        return abs(self.bottom - self.top)

    def get_bottom(self):
        return self.bottom

    def render(self, mAx):
        for n in self.nodes:
            n.render(mAx)
        if (self.three_dots is not None):
            self.three_dots.render(mAx)
        if (self.title is not None):
            mAx.text(x=self.get_center_x(), y=10, s=self.title, fontsize=self.font_size, horizontalalignment='center')


    def fully_connect(self, layer2, mAx):
        for a in self.nodes:
            for b in layer2.nodes:
                connect_nodes(a,b, mAx, self.edges_color, self.edges_width)


class ThreeDots(Layer):
    def __init__(self, top, x, dot_radius = 4, spacing = 2, color = "lightGray"):
        left = x - dot_radius
        Layer.__init__(self, left=left, num_nodes=3, node_radius=dot_radius, spacing_nodes=spacing, color=color)
        self.set_top(top)


class NNV():
    def __init__(self, layers_list, spacing_layer = 60, spacing_nodes=1, align = "middle", max_num_nodes_visible = 4, node_radius = 20, font_size = 18):
        self.layers = []
        left = 0
        self.left = 0
        self.spacing_layer = spacing_layer
        max_height = 0
        for l in layers_list:
            layer = Layer(left=left, num_nodes=l["units"], node_radius=node_radius, title=l["title"], color=l.get("color", "gray"), max_num_nodes_visible=max_num_nodes_visible, font_size=font_size, spacing_nodes=spacing_nodes, edges_color=l.get("edges_color","lightGray"), edges_width=l.get("edges_width", 4))
            self.layers.append(layer)
            left = layer.get_right() + self.spacing_layer
            max_height = max(max_height, layer.get_height())
        self.right = left

        # setting the alignment
        if (align == "top"):
            pass
        if (align == "middle"):
            for l in self.layers:
                empty_space = max_height - l.get_height()
                l.set_top(-empty_space/2)

    def render(self, save_to_file=None, do_not_show=False):
        mFig, mAx = plt.subplots()

        #creating layers
        for l in self.layers:
            l.render(mAx)


        #creating edges between nodes
        for i in range(len(self.layers) - 1):
            self.layers[i].fully_connect(self.layers[i+1], mAx)



        mAx.set_aspect("equal") # same spacing on both axis
        mAx.autoscale(enable=True, axis='both', tight=None) # fit axis values

        # plt.rcParams["figure.figsize"] = (200,10)
        plt.axis('off')
        if (save_to_file is not None):
            plt.savefig(save_to_file, bbox_inches='tight')

        if do_not_show == False:
            plt.show()

        return mFig, mAx