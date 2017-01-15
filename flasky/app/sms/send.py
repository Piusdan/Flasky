# Import the helper gateway class
from AfricasTalkingGateway import AfricasTalkingGateway, AfricasTalkingGatewayException
# Specify your login credentials


class AfricasTalking(object):
    username = "Nyongesa"
    apikey = "7df5ca02b98be748e2402cbf9f08bd469126db0fa307f9113eee33ce94f9a724"
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

            self.results = gateway.sendMessage(self.to, self.message)

            for recipient in self.results:
                # status is either "Success" or "error message"
                print 'number=%s;status=%s;messageId=%s;cost=%s' % (recipient['number'],
                                                                    recipient[
                                                                        'status'],
                                                                    recipient[
                                                                        'messageId'],
                                                                    recipient['cost'])
        except AfricasTalkingGatewayException, e:
            print 'Encountered an error while sending: %s' % str(e)


def main():
    ATObj = AfricasTalking(message=message, phonenumber=phonenumber_list)
    ATObj.send_sms() m

if __name__ == '__main__':
    main()
