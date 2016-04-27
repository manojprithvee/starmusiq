import requests,os,ctypes,zipfile,subprocess
import lxml.html as lh
def extractAll(zipName,language):
    hist={"Hindi":":wMQ1yJLK",'Malayalam':':8NBERKYD','Tamil':':RFpTSCAb','Telugu':':QRhWRY5A'}
    print "starting upload wait ..."
    output=Run_process("mcl put "+zipName+" "+hist[language])
    if "Traceback" in output:
        print "try:1"
        output=Run_process("mcl put "+zipName+" "+hist[language])
        if "Traceback" in output:
            print "try:2"
            output=Run_process("mcl put "+zipName+" "+hist[language])
            if "Traceback" in output:
                print "try:3"
                output=Run_process("mcl put "+zipName+" "+hist[language])
    if "Transfert completed" in output:
        print "upload success"
    try:
        os.remove(zipName)
    except Exception as e:
        print e

def Run_process(exe):
    p = subprocess.Popen(exe, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True, executable="/bin/bash")
    final = ""
    abc=0
    while True:
        retcode = p.poll()  # returns None while subprocess is running
        out = p.stdout.readline()
        temp = out
        global data
        final = final + out
        if retcode is not None:
            return final
       
os.system("mcl login --email=manoj.prithvee@gmail.com")  
link_list=list()
baseurl='http://www.starmusiq.com/mp3database.asp?Movie=&RecNextPg='
completed=list()
try:
    complete=open("complete","r")
    rawcompleted=complete.read()
    complete.close()
    completed=rawcompleted.split("\n")
except:
    print "running for the first time..."
for i in range(1,164):
    a = requests.get("http://www.starmusiq.com/mp3database.asp?Movie=&RecNextPg="+str(i))
    print "http://www.starmusiq.com/mp3database.asp?Movie=&RecNextPg="+str(i)
    doc = lh.fromstring(a.text)
    for i in doc.xpath('//table[@class="main_tb3"]//td/div[@align="center"]/a/@href'):
            id=int(i.replace("./tamil_movie_songs_listen_download.asp?MovieId=",""))
            if str(id) not in completed:
                print "http://www.starmusiq.com/tamil_movie_songs_listen_download.asp?MovieId="+str(id)
                try:
                    a = requests.get("http://www.starmusiq.com/tamil_movie_songs_listen_download.asp?MovieId="+str(id))
                except Exception as e:
                    print "network"
                    print e
                doc = lh.fromstring(a.text)
                songlist=list()
                try:
                    temp=doc.xpath('//tr/td/table/tr[4]/td/div/a/@href')[0]
                    if "http://filemirchi.info" in temp:
                        songlist.append(temp)
                    temp=doc.xpath('//tr/td/table/tr[3]/td/div/a/@href')[0]
                    if "http://filemirchi.info" in temp:
                        songlist.append(temp)
                except Exception as e:
                    print "xpath"
                    print e
                    
                if not songlist:
                    continue
                try:
                    os.system("wget -c "+str(songlist[0]))
                except Exception as e:
                    print "command"
                    print e
                finally:
                    try:
                        extractAll(str(songlist[0]).split("/")[-1],str(songlist[0]).split("/")[3])
                    except Exception as e:
                        print "zip"
                        print e
                    complete=open("complete","a")
                    print complete.write(str(id)+"\n")
                    complete.close()