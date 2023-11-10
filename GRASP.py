from manim import *
import random

config.max_files_cached = 1_000

problem = {
    "DOTS_mobject": [],
    "DOTS_coord": [],
    "DOTS_visited": [],
    "EDGES": [],
    "EDGES_main_mobject": [],
    "EDGES_tmp_mobject": [],
    "DISTANCES_mobjects": []
}


VISITING_DOT_COLOR = RED
VISITED_DOT_COLOR = GREY
DEFAULT_DOT_COLOR = WHITE
SELECTED_DOT_COLOR = ORANGE

MAIN_LINE_COLOR = GREY
EXPLORING_LINE_COLOR = BLUE


"""CODE: Initializes the dict with all the info for the problem"""
def build_problem(self):
    random.seed(2)
    N_POINTS = 20
    for _ in range(N_POINTS):
        x,y = random.uniform(-7, 7), random.uniform(-3, 3)
        problem["DOTS_mobject"].append(Dot(point=[x, y, 0.0], color=DEFAULT_DOT_COLOR))
        problem["DOTS_coord"].append((x,y))


"""ANIMATION: draws the problem on the screen"""
def display_problem(self, title=None):
    # Remove the title
    if title is not None:
        self.play(FadeOut(title))

    # Create the Dots
    self.play(
        LaggedStart(
            *[Create(d) for d in problem["DOTS_mobject"]],
            *[Create(e) for e in problem["EDGES_main_mobject"]],
            *[Create(e) for e in problem["EDGES_tmp_mobject"]]
            lag_ratio = 0.1
        )
    )

    self.wait()

get_huge_black_rectangle = lambda : Rectangle(height=100, width=100, color=BLACK, fill_color=BLACK, fill_opacity=1)

LINE_HEIGHT = 0.5
get_rectangle_while = lambda : Rectangle(height=LINE_HEIGHT, width=4.8).move_to(2.15*LEFT + 0.875*UP)
get_rectangle_construct = lambda : Rectangle(height=LINE_HEIGHT, width=5.4).move_to(1.14*LEFT + 0.425*UP)
get_rectangle_whole_if_feasible = lambda : Rectangle(height=LINE_HEIGHT*2 - 0.1, width=5.45).move_to(0.175*DOWN + 1.15*LEFT)
get_rectangle_local_search = lambda : Rectangle(height=LINE_HEIGHT, width=5.8).move_to(0.8*DOWN + 0.95*LEFT)


"""ANIMATION: Shows the code and draws a rectangle around the construction invocation"""
def show_code_grasp_focus_construct(s):
    rect = get_rectangle_construct()
    code_img = ImageMobject("my_media//construction_code_snippet_v2.png")

    # Show the code
    img, huge_rect = show_code_grasp(self, rect)
    self.wait()

    # Show specific implementation for helper function
    self.play(
        FadeOut(img), 
        FadeOut(rect), 
        FadeIn(code_img)
    )
    self.wait()

    # Scale and move the code
    self.play(
        FadeOut(huge_rect),
        code_img.animate.become(ImageMobject("my_media//construction_code_snippet_v2.png").scale(1/2).shift(UP*2 + LEFT*5))
    )
    self.wait()

    return code_img
    

"""ANIMATION: Shows the code and draws a rectangle around the local search invocation"""
def show_code_grasp_focus_search(s):

    rect = get_rectangle_local_search()
    code_img = ImageMobject("my_media//search_code_snippet_v3.png")

    # Show the code
    img, huge_rect = show_code_grasp(self, rect)
    self.wait()

    #Show specific implementation for helper function
    self.play(
        FadeOut(img), 
        FadeOut(rect), 
        FadeIn(code_img)
    )
    self.wait()

    # TODO: show first vs best approach
    code_img.become(ImageMobject("my_media//search_code_snippet_v2.png"))

    # Scale and move the code
    self.play(
        FadeOut(huge_rect),
        code_img.animate.become(ImageMobject("my_media//search_code_snippet_v4.png").scale(1/2).shift(UP*2 + LEFT*5))
    )
    self.wait()

    return code_img


