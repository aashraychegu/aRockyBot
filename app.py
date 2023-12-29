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


def get_name(
    ans: str,
    feedback: str,
):
    # global state.value["name"], state.value["url"], state.value["correct"], state.value["wrong"], state.value["skipped"], state.value["prevurl"], state.value["coft"], state.value["qnum"]
    out = ""
    fb = ""
    stats = ""
    state.value["qnum"] += 1
    if len(ans) >= 1:
        ans = ans.strip()
        deviance = check_2_strings(ans, state.value["name"])
        if ans in ["s", "/", "skip", "n", "r"]:
            fb += "The answer is: " + state.value["name"]
            state.value["skipped"] += 1
            state.value["prevurl"] = state.value["url"]
        elif deviance <= 26:
            fb += f"""Correct! - The answer is: {state.value["name"]}"""

            # print("Before:", state.value["url"], state.value["prevurl"], state.value["url"] == state.value["prevurl"])
            if state.value["prevurl"] != state.value["url"]:
                state.value["coft"] += 1
            # print("after:", state.value["url"], state.value["prevurl"], state.value["url"] == state.value["prevurl"])
            state.value["name"], state.value["url"] = get_rock_name_url()
            state.value["correct"] += 1
            # print("after2:", state.value["url"], state.value["prevurl"], state.value["url"] == state.value["prevurl"], "\n\n\n")
        else:
            state.value["wrong"] += 1
            fb += f"\n### Wrong! The answer isn't {ans}. \n ### Press s, r, or n to see the answer."
            state.value["prevurl"] = state.value["url"]

        stats = f"""
Statistic | Value
---: | :---
Correct | {state.value["correct"]}
Wrong | {state.value["wrong"]} 
Correct on first try | {state.value["coft"]}
Skipped | {state.value["skipped"]}
Total Rocks| {state.value["correct"] + state.value["wrong"] + state.value["skipped"]}
          """
        out = ""
    else:
        out = ans
        stats = feedback
    return (
        state.value["url"],
        out,
        f"""## Question {state.value["qnum"]}:\n ### {fb}""",
        stats,
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
        fn=get_name,
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
