from flask import Flask, render_template_string, request, redirect

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        return redirect('/announce', code=307)
    else:
        return render_template_string(
            """<!doctype html>
            <title>SSTI1</title>
            <h1>Home</h1>
            <p>I built a cool website that lets you announce whatever you want!*</p>
            <form action="/" method="POST">
                What do you want to announce:
                <input name="content" id="announce">
                <button type="submit">Ok</button>
            </form>
            <p style="font-size:10px; position:fixed; bottom:10px; left:10px;">
                *Announcements may only reach yourself
            </p>
            """
        )


@app.route("/announce", methods=["POST"])
def announcement():
    return render_template_string(
        """<!doctype html>
        <h1 style="font-size:100px;" align="center">"""
        + request.form.get("content", "")
        + """</h1>
        """
    )
