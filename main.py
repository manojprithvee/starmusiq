import requests,os,ctypes,zipfile
import lxml.html as lh
def extractAll(zipName,language):
    try:
        z = zipfile.ZipFile(zipName)
        for f in z.namelist():
            if f.endswith('/'):
                os.makedirs(f)
            else:
                # if os.name=='nt':
                #     z.extract(f,os.environ['USERPROFILE']+"\\Music\\"+language)
                # elif os.name=='posix':
                #     z.extract(f,os.environ['HOME']+"/Music/"+language)
                path=z.extract(f,"D:\Music\\"+language)
                os.rename(path,path.replace("-VmusiQ.Com","").replace("-StarMusiQ.Com",""))    
        z.close()
    except Exception as e:
        print e
    finally:
        z.close()
        
    try:
        os.remove(zipName)
    except Exception as e:
        print e
        
    
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
for i in range(1,165):
    a = requests.get("http://www.starmusiq.com/mp3database.asp?Movie=&RecNextPg="+str(i))
    print "http://www.starmusiq.com/mp3database.asp?Movie=&RecNextPg="+str(i)
    doc = lh.fromstring(a.text)
    for i in doc.xpath('//table[@class="main_tb3"]//td/div[@align="center"]/a/@href'):
            id=int(i.replace("./tamil_movie_songs_listen_download.asp?MovieId=",""))
            if str(id) not in completed:
                ctypes.windll.kernel32.SetConsoleTitleA(str(id))
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
                    break
                if not songlist:
                    break
                try:
                    os.system("wget.exe -c "+str(songlist[-1]))
                except Exception as e:
                    print "command"
                    print e
                finally:
                    try:
                        extractAll(str(songlist[-1]).split("/")[-1],str(songlist[-1]).split("/")[3])
                    except Exception as e:
                        print "ZIP"
                        print e
                    complete=open("complete","a")
                    print complete.write(str(id)+"\n")
                    complete.close()
            