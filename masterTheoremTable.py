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

        self.wait(3)