"""ANIMATION: Shows the code and draws a rectangle around the is_feasible snippet"""
def show_code_grasp_focus_feasible():
    rect = get_rectangle_whole_if_feasible()

    # Show the code
    img, huge_rect = show_code_grasp(self, rect)
    self.wait()

    # Remove the code and others
    self.play(
        FadeOut(huge_rect), 
        FadeOut(img), 
        FadeOut(rect)
    )


"""ANIMATION: Given the shown GRASP code it uses rectangles to focus on specific parts of the code"""
def explain_code_grasp(self):
    image, rect = show_code_grasp(self)

    # Remove image and rectangle
    self.play(FadeOut(image), FadeOut(rect))


"""ANIMATION: Shows the code for GRASP"""
def show_code_grasp(self, additional_mobjects=[]):
    rect = get_huge_black_rectangle()
    DOWN_SHIFT = 0
    image = ImageMobject("my_media//GRASP_code_snippet_v4.png").shift(DOWN_SHIFT * DOWN)

    self.play(
        FadeIn(rect),
        FadeIn(image),
        *[FadeIn(o) for o in additional_mobjects]    
    )

    self.wait()

    # Return the image so it can removed afterwards
    return image, rect


"""ANIMATION: Tries all p posible values to explain how its value affects the
behaviour of the greedy-randomized approach"""
def explain_p(self):
    DISTANCES = get_distances()
    MIN_P, MAX_P = 1, len(DISTANCES.values())
    MIN_C, MAX_C = min(DISTANCES.values()), max(DISTANCES.values())

    p = ValueTracker(5)

    box = Rectangle(width=4, height=5, fill_color=BLACK, fill_opacity=1).move_to([-5, 1, 0])

    # Order the costs
    next_to_mobjects = {
        dot: i
        for (i,dot) in enumerate(problem["DOTS_mobject"])
        if i not in problem["DOTS_visited"]
    }

    for (i,key) in enumerate(next_to_mobjects.keys()):
        next_to_mobjects[key] = problem["DISTANCES_mobjects"][i]

    dist_text = {
        distance: problem["DISTANCES_mobjects"][i]
        for (i,distance) in enumerate(DISTANCES.values())
    }

    SHIFT_DOWN = 0.25 * DOWN
    ORIGINAL_POSITION = LEFT*5 + UP*3.25

    for t in problem["DISTANCES_mobjects"]:
        t.set_z_index(box.z_index + 2)

    x_start_line, x_end_line = LEFT*5.5, LEFT*4.5
    get_line = lambda : Line(
        x_start_line + UP*3.25 + SHIFT_DOWN*int(p.get_value()) - SHIFT_DOWN*0.5,
        x_end_line + UP*3.25 + SHIFT_DOWN*int(p.get_value()) - SHIFT_DOWN*0.5,
        z_index = box.z_index + 1
    )
    line = get_line()

    get_text = lambda : Text(f"{int(p.get_value())}").scale(1/3).next_to(line, RIGHT)
    text = get_text()

    self.play(
        FadeIn(box),
        *[
            dist_text[distance].animate.move_to(ORIGINAL_POSITION + SHIFT_DOWN*i).scale(3/4)
            for (i,distance) in enumerate(sorted(dist_text.keys()))
        ]
    )

    self.wait()

    the_dots_1 = [problem["DOTS_mobject"][i] for (i,dist) in DISTANCES.items() if sorted(DISTANCES.values()).index(dist)+1 > int(p.get_value())]
    the_dots_2 = [problem["DOTS_mobject"][i] for (i,dist) in DISTANCES.items() if sorted(DISTANCES.values()).index(dist)+1 <=  int(p.get_value())]

    self.play(
        Create(line),
        Create(text),
        *[FadeToColor(d, DEFAULT_DOT_COLOR) for d in the_dots_1],
        *[FadeToColor(d, SELECTED_DOT_COLOR) for d in the_dots_2]
    )

    def line_updater(line):
        line.become(get_line())
        text.become(get_text())

    for (i,dist) in DISTANCES.items():
        def the_updater(x, dist=dist):
            x.set_color(DEFAULT_DOT_COLOR if (sorted(DISTANCES.values()).index(dist)+1 > int(p.get_value())) else SELECTED_DOT_COLOR)
        problem["DOTS_mobject"][i].add_updater(the_updater)
    
    line.add_updater(line_updater)
    text.add_updater(lambda z: z.become(get_text()))

    self.wait()

    # To min
    self.play(p.animate.set_value(MIN_P), run_time=2)
    self.wait()

    # To max
    self.play(p.animate.set_value(MAX_P), run_time=2)
    self.wait()

    # To medium
    self.play(p.animate.set_value(5), run_time=2)
    self.wait()

    line.clear_updaters()
    text.clear_updaters()

    for (i,dist) in DISTANCES.items():
        problem["DOTS_mobject"][i].clear_updaters()

    # Return distantes to original position and DOTS to original color
    self.play(
        *[distance.animate.next_to(dot, RIGHT).scale(4/3) for (dot,distance) in next_to_mobjects.items()],
        FadeOut(line),
        FadeOut(text),
        *[FadeToColor(problem["DOTS_mobject"][i], color=SELECTED_DOT_COLOR) for i in DISTANCES.keys()],
    )

    return box


