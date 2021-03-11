from flask import Flask, render_template, request,g
import httplib2
import json
import time
app = Flask(__name__)
dict_vocab={"&quot;":"\"","&#39;":"\'"}
flter_var="!)EhwLgOk4XD2f-eNYPY_IH_GU22NPCYoJ.Amf(lEfsxcaBJ4i"
@app.route('/')
def show_main():
    return render_template('search.html')


@app.route('/',methods=['POST'])
def post_handle():
    g.request_start_time =time.time()
    if request.method == 'POST':
        input= request.form
        if "tag" in input.keys():
            tag = request.form["tag"]
            if tag== "":
                return render_template('search.html')
            conn= httplib2.Http()
            start= int(g.request_start_time-604800)
            url="https://api.stackexchange.com/2.2/questions?pagesize=10"+"&fromdate="+str(start)+"&todate="+str(int(g.request_start_time))+"&order=desc&sort=votes&tagged="+tag+"&site=stackoverflow&filter="+flter_var
            f= conn.request(url)[1]
            f= f.decode('utf8')
            # with open('sample.JSON',encoding='utf-8') as f:
            content= json.loads(f)
            if 'error_id' in content:
                print("Error:+\n"+str(content))
                return "Ops! Something unexpected happens. Error has been logged in terminal."
            response = content['items']
            title_list=[]
            html_body_maker(title_list,response)
            url = "https://api.stackexchange.com/2.2/questions?pagesize=10" + "&fromdate=" + str(start) + "&todate=" + str(int(g.request_start_time)) + "&order=desc&sort=creation&tagged=" + tag + "&site=stackoverflow&filter=" + flter_var

            f = conn.request(url)[1]
            f = f.decode('utf8')
            content = json.loads(f)
            if 'error_id' in content:
                print("Error:+\n" + str(content))
                return "Ops! Something unexpected happens. Error has been logged in terminal."
            response = content['items']
            html_body_maker(title_list, response)
            title_list.sort(key=_takeSecond)
            title_list.reverse()
            g.request_time = lambda: "%.5fs" % (time.time() - g.request_start_time)
            return render_template('result.html',entries=title_list)

#helper method
def _takeSecond(elem):
    return elem[1]
#add score and creation time
def addFooter(body,score,time,indentation):
    body+="<p style=\"color:gray; font-size:80%;margin-left: "+indentation+"\">created at: "+str(time)+"<span style=\"color:green;\">   |   score: "+str(score)+"</span></p>"
    return body
#add comments body to the question
def add_question_comment(json,indentation):
    comments_Q_section=""
    if "comments" in json.keys():
        comments = json['comments']
        comments_Q_section+="<p style=\"margin-left: "+indentation+"\">"+"Comments:</p>"
        for c in comments:
            comments_Q_section+= "<p style=\"margin-left: "+indentation+"\">"
            comments_Q_section += c['body']
            comments_Q_section += "</p>"
            score= c['score']
            time = c['creation_date']
            comments_Q_section = addFooter(comments_Q_section,score,time,indentation)
    return comments_Q_section
#add answer body to the question
def add_question_Answers(json):
    answer_section=""
    counter=1
    if "answers" in json.keys():
        ans= json['answers']
        answer_section+= "<p>Answers:</p>"
        for a in ans:
            answer_section+= "<p>"
            answer_section += str(counter)+":"
            answer_section += a['body']
            answer_section += "</p>"
            score= a['score']
            time = a['creation_date']
            answer_section = addFooter(answer_section,score,time,"0px")
            answer_section += add_question_comment(a,"40px")
            counter+=1
    return answer_section
def html_body_maker(list,response):
    for question in response:
        title = question['title']
        time = question['creation_date']
        body = question['body']
        score = question['score']
        body = addFooter(body, score, time, "0px")

        comment = add_question_comment(question, "40px")
        ans = add_question_Answers(question)
        body += comment
        body += ans
        for k in dict_vocab.keys():
            title = title.replace(k, dict_vocab[k])
        list.append((title, time, body))
    return

if __name__ == '__main__':
    app.run(host='0.0.0.0')
