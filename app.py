from webbrowser import open as open_url
from load_rock import get_rock_name_url
from app_vars import *
from nltk import edit_distance
import gradio as g

global name, url, correct, wrong, previous_correctness, skipped, prevurl, coft, qnum
name, url = get_rock_name_url()
prevurl = ""
correct = 0
wrong = 0
skipped = 0
coft = 0
qnum = 0


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
    global name, url, correct, wrong, skipped, prevurl, coft, qnum
    out = ""
    fb = ""
    stats = ""
    qnum += 1
    if len(ans) >= 1:
        ans = ans.strip()
        deviance = check_2_strings(ans, name)
        if ans in ["s", "/", "skip", "n", "r"]:
            fb += "# The answer is: " + name
            skipped += 1
            prevurl = url
        elif deviance <= 26:
            fb += "## Correct! - The answer is: " + name

            # print("Before:", url, prevurl, url == prevurl)
            if prevurl != url:
                coft += 1
            # print("after:", url, prevurl, url == prevurl)
            name, url = get_rock_name_url()
            correct += 1
            # print("after2:", url, prevurl, url == prevurl, "\n\n\n")
        else:
            wrong += 1
            fb += f"## Wrong! The answer isn't '{ans}'.\n # Press s, r, or n to see the answer."
            prevurl = url

        stats = f" ### Question {qnum}: \n {fb} \n ## Correct: {correct} | Wrong: {wrong} | Correct on first try : {coft} | Skipped: {skipped} | Total: {correct + wrong + skipped} \n Your current deviance from the correct answer is: {deviance}"
        out = ""
    else:
        out = ans
        stats = feedback
    return (
        url,
        out,
        stats,
        f"""### [Click here to research the rock](https://www.mindat.org/search.php?search='{name}')""",
    )


with g.Blocks() as A:
    title = g.Markdown("# Practice Rocks and Minerals. By Aashray")
    with g.Row() as row:
        with g.Column(scale=5, min_width=1000,):
            img = g.Image(
                url,
                type="filepath",
                tool="select"
            )
        with g.Column(variant="panel"):
            with g.Group():
                inp = g.Textbox(
                    placeholder="Enter the rock name",
                    show_label=False,
                    max_lines=1,
                )
            feedback = g.Markdown(
                "### Type in the name of the rock and press enter to get started."
            )
            l = g.Markdown(
                f"""\n## [**Click here to research the rock**](https://www.mindat.org/search.php?search='{name}')"""
            )
    inp.submit(
        fn=get_name,
        inputs=[inp, feedback],
        outputs=[
            img,
            inp,
            feedback,
            l,
        ],
        scroll_to_output=True,
    )

A.launch(
    inbrowser=True,
)
