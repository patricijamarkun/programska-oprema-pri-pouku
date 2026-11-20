from pathlib import Path

import numpy as np
from manim import *
from manim.mobject.text.text_mobject import register_font


config.pixel_width = 1080
config.pixel_height = 1920
config.frame_width = 9
config.frame_height = 16
config.background_color = "#FFFFFF"



UL_RED = "#E03127"         # UL rdeča – naslovi, okvir rezultata, loki
UL_GRAY = "#58595B"        # UL siva – besedilo, pravi kot
UL_LIGHT_GRAY = "#E6E7E8"  # polnilo trikotnika
COLOR_A = "#2878AC"        # sinjemodra – kateta a
COLOR_B = "#F25E24"        # oranžna – kateta b
COLOR_C = "#00694E"        # zelena – hipotenuza c
COLOR_D = "#EC61A0"        # rožnata – ab, ab/2, 2ab


FONT_NAME = "Univerza Sans"
ASSET_DIR = Path(__file__).parent / "assets"
FONT_DIR = ASSET_DIR / "fonts"

A = 2.4
B = 1.6


def slovene_text(
    text: str,
    font_size: int,
    color: str = UL_GRAY,
    bold: bool = False,
) -> Text:
    with (
        register_font(FONT_DIR / "UniverzaSans-Regular.ttf"),
        register_font(FONT_DIR / "UniverzaSans-Bold.ttf"),
    ):
        return Text(
            text,
            font=FONT_NAME,
            font_size=font_size,
            color=color,
            weight=BOLD if bold else NORMAL,
            line_spacing=1.05,
            should_center=True,
        )


def centered_text(
    text: str,
    font_size: int,
    color: str = UL_GRAY,
    bold: bool = False,
) -> Paragraph:
    """Večvrstično besedilo, kjer je vsaka vrstica sredinsko poravnana."""
    with (
        register_font(FONT_DIR / "UniverzaSans-Regular.ttf"),
        register_font(FONT_DIR / "UniverzaSans-Bold.ttf"),
    ):
        return Paragraph(
            *[line.strip() for line in text.split("\n")],
            font=FONT_NAME,
            font_size=font_size,
            color=color,
            weight=BOLD if bold else NORMAL,
            line_spacing=1.05,
            alignment="center",
        )


def colored_math(
    *parts: str,
    colors: dict[int, str],
    font_size: int,
    max_width: float = 8.2,
) -> MathTex:
    formula = MathTex(
        *parts,
        font_size=font_size,
        color=UL_GRAY,
        should_center=True,
    )
    for index, color in colors.items():
        formula[index].set_color(color)
    if formula.width > max_width:
        formula.scale_to_fit_width(max_width)
    return formula


def side_square(p1, p2, opposite, color, stroke_width: float = 4):
    """Kvadrat nad stranico p1-p2 (na strani, ki je stran od opposite)
    in njegova 'sploščena' začetna oblika za animacijo rasti."""
    direction = p2 - p1
    length = np.linalg.norm(direction)
    normal = np.array([-direction[1], direction[0], 0]) / length
    if np.dot(normal, opposite - p1) > 0:
        normal = -normal
    style = dict(
        color=color,
        fill_color=color,
        fill_opacity=0.28,
        stroke_width=stroke_width,
    )
    square = Polygon(
        p1, p2, p2 + normal * length, p1 + normal * length, **style
    ).set_z_index(1)
    flat = Polygon(
        p1, p2, p2 + normal * 0.01, p1 + normal * 0.01, **style
    ).set_z_index(1)
    return flat, square


