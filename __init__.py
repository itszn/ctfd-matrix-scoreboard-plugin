import os

from flask import (
    render_template,
    jsonify,
    Blueprint,
    url_for,
    session,
    redirect,
    request
)
from sqlalchemy.sql import or_

from CTFd import utils, scoreboard
from CTFd.models import db, Solves, Challenges
from CTFd.plugins import override_template
from CTFd.utils.config import is_scoreboard_frozen, ctf_theme, is_users_mode
from CTFd.utils.config.visibility import challenges_visible, scores_visible
from CTFd.utils.dates import (
    ctf_started, ctftime, view_after_ctf, unix_time_to_utc
)
from CTFd.utils.user import is_admin, authed


def load(app):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    template_path = os.path.join(dir_path, 'scoreboard-matrix.html')
    override_template('scoreboard.html', open(template_path).read())

    matrix = Blueprint('matrix', __name__, static_folder='static')
    app.register_blueprint(matrix, url_prefix='/matrix')

    def get_standings():
        standings = scoreboard.get_standings()
        # TODO faster lookup here
        jstandings = []
        for team in standings:
            teamid = team[0]
            solves = db.session.query(Solves.challenge_id.label('challenge_id')).filter(Solves.team_id == teamid)
            freeze = utils.get_config('freeze')
            if freeze:
                freeze = unix_time_to_utc(freeze)
                if teamid != session.get('id'):
                    solves = solves.filter(Solves.date < freeze)
            solves = solves.all()
            jsolves = []
            for solve in solves:
                jsolves.append(solve.challenge_id)
            jstandings.append({'teamid': team[0], 'score': team[3], 'name': team[2], 'solves': jsolves})
        db.session.close()
        return jstandings

    def get_challenges():
        if not is_admin():
            if not ctftime():
                if view_after_ctf():
                    pass
                else:
                    return []
        if challenges_visible() and (ctf_started() or is_admin()):
            chals = db.session.query(
                Challenges.id,
                Challenges.name,
                Challenges.category
            ).filter(or_(Challenges.state != 'hidden', Challenges.state is None)).all()
            jchals = []
            for x in chals:
                jchals.append({
                    'id': x.id,
                    'name': x.name,
                    'category': x.category
                })

            # Sort into groups
            categories = set(map(lambda x: x['category'], jchals))
            jchals = [j for c in categories for j in jchals if j['category'] == c]
            return jchals
        return []

    def scoreboard_view():
        if scores_visible() and not authed():
            return redirect(url_for('auth.login', next=request.path))
        if not scores_visible():
            return render_template('scoreboard.html',
                                   errors=['Scores are currently hidden'])
        standings = get_standings()
        return render_template('scoreboard.html', standings=standings,
                               score_frozen=is_scoreboard_frozen(),
                               mode='users' if is_users_mode() else 'teams',
                               challenges=get_challenges(), theme=ctf_theme())

    def scores():
        json = {'standings': []}
        if scores_visible() and not authed():
            return redirect(url_for('auth.login', next=request.path))
        if not scores_visible():
            return jsonify(json)

        standings = get_standings()

        for i, x in enumerate(standings):
            json['standings'].append({'pos': i + 1, 'id': x['name'], 'team': x['name'],
                                      'score': int(x['score']), 'solves': x['solves']})
        return jsonify(json)

    app.view_functions['scoreboard.listing'] = scoreboard_view
    app.view_functions['scoreboard.score'] = scores
