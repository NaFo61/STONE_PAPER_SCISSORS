class UserNotFoundException(Exception):
    pass

class UserAlreadyExistsException(Exception):
    pass

class ProblemWithSomeParameterException(Exception):
    pass

class CriticalErrorException(Exception):
    pass