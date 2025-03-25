from manim import *

class QuickSortCallTree(Scene):
    def construct(self):
        # Configurazione iniziale
        array = [5, 1, 3, 4, 2]  # Array di esempio
        start_color = "#58C4DD"   # Colore radice
        end_color = "#FF6B6B"     # Colore foglie
        
        # Genera struttura albero ricorsivo
        root = self.create_call_tree(0, len(array)-1)
        
        # Crea layout albero con orientamento orizzontale
        tree = Tree(
            root,
            layout={"root": ORIGIN, "child_orientation": RIGHT},
            vertex_config={
                "stroke_width": 2,
                "fill_opacity": 0.7,
                "radius": 0.4
            },
            edge_config={
                "stroke_width": 2,
                "tip_shape": ArrowTriangleFilledTip,
                "tip_length": 0.15
            }
        ).scale(1.2)
        
        # Aggiungi contenuto ai nodi
        self.add_node_content(tree, array, start_color, end_color)
        
        # Animazione
        self.play(Create(tree.vertices), run_time=2)
        self.play(Create(tree.edges), run_time=1.5)
        self.wait()
        
        # Mostra etichette con effetto cascade
        for depth in self.get_depth_order(tree):
            self.play(
                *[FadeIn(v.label, shift=UP*0.3) for v in tree.vertices if v.depth == depth],
                lag_ratio=0.3
            )
        self.wait(3)

    def create_call_tree(self, start, end):
        # Simula chiamate ricorsive del Quicksort
        if start >= end:
            return None
            
        node = {"start": start, "end": end}
        mid = (start + end) // 2  # Per semplicità, partizione centrale
        
        node["left"] = self.create_call_tree(start, mid-1)
        node["right"] = self.create_call_tree(mid+1, end)
        return node

    def add_node_content(self, tree, array, start_color, end_color):
        # Calcola profondità massima per gradiente colore
        max_depth = max(v.depth for v in tree.vertices)
        
        for vertex in tree.vertices:
            node = vertex.value
            start = node["start"]
            end = node["end"]
            size = end - start + 1
            
            # Crea etichetta con informazioni
            label = VGroup(
                Text(f"Chiamata su: {start}-{end}", font_size=20),
                Text(f"Elementi: {size}", font_size=16)
            ).arrange(DOWN, center=False, aligned_edge=LEFT)
            
            # Aggiungi sfondo all'etichetta
            background = RoundedRectangle(
                width=label.width + 0.3,
                height=label.height + 0.2,
                corner_radius=0.1,
                fill_color=interpolate_color(
                    start_color,
                    end_color,
                    vertex.depth/max_depth
                ),
                fill_opacity=0.9,
                stroke_width=1
            )
            label.add_to_back(background)
            
            # Posiziona etichetta
            label.next_to(vertex, UP if vertex.depth%2 == 0 else DOWN, buff=0.15)
            vertex.label = label

    def get_depth_order(self, tree):
        # Restituisce ordine crescente di profondità
        depths = sorted({v.depth for v in tree.vertices})
        return depths