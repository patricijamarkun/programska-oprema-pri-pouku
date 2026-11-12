
from manim import *

# --------------------------------------------------
# NASTAVITVE VIDEA
# --------------------------------------------------

config.pixel_width = 1080
config.pixel_height = 1920
config.frame_width = 9
config.frame_height = 16

# --------------------------------------------------
# GRAFIČNA PODOBA UNIVERZE V LJUBLJANI
# --------------------------------------------------

OZADJE = "#FFFFFF"
RDECA = "#E03127"
SIVA = "#58595B"
SVETLA_SIVA = "#E6E7E8"
MODRA = "#2878AC"

FONT_NAME = "Arial"

# Geometrijske mere
A = 2.6
B = 1.8
S = A + B

# Velikost in položaj geometrijske konstrukcije
SCALE = 1.0
CENTER = DOWN * 0.1


class PitagorovIzrek(Scene):

    def construct(self):

        self.camera.background_color = OZADJE

        # --------------------------------------------------
        # POMOŽNE FUNKCIJE
        # --------------------------------------------------

        def napis(besedilo, velikost=32, barva=SIVA, bold=False):
            return Text(
                besedilo,
                font=FONT_NAME,
                font_size=velikost,
                color=barva,
                weight=BOLD if bold else NORMAL,
                line_spacing=1.15
            )

        def koordinata(x, y):
            return CENTER + np.array([
                (x - S / 2) * SCALE,
                (y - S / 2) * SCALE,
                0
            ])

        def naredi_kvadrat_in_trikotnike():

            # Zunanji kvadrat
            zunanji = Square(
                side_length=S * SCALE,
                color=SIVA,
                stroke_width=5
            ).move_to(CENTER)

            # Štirje skladni pravokotni trikotniki
            oglisca = [
                [(0, 0), (A, 0), (0, B)],
                [(S, 0), (A, 0), (S, A)],
                [(S, S), (S, A), (B, S)],
                [(0, S), (B, S), (0, B)]
            ]

            trikotniki = VGroup()

            for og in oglisca:
                t = Polygon(
                    *[koordinata(x, y) for x, y in og],
                    color=RDECA,
                    fill_color=RDECA,
                    fill_opacity=0.85,
                    stroke_width=3
                )
                trikotniki.add(t)

            # Notranji kvadrat s stranico c
            notranji = Polygon(
                *[
                    koordinata(A, 0),
                    koordinata(S, A),
                    koordinata(B, S),
                    koordinata(0, B)
                ],
                color=MODRA,
                fill_color=MODRA,
                fill_opacity=0.9,
                stroke_width=4
            )

            # Oznake zunanjih stranic
            oznake = VGroup()

            # Spodnja stranica
            oznake.add(
                MathTex("a", color=SIVA).scale(0.8).move_to(
                    koordinata(A / 2, -0.25)
                ),
                MathTex("b", color=SIVA).scale(0.8).move_to(
                    koordinata(A + B / 2, -0.25)
                )
            )

            # Desna stranica
            oznake.add(
                MathTex("a", color=SIVA).scale(0.8).move_to(
                    koordinata(S + 0.25, A / 2)
                ),
                MathTex("b", color=SIVA).scale(0.8).move_to(
                    koordinata(S + 0.25, A + B / 2)
                )
            )

            # Zgornja stranica
            oznake.add(
                MathTex("b", color=SIVA).scale(0.8).move_to(
                    koordinata(B / 2, S + 0.25)
                ),
                MathTex("a", color=SIVA).scale(0.8).move_to(
                    koordinata(B + A / 2, S + 0.25)
                )
            )

            # Leva stranica
            oznake.add(
                MathTex("b", color=SIVA).scale(0.8).move_to(
                    koordinata(-0.25, B / 2)
                ),
                MathTex("a", color=SIVA).scale(0.8).move_to(
                    koordinata(-0.25, B + A / 2)
                )
            )

            # Oznake hipotenuz
            oznake_c = VGroup()

            tocke_c = [
                ((A + S) / 2, A / 2),
                ((S + B) / 2, (A + S) / 2),
                (B / 2, (B + S) / 2),
                (A / 2, B / 2)
            ]

            for x, y in tocke_c:
                oznake_c.add(
                    MathTex("c", color=OZADJE)
                    .scale(0.8)
                    .move_to(koordinata(x, y))
                )

            return VGroup(
                trikotniki,
                notranji,
                zunanji,
                oznake,
                oznake_c
            )

        # --------------------------------------------------
        # 1. KADER – UVOD
        # --------------------------------------------------

        naslov = napis(
            "GEOMETRIJSKI DOKAZ",
            43,
            RDECA,
            True
        ).move_to(UP * 6.0)

        naslov2 = napis(
            "PITAGOROVEGA IZREKA",
            43,
            RDECA,
            True
        ).next_to(naslov, DOWN, buff=0.2)

        self.play(Write(naslov), run_time=1.5)
        self.play(Write(naslov2), run_time=1.5)

        # Pravokotni trikotnik
        A1 = LEFT * 1.6 + DOWN * 0.3
        B1 = RIGHT * 1.6 + DOWN * 0.3
        C1 = LEFT * 1.6 + UP * 2.1

        trikotnik_uvod = Polygon(
            A1, B1, C1,
            color=RDECA,
            stroke_width=6
        )

        pravi_kot = RightAngle(
            Line(A1, B1),
            Line(A1, C1),
            length=0.35,
            color=SIVA
        )

        oznaka_a = MathTex("a", color=RDECA).scale(1.1)
        oznaka_a.next_to(Line(A1, B1), DOWN, buff=0.15)

        oznaka_b = MathTex("b", color=RDECA).scale(1.1)
        oznaka_b.next_to(Line(A1, C1), LEFT, buff=0.15)

        oznaka_c = MathTex("c", color=RDECA).scale(1.1)
        oznaka_c.move_to(
            Line(B1, C1).get_center() + RIGHT * 0.35
        )

        trikotnik_uvod.move_to(DOWN * 0.2)

        # Premaknemo tudi oznake in pravi kot
        premik = trikotnik_uvod.get_center() - Polygon(
            A1, B1, C1
        ).get_center()

        self.play(Create(trikotnik_uvod))
        self.play(
            FadeIn(pravi_kot),
            Write(oznaka_a),
            Write(oznaka_b),
            Write(oznaka_c)
        )

        vprasanje = napis(
            "Zakaj je vsota kvadratov katet\n"
            "enaka kvadratu hipotenuze?",
            31,
            SIVA
        ).move_to(DOWN * 3.3)

        formula_uvod = MathTex(
            "a^2+b^2=c^2",
            color=RDECA
        ).scale(1.2).next_to(vprasanje, DOWN, buff=0.5)

        self.play(FadeIn(vprasanje))
        self.play(Write(formula_uvod))
        self.wait(2)

        # --------------------------------------------------
        # 2. KADER – ŠTIRJE SKLADNI TRIKOTNIKI
        # --------------------------------------------------

        self.play(
            FadeOut(VGroup(
                naslov, naslov2, trikotnik_uvod,
                pravi_kot, oznaka_a, oznaka_b,
                oznaka_c, vprasanje, formula_uvod
            ))
        )

        naslov2_kader = napis(
            "ŠTIRJE SKLADNI TRIKOTNIKI",
            38,
            RDECA,
            True
        ).move_to(UP * 6)

        self.play(Write(naslov2_kader))

        def mali_trikotnik(smer=1):
            t = Polygon(
                ORIGIN,
                RIGHT * 1.2,
                UP * 0.8,
                color=RDECA,
                fill_color=RDECA,
                fill_opacity=0.85,
                stroke_width=3
            )
            if smer == 1:
                return t
            return t.rotate(PI / 2 * smer)

        mini = VGroup(
            mali_trikotnik(1),
            mali_trikotnik(1).rotate(PI / 2),
            mali_trikotnik(1).rotate(PI),
            mali_trikotnik(1).rotate(3 * PI / 2)
        )

        mini.arrange_in_grid(
            rows=2,
            cols=2,
            buff=1.0
        ).move_to(UP * 0.7)

        self.play(
            LaggedStart(
                *[Create(t) for t in mini],
                lag_ratio=0.2
            ),
            run_time=2.5
        )

        oznake_mini = VGroup()

        for t in mini:
            oznake_mini.add(
                MathTex("a", color=SIVA).scale(0.55).move_to(
                    t.get_center() + DOWN * 0.35
                ),
                MathTex("b", color=SIVA).scale(0.55).move_to(
                    t.get_center() + LEFT * 0.35
                ),
                MathTex("c", color=SIVA).scale(0.55).move_to(
                    t.get_center() + RIGHT * 0.3 + UP * 0.2
                )
            )

        self.play(FadeIn(oznake_mini))

        razlaga2 = napis(
            "Vzamemo 4 skladne pravokotne trikotnike\n"
            "s katetama a in b ter hipotenuzo c.",
            29,
            SIVA
        ).move_to(DOWN * 3.3)

        self.play(FadeIn(razlaga2))
        self.wait(2)

        # --------------------------------------------------
        # 3. KADER – SESTAVLJANJE KVADRATA
        # --------------------------------------------------

        self.play(
            FadeOut(VGroup(
                naslov2_kader, mini,
                oznake_mini, razlaga2
            ))
        )

        konstrukcija = naredi_kvadrat_in_trikotnike()

        trikotniki, notranji, zunanji, oznake, oznake_c = konstrukcija

        # Najprej pokažemo zunanji kvadrat
        self.play(Create(zunanji))

        # Trikotniki se postopoma premaknejo na svoja mesta
        self.play(
            LaggedStart(
                *[FadeIn(t, scale=0.7) for t in trikotniki],
                lag_ratio=0.25
            ),
            run_time=2.5
        )

        # Pojavi se notranji kvadrat
        self.play(
            FadeIn(notranji),
            run_time=1.5
        )

        self.play(
            FadeIn(oznake),
            FadeIn(oznake_c)
        )

        razlaga3 = napis(
            "Te trikotnike zložimo v večji kvadrat\n"
            "s stranico a + b.",
            30,
            SIVA
        ).move_to(DOWN * 3.7)

        self.play(FadeIn(razlaga3))
        self.wait(2)

        # --------------------------------------------------
        # 4. KADER – ISTA SLIKA, DRUG ZAPIS
        # --------------------------------------------------

        razlaga4 = napis(
            "Izračunajmo ploščino kvadrata\n"
            "na dva različna načina.",
            32,
            RDECA,
            True
        ).move_to(DOWN * 3.7)

        # Geometrijska slika ostane popolnoma enaka
        self.play(
            FadeOut(razlaga3),
            FadeIn(razlaga4)
        )
        self.wait(2)

        # --------------------------------------------------
        # 5. KADER – PRVI NAČIN IZRAČUNA
        # --------------------------------------------------

        self.play(
            FadeOut(VGroup(
                konstrukcija,
                razlaga4
            ))
        )

        naslov5 = napis(
            "1. NAČIN IZRAČUNA",
            39,
            RDECA,
            True
        ).move_to(UP * 5.7)

        self.play(Write(naslov5))

        kvadrat_ploscina = Square(
            side_length=4.2,
            color=SIVA,
            fill_color=SVETLA_SIVA,
            fill_opacity=0.35,
            stroke_width=5
        ).move_to(UP * 0.9)

        oznaka_stranice = MathTex(
            "a+b",
            color=SIVA
        ).scale(1.1).next_to(kvadrat_ploscina, DOWN, buff=0.2)

        self.play(Create(kvadrat_ploscina))
        self.play(Write(oznaka_stranice))

        formula5a = MathTex(
            "P=(a+b)^2",
            color=SIVA
        ).scale(1.2).move_to(DOWN * 2.5)

        formula5b = MathTex(
            "P=a^2+2ab+b^2",
            color=RDECA
        ).scale(1.15).move_to(DOWN * 3.7)

        self.play(Write(formula5a))
        self.wait(1)
        self.play(TransformFromCopy(formula5a, formula5b))
        self.wait(2)

        # --------------------------------------------------
        # 6. KADER – DRUGI NAČIN IZRAČUNA
        # --------------------------------------------------

        self.play(
            FadeOut(VGroup(
                naslov5,
                kvadrat_ploscina,
                oznaka_stranice,
                formula5a,
                formula5b
            ))
        )

        naslov6 = napis(
            "2. NAČIN IZRAČUNA",
            39,
            RDECA,
            True
        ).move_to(UP * 5.7)

        self.play(Write(naslov6))

        konstrukcija2 = naredi_kvadrat_in_trikotnike()

        self.play(
            Create(konstrukcija2[2]),
            LaggedStart(
                *[FadeIn(t) for t in konstrukcija2[0]],
                lag_ratio=0.2
            ),
            FadeIn(konstrukcija2[1]),
            run_time=3
        )

        self.play(
            FadeIn(konstrukcija2[3]),
            FadeIn(konstrukcija2[4])
        )

        formula6a = MathTex(
            "P=c^2+4\\cdot\\frac{ab}{2}",
            color=SIVA
        ).scale(1.0).move_to(DOWN * 3.5)

        formula6b = MathTex(
            "P=c^2+2ab",
            color=RDECA
        ).scale(1.15).next_to(formula6a, DOWN, buff=0.5)

        self.play(Write(formula6a))
        self.wait(1)
        self.play(Write(formula6b))
        self.wait(2)

        # --------------------------------------------------
        # 7. KADER – ENAČENJE IZRAZOV
        # --------------------------------------------------

        self.play(
            FadeOut(VGroup(
                naslov6,
                konstrukcija2,
                formula6a,
                formula6b
            ))
        )

        naslov7 = napis(
            "ENAČIMO OBA IZRAZA",
            40,
            RDECA,
            True
        ).move_to(UP * 5.7)

        self.play(Write(naslov7))

        uvod7 = napis(
            "Ploščino velikega kvadrata smo izračunali\n"
            "na dva načina, zato izraza enačimo.",
            29,
            SIVA
        ).move_to(UP * 2.6)

        self.play(FadeIn(uvod7))

        enacba1 = MathTex(
            "a^2+2ab+b^2",
            "=",
            "c^2+2ab",
            font_size=53
        ).move_to(UP * 0.5)

        enacba1[0].set_color(RDECA)
        enacba1[2].set_color(MODRA)

        self.play(Write(enacba1))
        self.wait(2)

        odstejemo = napis(
            "Od obeh strani odštejemo 2ab.",
            31,
            SIVA
        ).move_to(DOWN * 1.3)

        self.play(FadeIn(odstejemo))

        enacba2 = MathTex(
            "a^2+b^2=c^2",
            font_size=76,
            color=RDECA
        ).move_to(DOWN * 3.0)

        self.play(
            TransformMatchingTex(
                enacba1.copy(),
                enacba2
            ),
            run_time=2
        )

        self.wait(2)

        # --------------------------------------------------
        # 8. KADER – REZULTAT
        # --------------------------------------------------

        self.play(
            FadeOut(VGroup(
                naslov7,
                uvod7,
                enacba1,
                odstejemo,
                enacba2
            ))
        )

        rezultat = MathTex(
            "a^2+b^2=c^2",
            color=RDECA
        ).scale(1.8).move_to(UP * 1.8)

        okvir = SurroundingRectangle(
            rezultat,
            color=SIVA,
            buff=0.3,
            stroke_width=3
        )

        self.play(Write(rezultat))
        self.play(Create(okvir))

        # Ponovimo začetni trikotnik
        t2 = Polygon(
            LEFT * 1.4 + DOWN * 1.8,
            RIGHT * 1.4 + DOWN * 1.8,
            LEFT * 1.4 + UP * 0.2,
            color=RDECA,
            stroke_width=5
        )

        ta = MathTex("a", color=SIVA).move_to(DOWN * 2.05)
        tb = MathTex("b", color=SIVA).move_to(LEFT * 1.65 + DOWN * 0.8)
        tc = MathTex("c", color=SIVA).move_to(RIGHT * 0.15 + DOWN * 0.5)

        self.play(
            Create(t2),
            Write(ta),
            Write(tb),
            Write(tc)
        )

        self.wait(2)

        # --------------------------------------------------
        # 9. KADER – DOKAZALI SMO!
        # --------------------------------------------------

        self.play(
            FadeOut(VGroup(
                rezultat, okvir,
                t2, ta, tb, tc
            ))
        )

        zakljucek = napis(
            "DOKAZALI SMO\n"
            "PITAGOROV IZREK!",
            55,
            RDECA,
            True
        ).move_to(UP * 1.0)

        self.play(
            Write(zakljucek),
            run_time=2.5
        )

        # Preprost nasmešek
        nasmeh = Arc(
            start_angle=PI,
            angle=PI,
            radius=0.65,
            color=SIVA,
            stroke_width=5
        ).move_to(DOWN * 1.5)

        oko1 = Dot(
            LEFT * 0.35 + DOWN * 0.7,
            color=SIVA
        )
        oko2 = Dot(
            RIGHT * 0.35 + DOWN * 0.7,
            color=SIVA
        )

        self.play(
            Create(nasmeh),
            FadeIn(oko1),
            FadeIn(oko2)
        )

        self.wait(3)

        # --------------------------------------------------
        # 10. KADER – LOGO FMF
        # --------------------------------------------------

        self.play(
            FadeOut(VGroup(
                zakljucek,
                nasmeh,
                oko1,
                oko2
            ))
        )

        # Če slikovnega logotipa ni v mapi, prikažemo preprosto besedilo.
        try:
            logo = ImageMobject("UL_FMF_logo.png")
            logo.scale_to_fit_width(7.5)
            logo.move_to(ORIGIN)
            logo_anim = logo
        except OSError:
            logo_anim = napis("FMF", 60, SIVA, True).move_to(ORIGIN)

        self.play(
            FadeIn(logo_anim),
            run_time=2
        )

        self.wait(4)

        self.play(FadeOut(logo_anim), run_time=1)


# Ta del kode izdela animacijo, ko datoteko poženete z gumbom ▶ v
# urejevalniku VS Code ali z ukazom `python pitagora.py`.
if __name__ == "__main__":
    with tempconfig({"quality": "low_quality", "preview": False}):
        PitagorovIzrek().render()
