from manim import *

class QuickSortIntro(Scene):
    def construct(self):

        title = Text("Quick Sort:", font_size=64, color=YELLOW).move_to(ORIGIN)
        self.play(Write(title), run_time=1.5)
        self.wait(0.5)

        subtitle = Text("worst case complexity", font_size=48, color=WHITE).next_to(title, DOWN)

        self.play(
            title.animate.shift(UP * 0.5),
            FadeIn(subtitle, shift=UP), 
            run_time=1.5
        )
        self.wait(0.5)

        self.play(Indicate(subtitle))
        self.wait(1)

        self.play(FadeOut(Group(title, subtitle)))