"""ANIMATION: Explains how to create the RCL"""
def explain_restricted_candidate_list(self):
    # Explain p
    box = explain_p(self)
    self.wait()

    # Explain alpha
    explain_alpha(self, box)


"""ANIMATION: Tries all alpha posible p to explain how its value affects the
behaviour of the greedy-randomized approach"""
def explain_alpha(self, box):
    MIN_ALPHA, MAX_ALPHA = 0, 1
    DISTANCES = get_distances()
    MIN_C, MAX_C = min(DISTANCES.values()), max(DISTANCES.values())

    # Alpha value to be changed
    alpha = ValueTracker(0.5)

    # Rectangle to used as a box containing all the info
    new_box = Rectangle(width=4, height=3, fill_color=BLACK, fill_opacity=1).move_to([-5, 2, 0])
    

    # Initial explanation for alpha
    raw_formula_text = Paragraph(r"[c_min ,", r"c_min + α*(c_max - c_min)]").shift(5*LEFT+2.75*UP).scale(2/5)
    alpha_range = Text(r"0 ≤ α ≤ 1").shift(5*LEFT+1.25*UP).scale(1/2)
    self.play(
        box.animate.become(new_box),
        FadeIn(raw_formula_text),
        FadeIn(alpha_range))
    self.wait()


    get_text = lambda : Text(f"[{MIN_C:.2f}, {(MIN_C+alpha.get_value()*(MAX_C-MIN_C)):.2f}]").shift(5*LEFT+2.75*UP).scale(1/2)
    # The text showing the MIN and MAX values allowed within the range
    range_text = get_text()
    
    x_start_line, x_end_line, y_line = -6.5, -3.5, 1.5
    # The line that will be traveled by the Dot
    line = Line((x_start_line, y_line, 0), (x_end_line, y_line, 0))

    get_dot = lambda : Dot(point=((x_start_line + alpha.get_value()*(x_end_line-x_start_line)), y_line, 0))
    # Dot to visually see where the alpha is located
    dot = get_dot()
    
    get_lambda_text = lambda : Text(f"{(alpha.get_value()):.2f}").scale(1/2).next_to(dot, DOWN)
    # Text displaying the value of alpha
    alpha_text = get_lambda_text()

    # All the objects to be displayed
    objects = [range_text, alpha_text, dot, line]
    self.play(
        *[FadeIn(o) for o in objects if o is not range_text],
        ReplacementTransform(raw_formula_text, range_text),
        *[
            FadeToColor(problem["DOTS_mobject"][i], color=SELECTED_DOT_COLOR)
            for i in DISTANCES.keys()
            if (DISTANCES[i] <= (MIN_C+alpha.get_value()*(MAX_C-MIN_C)))
        ],
        FadeOut(alpha_range)
    )

    self.wait()

    for (i,d) in DISTANCES.items():
        # Update the colors of the points if they can be included in RCL
        def the_updater(x, i=i):
            x.set_color(DEFAULT_DOT_COLOR if (DISTANCES[i] > (MIN_C+alpha.get_value()*(MAX_C-MIN_C))) else SELECTED_DOT_COLOR)
        problem["DOTS_mobject"][i].add_updater(the_updater)

    def update_lambda(point):
        point.become(get_dot())
        alpha_text.become(get_lambda_text())
    
    dot.add_updater(update_lambda)
    range_text.add_updater(lambda z: z.become(get_text()))

    # From center to MAX
    self.play(alpha.animate.set_value(MAX_ALPHA), run_time=2)
    self.wait()

    # From MAX to MIN
    self.play(alpha.animate.set_value(MIN_ALPHA), run_time=2)
    self.wait()

    # From MIN to center
    self.play(alpha.animate.set_value(0.5), run_time=2)
    self.wait()

    for i in DISTANCES.keys():
        problem["DOTS_mobject"][i].clear_updaters()
    
    range_text.clear_updaters()
    dot.clear_updaters()
    alpha_text.clear_updaters()

    # Restore view to match previous
    objects = [range_text, alpha_text, line, dot]
    self.play(
        *[FadeOut(o) for o in objects],
        FadeOut(box),
        FadeOut(new_box),
        *[FadeToColor(problem["DOTS_mobject"][i], color=SELECTED_DOT_COLOR) for i in DISTANCES.keys()],
    )

    self.wait()


