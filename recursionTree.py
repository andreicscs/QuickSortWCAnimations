from manim import *
from manim import config

class EnhancedQuickSortTree(Scene):
    def construct(self):
        self.camera.background_color = "#1a1a1a"
        original_array = [1, 2, 3, 4, 5, 6, 7]
        node_scale = 0.5  # Reduced global scaling factor

        # Enhanced array visualization with better typography.
        # The pivot is highlighted (always the last element).
        def create_array_node(arr, pivot_index=None):
            elements = VGroup()
            for i, num in enumerate(arr):
                bg_color = "#2e68cc" if i != pivot_index else "#cc302e"
                element = VGroup(
                    RoundedRectangle(
                        corner_radius=0.1,
                        height=0.6,
                        width=0.6,
                        fill_color=bg_color,
                        fill_opacity=1,
                        stroke_color=WHITE,
                        stroke_width=1.5
                    ),
                    Text(str(num), font_size=22, color=WHITE)
                )
                elements.add(element)
            elements.arrange(RIGHT, buff=0.15)
            info_text = Text(f"Size: {len(arr)}", font_size=18, color="#e1e1e1").next_to(elements, DOWN, buff=0.2)
            return VGroup(elements, info_text).scale(node_scale)

        # Build the tree recursively simulating quicksort partition.
        def build_tree(arr, depth=0):
            if not arr:
                return None
            # Choose the last element as the pivot.
            node = {
                "viz": create_array_node(arr, pivot_index=len(arr)-1),
                "depth": depth,
                "children": []
            }
            if len(arr) > 1:
                pivot = arr[-1]
                # Partition (excluding pivot) into left (smaller) and right (greater).
                left = [x for x in arr[:-1] if x < pivot]
                right = [x for x in arr[:-1] if x > pivot]
                node["children"] = [
                    build_tree(left, depth+1),
                    build_tree(right, depth+1)
                ]
            return node

        # First, build the tree.
        root = build_tree(original_array)

        # Collect nodes layer by layer to determine max depth.
        def collect_layers(node, depth=0, parent=None, layers=None):
            if layers is None:
                layers = {}
            if depth not in layers:
                layers[depth] = []
            layers[depth].append((node, parent))
            for child in node["children"]:
                if child:
                    collect_layers(child, depth+1, node, layers)
            return layers

        layers = collect_layers(root)
        max_depth = max(layers.keys())

        # Compute dynamic spacing parameters (scaled down).
        vertical_gap = config.frame_height / (max_depth + 6)  # Increased denominator for smaller gap
        initial_dx = config.frame_width / (6 * (max_depth + 1))  # Smaller horizontal gap
        # Place the root near the top of the screen.
        initial_y = config.frame_height/2 - vertical_gap

        # Layout the tree using computed positions, with horizontal spacing adjusted per level.
        def layout_tree(node, x=0, y=initial_y, depth=0):
            if not node:
                return
            node["viz"].move_to(RIGHT*x + UP*y)
            current_dx = initial_dx * (max_depth - depth + 1)/(max_depth+1)
            if node["children"]:
                left_child, right_child = node["children"]
                layout_tree(left_child, x - current_dx, y - vertical_gap, depth+1)
                layout_tree(right_child, x + current_dx, y - vertical_gap, depth+1)

        layout_tree(root)

        # Create depth markers as a dictionary.
        depth_markers = {
            d: Text(f"{d}", font_size=17, color="#e1e1e1")
                .to_edge(LEFT)
                .shift(UP*(config.frame_height/2 - (d+1)*vertical_gap))
            for d in range(max_depth + 1)
        }

        # Animate the tree "growing" layer by layer with corresponding depth markers.
        self.play(FadeIn(depth_markers[0], shift=RIGHT))
        self.play(DrawBorderThenFill(root["viz"], run_time=0.8))
        
        for depth in sorted(layers.keys()):
            if depth == 0:
                continue
            self.play(FadeIn(depth_markers[depth], shift=RIGHT))
            for node, parent in layers[depth]:
                if parent is None:
                    continue
                arrow = Arrow(
                    parent["viz"].get_bottom(),
                    node["viz"].get_top(),
                    color="#5a5a5a",
                    stroke_width=2.5,
                    tip_shape=ArrowCircleTip,
                    tip_length=0.15
                )
                self.play(Create(arrow, run_time=1.5))
                self.play(DrawBorderThenFill(node["viz"], run_time=0.8))
        self.wait(2)
