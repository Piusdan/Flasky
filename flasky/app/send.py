# Import the helper gateway class
from AfricasTalkingGateway import AfricasTalkingGateway, AfricasTalkingGatewayException
# Specify your login credentials


class AfricasTalking(object):
    username = "PiusDan"
    apikey = "5dfcc116a8a9f9e56641ff31fbce1ca82896462d2683400e76712c351a686628"
    # Create a new instance of our awesome gateway class
    gateway = AfricasTalkingGateway(username, apikey)

    def __init__(self, message=None, phonenumber=None):
        self.to = phonenumber
        # And of course we want our recipients to know what we really do
        self.message = message

    def send_sms(self):
        # Any gateway errors will be captured by our custom Exception class below,
        # so wrap the call in a try-catch block
        try:
            # Thats it, hit send and we'll take care of the rest.

            results = self.gateway.sendMessage(self.to, self.message)

            for recipient in results:
                # status is either "Success" or "error message"
                print 'number=%s;status=%s;messageId=%s;cost=%s' % (recipient['number'],
                                                                    recipient[
                                                                        'status'],
                                                                    recipient[
                                                                        'messageId'],
                                                                    recipient['cost'])
        except AfricasTalkingGatewayException, e:
            print 'Encountered an error while sending: %s' % str(e)