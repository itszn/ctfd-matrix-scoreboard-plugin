from flask import (
    render_template,
    Blueprint,
    session,
    request
)

from CTFd import utils, scoreboard
from CTFd.api.v1.challenges import ChallengeList
from CTFd.models import db, Solves
from CTFd.utils.config import is_scoreboard_frozen
from CTFd.utils.config.visibility import challenges_visible
from CTFd.utils.dates import unix_time_to_utc
from CTFd.utils.decorators.visibility import check_score_visibility
from CTFd.utils.helpers import get_infos
from CTFd.utils.modes import get_mode_as_word, TEAMS_MODE


def load(app):
    app.register_blueprint(Blueprint(
        'matrix', __name__,
        static_folder='static',
        template_folder='templates',
    ), url_prefix='/matrix')

    def get_standings():
        standings = scoreboard.get_standings()
        # TODO faster lookup here
        jstandings = []
        for team in standings:
            teamid = team[0]
            solves = db.session.query(Solves.challenge_id.label('challenge_id'))
            if get_mode_as_word() == TEAMS_MODE:
                solves = solves.filter(Solves.team_id == teamid)
            else:
                solves = solves.filter(Solves.user_id == teamid)
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
        if not challenges_visible():
            return []
        jchals = ChallengeList.get(request.args)
        # Sort into groups
        categories = set(map(lambda x: x['category'], jchals['data']))
        jchals = [j for c in categories for j in jchals['data'] if j['category'] == c]
        return jchals

    @check_score_visibility
    def scoreboard_view():
        standings = get_standings()
        infos = get_infos()

        if is_scoreboard_frozen():
            infos.append("Scoreboard has been frozen")

        return render_template('scoreboard-matrix.html', standings=standings,
                               challenges=get_challenges())

    app.view_functions['scoreboard.listing'] = scoreboard_view
