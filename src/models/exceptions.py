class DuplicatedPublicationError(Exception):
    """Erro lançado quando uma publicação duplicada é cadastrada."""
    pass

class InvalidStatusError(Exception):
    """Erro lançado quando uma transição de status inválida é tentada."""
    pass

class InvalidEvaluationError(Exception):
    """Erro lançado quando uma avaliação inválida é atribuída."""
    pass

class InvalidAnnotationError(Exception):
    """Erro lançado quando uma anotação inválida é atribuída"""