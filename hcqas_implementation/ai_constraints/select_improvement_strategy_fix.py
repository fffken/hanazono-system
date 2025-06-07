def _select_improvement_strategy(self, iteration: int, current_quality: int) -> str:
    """改善戦略選択"""

    if iteration == 0:
        return 'incremental_improvement'
    elif iteration == 1:
        return 'template_fallback'
    elif iteration == 2:
        return 'pattern_matching'
    else:
        return 'manual_escalation'
