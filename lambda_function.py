"""
In this file we specify default event handlers which are then populated into the handler map using metaprogramming
Copyright Anjishnu Kumar 2015
Happy Hacking!
"""

from ask import alexa
from datetime import datetime

def lambda_handler(request_obj, context=None):
    '''
    This is the main function to enter to enter into this code.
    If you are hosting this code on AWS Lambda, this should be the entry point.
    Otherwise your server can hit this code as long as you remember that the
    input 'request_obj' is JSON request converted into a nested python object.
    '''

    metadata = {'user_name' : ''} # add your own metadata to the request using key value pairs
    
    ''' inject user relevant metadata into the request if you want to, here.    
    e.g. Something like : 
    ... metadata = {'user_name' : some_database.query_user_name(request.get_user_id())}

    Then in the handler function you can do something like -
    ... return alexa.create_response('Hello there {}!'.format(request.metadata['user_name']))
    '''
    return alexa.route_request(request_obj, metadata)


@alexa.default_handler()
def default_handler(request):
    """ The default handler gets invoked if no handler is set for a request type """
    return alexa.create_response(	message="Ask me what time it is",
    								reprompt_message="Ask me what time it is")
    
@alexa.request_handler("LaunchRequest")
def launch_request_handler(request):
    ''' Handler for LaunchRequest '''
    return alexa.create_response(	message="Hello, Welcome to Binary Clock, ask me what time it is",
    								reprompt_message="Ask me what time it is")

@alexa.request_handler("SessionEndedRequest")
def session_ended_request_handler(request):
    return alexa.create_response(message="Goodbye!",end_session=True)

@alexa.intent_handler('AMAZON.StopIntent')
def stop_intent_handler(request):
    return alexa.create_response(message="Goodbye!",end_session=True)

@alexa.intent_handler('AMAZON.CancelIntent')
def stop_intent_handler(request):
    return alexa.create_response(message="Goodbye!",end_session=True)

@alexa.intent_handler('GetTime')
def get_time_intent_handler(request):
    
    request_text = request.request['request']['intent']['slots']['value']['value']
	
    phrases_array = ["what time is it", "what time it is", "what time it is in binary" , "what time is it in binary"]
	
    if request_text in phrases_array:
		
    	binary_arrays = get_binary_arrays(str(datetime.utcnow().time()))

    	binary_time_array = []
    
    	for array in binary_arrays:
        	binary_time_array.append(binary_to_words(array))
    
    	return alexa.create_response(message="The current time in binary is " + 
    							binary_time_array[0] + " hours, and " + 
    							binary_time_array[1] + " minutes, and " + 
    							binary_time_array[2] + " seconds, Coordinated Universal Time"
    							, end_session=True
            					)
    else:
    	return alexa.create_response(message="I didn't understand that. Ask me what time it is "
    							, end_session=False, 
    							reprompt_message="Ask me what time it is"
            					)


#Convert a number string to binary
def get_binary(num_str):
    powers_2_values_array = [32,16,8,4,2,1]

    binary_output = []
    working_int = int(num_str)
    
    for binary_value in powers_2_values_array:
        if binary_value <= working_int:
            binary_output.append(1)
            working_int = working_int - binary_value
        
        else:
            binary_output.append(0)

    return binary_output

#Create Time arrays in binary arrays for hours minutes and seconds.
def get_binary_arrays(time_str):

    time_array = time_str.split(":")

    time_array[2] = str(int(round(float(time_array[2]))))

    binary_arrays_to_output = []
    for time_section in time_array:
        binary_arrays_to_output.append(get_binary(time_section))
    return binary_arrays_to_output

#Create an array of words for the binary numbers in an array
def binary_to_words(binary_array):
    binary_in_words = []
    for element in binary_array:
        if element == 1:
            binary_in_words.append("one")
        elif element == 0:
            binary_in_words.append("zero")
    return array_to_string(binary_in_words)

#Turn array into string separated by spaces eg. "one zero one"
def array_to_string(array):
    output = ""
    for element in array:
        output = output + " " + str(element)
    return output.strip()
