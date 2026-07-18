from dishka import Provider, Scope, provide_all

from app.presentation.telegram.flows.common.menu import CommonMenuFlow
from app.presentation.telegram.flows.extra.errors import ExtraErrorsFlow
from app.presentation.telegram.flows.extra.pm import PMFlow


class FlowsProvider(Provider):
    scope = Scope.REQUEST

    flows = provide_all(CommonMenuFlow, ExtraErrorsFlow, PMFlow)
