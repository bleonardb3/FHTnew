import urllib3, requests, json, os
from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, RadioField, FloatField, IntegerField
from wtforms.validators import Required, Length, NumberRange

#url = 'https://ibm-watson-ml.mybluemix.net'
#username = '1e31f23c-ad34-4927-8283-a55f66caec00'
#password = 'ec54ced2-3909-4378-a42f-ee7e5081dd3d'

if 'VCAP_SERVICES' in os.environ:
    vcap = json.loads(os.getenv('VCAP_SERVICES'))
    print('Found VCAP_SERVICES')
    if 'pm-20' in vcap:
        creds = vcap['pm-20'][0]['credentials']
        username = creds['username']
        password = creds['password']
        url = creds['url']
scoring_endpoint = 'https://ibm-watson-ml.mybluemix.net/v3/wml_instances/374817e5-8365-42da-a434-cb20e3d1fba4/published_models/9b867182-4926-4144-812b-cc8cf6ea33bf/deployments/c45a87fb-50d1-4b17-ad04-703f551aa99d/online'
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secretpassw0rd'
bootstrap = Bootstrap(app)

class FHTForm(FlaskForm):
  categories = RadioField('Categories', coerce=int, choices=[('1','Sports/Travel'),('2','Engineering'),('3','Information Technology'),('4','Journalism'),('5','Government'),('6','Medical'), ('7','Science'),('8','Arts'),('9','Advertising'),('10','Legal'),('11','Construction'),('12','Retail'),('13','Education'),('14','Finance'),('15','Other')])
  age = IntegerField('Age:')
  countries_visited_count = IntegerField('Number of countries visited:')
  submit = SubmitField('Submit')
@app.route('/', methods=['GET', 'POST'])
def index():
  form = FHTForm()
  if form.is_submitted(): 
    category = form.categories.data
    print (category)
    form.categories.data = ''
    age = form.age.data
    print (age)
    form.age.data = ''
    countries_visited_count = form.countries_visited_count.data
    form.countries_visited_count.data = ''
        
    headers = urllib3.util.make_headers(basic_auth='{}:{}'.format(username, password))
    path = '{}/v3/identity/token'.format(url)
    response = requests.get(path, headers=headers)
    mltoken = json.loads(response.text).get('token')
    scoring_header = {'Content-Type': 'application/json', 'Authorization': 'Bearer' + mltoken}
    payload = {"fields": ["Code","Age","Countries_Visited_Count"], "values": [[category,age,countries_visited_count]]}
    scoring = requests.post(scoring_endpoint, json=payload, headers=scoring_header)

    scoringDICT = json.loads(scoring.text) 
    print ("scoringDICT: ",scoringDICT)
   # scoringList = scoringDICT['values'].pop()[11:13]
   # print (scoringList)
   # score = scoringList[1:].pop()
   # probability_died = scoringList[0:1].pop()[0:1].pop()
   # print (probability_died)
   # probability_survived = scoringList[0:1].pop()[1:].pop()
   # if (score == 10.0) :
   #   score_str = "high risk"
   #   probability = probability_high_risk                                        
   # else :
   #   score_str = "not a high risk"
   #   probability = probability_not_high_risk
    score_str = "test"
    probability = 1

    return render_template('score.html', form=form, scoring=score_str,probability=probability)
  return render_template('index.html', form=form)
port = os.getenv('PORT', '5000')
if __name__ == "__main__":
  app.run(host='0.0.0.0', port=int(port))
