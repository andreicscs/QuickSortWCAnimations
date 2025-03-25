from manim import *

class PerfectMorningTable(Scene):
    def construct(self):
        # 1. DATI DELLA TABELLA (formattazione chiara)
        headers = ["Livello j", "Dimensione", "Sottoproblemi", "Operazioni"]
        rows = [
            ["0", "n", "Θ(1)", "Θ(n)"],
            ["1", "n-1", "Θ(1)", "Θ(n)"],
            ["2", "n-2", "Θ(1)", "Θ(n)"],
            ["⋮", "⋮", "⋮", "⋮"],
            ["j", "n-j", "Θ(1)", "Θ(n)"],
            ["L", "1", "Θ(1)", "Θ(n)"]
        ]

        # 2. CREAZIONE TABELLA (con controllo totale)
        table = Table(
            rows,
            col_labels=[Text(h, color="#58C4DD") for h in headers],  # Intestazioni colorate
            include_outer_lines=True,
            line_config={"stroke_width": 1.5, "color": WHITE},
            arrange_in_grid_config={"cell_alignment": ORIGIN}  # Allineamento garantito
        ).scale(0.5).center()

        # 3. ANIMAZIONE STEP-BY-STEP
        # Prima le linee
        self.play(
            LaggedStart(
                Create(table.get_horizontal_lines()),
                Create(table.get_vertical_lines()),
            lag_ratio=0.3,
            run_time=1.5
        ))
        self.wait(0.3)

        # Poi le intestazioni
        self.play(FadeIn(table.get_col_labels(), shift=0.2*DOWN))
        self.wait(0.3)

        # Infine le righe una ad una
        for row in table.get_rows()[1:]:
            self.play(
                LaggedStart(*[FadeIn(cell) for cell in row], lag_ratio=0.3),
                run_time=1.3
            )
            self.wait(0.2)

        self.wait(1)

        # 4. EVIDENZIAZIONE DELL'ULTIMA RIGA
        self.play(Indicate(table.get_rows()[-1]))
        self.wait(1)

        # 5. TRASFORMAZIONE IN FORMULA n-j=1 -> L=n-j
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

        # Fade out tutto
        #self.play(FadeOut(Group(table, inverse_formula)))

        self.play(
            table.animate.scale(0.5).to_edge(LEFT, buff=DEFAULT_MOBJECT_TO_EDGE_BUFFER),
        )

        # 3. Extract Last Column (Operazioni Column)
        last_column = VGroup(*[table.get_entries((i + 1, 4)) for i in range(len(rows)+1)])
        zoomed_column = last_column.copy().scale(1.5).next_to(table, RIGHT)
        self.play(Indicate(last_column))
        self.wait(1)
        
        self.play(TransformFromCopy(last_column, zoomed_column))  # Zoom effect
        self.wait(2)

        # Display Θ(n)
        operationComplexity = MathTex(r"\Theta(n) \times L", font_size=36).next_to(table, RIGHT, buff=1)
        self.play(ReplacementTransform(zoomed_column, operationComplexity))
        self.wait(1)

        # Circumscribe the existing solution as reference
        self.play(Circumscribe(solution))
        self.wait(1)

        # Replace L with (n-1)
        LValue = MathTex(r"\Theta(n) \times (n-1)", font_size=36)
        self.play(TransformMatchingTex(operationComplexity, LValue))
        self.wait(1)
        self.play(FadeOut(inverse_formula))

        # Replace (n-1) with n
        n = MathTex(r"\Theta(n) \times n", font_size=36)
        self.play(TransformMatchingTex(LValue, n))
        self.wait(1)

        # Transform into final complexity Θ(n^2)
        complexityResult = MathTex(r"\Theta(n \times n)", font_size=36)
        self.play(
            TransformMatchingTex(n, complexityResult)
        )
        self.wait(1)

        # Final transformation to Θ(n^2)
        complexityResultPOW = MathTex(r"\Theta(n^2)", font_size=48)
        self.play(
            TransformMatchingTex(complexityResult, complexityResultPOW)
        )
        self.wait(5)
        self.play(
            FadeOut(table),
            #FadeToColor(complexityResultPOW, color=YELLOW),

        )

        self.play(
            complexityResultPOW.animate.scale(2).center(),
        )
        self.play(
            Indicate(complexityResultPOW),
        )

        self.wait(5)