"""CODE: Calculates the distance from the last visited point to all non-visited points"""
def get_distances():
    last_x, last_y = problem["DOTS_coord"][ problem["DOTS_visited"][-1] ]

    return {
        i: (abs(p_x-last_x)**2 + abs(p_y - last_y)**2)**(1/2)
        for (i,(p_x, p_y)) in enumerate(problem["DOTS_coord"])
        if i not in problem["DOTS_visited"]
    }


"""CODE: Calculates the RCL given a list of distances and alpha value"""
def get_restricted_candidate_list(distances, alpha):
    max_distance, min_distance = max(distances.values()), min(distances.values())

    return {
        i: distance
        for (i,distance) in distances.items()
        if distance>=min_distance  and  distance<=(min_distance + alpha*(max_distance-min_distance))
    }


"""ANIMATION & CODE: greedy-randomized construction of a solution.
Shows the process and updates the dict"""
def construct_initial_solution(self, img_code):
    alpha = 0.2

    random.seed(0)

    # Choose initial point and modify list
    index = random.randint(0, len(problem["DOTS_mobject"]))
    problem["DOTS_visited"].append(index)

    pos_solution = LEFT*6.6 + UP*2.825
    pos_get_cand_1 = LEFT*6.6 + UP*2.67
    pos_while = LEFT*6.6 + UP*2.4
    pos_costs = LEFT*6.6 + UP*2.25
    pos_RCL = LEFT*6.6 + UP*1.8
    pos_random = LEFT*6.6 + UP*1.65
    pos_append = LEFT*6.6 + UP*1.5
    pos_get_cand_2 = LEFT*6.6 + UP*1.355
    pos_return = LEFT*6.6 + UP*1.08

    arrow = Arrow(start=pos_solution, end=pos_solution+RIGHT).scale(1/2).move_to(pos_solution)

    # Change color of the point
    self.play(
        FadeToColor(problem["DOTS_mobject"][index], color=VISITING_DOT_COLOR),
        Create(arrow)
    )
    self.wait()

    NUM_STEP_BY_STEP = 2

    # Repeat until all points have been visited
    while len(problem["DOTS_visited"]) != len(problem["DOTS_mobject"]):
        # Move arrow and color candidates
        if len(problem["DOTS_visited"]) <= NUM_STEP_BY_STEP:
            self.play(
                arrow.animate.move_to(pos_get_cand_1 if len(problem["DOTS_visited"])==1 else pos_get_cand_2),
                *[FadeToColor(p, SELECTED_DOT_COLOR) for (i,p) in enumerate(problem["DOTS_mobject"]) if i not in problem["DOTS_visited"]]
            )
            self.wait()
        elif len(problem["DOTS_visited"]) == NUM_STEP_BY_STEP+1:
            self.play(arrow.animate.move_to(pos_while))
            self.wait()

        last_x, last_y = problem["DOTS_coord"][ problem["DOTS_visited"][-1] ]

        # Evaluate all remaining points
        distances = get_distances()
        if len(problem["DOTS_visited"]) <= NUM_STEP_BY_STEP:
            distances_text = [
                Text(f"{distances[i]:.2f}").next_to(dot, RIGHT).scale(1/2.5).shift(LEFT*0.5)
                for (i,dot) in enumerate(problem["DOTS_mobject"])
                if i not in problem["DOTS_visited"]
            ]
            problem["DISTANCES_mobjects"].extend(distances_text)
            self.play(
                arrow.animate.move_to(pos_costs),
                *[FadeIn(t) for t in distances_text]
            )
            self.wait()

        if len(problem["DOTS_visited"]) == 1:
            self.play(
                arrow.animate.move_to(pos_RCL),
            )
            self.wait()
            # Pause to explain the RCL
            explain_restricted_candidate_list(self)

        # Filter out the worst ones
        restricted_candidate_list = get_restricted_candidate_list(distances, alpha)

        # Animation to show restricted candidate_list
        if len(problem["DOTS_visited"]) <= NUM_STEP_BY_STEP:
            the_dots_1 = [d for (i,d) in enumerate(problem["DOTS_mobject"]) if i not in problem["DOTS_visited"] and i not in restricted_candidate_list.keys()]
            the_dots_2 = [d for (i,d) in enumerate(problem["DOTS_mobject"]) if i not in problem["DOTS_visited"] and i in restricted_candidate_list.keys()]
            self.play(
                *[FadeToColor(d, color=DEFAULT_DOT_COLOR) for d in the_dots_1],
                *[FadeToColor(d, color=SELECTED_DOT_COLOR) for d in the_dots_2],
                arrow.animate.move_to(pos_RCL),
                *[FadeOut(t) for t in distances_text]
            )
            self.wait()
        
        problem["DISTANCES_mobjects"].clear()

        # Choose next point randomly
        index = random.choice(list(restricted_candidate_list.keys()))
        if len(problem["DOTS_visited"]) <= NUM_STEP_BY_STEP:
            the_dots = [d for (i,d) in enumerate(problem["DOTS_mobject"]) if i in restricted_candidate_list.keys()]
            self.play(
                *[FadeToColor(d, color=DEFAULT_DOT_COLOR) for d in the_dots if d is not problem["DOTS_mobject"][index]],
                arrow.animate.move_to(pos_random)
            )
            self.wait()

        # Animations for visiting
        new_x, new_y = problem["DOTS_coord"][index]
        line = Line([last_x, last_y, 0], [new_x, new_y, 0], color=MAIN_LINE_COLOR)
        if len(problem["DOTS_visited"]) <= NUM_STEP_BY_STEP:
            self.play(
                FadeToColor(problem["DOTS_mobject"][problem["DOTS_visited"][-1]], color=VISITED_DOT_COLOR),
                FadeToColor(problem["DOTS_mobject"][index], color=VISITING_DOT_COLOR),
                Create(line),
                arrow.animate.move_to(pos_append),
                run_time = 1
            )
            self.wait()
        else:
            self.play(
                FadeToColor(problem["DOTS_mobject"][problem["DOTS_visited"][-1]], color=VISITED_DOT_COLOR),
                FadeToColor(problem["DOTS_mobject"][index], color=VISITING_DOT_COLOR),
                Create(line),
                run_time = 1/3
            )

        problem["EDGES_main_mobject"].append(line)
        problem["DOTS_visited"].append(index)

    # Go back to initial position
    last_x, last_y = problem["DOTS_coord"][ problem["DOTS_visited"][-1] ]
    new_x, new_y = problem["DOTS_coord"][ problem["DOTS_visited"][0] ]
    line = Line([last_x, last_y, 0], [new_x, new_y, 0], color=MAIN_LINE_COLOR)
    self.play(
        FadeToColor(problem["DOTS_mobject"][problem["DOTS_visited"][-1]], color=VISITED_DOT_COLOR),
        Create(line),
        arrow.animate.move_to(pos_return)
    )
    problem["EDGES_main_mobject"].append(line)

    self.wait()

    # Remove code
    self.play(FadeOut(arrow), FadeOut(img_code))
    self.wait()


