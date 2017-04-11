from flask import render_template
from CTFd import utils, scoreboard

ROOT = '/plugins/ctfd-matrix-scoreboard-plugin/'

def load(app):
    print "load"

    def scoreboard_view():
        if utils.get_config('view_scoreboard_if_authed') and not utils.authed():
            return redirect(url_for('auth.login', next=request.path))
        if utils.hide_scores():
            return render_template('..'+ROOT+'templates/scoreboard.html', errors=['Scores are currently hidden'])
        standings = scoreboard.get_standings()
        return render_template('/..'+ROOT+'templates/scoreboard.html', teams=standings, score_frozen=utils.is_scoreboard_frozen())


    app.view_functions['scoreboard.scoreboard_view']  = scoreboard_view

