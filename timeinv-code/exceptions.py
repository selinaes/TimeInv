# =================================================================================
#  Create custom exceptions to be used in app.py
#  Authors: Francisca Moya Jimenez, Jiawei Liu, Candice Ye, and Diana Hernandez
# =================================================================================


class UsernameNonExistent(Exception):
    """Exception raised when a username has not been added to the
        organization.

    Attributes: 
        message -- explanation of the error
    """

    def __init__(self, message="""A user with the given username has not been added to your
                        organization. Contact your manager to request access."""):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'username error -> {self.message}'

class UsernameFormatError(Exception):
    """Exception raised when username is longer than 10 characters.

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message="Could not sign up user. The username must have at most 10 characters."):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'username error -> {self.message}'

class UsernameNonExistent(Exception):
    """Exception raised when a username has not been added to the
        organization.

    Attributes: 
        message -- explanation of the error
    """

    def __init__(self, message="""A user with the given username has not been added to your
                        organization. Contact your manager to request access."""):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'username error -> {self.message}'

class ProductNonExistent(Exception):
    """Exception raised when a product does not exist in the db.

    Attributes: 
        message -- explanation of the error
    """

    def __init__(self, message="No product found with given sku"):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'product error -> {self.message}'

class LowInventory(Exception):
    """Exception raised when a product does not exist in the db.

    Attributes: 
        message -- explanation of the error
    """

    def __init__(self, units, message="Not enough availability of the product to perform the sale."):
        self.message = message + " There are only " + str(units) + " units available."
        super().__init__(self.message)

    def __str__(self):
        return f'low inventory -> {self.message}'

class ProductSortInvalid(Exception):
    """Exception raised when a product sorting criteria is invalid.

    Attributes: 
        message -- explanation of the error
    """
    def __init__(self, message="Type to sort by in products is not permitted"):
        self.message = message 
        super().__init__(self.message)

    def __str__(self):
        return f'product sort invalid -> {self.message}'

class TransactionSortInvalid(Exception):
    """Exception raised when a transaction sorting criteria is invalid.

    Attributes: 
        message -- explanation of the error
    """
    def __init__(self, message="Type to sort by in transactions is not permitted"):
        self.message = message 
        super().__init__(self.message)

    def __str__(self):
        return f'transaction sort invalid -> {self.message}'

class TransactionSearchInvalid(Exception):
    """Exception raised when a transaction searching column is invalid.

    Attributes: 
        message -- explanation of the error
    """
    def __init__(self, message="Column to search by in transactions is not permitted"):
        self.message = message 
        super().__init__(self.message)

    def __str__(self):
        return f'transaction search invalid -> {self.message}'

class FileHasIncorrectFormat(Exception):
    """Exception raised when a file uploaded doesn't have the following
    formats: jpeg, jpg, png

    Attributes: 
        message -- explanation of the error
    """

    def __init__(self, message="""Error inserting the product. File uploaded has incorrect format.
    File must be a jpg, jpeg or png file."""):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'file upload error -> {self.message}'