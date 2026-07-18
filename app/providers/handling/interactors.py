from dishka import Provider, Scope, provide_all

from app.application.interactors.pm.user_status import PMInteractor


class InteractorsProvider(Provider):
    scope = Scope.REQUEST

    interactors = provide_all(PMInteractor)