"""ANIMATION: Shows the title to do the introduction"""
def show_introduction(self):
    group_name = Paragraph("Grupo 1", "\tDavid González Fernández", "\tSergio Arroni del Riego", "\tJosé Manuel Lamas Pérez").scale(2/5).shift(DOWN*3)

    title_whole_name = Paragraph("Greedy", "Randomized", "Adaptive", "Search", "Procedure").shift(UP*0.5)
    self.add(title_whole_name, group_name)
    self.wait()

    title_GRASP = Text("GRASP").shift(UP*2)

    details_text = Paragraph("• Multicomienzo", "\n• Optimización combinatoria").scale(2/3)

    self.play(
        ReplacementTransform(title_whole_name, title_GRASP),
        FadeOut(group_name),
        FadeIn(details_text)
    )
    self.wait()

    self.play(FadeOut(title_GRASP), FadeOut(details_text))
    self.wait()


"""CODE: Returns the total cost given an order of visited nodes"""
def get_total_cost(order):
    res = 0

    for i in range(len(order)):
        if i+1 < len(order):
            coord_start, coord_end = problem["DOTS_coord"][order[i]], problem["DOTS_coord"][order[i+1]]
            prev = res
            res += (abs(coord_start[0] - coord_end[0])**2 + abs(coord_start[1] - coord_end[1])**2)**(1/2)
            assert res >= 0
            assert res >= prev

        else:
            assert problem["DOTS_coord"][order[i]] == problem["DOTS_coord"][order[-1]]
            # TODO: simplify using the formula in the assert below
            assert i==len(order)-1  and  (i+1)%len(order) == 0

            res += (
                abs(problem["DOTS_coord"][order[i]][0] - problem["DOTS_coord"][order[0]][0])**2 + 
                abs(problem["DOTS_coord"][order[i]][1] - problem["DOTS_coord"][order[0]][1])**2
            )**(1/2)

            assert res >= 0
            assert res >= prev


    return res