class PitagorovIzrek(Scene):
    def construct(self):
        self.camera.background_color = "#FFFFFF"

        def heading(text: str, size: int = 48) -> Text:
            return slovene_text(text, size, UL_RED, bold=True).move_to(UP * 6.55)

        # 1. Uvodno vprašanje
        title = centered_text(
            "GEOMETRIJSKI DOKAZ\nPITAGOROVEGA IZREKA",
            46,
            UL_RED,
            bold=True,
        ).move_to(DOWN * 5.4)

        a_point = LEFT * 2.6 + UP * 0.6
        b_point = RIGHT * 2.6 + UP * 0.6
        # Razmerje katet b : a = B : A (enako v vseh kadrih).
        c_point = b_point + UP * np.linalg.norm(b_point - a_point) * B / A
        triangle_fill = Polygon(
            a_point,
            b_point,
            c_point,
            stroke_opacity=0,
            fill_color=UL_LIGHT_GRAY,
            fill_opacity=0.75,
        )
        side_a = Line(a_point, b_point, color=COLOR_A, stroke_width=8)
        side_b = Line(b_point, c_point, color=COLOR_B, stroke_width=8)
        side_c = Line(a_point, c_point, color=COLOR_C, stroke_width=8)
        left_angle = RightAngle(
            Line(a_point, b_point),
            Line(b_point, c_point),
            length=0.42,
            quadrant=(-1, 1),
            color=UL_RED,
            stroke_width=6,
        )
        VGroup(side_a, side_b, side_c, left_angle).set_z_index(3)

        label_a = MathTex("a", color=COLOR_A).scale(0.95).next_to(
            Line(a_point, b_point), DOWN, buff=0.16
        )
        label_b = MathTex("b", color=COLOR_B).scale(0.95).next_to(
            Line(b_point, c_point), RIGHT, buff=0.18
        )
        label_c = MathTex("c", color=COLOR_C).scale(0.95).move_to(
            (a_point + c_point) / 2 + LEFT * 0.35 + UP * 0.35
        )
        triangle_labels = VGroup(label_a, label_b, label_c).set_z_index(4)
        question = slovene_text(
            "Zakaj velja Pitagorov izrek?",
            46,
            UL_GRAY,
            bold=True,
        ).move_to(UP * 6.2)
        opening_formula = colored_math(
            "a^2",
            "+",
            "b^2",
            "=",
            "c^2",
            colors={0: COLOR_A, 2: COLOR_B, 4: COLOR_C},
            font_size=76,
        ).move_to(DOWN * 3.85)

        # Trikotnik se pojavi naenkrat, stranice so že označene.
        self.play(
            FadeIn(question),
            FadeIn(VGroup(triangle_fill, side_a, side_b, side_c, triangle_labels)),
            run_time=1.0,
        )

        # Poudarimo pravi kot.
        self.play(Create(left_angle), run_time=0.5)
        self.play(
            Indicate(left_angle, scale_factor=1.8, color=UL_RED),
            Flash(
                left_angle.get_center(),
                color=UL_RED,
                line_length=0.25,
                flash_radius=0.45,
                num_lines=10,
            ),
            run_time=1.1,
        )
        self.wait(0.4)

        # Kopija velikega trikotnika za zaključni kader.
        final_triangle_template = VGroup(
            triangle_fill, side_a, side_b, side_c, left_angle, triangle_labels
        ).copy()

        # Trikotnik zmanjšamo, oznake stranic premaknemo v notranjost.
        shrink = 3.0 / np.linalg.norm(b_point - a_point)
        right_vertex = RIGHT * 1.5 + UP * 0.3
        small_a = right_vertex + (a_point - b_point) * shrink
        small_c = right_vertex + (c_point - b_point) * shrink
        hyp_mid = (small_a + small_c) / 2
        inward = np.array([-(small_c - small_a)[1], (small_c - small_a)[0], 0])
        inward = inward / np.linalg.norm(inward)
        if np.dot(inward, right_vertex - hyp_mid) < 0:
            inward = -inward
        self.play(
            VGroup(triangle_fill, side_a, side_b, side_c, left_angle)
            .animate.scale(shrink, about_point=b_point)
            .shift(right_vertex - b_point),
            label_a.animate.scale(0.8).move_to(
                (small_a + right_vertex) / 2 + UP * 0.28 + LEFT * 0.3
            ),
            label_b.animate.scale(0.8).move_to(
                (right_vertex + small_c) / 2 + LEFT * 0.28
            ),
            label_c.animate.scale(0.8).move_to(hyp_mid + inward * 0.32),
            run_time=1.2,
        )

        # Kvadrati nad stranicami a, b in c ter sproti formula.
        p_a, p_b, p_c = side_a.get_start(), side_a.get_end(), side_b.get_end()
        side_squares = VGroup()
        square_labels = VGroup()
        formula_parts = [
            opening_formula[0],
            VGroup(opening_formula[1], opening_formula[2]),
            VGroup(opening_formula[3], opening_formula[4]),
        ]
        for (p1, p2, opposite), tex, color, part in zip(
            [(p_a, p_b, p_c), (p_b, p_c, p_a), (p_a, p_c, p_b)],
            ["a^2", "b^2", "c^2"],
            [COLOR_A, COLOR_B, COLOR_C],
            formula_parts,
        ):
            flat, square = side_square(p1, p2, opposite, color)
            square_label = (
                MathTex(tex, color=color, font_size=60)
                .move_to(square.get_center())
                .set_z_index(4)
            )
            # Najprej cel kvadrat, nato zapis v njem (in hkrati v formuli).
            self.play(ReplacementTransform(flat, square), run_time=1.0)
            self.play(Write(square_label), Write(part), run_time=0.8)
            self.wait(0.4)
            side_squares.add(square)
            square_labels.add(square_label)

        self.play(FadeIn(title), run_time=0.8)  # naenkrat, ne po črkah
        self.wait(1.6)

        # 2. Štiri pravokotne trikotnike zložimo v kvadrat s stranico a + b
        self.play(
            FadeOut(
                VGroup(
                    title,
                    triangle_fill,
                    side_a,
                    side_b,
                    side_c,
                    left_angle,
                    triangle_labels,
                    side_squares,
                    square_labels,
                    question,
                    opening_formula,
                )
            ),
            run_time=0.8,
        )

        leg_a = 3.0
        leg_b = leg_a * B / A  # enako razmerje kot v ostalih kadrih (b = 2/3 a)
        side = leg_a + leg_b

        def right_triangle(r, pa, pb) -> VGroup:
            """Pravokotni trikotnik s pravim kotom v r, kateto a (r-pa),
            kateto b (r-pb) in hipotenuzo c (pa-pb)."""
            fill = Polygon(
                r, pa, pb,
                stroke_opacity=0,
                fill_color=UL_LIGHT_GRAY,
                fill_opacity=0.85,
            )
            leg_a_line = Line(r, pa, color=COLOR_A, stroke_width=6)
            leg_b_line = Line(r, pb, color=COLOR_B, stroke_width=6)
            hypotenuse = Line(pa, pb, color=COLOR_C, stroke_width=6)
            angle = RightAngle(
                Line(r, pb), Line(r, pa),
                length=0.28, quadrant=(1, 1),
                color=UL_RED, stroke_width=4,
            )
            return VGroup(fill, leg_a_line, leg_b_line, hypotenuse, angle).set_z_index(2)

        def label_spot(p1, p2, away_from, offset):
            """Točka ob sredini daljice p1-p2, odmaknjena stran od away_from."""
            mid = (p1 + p2) / 2
            d = p2 - p1
            normal = np.array([-d[1], d[0], 0]) / np.linalg.norm(d)
            if np.dot(normal, away_from - mid) > 0:
                normal = -normal
            return mid + normal * offset

        def label_positions(r, pa, pb):
            return [
                label_spot(r, pa, pb, 0.3),   # a stran od trikotnika
                label_spot(r, pb, pa, 0.3),   # b stran od trikotnika
                label_spot(pa, pb, r, 0.32),  # c stran od pravega kota
            ]

        # Začetna postavitev: 2 x 2 enaki trikotniki
        # (pravi kot spodaj levo, a vodoravno, b navpično).
        grid_centers = [
            UP * 2.3 + LEFT * 1.9,    # -> zgoraj levo v kvadratu
            UP * 2.3 + RIGHT * 1.9,   # -> zgoraj desno
            DOWN * 0.9 + LEFT * 1.9,  # -> spodaj levo
            DOWN * 0.9 + RIGHT * 1.9, # -> spodaj desno
        ]
        start_vertices = []
        for center in grid_centers:
            r = center + LEFT * leg_a / 2 + DOWN * leg_b / 2
            start_vertices.append((r, r + RIGHT * leg_a, r + UP * leg_b))

        # Končna postavitev v kvadratu (kot na skici).
        square_center = UP * 0.55
        corner = square_center + np.array([-side / 2, -side / 2, 0])

        def q(x, y):
            return corner + np.array([x, y, 0])

        s, a_, b_ = side, leg_a, leg_b
        target_vertices = [
            (q(0, s), q(0, b_), q(b_, s)),  # zgoraj levo
            (q(s, s), q(b_, s), q(s, a_)),  # zgoraj desno
            (q(0, 0), q(a_, 0), q(0, b_)),  # spodaj levo
            (q(s, 0), q(s, a_), q(a_, 0)),  # spodaj desno
        ]
        rotations = [-PI / 2, PI, 0, PI / 2]

        four_triangles = VGroup()
        four_labels = VGroup()
        label_targets = []
        for (r, pa, pb), (rt, pat, pbt) in zip(start_vertices, target_vertices):
            four_triangles.add(right_triangle(r, pa, pb))
            labels = VGroup(
                *[
                    MathTex(tex, color=color, font_size=44).move_to(pos)
                    for tex, color, pos in zip(
                        ["a", "b", "c"],
                        [COLOR_A, COLOR_B, COLOR_C],
                        label_positions(r, pa, pb),
                    )
                ]
            ).set_z_index(4)
            four_labels.add(labels)
            label_targets.append(label_positions(rt, pat, pbt))

        def rigid_motion(tri, labels, angle, start_tri, target_tri):
            """Trikotnik zavrti okoli težišča in ga premakne na cilj.
            Oznake potujejo skupaj s trikotnikom, a ostanejo pokončne."""
            c0 = np.mean(start_tri, axis=0)
            c1 = np.mean(target_tri, axis=0)
            original = tri.copy()
            label_starts = [label.get_center() for label in labels]

            def update(group, alpha):
                group[0].become(
                    original.copy()
                    .rotate(angle * alpha, about_point=c0)
                    .shift((c1 - c0) * alpha)
                )
                rotation = rotation_matrix(angle * alpha, OUT)
                for label, p in zip(group[1], label_starts):
                    label.move_to(c0 + rotation @ (p - c0) + (c1 - c0) * alpha)

            return UpdateFromAlphaFunc(VGroup(tri, labels), update)

        # Zgornji zapis po višini na sredini med vrhom videa in trikotniki.
        triangles_top = VGroup(four_triangles, four_labels).get_top()[1]
        top_text = centered_text(
            "4 pravokotne trikotnike",
            40,
            UL_GRAY,
            bold=True,
        ).move_to(UP * (config.frame_height / 2 + triangles_top) / 2)
        bottom_text = centered_text(
            "zložimo v kvadrat\ns stranico a + b.",
            40,
            UL_GRAY,
            bold=True,
        ).move_to(DOWN * 4.4)

        self.play(FadeIn(top_text), run_time=1.0)
        self.wait(0.5)
        self.play(
            FadeIn(four_triangles, scale=0.9),
            FadeIn(four_labels),
            run_time=1.5,
        )
        self.wait(1.0)
        self.play(FadeIn(bottom_text), run_time=1.0)
        self.wait(0.8)

        # Trikotniki se zložijo v kvadrat; oznake ostanejo pokončne.
        self.play(
            *[
                rigid_motion(tri, labels, angle, start, target)
                for tri, labels, angle, start, target in zip(
                    four_triangles,
                    four_labels,
                    rotations,
                    start_vertices,
                    target_vertices,
                )
            ],
            run_time=2.5,
        )
        # Za vsak primer oznake postavimo natanko na končna mesta.
        for labels, targets in zip(four_labels, label_targets):
            for label, target in zip(labels, targets):
                label.move_to(target)
        self.wait(2.0)

        # Zapisa zamenjamo z novim naslovom; kvadrat ostane enak.
        area_two_ways = centered_text(
            "Izračunajmo ploščino\ndobljenega kvadrata\nna 2 načina.",
            40,
            UL_GRAY,
            bold=True,
        ).move_to(UP * 5.9)
        self.play(FadeOut(top_text), FadeOut(bottom_text), run_time=0.8)
        self.play(FadeIn(area_two_ways), run_time=1.0)
        self.wait(2.5)

        # 3. 1. način: notranji kvadrat + 4 trikotniki
        def note_text(text: str, color: str, math: str | None = None) -> VGroup:
            """Zapis pod naslovom; po potrebi z matematičnim delom na koncu."""
            words = centered_text(text, 34, color, bold=True)
            group = VGroup(words)
            if math is not None:
                formula = MathTex(math, color=color, font_size=44)
                last_line = words[-1]
                formula.next_to(last_line, RIGHT, buff=0.16)
                if r"\frac" in math:
                    # ulomek sredinsko ob zadnji vrstici
                    formula.match_y(last_line)
                else:
                    # poravnava po osnovni črti (zadnja črka nima spodnjega dela)
                    formula.shift(
                        UP * (last_line[-1].get_bottom()[1] - formula[0][0].get_bottom()[1])
                    )
                group.add(formula)
            if group.width > 8.3:
                group.scale_to_fit_width(8.3)
            return group

        method_one_title = heading("1. NAČIN:").to_edge(LEFT, buff=0.6)
        note_c = note_text("ploščina notranjega kvadrata", COLOR_C, "c^2")
        note_triangles = note_text(
            "ploščine 4 enakih\npravokotnih trikotnikov", COLOR_D, r"\frac{ab}{2}"
        )
        # Zapisi drug pod drugim, zgornji rob tik pod naslovom.
        notes = VGroup(note_c, note_triangles).arrange(DOWN, buff=0.18)
        notes.set_x(0).shift(UP * (5.95 - notes.get_top()[1]))

        # Obarvanje lika: zelen notranji kvadrat in rdeči trikotniki.
        inner_square_c = Polygon(
            q(a_, 0), q(s, a_), q(b_, s), q(0, b_),
            stroke_width=0,
            fill_color=COLOR_C,
            fill_opacity=0.34,
        ).set_z_index(1)
        inner_label = MathTex("c^2", color=COLOR_C, font_size=60).move_to(
            square_center
        ).set_z_index(4)
        triangle_area_labels = VGroup(
            *[
                MathTex(r"\frac{ab}{2}", color=COLOR_D, font_size=38)
                .move_to(np.mean(vertices, axis=0))
                .set_z_index(4)
                for vertices in target_vertices
            ]
        )

        # Formula v eni vrstici; zadnji člen se preuredi kar na mestu:
        # 4·ab/2  ->  (4/2)·ab  ->  2ab
        p1_versions = [
            colored_math(
                "P_1", "=", "c^2", "+", last,
                colors={2: COLOR_C, 4: COLOR_D},
                font_size=52,
            )
            for last in [r"4\cdot\frac{ab}{2}", r"\frac{4}{2}\cdot ab", "2ab"]
        ]
        # Kvadrat ostane na istem mestu; formula je pod njim z enakim
        # razmikom, kot je med zapisi in kvadratom.
        figure = VGroup(four_triangles, four_labels)
        gap = notes.get_bottom()[1] - figure.get_top()[1]
        p1_line = p1_versions[0]
        p1_line.shift(
            UP * (figure.get_bottom()[1] - gap - p1_line.get_top()[1])
            + LEFT * p1_line.get_x()
        )
        for version in p1_versions[1:]:
            version.shift(p1_line[1].get_center() - version[1].get_center())

        self.play(FadeOut(area_two_ways), run_time=0.8)
        self.play(Write(method_one_title), run_time=0.8)
        self.wait(0.3)
        self.play(Write(p1_line[:2]), run_time=1.0)
        self.wait(0.8)

        # Zeleno: notranji kvadrat c^2
        self.play(
            FadeIn(note_c, shift=DOWN * 0.15),
            Write(p1_line[2]),
            FadeIn(inner_square_c),
            Write(inner_label),
            run_time=1.3,
        )
        self.wait(0.8)

        self.play(Write(p1_line[3]), run_time=0.6)
        self.wait(0.3)

        # Rdeče: 4 trikotniki s ploščino ab/2
        self.play(
            FadeIn(note_triangles, shift=DOWN * 0.15),
            Write(p1_line[4]),
            *[tri[0].animate.set_fill(COLOR_D, opacity=0.28) for tri in four_triangles],
            FadeIn(triangle_area_labels),
            run_time=1.3,
        )
        self.wait(1.2)

        # Preurejanje zadnjega člena v isti vrstici.
        self.play(
            TransformMatchingShapes(p1_line[4], p1_versions[1][4]), run_time=1.0
        )
        self.wait(0.5)
        self.play(
            TransformMatchingShapes(p1_versions[1][4], p1_versions[2][4]),
            run_time=1.0,
        )
        # Krajšo vrstico poravnamo nazaj na sredino.
        final_p1 = VGroup(*p1_line[:4], p1_versions[2][4])
        self.play(final_p1.animate.set_x(0), run_time=0.6)
        self.wait(2.0)

        # 4. 2. način: P_2 = (a+b)(a+b) = a^2 + 2ab + b^2
        # Indeksi trikotnikov: 0 zgoraj levo, 1 zgoraj desno, 2 spodaj levo,
        # 3 spodaj desno; v vsakem: 0 polnilo, 1 kateta a, 2 kateta b,
        # 3 hipotenuza, 4 pravi kot. Oznake: 0 a, 1 b, 2 c.
        tl, tr, bl, br = four_triangles
        lab_tl, lab_tr, lab_bl, lab_br = four_labels

        # Desna in spodnja stranica ostaneta barvni z oznakami a, b.
        kept_sides = VGroup(tr[2], br[1], bl[1], br[2])
        kept_labels = VGroup(lab_tr[1], lab_br[0], lab_bl[0], lab_br[1])
        # Zgornja in leva stranica ostaneta vidni, le posivita.
        gray_sides = VGroup(tl[2], tr[1], tl[1], bl[2])
        removed = VGroup(
            *[tri[k] for tri in four_triangles for k in (0, 3, 4)],
            *[labels[2] for labels in four_labels],
            lab_tl[0], lab_tl[1], lab_tr[0], lab_bl[1],
            inner_square_c, inner_label, triangle_area_labels,
            notes, final_p1,
        )

        # Oznaki a + b (kvadrat se vrne na prvotno mesto, zato q(...) brez premika).
        top_ref = Line(q(0, s), q(s, s))
        left_ref = Line(q(0, 0), q(0, s))
        sum_labels = VGroup(
            MathTex("a+b", color=UL_GRAY, font_size=44).next_to(top_ref, UP, buff=0.18),
            MathTex("a+b", color=UL_GRAY, font_size=44).next_to(left_ref, LEFT, buff=0.2),
        ).set_z_index(4)

        method_two_title = heading("2. NAČIN:").to_edge(LEFT, buff=0.6)

        # Deli kvadrata: a^2 spodaj levo, ab desno spodaj in levo zgoraj,
        # b^2 zgoraj desno (skladno z oznakami na spodnji in desni stranici).
        def part(x, y, w, h, color):
            return Polygon(
                q(x, y), q(x + w, y), q(x + w, y + h), q(x, y + h),
                color=color,
                fill_color=color,
                fill_opacity=0.28,
                stroke_width=3,
            ).set_z_index(1)

        part_a2 = part(0, 0, a_, a_, COLOR_A)
        part_ab_1 = part(a_, 0, b_, a_, COLOR_D)
        part_ab_2 = part(0, a_, a_, b_, COLOR_D)
        part_b2 = part(a_, a_, b_, b_, COLOR_B)
        part_labels = [
            MathTex("a^2", color=COLOR_A, font_size=56).move_to(part_a2),
            MathTex("ab", color=COLOR_D, font_size=48).move_to(part_ab_1),
            MathTex("ab", color=COLOR_D, font_size=48).move_to(part_ab_2),
            MathTex("b^2", color=COLOR_B, font_size=50).move_to(part_b2),
        ]
        for label in part_labels:
            label.set_z_index(4)

        # Indeksi: 0 P_2=, 1 (, 2 a, 3 +, 4 b, 5 ), 6 (, 7 a, 8 +, 9 b, 10 ),
        #          11 =, 12 a^2, 13 +, 14 2ab, 15 +, 16 b^2
        formula_p2 = colored_math(
            "P_2=",
            "(", "a", "+", "b", ")",
            "(", "a", "+", "b", ")",
            "=",
            "a^2", "+", "2ab", "+", "b^2",
            colors={
                2: COLOR_A, 4: COLOR_B, 7: COLOR_A, 9: COLOR_B,
                12: COLOR_A, 14: COLOR_D, 16: COLOR_B,
            },
            font_size=48,
        ).move_to(DOWN * 3.4)

        arc_top_y = formula_p2[1].get_top()[1] + 0.08
        arc_bottom_y = formula_p2[1].get_bottom()[1] - 0.08

        def expansion_arc(left, right, above: bool) -> ArcBetweenPoints:
            """Rdeča krivulja, ki poveže dva člena, ki ju zmnožimo."""
            y = arc_top_y if above else arc_bottom_y
            return ArcBetweenPoints(
                np.array([left.get_x(), y, 0]),
                np.array([right.get_x(), y, 0]),
                angle=-0.45 * PI if above else 0.45 * PI,
                color=UL_RED,
                stroke_width=3.5,
            ).set_z_index(7)

        fa1, fb1, fa2, fb2 = formula_p2[2], formula_p2[4], formula_p2[7], formula_p2[9]
        arc_aa = expansion_arc(fa1, fa2, above=True)
        arc_ab = expansion_arc(fa1, fb2, above=False)
        arc_ba = expansion_arc(fb1, fa2, above=False)
        arc_bb = expansion_arc(fb1, fb2, above=True)

        # Pospravimo 1. način; kvadrat ostane na istem mestu.
        self.play(
            FadeOut(removed),
            ReplacementTransform(method_one_title, method_two_title),
            gray_sides.animate.set_color(UL_GRAY),
            FadeIn(sum_labels),
            run_time=1.4,
        )
        self.wait(0.5)
        self.play(Write(formula_p2[0]), run_time=0.8)
        self.wait(0.3)
        self.play(Write(formula_p2[1:12]), run_time=1.6)
        self.wait(0.6)

        # a · a = a^2
        self.play(Create(arc_aa), run_time=0.8)
        self.play(
            Write(formula_p2[12]),
            FadeIn(part_a2),
            FadeIn(part_labels[0]),
            run_time=1.2,
        )
        self.wait(0.5)

        # a · b + b · a = 2ab
        self.play(Create(arc_ab), Create(arc_ba), run_time=0.9)
        self.play(
            Write(formula_p2[13:15]),
            FadeIn(part_ab_1),
            FadeIn(part_ab_2),
            FadeIn(part_labels[1]),
            FadeIn(part_labels[2]),
            run_time=1.2,
        )
        self.wait(0.5)

        # b · b = b^2
        self.play(Create(arc_bb), run_time=0.8)
        self.play(
            Write(formula_p2[15:]),
            FadeIn(part_b2),
            FadeIn(part_labels[3]),
            run_time=1.2,
        )
        self.wait(2.5)

        # 5. Enačimo oba izraza: c^2 + 2ab = a^2 + 2ab + b^2  ->  c^2 = a^2 + b^2
        self.play(*[FadeOut(mob) for mob in self.mobjects], run_time=0.8)

        equate_title = centered_text(
            "ENAČIMO OBA IZRAZA\nZA PLOŠČINO",
            43,
            UL_RED,
            bold=True,
        ).move_to(UP * 6.35)

        eq_p = colored_math("P_1", "=", "P_2", colors={}, font_size=56).move_to(
            UP * 4.5
        )
        # 0 c^2, 1 +, 2 2ab, 3 =, 4 a^2, 5 +, 6 2ab, 7 +, 8 b^2
        eq_full = colored_math(
            "c^2", "+", "2ab", "=", "a^2", "+", "2ab", "+", "b^2",
            colors={0: COLOR_C, 2: COLOR_D, 4: COLOR_A, 6: COLOR_D, 8: COLOR_B},
            font_size=52,
        ).move_to(UP * 3.1)
        subtract_note = centered_text(
            "Na obeh straneh odštejemo 2ab:",
            34,
            UL_GRAY,
            bold=True,
        ).move_to(UP * 1.85)
        # 0 c^2, 1 +, 2 2ab, 3 -, 4 2ab, 5 =, 6 a^2, 7 +, 8 2ab, 9 +, 10 b^2,
        # 11 -, 12 2ab
        eq_sub = colored_math(
            "c^2", "+", "2ab", "-", "2ab", "=",
            "a^2", "+", "2ab", "+", "b^2", "-", "2ab",
            colors={
                0: COLOR_C, 2: COLOR_D, 4: COLOR_D,
                6: COLOR_A, 8: COLOR_D, 10: COLOR_B, 12: COLOR_D,
            },
            font_size=48,
            max_width=7.4,  # dovolj odmika od robov zaslona
        ).move_to(UP * 0.6)
        eq_result = colored_math(
            "c^2", "=", "a^2", "+", "b^2",
            colors={0: COLOR_C, 2: COLOR_A, 4: COLOR_B},
            font_size=72,
        ).move_to(DOWN * 1.3)
        result_frame = SurroundingRectangle(
            eq_result, color=UL_RED, buff=0.3, stroke_width=5
        )

        self.play(Write(equate_title), run_time=0.9)
        self.wait(0.3)
        self.play(Write(eq_p), run_time=1.0)
        self.wait(0.6)

        # P_1 -> c^2 + 2ab,  P_2 -> a^2 + 2ab + b^2
        self.play(
            TransformFromCopy(eq_p[0], eq_full[0:3]),
            TransformFromCopy(eq_p[1], eq_full[3]),
            TransformFromCopy(eq_p[2], eq_full[4:]),
            run_time=1.6,
        )
        self.wait(0.8)

        # Na obeh straneh odštejemo 2ab.
        self.play(FadeIn(subtract_note), run_time=0.8)
        self.wait(0.4)
        line_map = {0: 0, 1: 1, 2: 2, 3: 5, 4: 6, 5: 7, 6: 8, 7: 9, 8: 10}
        self.play(
            *[
                TransformFromCopy(eq_full[src], eq_sub[dst])
                for src, dst in line_map.items()
            ],
            run_time=1.2,
        )
        self.wait(0.3)
        new_terms = VGroup(eq_sub[3:5], eq_sub[11:13])
        self.play(Write(new_terms), run_time=1.0)  # brez povečevanja
        self.wait(0.8)

        # 2ab - 2ab = 0 na vsaki strani: para se spusti pod vrstico, se združi
        # v 0 in izgine (nad vrstico je sivi zapis).
        pairs = [
            (VGroup(eq_sub[1], eq_sub[2]), VGroup(eq_sub[3], eq_sub[4])),  # levo
            (VGroup(eq_sub[7], eq_sub[8]), VGroup(eq_sub[11], eq_sub[12])),  # desno
        ]
        meet_points = [
            (plus.get_center() + minus.get_center()) / 2 + DOWN * 0.8
            for plus, minus in pairs
        ]
        self.play(
            *[
                term.animate.move_to(point)
                for (plus, minus), point in zip(pairs, meet_points)
                for term in (plus, minus)
            ],
            run_time=1.0,
        )
        zeros = [
            MathTex("0", color=UL_GRAY, font_size=48).move_to(point)
            for point in meet_points
        ]
        self.play(
            *[
                ReplacementTransform(VGroup(plus, minus), zero)
                for (plus, minus), zero in zip(pairs, zeros)
            ],
            run_time=0.6,
        )
        self.wait(0.3)
        self.play(*[FadeOut(zero, scale=0.4) for zero in zeros], run_time=0.5)

        # Preostanek vrstice se strne: c^2 = a^2 + b^2
        eq_short = colored_math(
            "c^2", "=", "a^2", "+", "b^2",
            colors={0: COLOR_C, 2: COLOR_A, 4: COLOR_B},
            font_size=48,
        )
        eq_short.scale(eq_sub[0].height / eq_short[0].height)
        eq_short.shift(
            UP * (eq_sub[5].get_y() - eq_short[1].get_y()) + LEFT * eq_short.get_x()
        )
        short_map = {0: 0, 5: 1, 6: 2, 9: 3, 10: 4}
        self.play(
            *[
                ReplacementTransform(eq_sub[src], eq_short[dst])
                for src, dst in short_map.items()
            ],
            run_time=0.9,
        )
        self.wait(0.5)

        # Rezultat povečan v okvirju.
        self.play(TransformFromCopy(eq_short, eq_result), run_time=1.2)
        self.play(Create(result_frame), run_time=0.7)
        self.wait(2.5)

        # 6. Sklep: formula v okvirju ostane, izpeljavo zamenja trikotnik iz 1. kadra.
        final_title = centered_text(
            "DOKAZALI SMO\nPITAGOROV IZREK!",
            46,
            UL_RED,
            bold=True,
        ).move_to(UP * 6.3)
        closing_triangle = final_triangle_template.copy().move_to(UP * 2.75)
        derivation = VGroup(eq_p, eq_full, subtract_note, eq_short)
        # Pitagora (slike pripravi assets/pripravi_pitagoro.py).
        pythagoras = {
            name: ImageMobject(str(ASSET_DIR / f"pitagora_{name}.png"))
            .set_height(3.8)
            .move_to(DOWN * 4.35)
            for name in ["odprto", "priprto", "zaprto"]
        }

        self.play(
            ReplacementTransform(equate_title, final_title),
            FadeOut(derivation),
            run_time=1.0,
        )
        self.play(FadeIn(closing_triangle, scale=0.9), run_time=1.2)
        self.wait(0.4)
        self.play(FadeIn(pythagoras["odprto"], scale=0.9), run_time=0.8)
        self.wait(0.9)

        # Mežik: odprto -> priprto -> zaprto -> priprto -> odprto
        self.add(pythagoras["priprto"])
        self.wait(0.05)
        self.add(pythagoras["zaprto"])
        self.wait(0.4)
        self.remove(pythagoras["zaprto"])
        self.wait(0.05)
        self.remove(pythagoras["priprto"])
        self.wait(2.5)


