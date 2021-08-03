from .aos_opt import DefaultOpiton


class AosconfOption(DefaultOpiton):
    def __init__(self, name, sub, default):
        # Prepare arg for substitution
        sub = f"$({sub})"
        super().__init__(name, sub, default)