"""ANIMATION: Displays the title of the problem"""
def introduce_problem(self):
    title = Text("Problema del viajante")
    self.play(Create(title))
    return title


"""ANIMATION & CODE: performs the local search given the current solution in the dict
Shows the process and updates the dict"""
def do_local_search(self, code_img):
    is_optimal = False
    
    solution = problem["DOTS_visited"].copy()
    solution_cost = get_total_cost(solution)

    # Make a copy of all the edges
    for edge in problem["EDGES_main_mobject"]:
        new_edge = Line(edge.start, edge.end, color=MAIN_LINE_COLOR)
        problem["EDGES_tmp_mobject"].append(new_edge)
    
    # Color the edges
    self.add(*problem["EDGES_tmp_mobject"])
    self.play(*[FadeToColor(l, EXPLORING_LINE_COLOR) for l in problem["EDGES_tmp_mobject"]])
    self.wait()

    assert len(problem["DOTS_visited"]) == len(problem["EDGES_tmp_mobject"])
    for (i,edge) in enumerate(problem["EDGES_tmp_mobject"]):
        def the_updater(edge, i=i):
            edge.become(Line(
                problem["DOTS_mobject"][problem["DOTS_visited"][i]].get_center(),
                problem["DOTS_mobject"][problem["DOTS_visited"][(i+1)%len(problem["DOTS_visited"])]].get_center(),
                color=EXPLORING_LINE_COLOR
            ))
        edge.add_updater(the_updater)

    # Main loop while current solution is not yet optimal
    # TODO show cost

    while not is_optimal:
        # TODO: re-draw the edges (not needed when it's the first iteration)
        is_optimal = True

        # Iterate over permutations 
        for i in range(len(solution)):
            new_solution = solution.copy()
            new_solution[i-1], new_solution[i] = new_solution[i], new_solution[i-1]

            # Do the permutation
            self.play(
                problem["DOTS_mobject"][problem["DOTS_visited"][i]].
                    animate.move_to(problem["DOTS_mobject"][problem["DOTS_visited"][(i+1)%len(problem["DOTS_mobject"])]].get_center()),
                problem["DOTS_mobject"][problem["DOTS_visited"][(i+1)%len(problem["DOTS_mobject"])]].
                    animate.move_to(problem["DOTS_mobject"][problem["DOTS_visited"][i]].get_center())
            )
            self.wait()

            # Compare solutions
            new_cost = get_total_cost(new_solution)
            if new_cost < solution_cost:
                solution, solution_cost = new_solution, new_cost
                # FIXME: uncomment
                # is_optimal = False # TODO: 

                # TODO: decide whether to do first-fit or best-fit

            # TODO: display new cost

            # Return animation to prev state: move edges to original position
            self.play(
                problem["DOTS_mobject"][problem["DOTS_visited"][i]].
                    animate.move_to(problem["DOTS_mobject"][problem["DOTS_visited"][(i+1)%len(problem["DOTS_mobject"])]].get_center()),
                problem["DOTS_mobject"][problem["DOTS_visited"][(i+1)%len(problem["DOTS_mobject"])]].
                    animate.move_to(problem["DOTS_mobject"][problem["DOTS_visited"][i]].get_center())
            )

            # TODO: decide whether to do first-fit or best-fit
            # TODO: show the best_one of all (if using best-fit)

    self.play(FadeOut(code_img))


