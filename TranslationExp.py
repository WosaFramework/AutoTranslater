# Import required libs
import re
import json
import http.client

# Simple script config
toLang = 'sv'
conn = http.client.HTTPSConnection('google-translate1.p.rapidapi.com')
file_path = 'to_file_path'
rapidapi_key = 'your_key_here'

# Main func
def main():
    counter = 1

    with open(file_path, 'r', encoding='utf-8-sig') as file:
        print('Parsing & caching json file...')
        data = json.load(file)

    with open(file_path, 'w', encoding='utf-8-sig') as file:
        print('Truncating old json file.')
        file.truncate()

    with open(file_path, 'r', encoding='utf-8-sig') as file:
        for string in data:
            if len(string) > 2:
                data[string] = handleString(translate(data[string], string))
                print('string ' + string + ' was translated successfully [' + data[string] + '] (' + str(counter) + '/' + str(len(data)) + ').')

                counter += 1
    
    with open(file_path, 'w') as file:
        print('Writing & closing replaced file...')
        file.write(json.dumps(data))
        file.close()

    print('New json file saved.')


# Translate Func
def translate(input, label):
    payload = 'q=' + input + '&target=' + toLang + '&source=en'
    try:
        headers = {'content-type': 'application/x-www-form-urlencoded','accept-encoding': 'application/gzip','x-rapidapi-host': 'google-translate1.p.rapidapi.com','x-rapidapi-key': rapidapi_key }
        conn.request('POST', '/language/translate/v2', payload, headers)

        res = conn.getresponse()
        data = res.read()
        data = data.decode('utf-8')
        data = json.loads(data)
        data = data['data']['translations'][0]['translatedText']
    except:
        data = ':<?>: An exception occured for label ' + label + ' :<?>: '


    return data
    

# handling the string to make it "correct" in terms of GTA, ~ ? ~ space handling.
def handleString(str):
    str = re.sub(r'~ ([A-Z\n_]*) ~', r'~\1~', str) # only uppercased for control displaying
    str = re.sub(r'~ (.) ~', r'~\1~', str) # one character only, used for coloring
    str = re.sub(r' ~(.)~ ', r' ~\1~', str) # used to place coloring at the right spot to avoid double spaces
    str = re.sub(r' ~ ', r' ', str) # remove random flawed stuff just causing double spaces to occur

    return str


# Run function tree
main()