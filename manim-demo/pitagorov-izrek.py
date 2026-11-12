from manim import *
import numpy as np


config.pixel_width = 1080
config.pixel_height = 1920
config.frame_width = 9
config.frame_height = 16


class PitagorovGeometrijskiDokaz(Scene):
    def construct(self):
        self.camera.background_color = "#101827"

        # Uvodno vprašanje
        naslov = Text(
            "PITAGOROV IZREK",
            font_size=52,
            weight=BOLD,
            color=YELLOW,
        ).move_to(UP * 6.5)

        vprasanje = Text(
            "Ali je vsota kvadratov katet\n"
            "enaka kvadratu hipotenuze?",
            font_size=38,
            line_spacing=1.2,
        ).move_to(UP * 4.5)

        self.play(FadeIn(naslov), run_time=1)
        self.play(Write(vprasanje), run_time=2)

        # Pravokotni trikotnik z označenimi stranicami
        A = np.array([-1.5, -1.5, 0])
        B = np.array([1.3, -1.5, 0])
        C = np.array([-1.5, 0.6, 0])

        trikotnik = Polygon(
            A, B, C,
            color=BLUE_C,
            stroke_width=5,
            fill_color=BLUE_E,
            fill_opacity=0.35,
        )

        oznaka_a = MathTex("a", font_size=42).move_to([-0.1, -1.9, 0])
        oznaka_b = MathTex("b", font_size=42).move_to([-1.9, -0.45, 0])
        oznaka_c = MathTex("c", font_size=42).move_to([0.0, -0.35, 0])

        pravi_kot = VGroup(
            Line(A + RIGHT * 0.3, A + RIGHT * 0.3 + UP * 0.3),
            Line(A + RIGHT * 0.3 + UP * 0.3, A + UP * 0.3),
        )

        zacetna_enacba = MathTex(
            "a^2+b^2=c^2",
            font_size=56,
            color=YELLOW,
        ).move_to(DOWN * 4.1)

        self.play(Create(trikotnik), Create(pravi_kot), run_time=2)
        self.play(
            FadeIn(oznaka_a),
            FadeIn(oznaka_b),
            FadeIn(oznaka_c),
            run_time=1,
        )
        self.play(Write(zacetna_enacba), run_time=2)
        self.wait(2)

        self.play(
            FadeOut(naslov, vprasanje, trikotnik, pravi_kot,
                    oznaka_a, oznaka_b, oznaka_c, zacetna_enacba),
            run_time=1,
        )

        # Veliki kvadrat s štirimi skladnimi pravokotnimi trikotniki
        a, b = 3, 2
        stranica = a + b
        merilo = 0.8
        x0 = -stranica * merilo / 2
        y0 = 0.45 - stranica * merilo / 2

        def Tocka(x, y):
            return np.array([
                x0 + x * merilo,
                y0 + y * merilo,
                0,
            ])

        veliki_kvadrat = Polygon(
            Tocka(0, 0),
            Tocka(stranica, 0),
            Tocka(stranica, stranica),
            Tocka(0, stranica),
            color=WHITE,
            stroke_width=4,
        )

        trikotniki = VGroup(
            Polygon(Tocka(0, 0), Tocka(a, 0), Tocka(0, b)),
            Polygon(
                Tocka(stranica, 0),
                Tocka(stranica - b, 0),
                Tocka(stranica, a),
            ),
            Polygon(
                Tocka(stranica, stranica),
                Tocka(stranica - a, stranica),
                Tocka(stranica, stranica - b),
            ),
            Polygon(
                Tocka(0, stranica),
                Tocka(0, stranica - a),
                Tocka(b, stranica),
            ),
        )

        barve = [BLUE_D, TEAL_D, PURPLE_D, GREEN_D]
        for trikotnik_i, barva in zip(trikotniki, barve):
            trikotnik_i.set_fill(barva, opacity=0.8)
            trikotnik_i.set_stroke(WHITE, width=2)

        naslov_diagrama = Text(
            "Štirje enaki pravokotni trikotniki",
            font_size=36,
            color=YELLOW,
        ).move_to(UP * 5.7)

        self.play(Write(naslov_diagrama), run_time=2)
        self.play(
            Create(veliki_kvadrat),
            *[FadeIn(t) for t in trikotniki],
            run_time=4,
        )

        oznake_stranic = VGroup(
            MathTex("a", font_size=38).move_to(Tocka(a / 2, -0.45)),
            MathTex("b", font_size=38).move_to(Tocka(-0.45, b / 2)),
            MathTex("c", font_size=38).move_to(
                Tocka((a + stranica) / 2, a / 2) + RIGHT * 0.25
            ),
        )
        self.play(FadeIn(oznake_stranic), run_time=1)

        srednji_kvadrat = Polygon(
            Tocka(a, 0),
            Tocka(stranica, a),
            Tocka(b, stranica),
            Tocka(0, b),
            color=YELLOW,
            stroke_width=5,
            fill_color="#101827",
            fill_opacity=1,
        )
        oznaka_c_kvadrat = MathTex(
            "c^2",
            font_size=44,
            color=YELLOW,
        ).move_to(Tocka(stranica / 2, stranica / 2))

        self.play(
            Create(srednji_kvadrat),
            FadeIn(oznaka_c_kvadrat),
            run_time=2,
        )
        self.wait(3)

        # Prvi izračun ploščine
        naslov_prve_ploscine = Text(
            "Ploščina velikega kvadrata",
            font_size=38,
            color=YELLOW,
        ).move_to(UP * 5.7)

        self.play(
            FadeOut(naslov_diagrama),
            FadeIn(naslov_prve_ploscine),
            run_time=1.5,
        )

        formula = MathTex(
            "(a+b)^2=a^2+2ab+b^2",
            font_size=48,
        ).move_to(DOWN * 4.8)

        self.play(Write(formula), run_time=2.5)
        self.wait(3)

        # Drugi izračun ploščine: štirje trikotniki in srednji kvadrat
        nova_formula = MathTex(
            "4\\cdot\\frac{ab}{2}+c^2=2ab+c^2",
            font_size=45,
        ).move_to(DOWN * 4.8)

        naslov_druge_ploscine = Text(
            "Isto ploščino izračunamo še drugače",
            font_size=34,
            color=YELLOW,
        ).move_to(UP * 5.7)

        self.play(
            ReplacementTransform(formula, nova_formula),
            FadeOut(naslov_prve_ploscine),
            FadeIn(naslov_druge_ploscine),
            run_time=2,
        )
        formula = nova_formula
        self.wait(3)

        # Izenačimo izraza in odštejemo 2ab
        naslednja_formula = MathTex(
            "a^2+2ab+b^2=2ab+c^2",
            font_size=46,
        ).move_to(DOWN * 4.8)

        self.play(
            ReplacementTransform(formula, naslednja_formula),
            run_time=2.5,
        )
        formula = naslednja_formula
        self.wait(3)

        koncna_formula = MathTex(
            "a^2+b^2=c^2",
            font_size=60,
            color=YELLOW,
        ).move_to(DOWN * 4.8)

        self.play(
            ReplacementTransform(formula, koncna_formula),
            run_time=2,
        )
        self.wait(3)

        zakljucek = Text(
            "Dokazali smo Pitagorov izrek!",
            font_size=38,
            color=GREEN_A,
        ).move_to(UP * 5.7)

        self.play(
            FadeOut(naslov_druge_ploscine),
            FadeIn(zakljucek),
            run_time=1.5,
        )
        self.wait(3)

        # Zaključni zaslon; napis FMF lahko zamenjaš z datoteko logotipa.
        self.play(
            FadeOut(
                veliki_kvadrat,
                trikotniki,
                oznake_stranic,
                srednji_kvadrat,
                oznaka_c_kvadrat,
                koncna_formula,
                zakljucek,
            ),
            run_time=2,
        )

        logo_fmf = Text(
            "FMF",
            font_size=80,
            weight=BOLD,
            color=WHITE,
        )
        self.play(FadeIn(logo_fmf), run_time=2)
        self.wait(3)
        self.play(FadeOut(logo_fmf), run_time=1.5)