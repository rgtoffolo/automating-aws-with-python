"""Class for error management."""

# boto3 error handling
#   ['Error']['Code'] e.g. 'EntityAlreadyExists' or 'ValidationError'
#   ['ResponseMetadata']['HTTPStatusCode'] e.g. 400
#   ['ResponseMetadata']['RequestId'] e.g. 'd2b06652-88d7-11e5-99d0-812348583a35'
#   ['Error']['Message'] e.g. "An error occurred (EntityAlreadyExists) ..."
#   ['Error']['Type'] e.g. 'Sender'

class ErrManager:
    """Manage error messages."""

    def __init__(self):
        pass

    def err_manager(e):
        """Manage errors to show the correct output."""
        if e.response['Error']['Code'] == "AuthFailure":
            print("Authentication Failure: your athentication keys are invalid or disabled.")
        else:
            print("Unexpected error: ", e)
