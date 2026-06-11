class Singleton:
    """
    Returns a page object instance scoped to the current scenario.
    Instances are stored on `context`, which Behave resets between scenarios,
    so there is no risk of a stale driver reference across scenarios.
    """

    @staticmethod
    def getInstance(context, classe):
        attr_name = f'_page_{classe.__name__}'
        if not hasattr(context, attr_name):
            setattr(context, attr_name, classe(context.browser))
        return getattr(context, attr_name)
