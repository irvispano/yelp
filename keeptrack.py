import datetime
import pickle
def UtcNow():
    now = datetime.datetime.utcnow()
    return now
# keeptrack={}
# with open("visi.pickle",'wb') as f:
#       pickle.dump(keeptrack,f)

def keeptrack_f():

  with open("visi.pickle","rb") as f:
    keeptrack=pickle.load(f)
    
  todays_date_format="D"+UtcNow().date().strftime('%y%m%d')
  if keeptrack.get(todays_date_format,0):
    keeptrack[todays_date_format]+=1
    with open("visi.pickle",'wb') as ff:
      pickle.dump(keeptrack,ff)
    
  else:  
    keeptrack[todays_date_format]=1
    with open("visi.pickle",'wb') as ff:
        pickle.dump(keeptrack,ff)
    
  return keeptrack[todays_date_format]

if __name__ == '__main__':
    f=open("visi.pickle","rb") 
    keeptrack=pickle.load(f)
    keeptrack_f()