"""MAIN"""
class GRASP(Scene):
    def construct(self):
        # Show the name and meaning
        show_introduction(self)

        # Show the general code for GRASP
        explain_code_grasp(self)
        self.wait()

        # Introduce the problem to solve
        build_problem(self)
        title = introduce_problem(self)
        self.wait()
        # TODO: explain how to solve the problem (brute force and other ways)
        # Draw the built problem on the screen
        display_problem(self, title)
        self.wait()

        # Show the general code and the code for construction
        code_img = show_code_grasp_focus_construct(self)
        # Visualize construction
        construct_initial_solution(self, code_img)

        # Show the general code and focus on repair
        show_code_grasp_focus_feasible(self)
        # TODO: Show the idea behind repair
        # TODO: explain reason behind it
        # TODO: Visualize repair

        # Show the general code and focus on local search
        code_img = show_code_grasp_focus_search(self)
        # Visualize local search
        do_local_search(self, code_img)
        # TODO: differenciate between best and first
        # TODO: explain what the neighborhood is

        # TODO: Redo explanation of code

        # TODO: Show how parameters affect the found solution, exploration space, execution time
        # TODO: pending: order-vs-value, alpha value, p value, first-vs-best
        # TODO: Explain best choice of parameters

        # TODO: Show extensions and improvements to the algorithm

        # TODO: End of video
        # TODO: Add references
        # TODO: Show our names