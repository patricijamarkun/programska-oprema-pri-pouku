from pathlib import Path
import warnings

import numpy as np
from manim import *
from manimpango import list_fonts


config.pixel_width = 1080
config.pixel_height = 1920
config.frame_width = 9
config.frame_height = 16
config.background_color = "#FFFFFF"


UL_RED = "#E03127"
UL_GRAY = "#58595B"
UL_LIGHT_GRAY = "#E6E7E8"
COLOR_A = "#2878AC"
COLOR_B = "#F25E24"
COLOR_C = "#00694E"
COLOR_AB = UL_RED

_installed_fonts = {font.casefold() for font in list_fonts()}
if "univerza sans" in _installed_fonts:
    FONT_NAME = "Univerza Sans"
else:
    FONT_NAME = "Arial"
    warnings.warn(
        "Univerza Sans is not installed; using Arial, the official UL fallback.",
        RuntimeWarning,
        stacklevel=2,
    )

LOGO_PATH = Path(__file__).parent / "assets" / "ul_fmf_logo.png"

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
    return Text(
        text,
        font=FONT_NAME,
        font_size=font_size,
        color=color,
        weight=BOLD if bold else NORMAL,
        line_spacing=1.05,
    )


def colored_math(
    *parts: str,
    colors: dict[int, str],
    font_size: int,
    max_width: float = 8.2,
) -> MathTex:
    formula = MathTex(*parts, font_size=font_size, color=UL_GRAY)
    for index, color in colors.items():
        formula[index].set_color(color)
    if formula.width > max_width:
        formula.scale_to_fit_width(max_width)
    return formula


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
            bottom_a = Line(
                point(0, 0) + DOWN * 0.12,
                point(A, 0) + DOWN * 0.12,
                color=COLOR_A,
                stroke_width=6,
            )
            bottom_b = Line(
                point(A, 0) + DOWN * 0.12,
                point(S, 0) + DOWN * 0.12,
                color=COLOR_B,
                stroke_width=6,
            )
            right_a = Line(
                point(S, 0) + RIGHT * 0.12,
                point(S, A) + RIGHT * 0.12,
                color=COLOR_A,
                stroke_width=6,
            )
            right_b = Line(
                point(S, A) + RIGHT * 0.12,
                point(S, S) + RIGHT * 0.12,
                color=COLOR_B,
                stroke_width=6,
            )

            labels = VGroup(
                MathTex("a", color=COLOR_A).scale(0.7).next_to(
                    bottom_a, DOWN, buff=0.04
                ),
                MathTex("b", color=COLOR_B).scale(0.7).next_to(
                    bottom_b, DOWN, buff=0.04
                ),
                MathTex("a", color=COLOR_A).scale(0.7).next_to(
                    right_a, RIGHT, buff=0.05
                ),
                MathTex("b", color=COLOR_B).scale(0.7).next_to(
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
        ).move_to(UP * 6.35)

        a_point = LEFT * 1.55 + DOWN * 0.1
        b_point = RIGHT * 1.55 + DOWN * 0.1
        c_point = LEFT * 1.55 + UP * 2.45
        triangle_fill = Polygon(
            a_point,
            b_point,
            c_point,
            stroke_opacity=0,
            fill_color=UL_LIGHT_GRAY,
            fill_opacity=0.75,
        )
        side_a = Line(a_point, b_point, color=COLOR_A, stroke_width=8)
        side_b = Line(a_point, c_point, color=COLOR_B, stroke_width=8)
        side_c = Line(b_point, c_point, color=COLOR_C, stroke_width=8)
        right_angle = RightAngle(
            Line(a_point, b_point),
            Line(a_point, c_point),
            length=0.28,
            color=UL_GRAY,
        )

        label_a = MathTex("a", color=COLOR_A).scale(0.95).next_to(
            Line(a_point, b_point), DOWN, buff=0.12
        )
        label_b = MathTex("b", color=COLOR_B).scale(0.95).next_to(
            Line(a_point, c_point), LEFT, buff=0.12
        )
        label_c = MathTex("c", color=COLOR_C).scale(0.95).move_to(
            (b_point + c_point) / 2 + RIGHT * 0.22 + UP * 0.08
        )
        triangle_labels = VGroup(label_a, label_b, label_c)

        question = slovene_text(
            "Zakaj velja Pitagorov izrek?",
            38,
            UL_GRAY,
            bold=True,
        ).move_to(DOWN * 1.8)
        opening_formula = colored_math(
            "a^2",
            "+",
            "b^2",
            "=",
            "c^2",
            colors={0: COLOR_A, 2: COLOR_B, 4: COLOR_C},
            font_size=76,
        ).move_to(DOWN * 3.25)

        self.play(Write(title), run_time=1.2)
        self.play(
            FadeIn(triangle_fill),
            Create(side_a),
            Create(side_b),
            Create(side_c),
            run_time=1.6,
        )
        self.play(
            FadeIn(right_angle),
            Write(triangle_labels),
            run_time=0.9,
        )
        self.play(FadeIn(question), run_time=0.8)
        self.play(Write(opening_formula), run_time=1.2)
        self.wait(2.2)

        # 2. Kvadrat s stranico a + b
        self.play(
            FadeOut(
                VGroup(
                    title,
                    triangle_fill,
                    side_a,
                    side_b,
                    side_c,
                    right_angle,
                    triangle_labels,
                    question,
                    opening_formula,
                )
            ),
            run_time=0.8,
        )

        title = heading("KVADRAT S STRANICO a + b")
        outer_square = Square(
            side_length=S * DIAGRAM_SCALE,
            color=UL_GRAY,
            stroke_width=4,
        ).move_to(DIAGRAM_CENTER).set_z_index(4)
        side_dimensions = dimensions().set_z_index(5)
        total_side = MathTex("a+b", color=UL_GRAY).scale(0.9).move_to(
            point(S / 2, S) + UP * 0.25
        )
        explanation = slovene_text(
            "Njegovo ploščino bomo izračunali na dva načina.",
            32,
        ).move_to(DOWN * 3.55)

        self.play(Write(title), Create(outer_square), run_time=1.5)
        self.play(FadeIn(side_dimensions), Write(total_side), run_time=0.8)
        self.play(FadeIn(explanation), run_time=0.6)
        self.wait(2)

        # 3. Prvi način: kvadrati in pravokotnika
        self.play(
            FadeOut(total_side),
            FadeOut(explanation),
            FadeOut(title),
            run_time=0.6,
        )
        title = heading("1. NAČIN IZRAČUNA")
        a_square = tile(0, 0, A, A, COLOR_A)
        b_square = tile(A, A, B, B, COLOR_B)
        ab_rectangle_1 = tile(A, 0, B, A, COLOR_AB)
        ab_rectangle_2 = tile(0, A, A, B, COLOR_AB)
        area_pieces = VGroup(
            a_square,
            b_square,
            ab_rectangle_1,
            ab_rectangle_2,
        )
        area_labels = VGroup(
            MathTex("a^2", color=COLOR_A, font_size=48).move_to(point(A / 2, A / 2)),
            MathTex("b^2", color=COLOR_B, font_size=44).move_to(
                point(A + B / 2, A + B / 2)
            ),
            MathTex("ab", color=COLOR_AB, font_size=44).move_to(
                point(A + B / 2, A / 2)
            ),
            MathTex("ab", color=COLOR_AB, font_size=44).move_to(
                point(A / 2, A + B / 2)
            ),
        ).set_z_index(6)

        formula_one = colored_math(
            "P_1=",
            "(a+b)^2",
            "=",
            "a^2",
            "+",
            "2ab",
            "+",
            "b^2",
            colors={
                3: COLOR_A,
                5: COLOR_AB,
                7: COLOR_B,
            },
            font_size=48,
        ).move_to(DOWN * 2.45)

        self.play(Write(title), run_time=0.7)
        self.play(
            LaggedStart(
                *[FadeIn(piece) for piece in area_pieces],
                lag_ratio=0.16,
            ),
            run_time=1.8,
        )
        self.play(LaggedStart(*[Write(label) for label in area_labels]), run_time=1)
        self.play(Write(formula_one), run_time=1.5)
        self.wait(3)

        # 4. Drugi način: štirje trikotniki in kvadrat c^2
        triangle_vertices = [
            [(0, 0), (A, 0), (0, B)],
            [(S, 0), (A, 0), (S, A)],
            [(S, S), (S, A), (B, S)],
            [(0, S), (B, S), (0, B)],
        ]
        triangles = VGroup(
            *[
                Polygon(
                    *[point(x, y) for x, y in vertices],
                    color=COLOR_AB,
                    fill_color=COLOR_AB,
                    fill_opacity=0.28,
                    stroke_width=3,
                ).set_z_index(1)
                for vertices in triangle_vertices
            ]
        )
        inner_square = Polygon(
            point(A, 0),
            point(S, A),
            point(B, S),
            point(0, B),
            color=COLOR_C,
            fill_color=COLOR_C,
            fill_opacity=0.34,
            stroke_width=4,
        ).set_z_index(2)

        inner_center = inner_square.get_center()
        hypotenuse_segments = [
            (point(A, 0), point(0, B)),
            (point(A, 0), point(S, A)),
            (point(S, A), point(B, S)),
            (point(B, S), point(0, B)),
        ]
        c_labels = VGroup()
        for start, end in hypotenuse_segments:
            midpoint = (start + end) / 2
            outward = midpoint - inner_center
            outward = outward / np.linalg.norm(outward)
            c_labels.add(
                MathTex("c", color=COLOR_C)
                .scale(0.68)
                .move_to(midpoint + outward * 0.2)
            )
        c_labels.set_z_index(6)

        title_four = heading("2. NAČIN IZRAČUNA")
        formula_two = colored_math(
            "P_2=",
            "c^2",
            "+",
            r"4\cdot\frac{ab}{2}",
            colors={1: COLOR_C, 3: COLOR_AB},
            font_size=52,
        ).move_to(DOWN * 2.35)
        area_note_c = slovene_text(
            "c² je ploščina srednjega kvadrata",
            29,
            COLOR_C,
        ).move_to(DOWN * 3.35)
        area_note_triangles = slovene_text(
            "4 · ab/2 je ploščina štirih trikotnikov",
            29,
            COLOR_AB,
        ).move_to(DOWN * 4.05)

        self.play(
            FadeOut(area_labels),
            FadeOut(formula_one),
            FadeOut(title),
            FadeIn(title_four),
            ReplacementTransform(area_pieces, triangles),
            FadeIn(inner_square),
            run_time=3,
        )
        self.play(FadeIn(c_labels), Write(formula_two), run_time=1.6)
        self.play(FadeIn(area_note_c), FadeIn(area_note_triangles), run_time=0.8)
        self.wait(3.2)

        # 5. Izenačenje ploščin in poenostavitev
        self.play(
            FadeOut(
                VGroup(
                    title_four,
                    outer_square,
                    side_dimensions,
                    triangles,
                    inner_square,
                    c_labels,
                    formula_two,
                    area_note_c,
                    area_note_triangles,
                )
            ),
            run_time=0.8,
        )
        title_five = slovene_text(
            "ENAČIMO OBA IZRAZA\nZA PLOŠČINO",
            43,
            UL_RED,
            bold=True,
        ).move_to(UP * 6.35)
        self.play(Write(title_five), run_time=0.7)

        equation_one = colored_math(
            "(",
            "a",
            "+",
            "b",
            ")(",
            "a",
            "+",
            "b",
            ")",
            "=",
            "c^2",
            "+",
            r"4\cdot\frac{ab}{2}",
            colors={
                1: COLOR_A,
                3: COLOR_B,
                5: COLOR_A,
                7: COLOR_B,
                10: COLOR_C,
                12: COLOR_AB,
            },
            font_size=46,
        ).move_to(UP * 2.1)
        equation_two = colored_math(
            "a^2",
            "+",
            "2ab",
            "+",
            "b^2",
            "=",
            "c^2",
            "+",
            "2ab",
            colors={
                0: COLOR_A,
                2: COLOR_AB,
                4: COLOR_B,
                6: COLOR_C,
                8: COLOR_AB,
            },
            font_size=54,
        ).move_to(UP * 1.55)

        self.play(Write(equation_one), run_time=1.8)
        self.wait(1.2)
        self.play(TransformMatchingTex(equation_one, equation_two), run_time=2)

        subtract_note = slovene_text(
            "Od obeh strani odštejemo 2ab.",
            32,
        ).move_to(DOWN * 0.15)
        self.play(FadeIn(subtract_note), run_time=0.6)
        strike_left = Line(
            equation_two[2].get_corner(DL) + DOWN * 0.04,
            equation_two[2].get_corner(UR) + UP * 0.04,
            color=UL_RED,
            stroke_width=5,
        ).set_z_index(8)
        strike_right = Line(
            equation_two[8].get_corner(DL) + DOWN * 0.04,
            equation_two[8].get_corner(UR) + UP * 0.04,
            color=UL_RED,
            stroke_width=5,
        ).set_z_index(8)
        self.play(Create(strike_left), Create(strike_right), run_time=0.7)
        self.wait(0.8)

        result_formula = colored_math(
            "a^2",
            "+",
            "b^2",
            "=",
            "c^2",
            colors={0: COLOR_A, 2: COLOR_B, 4: COLOR_C},
            font_size=76,
        ).move_to(DOWN * 2.3)
        result_frame = SurroundingRectangle(
            result_formula,
            color=UL_RED,
            buff=0.25,
            stroke_width=4,
        )
        self.play(
            FadeOut(equation_two),
            FadeOut(strike_left),
            FadeOut(strike_right),
            FadeOut(subtract_note),
            Write(result_formula),
            run_time=1.5,
        )
        self.play(Create(result_frame), run_time=0.5)
        self.wait(2)

        # 6. Sklep
        self.play(
            FadeOut(VGroup(title_five, result_formula, result_frame)),
            run_time=0.8,
        )
        title_six = slovene_text(
            "DOKAZALI SMO\nPITAGOROV IZREK",
            49,
            UL_RED,
            bold=True,
        ).move_to(UP * 4.2)
        final_formula = colored_math(
            "a^2",
            "+",
            "b^2",
            "=",
            "c^2",
            colors={0: COLOR_A, 2: COLOR_B, 4: COLOR_C},
            font_size=88,
        ).move_to(UP * 0.8)
        final_frame = SurroundingRectangle(
            final_formula,
            color=UL_RED,
            buff=0.3,
            stroke_width=4,
        )
        smile = VGroup(
            Arc(
                start_angle=PI,
                angle=PI,
                radius=0.65,
                color=UL_GRAY,
                stroke_width=5,
            ).move_to(DOWN * 2.1),
            Dot(LEFT * 0.3 + DOWN * 1.25, color=UL_GRAY, radius=0.06),
            Dot(RIGHT * 0.3 + DOWN * 1.25, color=UL_GRAY, radius=0.06),
        )
        self.play(Write(title_six), run_time=1.2)
        self.play(Write(final_formula), run_time=1.4)
        self.play(Create(final_frame), run_time=0.5)
        self.play(FadeIn(smile), run_time=0.8)
        self.wait(3.2)

        # 7. Zaključni logotip FMF
        self.play(
            FadeOut(VGroup(title_six, final_formula, final_frame, smile)),
            run_time=1,
        )
        if not LOGO_PATH.is_file():
            raise FileNotFoundError(f"FMF logo image is missing: {LOGO_PATH}")
        logo = ImageMobject(str(LOGO_PATH)).scale_to_fit_width(7.2)
        logo.move_to(ORIGIN)
        self.play(FadeIn(logo), run_time=1.5)
        self.wait(4)


if __name__ == "__main__":
    PitagorovIzrek().render()