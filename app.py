from load_rock import get_rock_name_url
from app_vars import *
from nltk import edit_distance
import gradio as g
from urllib.request import urlretrieve

state = g.State(
    {a: b for a, b in (zip(["name", "url"], get_rock_name_url()))}
    | dict(correct=0, wrong=0, skipped=0, prevurl="", coft=0, qnum=1)
)


def check_2_strings(a: str, b: str):
    return (
        edit_distance(a, b, substitution_cost=5, transpositions=True)
        / ((len(a) + len(b)))
        * 100
    )


def update_app(
    user_answer: str,
    feedback: str,
):
    answer_box_output = ""
    feedback_to_user = ""
    user_statistics = ""
    state.value["qnum"] += 1
    if len(user_answer) >= 1:
        user_answer = user_answer.strip()
        deviance = check_2_strings(user_answer, state.value["name"])
        if user_answer in ["s", "/", "skip", "n", "r"]:
            feedback_to_user += "The answer is: " + state.value["name"]
            state.value["skipped"] += 1
            state.value["prevurl"] = state.value["url"]
        elif deviance <= 26:
            feedback_to_user += f"""Correct! - The answer is: {state.value["name"]}"""

            if state.value["prevurl"] != state.value["url"]:
                state.value["coft"] += 1
            state.value["name"], state.value["url"] = get_rock_name_url()
            state.value["correct"] += 1
        else:
            state.value["wrong"] += 1
            feedback_to_user += f"\n### Wrong! The answer isn't {user_answer}. \n ### Press s, r, or n to see the answer."
            state.value["prevurl"] = state.value["url"]

        user_statistics = f"""
                        Statistic | Value
                        ---: | :---
                        Correct | {state.value["correct"]}
                        Wrong | {state.value["wrong"]} 
                        Correct on first try | {state.value["coft"]}
                        Skipped | {state.value["skipped"]}
                        Total Rocks| {state.value["correct"] + state.value["wrong"] + state.value["skipped"]}
                        """
        answer_box_output = ""
    else:
        answer_box_output = user_answer
        user_statistics = feedback
    return (
        state.value["url"],
        answer_box_output,
        f"""## Question {state.value["qnum"]}:\n ### {feedback_to_user}""",
        user_statistics,
        rf"""### [Click here to research the rock](https://www.mindat.org/search.php?search={state.value["name"].strip().replace(" ", "%20")})""",
    )


with g.Blocks() as A:
    title = g.Markdown("# Practice Rocks and Minerals. By Aashray")
    with g.Row():
        inp = g.Textbox(
            placeholder="""Enter the rock/mineral's name here. Press s, r, or n to skip the question.""",
            show_label=False,
            max_lines=1,
            autofocus=True,
            autoscroll=True,
        )
    with g.Row() as row:
        with g.Column(
            scale=7,
            min_width=1000,
        ):
            img = g.ImageEditor(
                state.value["url"],
                type="filepath",
            )
        with g.Column(variant="panel"):
            feedback = g.Markdown(
                f"""### Question {state.value["qnum"]}: Type in the name of the rock/mineral to get started!"""
            )
            stats = g.Markdown(
                f"""
                Statistic | Value
                ---: | :---
                Correct | {state.value["correct"]}
                Wrong | {state.value["wrong"]} 
                Correct on first try | {state.value["coft"]}
                Skipped | {state.value["skipped"]}
                Total | {state.value["correct"] + state.value["wrong"] + state.value["skipped"]}
                """
            )
            link = g.Markdown(
                f"""### [Click here to research the rock](https://www.mindat.org/search.php?search={state.value["name"].strip().replace(" ", "%20")})"""
            )
    inp.submit(
        fn=update_app,
        inputs=[inp, stats],
        outputs=[
            img,
            inp,
            feedback,
            stats,
            link,
        ],
    )

A.launch(
    inbrowser=True,
)
