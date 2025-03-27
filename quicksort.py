from manim import *

class QuicksortScene(Scene):
    def construct(self):
        self.arr = [1, 2, 3, 4, 5, 6, 7]
        self.step_counter = 0
        
        self.main_group = self.create_array(self.arr, depth=0)
        self.play(Create(self.main_group))
        self.wait(0.5)
        
        self.step_text = Text(f"Step: {self.step_counter}", font_size=24).to_edge(UP+RIGHT)
        self.add(self.step_text)
        
        self.yellow_dot = Dot(color=YELLOW, radius=0.07).set_opacity(0)
        self.orange_dot = Dot(color=ORANGE, radius=0.07).set_opacity(0)
        self.add(self.yellow_dot, self.orange_dot)
        
        self.quicksort(0, len(self.arr)-1, 0)
        self.wait(2)

    def create_array(self, arr, depth, parent_center=ORIGIN):
        elements = VGroup()
        spacing = 0.8 / (depth + 1)
        for i, num in enumerate(arr):
            square = Square(side_length=0.6, color=WHITE, fill_color=BLACK, fill_opacity=1)
            number = Text(str(num), font_size=24, font="Arial")
            group = VGroup(square, number)
            
            x_offset = (i - (len(arr)-1)/2) * spacing
            y_offset = -depth * 2.0
            group.move_to(parent_center + [x_offset, y_offset, 0])
            
            elements.add(group)
        return elements

    def quicksort(self, low, high, depth):
        if low < high:
            subarray_rect = self.create_subarray_rectangle(low, high)
            self.play(Create(subarray_rect), run_time=0.5)
            
            pi = self.partition(low, high)
            
            self.play(self.main_group[pi][0].animate.set_fill(GREEN, opacity=0.7), run_time=0.5)
            
            if high - low + 1 == 2:
                self.play(
                    self.main_group[low][0].animate.set_fill(GREEN, opacity=0.7),
                    self.main_group[high][0].animate.set_fill(GREEN, opacity=0.7),
                    run_time=0.5
                )
            
            self.play(Uncreate(subarray_rect), run_time=0.5)
            
            self.quicksort(low, pi-1, depth+1)
            self.quicksort(pi+1, high, depth+1)
        elif low == high:
            self.play(self.main_group[low][0].animate.set_fill(GREEN, opacity=0.7), run_time=0.5)

    def create_subarray_rectangle(self, low, high):
        left = min([self.main_group[i].get_left()[0] for i in range(low, high+1)])
        right = max([self.main_group[i].get_right()[0] for i in range(low, high+1)])
        top = max([self.main_group[i].get_top()[1] for i in range(low, high+1)]) + 0.3
        bottom = min([self.main_group[i].get_bottom()[1] for i in range(low, high+1)]) - 0.3
        
        rect = Rectangle(
            width=right - left+0.4,
            height=top - bottom,
            color=BLUE_B,
            stroke_width=2
        )
        rect.move_to([(left + right)/2, (top + bottom)/2, 0])
        return rect

    def partition(self, low, high):
        pivot_idx = high
        pivot_value = int(self.main_group[pivot_idx][1].text)
        
        pivot_arrow = Vector(DOWN, color=YELLOW, stroke_width=3, tip_length=0.2).scale(0.7)
        pivot_arrow.next_to(self.main_group[pivot_idx], UP, buff=0.1)

        # First-time pivot label setup
        if not hasattr(self, 'pivot_label_shown'):
            self.pivot_label_shown = False
        pivot_label = None
        
        if not self.pivot_label_shown:
            pivot_label = Text("Pivot", font_size=24, color=YELLOW)\
                .next_to(pivot_arrow, UP, buff=0.15)\
                .set_opacity(0)
            self.pivot_label_shown = True

        # Animation sequence
        if pivot_label:
            self.play(
                Create(pivot_arrow),
                pivot_label.animate.set_opacity(1).shift(UP*0.1).scale(1.2),
                run_time=0.5
            )
            self.play(
                pivot_label.animate.shift(DOWN*0.1).scale(1/1.2),
                run_time=0.3
            )
        else:
            self.play(Create(pivot_arrow), run_time=0.5)
        
        self.play(self.main_group[pivot_idx][0].animate.set_fill(RED, opacity=0.5), run_time=0.5)

        i = low - 1
        
        # Initialize dots with current positions
        orange_start_pos = self.main_group[low].get_corner(UL) + RIGHT*0.07 + DOWN*0.07
        yellow_start_pos = self.main_group[low].get_corner(DL) + RIGHT*0.07 + UP*0.07

        self.play(
            self.orange_dot.animate.set_opacity(0),
            self.orange_dot.animate.move_to(orange_start_pos),
            self.yellow_dot.animate.set_opacity(0),
            self.yellow_dot.animate.move_to(yellow_start_pos),
            run_time=0.1
        )
        self.play(
            self.orange_dot.animate.set_opacity(1),
            self.yellow_dot.animate.set_opacity(1),
            run_time=0.1
        )

        for j in range(low, high):
            self.step_counter += 1
            new_step = Text(f"Step: {self.step_counter}", font_size=24).to_edge(UP+RIGHT)
            self.play(Transform(self.step_text, new_step), run_time=0.1)
            
            orange_pos = self.main_group[j].get_corner(UL) + RIGHT*0.07 + DOWN*0.07
            self.play(
                self.orange_dot.animate.move_to(orange_pos).set_opacity(1),
                run_time=0.5
            )
            

            yellow_anim = []
            if i >= low:
                yellow_pos = self.main_group[i].get_corner(DL) + RIGHT*0.07 + UP*0.07
                yellow_anim.append(
                    self.yellow_dot.animate.move_to(yellow_pos).set_opacity(1)
                )

            # Only play if there are animations
            if yellow_anim:
                self.play(*yellow_anim, run_time=0.5)
            else:  # Maintain timing consistency
                self.wait(0.5)
            
            current_value = int(self.main_group[j][1].text)
            comparison = Text(f"{current_value} <= {pivot_value} ?", font_size=20).next_to(self.main_group, DOWN*2)
            self.play(Write(comparison))
            
            if current_value < pivot_value:
                prev_i = i
                i += 1

                if prev_i >= low and i >= low:
                    new_yellow_pos = self.main_group[i].get_corner(DL) + RIGHT*0.07 + UP*0.07
                    self.play(self.yellow_dot.animate.move_to(new_yellow_pos), run_time=0.5)
                elif prev_i >= low and i < low:
                    self.play(self.yellow_dot.animate.set_opacity(0), run_time=0.3)
                elif i >= low:
                    new_yellow_pos = self.main_group[i].get_corner(DL) + RIGHT*0.07 + UP*0.07
                    self.play(
                        self.yellow_dot.animate.move_to(new_yellow_pos).set_opacity(1),
                        run_time=0.5
                    )
                if i != j:
                    self.step_counter += 1
                    new_step = Text(f"Step: {self.step_counter}", font_size=24).to_edge(UP+RIGHT)
                    self.play(Transform(self.step_text, new_step), run_time=0.1)
                    self.arr[i], self.arr[j] = self.arr[j], self.arr[i]
                    self.swap_elements(i, j)
            
            self.play(FadeOut(comparison), run_time=0.5)

        if pivot_label:
            self.play(
                Uncreate(pivot_arrow),
                FadeOut(pivot_label),
                run_time=0.5
            )
        else:
            self.play(
                Uncreate(pivot_arrow),
                run_time=0.5
            )

        if i+1 != high:
            orange_pos = self.main_group[high].get_corner(UL) + RIGHT*0.07 + DOWN*0.07
            self.play(
                self.orange_dot.animate.move_to(orange_pos).set_opacity(1),
                run_time=0.5
            )
            current_value = int(self.main_group[j+1][1].text)
            comparison = Text(f"{current_value} <= {pivot_value} ?", font_size=20).next_to(self.main_group, DOWN*2)
            self.play(Write(comparison))

            self.play(self.orange_dot.animate.set_opacity(0), self.yellow_dot.animate.set_opacity(0), run_time=0.3)
            self.arr[i+1], self.arr[high] = self.arr[high], self.arr[i+1]
            self.step_counter += 1
            new_step = Text(f"Step: {self.step_counter}", font_size=24).to_edge(UP+RIGHT)
            self.play(Transform(self.step_text, new_step), run_time=0.1)
            self.swap_elements(i+1, high)
            self.play(FadeOut(comparison), run_time=0.5)

        self.play(
            self.main_group[i+1][0].animate.set_fill(GREEN, opacity=0.7),
            self.orange_dot.animate.set_opacity(0),
            self.yellow_dot.animate.set_opacity(0),
            run_time=0.3
        )

        return i+1


    def swap_elements(self, i, j):
        arrow_style = {
            "stroke_width": 3,
            "tip_length": 0.2,
            "color": GREEN_B
        }
        
        arrow1 = CurvedArrow(
            self.main_group[i].get_center() + DOWN*0.5,
            self.main_group[j].get_center() + DOWN*0.5, 
            angle=PI/2,
            **arrow_style
        )
        

        arrow2 = CurvedArrow(
            self.main_group[j].get_center() + UP*0.5,
            self.main_group[i].get_center() + UP*0.5,
            angle=PI/2,
            **arrow_style
        )
        
        self.play(
            Create(arrow1),
            Create(arrow2),
            run_time=0.5
        )
        
        self.play(
            self.main_group[i].animate.move_to(self.main_group[j].get_center()),
            self.main_group[j].animate.move_to(self.main_group[i].get_center()),
            run_time=0.7
        )
        
        self.main_group[i], self.main_group[j] = self.main_group[j], self.main_group[i]
        self.play(
            FadeOut(arrow1), 
            FadeOut(arrow2), 
            run_time=0.3
        )