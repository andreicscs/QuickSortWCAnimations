from manim import *

class MasterTheoremTable(Scene):
    def construct(self):
        headers = ["Livello j", "Dimensione", "Sottoproblemi", "Operazioni"]
        rows = [
            ["0", "n", "Θ(1)", "Θ(n)"],
            ["1", "n-1", "Θ(1)", "Θ(n)"],
            ["2", "n-2", "Θ(1)", "Θ(n)"],
            ["⋮", "⋮", "⋮", "⋮"],
            ["j", "n-j", "Θ(1)", "Θ(n)"],
            ["L", "1", "Θ(1)", "Θ(n)"]
        ]

        table = Table(
            rows,
            col_labels=[Text(h, color="#58C4DD") for h in headers], 
            include_outer_lines=True,
            line_config={"stroke_width": 1.5, "color": WHITE},
            arrange_in_grid_config={"cell_alignment": ORIGIN}
        ).scale(0.5).center()


        self.play(
            LaggedStart(
                Create(table.get_horizontal_lines()),
                Create(table.get_vertical_lines()),
            lag_ratio=0.3,
            run_time=1.5
        ))
        self.wait(0.3)

        self.play(FadeIn(table.get_col_labels(), shift=0.2*DOWN))
        self.wait(0.3)

        for row in table.get_rows()[1:]:
            self.play(
                LaggedStart(*[FadeIn(cell) for cell in row], lag_ratio=0.3),
                run_time=1.3
            )
            self.wait(0.2)

        self.wait(1)

        self.play(Indicate(table.get_rows()[-1]))
        self.wait(1)

        highlight_cells = [table.get_entries((6, 1)), table.get_entries((6, 2))]
        self.play(*[Flash(cell) for cell in highlight_cells])
        self.wait(1)

        formula = MathTex("n - j = 1").next_to(table, DOWN/2, buff=1)
        self.play(Write(formula))
        self.wait(3)

        inverse_formula = MathTex("j = n - 1").next_to(table, DOWN/2, buff=1)
        self.play(TransformMatchingTex(formula, inverse_formula))
        self.wait(2)

        solution = MathTex("L = n - 1").next_to(table, DOWN/2, buff=1)
        self.play(Transform(inverse_formula, solution))
        self.wait(5)



        self.play(
            table.animate.scale(0.5).to_edge(LEFT, buff=DEFAULT_MOBJECT_TO_EDGE_BUFFER),
        )

        last_column = VGroup(*[table.get_entries((i + 1, 4)) for i in range(len(rows)+1)])
        zoomed_column = last_column.copy().scale(1.5).next_to(table, RIGHT)
        self.play(Indicate(last_column))
        self.wait(1)
        
        self.play(TransformFromCopy(last_column, zoomed_column)) 
        self.wait(2)

        operationComplexity = MathTex(r"\Theta(n) \times L", font_size=36).next_to(table, RIGHT, buff=1)
        self.play(ReplacementTransform(zoomed_column, operationComplexity))
        self.wait(1)

        self.play(Circumscribe(solution))
        self.wait(1)

        LValue = MathTex(r"\Theta(n) \times (n-1)", font_size=36)
        self.play(TransformMatchingTex(operationComplexity, LValue))
        self.wait(1)
        self.play(FadeOut(inverse_formula))

        n = MathTex(r"\Theta(n) \times n", font_size=36)
        self.play(TransformMatchingTex(LValue, n))
        self.wait(1)

        complexityResult = MathTex(r"\Theta(n \times n)", font_size=36)
        self.play(
            TransformMatchingTex(n, complexityResult)
        )
        self.wait(1)

        complexityResultPOW = MathTex(r"\Theta(n^2)", font_size=48)
        self.play(
            TransformMatchingTex(complexityResult, complexityResultPOW)
        )
        self.wait(5)
        self.play(
            FadeOut(table),

        )

        self.play(
            complexityResultPOW.animate.scale(2).center(),
        )
        self.play(
            Indicate(complexityResultPOW),
        )

        self.wait(5)