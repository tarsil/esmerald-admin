from esmerald import Gateway

from .views import welcome

route_patterns = [Gateway(handler=welcome, name="welcome")]
