import json
import time
import urllib
import urllib2

def pushData(id,data):
    #print data
    resource_dict = {
         "resource_id": id,
          "force": True,

           "records":[data],
           "method": "insert",
    }
    json_coded = json.dumps(resource_dict)
    post_dict = urllib.quote(json_coded)

    post_url = "http://202.121.178.214/api/3/action/datastore_upsert"
    request = urllib2.Request(post_url)

    request.add_header('Authorization', 'dbf651ea-71cf-4c78-844a-8f7bf3db81e2')

    response = urllib2.urlopen(request, post_dict)

    #print response.read()