class Thumbnail(Scene):
    """Naslovna sličica videa (render z: manim -s PI.py Thumbnail)."""

    def construct(self):
        self.camera.background_color = "#FFFFFF"

        # Zgornji in spodnji rdeč pas
        top_bar = Rectangle(
            width=config.frame_width, height=0.35, fill_color=UL_RED,
            fill_opacity=1, stroke_width=0,
        ).to_edge(UP, buff=0)
        bottom_bar = top_bar.copy().to_edge(DOWN, buff=0)

        title = VGroup(
            centered_text("PITAGOROV", 92, UL_RED, bold=True),
            centered_text("IZREK", 92, UL_RED, bold=True),
        ).arrange(DOWN, buff=0.35)
        title.move_to(UP * 5.4).set_x(0)

        # Trikotnik s kvadrati nad stranicami
        a_len, b_len = 2.4, 1.6
        right_vertex = RIGHT * 1.6 + DOWN * 0.9
        p_a = right_vertex + LEFT * a_len
        p_b = right_vertex
        p_c = right_vertex + UP * b_len

        squares = VGroup()
        labels = VGroup()
        for (p1, p2, opposite), tex, color in zip(
            [(p_a, p_b, p_c), (p_b, p_c, p_a), (p_a, p_c, p_b)],
            ["a^2", "b^2", "c^2"],
            [COLOR_A, COLOR_B, COLOR_C],
        ):
            _, square = side_square(p1, p2, opposite, color, stroke_width=6)
            square.set_fill(color, opacity=0.35)
            squares.add(square)
            labels.add(
                MathTex(tex, color=color, font_size=84)
                .move_to(square.get_center())
                .set_z_index(4)
            )

        triangle = Polygon(
            p_a, p_b, p_c,
            stroke_opacity=0, fill_color=UL_LIGHT_GRAY, fill_opacity=1,
        ).set_z_index(2)
        sides = VGroup(
            Line(p_a, p_b, color=COLOR_A, stroke_width=10),
            Line(p_b, p_c, color=COLOR_B, stroke_width=10),
            Line(p_a, p_c, color=COLOR_C, stroke_width=10),
        ).set_z_index(3)
        right_angle = RightAngle(
            Line(p_a, p_b), Line(p_b, p_c), length=0.3,
            quadrant=(-1, 1), color=UL_RED, stroke_width=6,
        ).set_z_index(3)
        figure = VGroup(squares, triangle, sides, right_angle, labels)
        figure.move_to(DOWN * 0.75)

        formula = colored_math(
            "a^2", "+", "b^2", "=", "c^2",
            colors={0: COLOR_A, 2: COLOR_B, 4: COLOR_C},
            font_size=100,
        ).move_to(DOWN * 5.85)
        frame = SurroundingRectangle(
            formula, color=UL_RED, buff=0.3, stroke_width=6, corner_radius=0.15
        )

        self.add(top_bar, bottom_bar, title, figure, formula, frame)


if __name__ == "__main__":
    PitagorovIzrek().render()