from pathlib import Path

import numpy as np
from manim import *
from manim.mobject.text.text_mobject import register_font


config.pixel_width = 1080
config.pixel_height = 1920
config.frame_width = 9
config.frame_height = 16
config.background_color = "#FFFFFF"


UL_RED = "#E03127"
UL_GRAY = "#58595B"
UL_LIGHT_GRAY = "#E6E7E8"
COLOR_A = "#40AEAD"
COLOR_B = "#F25E24"
COLOR_C = "#00694E"
COLOR_D = "#E03127"

FONT_NAME = "Univerza Sans"
FONT_DIR = Path(__file__).parent / "assets" / "fonts"

A = 2.4
B = 1.6
S = A + B
DIAGRAM_SCALE = 1.1
DIAGRAM_CENTER = UP * 1.0


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

        def point(x: float, y: float) -> np.ndarray:
            return DIAGRAM_CENTER + np.array(
                [
                    (x - S / 2) * DIAGRAM_SCALE,
                    (y - S / 2) * DIAGRAM_SCALE,
                    0,
                ]
            )

        def heading(text: str, size: int = 48) -> Text:
            return slovene_text(text, size, UL_RED, bold=True).move_to(UP * 6.55)

        def dimensions() -> VGroup:
            bottom_a = DoubleArrow(
                point(0, 0) + DOWN * 0.12,
                point(A, 0) + DOWN * 0.12,
                color=COLOR_A,
                stroke_width=6,
                buff=0,
                tip_length=0.12,
            )
            bottom_b = DoubleArrow(
                point(A, 0) + DOWN * 0.12,
                point(S, 0) + DOWN * 0.12,
                color=COLOR_B,
                stroke_width=6,
                buff=0,
                tip_length=0.12,
            )
            right_a = DoubleArrow(
                point(S, 0) + RIGHT * 0.12,
                point(S, A) + RIGHT * 0.12,
                color=COLOR_A,
                stroke_width=6,
                buff=0,
                tip_length=0.12,
            )
            right_b = DoubleArrow(
                point(S, A) + RIGHT * 0.12,
                point(S, S) + RIGHT * 0.12,
                color=COLOR_B,
                stroke_width=6,
                buff=0,
                tip_length=0.12,
            )

            labels = VGroup(
                MathTex("a", color=COLOR_A).scale(0.95).next_to(
                    bottom_a, DOWN, buff=0.04
                ),
                MathTex("b", color=COLOR_B).scale(0.95).next_to(
                    bottom_b, DOWN, buff=0.04
                ),
                MathTex("a", color=COLOR_A).scale(0.95).next_to(
                    right_a, RIGHT, buff=0.05
                ),
                MathTex("b", color=COLOR_B).scale(0.95).next_to(
                    right_b, RIGHT, buff=0.05
                ),
            )
            return VGroup(bottom_a, bottom_b, right_a, right_b, labels)

        def tile(x: float, y: float, width: float, height: float, color: str):
            return Polygon(
                point(x, y),
                point(x + width, y),
                point(x + width, y + height),
                point(x, y + height),
                color=color,
                fill_color=color,
                fill_opacity=0.28,
                stroke_width=3,
            ).set_z_index(1)


        # 1. Uvodno vprašanje
        title = slovene_text(
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
            run_time=1.2,
        )

        # Poudarimo pravi kot.
        self.play(Create(left_angle), run_time=0.6)
        self.play(
            Indicate(left_angle, scale_factor=1.8, color=UL_RED),
            Flash(
                left_angle.get_center(),
                color=UL_RED,
                line_length=0.25,
                flash_radius=0.45,
                num_lines=10,
            ),
            run_time=1.3,
        )
        self.wait(0.6)

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
            run_time=1.5,
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
            self.play(ReplacementTransform(flat, square), run_time=1.2)
            self.play(Write(square_label), Write(part), run_time=1.0)
            self.wait(0.5)
            side_squares.add(square)
            square_labels.add(square_label)

        self.play(Write(title), run_time=1.0)
        self.wait(1.8)

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

        top_text = centered_text(
            "4 pravokotne trikotnike\ns katetama a in b\nter hipotenuzo c",
            40,
            UL_GRAY,
            bold=True,
        ).move_to(UP * 5.9)
        bottom_text = centered_text(
            "zložimo v večji kvadrat\ns stranico a + b.",
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

        # ===== ZAKOMENTIRANO: kadri po 1. kadru (od ~16 s naprej) =====
        # # 2. Kvadrat s stranico a + b
        # self.play(
            # FadeOut(
                # VGroup(
                    # title,
                    # triangle_fill,
                    # side_a,
                    # side_b,
                    # side_c,
                    # left_angle,
                    # triangle_labels,
                    # side_squares,
                    # square_labels,
                    # question,
                    # opening_formula,
                # )
            # ),
            # run_time=0.8,
        # )

        # title = slovene_text(
            # "Poglejmo si kvadrat \n    s stranico a + b",
            # 42,
            # UL_GRAY,
            # bold=True,
        # ).move_to(UP * 5.55)
        # outer_square = Square(
            # side_length=S * DIAGRAM_SCALE,
            # color=UL_GRAY,
            # stroke_width=4,
        # ).move_to(DIAGRAM_CENTER).set_z_index(4)
        # side_length_labels = VGroup(
            # MathTex("a+b", color=UL_GRAY, font_size=40).next_to(
                # outer_square, UP, buff=0.18
            # ),
            # MathTex("a+b", color=UL_GRAY, font_size=40).next_to(
                # outer_square, LEFT, buff=0.2
            # ),
        # ).set_z_index(6)
        # side_dimensions = dimensions().set_z_index(5)
        # explanation = slovene_text(
            # "in izračunajmo njegovo\n  ploščino na 2 načina.",
            # 42,
            # UL_GRAY,
            # bold=True,
        # ).move_to(DOWN * 3.55)

        # self.play(
            # Write(title),
            # Create(outer_square),
            # FadeIn(side_length_labels),
            # run_time=1.5,
        # )
        # self.play(FadeIn(side_dimensions), run_time=0.8)
        # self.play(FadeIn(explanation), run_time=0.6)
        # self.wait(2)

        # # 3. Prvi način: kvadrati in pravokotnika
        # self.play(
            # FadeOut(explanation),
            # FadeOut(title),
            # run_time=0.6,
        # )
        # title = heading("1. NAČIN:")
        # area_heading = (
            # centered_text(
                # "Izračunajmo ploščino\nkvadrata s stranico a + b.",
                # 42,
                # UL_GRAY,
                # bold=True,
            # )
            # .next_to(title, DOWN, buff=0.35)
            # .set_x(0)
        # )
        # a_square = tile(0, 0, A, A, COLOR_A)
        # b_square = tile(A, A, B, B, COLOR_B)
        # ab_rectangle_1 = tile(A, 0, B, A, COLOR_D)
        # ab_rectangle_2 = tile(0, A, A, B, COLOR_D)
        # area_pieces = VGroup(
            # a_square,
            # b_square,
            # ab_rectangle_1,
            # ab_rectangle_2,
        # )
        # area_labels = VGroup(
            # MathTex("a^2", color=COLOR_A, font_size=48).move_to(point(A / 2, A / 2)),
            # MathTex("b^2", color=COLOR_B, font_size=44).move_to(
                # point(A + B / 2, A + B / 2)
            # ),
            # MathTex("ab", color=COLOR_D, font_size=44).move_to(
                # point(A + B / 2, A / 2)
            # ),
            # MathTex("ab", color=COLOR_D, font_size=44).move_to(
                # point(A / 2, A + B / 2)
            # ),
        # ).set_z_index(6)

        # # Indeksi: 0 P_1=, 1 (, 2 a, 3 +, 4 b, 5 ), 6 (, 7 a, 8 +, 9 b, 10 ),
        # #          11 =, 12 a^2, 13 +, 14 2ab, 15 +, 16 b^2
        # formula_one = colored_math(
            # "P_1=",
            # "(", "a", "+", "b", ")",
            # "(", "a", "+", "b", ")",
            # "=",
            # "a^2",
            # "+",
            # "2ab",
            # "+",
            # "b^2",
            # colors={
                # 2: COLOR_A,
                # 4: COLOR_B,
                # 7: COLOR_A,
                # 9: COLOR_B,
                # 12: COLOR_A,
                # 14: COLOR_D,
                # 16: COLOR_B,
            # },
            # font_size=48,
        # ).move_to(DOWN * 3.0)

        # arc_top_y = formula_one[1].get_top()[1] + 0.08
        # arc_bottom_y = formula_one[1].get_bottom()[1] - 0.08

        # def expansion_arc(left, right, above: bool) -> ArcBetweenPoints:
            # """Rdeča krivulja, ki poveže dva člena, ki ju zmnožimo."""
            # y = arc_top_y if above else arc_bottom_y
            # return ArcBetweenPoints(
                # np.array([left.get_x(), y, 0]),
                # np.array([right.get_x(), y, 0]),
                # angle=-0.45 * PI if above else 0.45 * PI,
                # color=UL_RED,
                # stroke_width=3.5,
            # ).set_z_index(7)

        # a1, b1, a2, b2 = formula_one[2], formula_one[4], formula_one[7], formula_one[9]
        # arc_aa = expansion_arc(a1, a2, above=True)
        # arc_ab = expansion_arc(a1, b2, above=False)
        # arc_ba = expansion_arc(b1, a2, above=False)
        # arc_bb = expansion_arc(b1, b2, above=True)
        # expansion_arcs = VGroup(arc_aa, arc_ab, arc_ba, arc_bb)

        # self.play(Write(title), run_time=0.8)
        # self.wait(0.3)
        # self.play(FadeIn(area_heading), run_time=0.9)
        # self.wait(0.5)
        # self.play(Write(formula_one[:12]), run_time=1.6)
        # self.wait(0.6)

        # # a · a = a^2
        # self.play(Create(arc_aa), run_time=0.8)
        # self.play(
            # Write(formula_one[12]),
            # FadeIn(a_square),
            # FadeIn(area_labels[0]),
            # run_time=1.2,
        # )
        # self.wait(0.5)

        # # a · b + b · a = 2ab
        # self.play(Create(arc_ab), Create(arc_ba), run_time=0.9)
        # self.play(
            # Write(formula_one[13:15]),
            # FadeIn(ab_rectangle_1),
            # FadeIn(ab_rectangle_2),
            # FadeIn(area_labels[2]),
            # FadeIn(area_labels[3]),
            # run_time=1.2,
        # )
        # self.wait(0.5)

        # # b · b = b^2
        # self.play(Create(arc_bb), run_time=0.8)
        # self.play(
            # Write(formula_one[15:]),
            # FadeIn(b_square),
            # FadeIn(area_labels[1]),
            # run_time=1.2,
        # )
        # self.wait(2.5)

        # # 4. Drugi način: štirje trikotniki in kvadrat c^2
        # triangle_vertices = [
            # [(0, 0), (A, 0), (0, B)],
            # [(S, 0), (A, 0), (S, A)],
            # [(S, S), (S, A), (B, S)],
            # [(0, S), (B, S), (0, B)],
        # ]
        # triangles = VGroup(
            # *[
                # Polygon(
                    # *[point(x, y) for x, y in vertices],
                    # color=COLOR_D,
                    # fill_color=COLOR_D,
                    # fill_opacity=0,  # pobarvajo se šele v rdečem koraku
                    # # Brez obrobe: stranice trikotnikov so že stranice velikega
                    # # kvadrata in zelene stranice c (rdeča črta bi prehitevala).
                    # stroke_width=0,
                # ).set_z_index(1)
                # for vertices in triangle_vertices
            # ]
        # )
        # inner_square = Polygon(
            # point(A, 0),
            # point(S, A),
            # point(B, S),
            # point(0, B),
            # color=COLOR_C,
            # fill_color=COLOR_C,
            # fill_opacity=0,  # notranjost se pobarva šele v zelenem koraku
            # stroke_width=7,  # odebeljene stranice c
        # ).set_z_index(2)

        # inner_center = inner_square.get_center()
        # hypotenuse_segments = [
            # (point(A, 0), point(0, B)),
            # (point(A, 0), point(S, A)),
            # (point(S, A), point(B, S)),
            # (point(B, S), point(0, B)),
        # ]
        # c_labels = VGroup()
        # for start, end in hypotenuse_segments:
            # # Oznake c so v notranjosti zelenega kvadrata, da se ne
            # # prekrivajo z zapisi ab/2 v trikotnikih.
            # midpoint = (start + end) / 2
            # inward = inner_center - midpoint
            # inward = inward / np.linalg.norm(inward)
            # c_labels.add(
                # MathTex("c", color=COLOR_C)
                # .scale(0.75)
                # .move_to(midpoint + inward * 0.26)
            # )
        # c_labels.set_z_index(6)
        # triangle_label_offsets = [LEFT * 0.12, DOWN * 0.12, RIGHT * 0.12, UP * 0.12]
        # area_labels_two = VGroup(
            # MathTex("c^2", color=COLOR_C, font_size=44).move_to(inner_center),
            # *[
                # MathTex(r"\frac{ab}{2}", color=COLOR_D, font_size=32).move_to(
                    # np.mean([point(*vertex) for vertex in vertices], axis=0)
                    # + offset
                # )
                # for vertices, offset in zip(
                    # triangle_vertices, triangle_label_offsets
                # )
            # ],
        # ).set_z_index(6)

        # title_four = heading("2. NAČIN:")
        # area_heading_four = (
            # centered_text(
                # "Izračunajmo ploščino\nkvadrata po delih.",
                # 42,
                # UL_GRAY,
                # bold=True,
            # )
            # .next_to(title_four, DOWN, buff=0.35)
            # .set_x(0)
        # )
        # formula_two = colored_math(
            # "P_2=",
            # "c^2",
            # "+",
            # r"4\cdot\frac{ab}{2}",
            # colors={1: COLOR_C, 3: COLOR_D},
            # font_size=52,
        # ).move_to(DOWN * 2.85)
        # area_note_c = VGroup(
            # MathTex("c^2", font_size=40, color=COLOR_C),
            # slovene_text("je ploščina srednjega kvadrata", 29, COLOR_C),
        # ).arrange(RIGHT, buff=0.15).move_to(DOWN * 3.95)
        # area_note_triangles = VGroup(
            # MathTex(r"4\cdot\frac{ab}{2}", font_size=40, color=COLOR_D),
            # slovene_text("je ploščina štirih trikotnikov", 29, COLOR_D),
        # ).arrange(RIGHT, buff=0.15).move_to(DOWN * 4.85)

        # # Najprej pospravimo 1. način, kratek premor, nato 2. način.
        # self.play(
            # FadeOut(area_labels),
            # FadeOut(formula_one),
            # FadeOut(expansion_arcs),
            # FadeOut(title),
            # FadeOut(area_heading),
            # FadeOut(area_pieces, shift=DOWN * 0.15),
            # run_time=1.0,
        # )
        # self.wait(1.2)
        # # Trikotniki nastanejo z izrisom zelenih stranic c (odebeljene in
        # # označene); njihova notranjost se pobarva šele v rdečem koraku.
        # self.add(triangles)
        # self.play(
            # FadeIn(title_four),
            # Create(inner_square),
            # FadeIn(c_labels, rate_func=squish_rate_func(smooth, 0.5, 1)),
            # run_time=2.0,
        # )
        # self.wait(0.3)
        # self.play(FadeIn(area_heading_four), run_time=0.9)
        # self.wait(0.5)
        # self.play(Write(formula_two[0]), run_time=0.8)
        # self.wait(0.3)

        # # Zeleno naenkrat: notranjost kvadrata, c^2, člen v formuli in zapis.
        # self.play(
            # inner_square.animate.set_fill(COLOR_C, opacity=0.34),
            # FadeIn(area_labels_two[0]),
            # Write(formula_two[1]),
            # FadeIn(area_note_c),
            # run_time=1.5,
        # )
        # self.wait(0.8)

        # # Rdeče naenkrat: trikotniki, ab/2, člen v formuli in zapis.
        # self.play(
            # triangles.animate.set_fill(COLOR_D, opacity=0.28),
            # FadeIn(area_labels_two[1:]),
            # Write(formula_two[2:]),
            # FadeIn(area_note_triangles),
            # run_time=1.5,
        # )
        # self.wait(3.0)

        # # 5. Izenačenje ploščin in poenostavitev
        # self.play(
            # FadeOut(
                # VGroup(
                    # title_four,
                    # outer_square,
                    # side_dimensions,
                    # side_length_labels,
                    # triangles,
                    # inner_square,
                    # c_labels,
                    # area_labels_two,
                    # area_heading_four,
                    # formula_two,
                    # area_note_c,
                    # area_note_triangles,
                # )
            # ),
            # run_time=0.8,
        # )
        # title_five = centered_text(
            # "ENAČIMO OBA IZRAZA\nZA PLOŠČINO",
            # 43,
            # UL_RED,
            # bold=True,
        # ).move_to(UP * 6.35)
        # self.play(Write(title_five), run_time=0.7)

        # equation_relation = colored_math(
            # "P_1",
            # "=",
            # "P_2",
            # colors={0: UL_GRAY, 2: UL_GRAY},
            # font_size=54,
        # ).move_to(UP * 3.45)
        # equation_one = colored_math(
            # "(",
            # "a",
            # "+",
            # "b",
            # ")^2",
            # "=",
            # "c^2",
            # "+",
            # r"4\cdot\frac{ab}{2}",
            # colors={1: COLOR_A, 3: COLOR_B, 6: COLOR_C, 8: COLOR_D},
            # font_size=44,
        # ).move_to(UP * 2.25)
        # equation_two = colored_math(
            # "a^2",
            # "+",
            # "2ab",
            # "+",
            # "b^2",
            # "=",
            # "c^2",
            # "+",
            # "2ab",
            # colors={
                # 0: COLOR_A,
                # 2: COLOR_D,
                # 4: COLOR_B,
                # 6: COLOR_C,
                # 8: COLOR_D,
            # },
            # font_size=50,
        # ).move_to(UP * 1.05)

        # self.play(Write(equation_relation), run_time=1.1)
        # self.wait(0.35)
        # self.play(Write(equation_one), run_time=1.6)
        # self.wait(0.35)
        # self.play(Write(equation_two), run_time=1.6)

        # subtract_note = slovene_text(
            # "Na obeh straneh odštejemo 2ab in dobimo:",
            # 32,
        # ).move_to(DOWN * 0.25)
        # self.play(FadeIn(subtract_note), run_time=0.6)
        # strike_left = Line(
            # equation_two[2].get_corner(DL) + DOWN * 0.04,
            # equation_two[2].get_corner(UR) + UP * 0.04,
            # color=UL_RED,
            # stroke_width=5,
        # ).set_z_index(8)
        # strike_right = Line(
            # equation_two[8].get_corner(DL) + DOWN * 0.04,
            # equation_two[8].get_corner(UR) + UP * 0.04,
            # color=UL_RED,
            # stroke_width=5,
        # ).set_z_index(8)
        # self.play(Create(strike_left), Create(strike_right), run_time=0.7)
        # self.wait(0.5)

        # result_formula = colored_math(
            # "a^2",
            # "+",
            # "b^2",
            # "=",
            # "c^2",
            # colors={0: COLOR_A, 2: COLOR_B, 4: COLOR_C},
            # font_size=76,
        # ).move_to(DOWN * 2.1)
        # result_frame = SurroundingRectangle(
            # result_formula,
            # color=UL_RED,
            # buff=0.25,
            # stroke_width=4,
        # )
        # self.play(Write(result_formula), run_time=1.5)
        # self.play(Create(result_frame), run_time=0.5)
        # self.wait(2)

        # # 6. Sklep
        # self.play(
            # FadeOut(
                # VGroup(
                    # title_five,
                    # equation_relation,
                    # equation_one,
                    # equation_two,
                    # subtract_note,
                    # strike_left,
                    # strike_right,
                # )
            # ),
            # run_time=0.8,
        # )
        # title_six = centered_text(
            # "DOKAZALI SMO\nPITAGOROV IZREK!",
            # 49,
            # UL_RED,
            # bold=True,
        # ).move_to(UP * 5.35)
        # final_triangle = final_triangle_template.move_to(UP * 1.2)
        # smile = VGroup(
            # Arc(
                # start_angle=PI,
                # angle=PI,
                # radius=0.65,
                # color=UL_GRAY,
                # stroke_width=5,
            # ).move_to(DOWN * 4.1),
            # Dot(LEFT * 0.3 + DOWN * 3.25, color=UL_GRAY, radius=0.06),
            # Dot(RIGHT * 0.3 + DOWN * 3.25, color=UL_GRAY, radius=0.06),
        # ).set_z_index(8)
        # self.play(
            # Write(title_six),
            # FadeIn(final_triangle),
            # run_time=1.5,
        # )
        # self.play(FadeIn(smile), run_time=0.8)
        # self.wait(6)


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