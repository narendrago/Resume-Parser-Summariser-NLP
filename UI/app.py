from flask import Flask,render_template,request

import spacy
import pickle
import random
import nltk
import os
import pandas as pd
# nltk.download('stopwords')
from nltk.corpus import stopwords
import numpy as np
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from PIL import Image
from nltk.stem import PorterStemmer
stpwords = stopwords.words('english')
import sys,fitz
import joblib



app=Flask(__name__)

# train_data=pickle.load(open('/Users/narendraomprakash/Desktop/Narendra/Semester-V-FALL2021/NLP/J Component/UI/static/train_data.pkl', 'rb'))

# nlp= spacy.blank('en')

# def train_model(train_data):
#     if 'ner' not in nlp.pipe_names:
#         # ner = nlp.add_pipe('ner')
#         ner=nlp.add_pipe('ner', last = True)
        
#     for _, annotation in train_data:
#         for ent in annotation['entities']:
#             ner.add_label(ent[2])
            
#     other_pipes = [pipe for pipe in nlp.pipe_names if pipe != 'ner']
#     with nlp.disable_pipes(*other_pipes):
#         optimizer = nlp.begin_training()
#         for itn in range(10):
#             print('Starting iteration ' + str(itn))
#             random.shuffle(train_data)
#             losses = {}
#             index = 0
#             for text, annotations in train_data:
#                 try:
#                     nlp.update(
#                         [text],
#                         [annotations],
#                         drop=0.2,
#                         sgd = optimizer,
#                         losses = losses)
#                 except Exception as e:
#                     pass
#             print(losses)

# train_model(train_data)
# nlp.to_disk('/Users/narendraomprakash/Desktop/Narendra/Semester-V-FALL2021/NLP/J Component/UI/nlp_model')
# nlp_model = spacy.load('/Users/narendraomprakash/Desktop/Narendra/Semester-V-FALL2021/NLP/J Component/UI/nlp_model')

# # !!! IF THE MODEL GETS SAVED ONCE, THEN USE BELOW TWO LINES AND UNCOMMENT THE TRAINING PART
# # filename='/Users/narendraomprakash/Desktop/Narendra/Semester-V-FALL2021/NLP/J Component/UI/static/nlp.pkl'
# # nlp_model=joblib.load(filename)

# def pdf2text(input_resume):
#     doc = fitz.open(input_resume)
#     text = ""
#     for page in doc:
#         text = text+ str(page.get_text())
#     tx = " ".join(text.split('\n'))
#     return tx


# def candidateMatching(required_skills,updated_tokens_list,bigrams):
#     list_skills = required_skills.lower().split(",")
#     found_skills_each_resume = []
#     score = 0
#     for x in list_skills:
#         if len(x.split()) > 1:
#             l = [w for w in x.split()]
#             li = []
#             t = tuple(l)
#             li.append(t)
#             if li[0] in bigrams:
#                 score+=1
#                 found_skills_each_resume.append(' '.join(l))
#         else:
#             if x in updated_tokens_list:
#                 score += 1
#                 found_skills_each_resume.append(x)

#     req_skills_len = len(list_skills)
#     match = round(score / req_skills_len * 100, 1)
    
#     return found_skills_each_resume,match

# def bigramGenerator(text):
#     list = []
#     list.append(text.lower())
#     bigrams = [b for l in list for b in zip(l.split(" ")[:-1], l.split(" ")[1:])]
#     return bigrams

# def stemming_tokenizer(tokens_list):
#     rootWord = []
#     tokens = [x.lower() for xs in tokens_list for x in xs.split(',')]
#     ps = PorterStemmer()
#     for w in tokens_list:
#         if w not in stpwords:
#             rootWord.append(ps.stem(w))
#     return rootWord

# def lemma_tokenizer(tokens_list):
#     rootWord = []
#     for token in tokens_list:
#         if token.lemma_ not in stpwords:
#             rootWord.append(token.lemma_)
#     return [x.lower() for xs in rootWord for x in xs.split(',')]

# extractedDetails={} 
# final_token_list=[]
# found_skills = {}
# bigrams=[]

# n_resumes=0
# def entity_extraction(resume, required_skills):
#     test=pdf2text(resume)
#     doc = nlp_model(test)
#     l=[]
#     s=[]
#     x={}
#     for ent in doc.ents:
#         if ent.label_.upper() not in l:
#             l.append(ent.label_.upper())
#             print(f'{ent.label_.upper():{30}}- {ent.text}')
#             x[ent.label_.upper()]=ent.text
#         text_list=[test]
#         tokens_list=' '.join(text_list).split()
        

#     updated_tokens_list=lemma_tokenizer(doc)
#     final_token_list.extend(updated_tokens_list)
#     bigrams.extend(bigramGenerator(test))
#     x['Skills'],x['Match']=candidateMatching(required_skills,updated_tokens_list,bigrams)
#     extractedDetails[n_resumes]=x



# def cutoff_checker(extractedDetails, cutoff):
#     ranking={}
#     for i in range(len(extractedDetails)):
#         name = extractedDetails.get(i, {}).get('NAME')
#         match = extractedDetails.get(i, {}).get('Match')
#         if match>=cutoff:
#             ranking[name]=match
#     return ranking

@app.route('/')
@app.route('/home')
def home():
    return render_template('index.html')

@app.route('/resumepath')
def resumepath():
    return render_template('resumepath.html')

@app.route('/resumeparse',methods=['GET', 'POST'])
def resumeparse():
    if request.method == 'POST':
        rankingResumes={}
        resumepathname=request.form.get('resumepath')
        skillset=request.form.get('skillset')
        cutoffscore=float(request.form.get('cutoff'))       
        os.chdir(str(resumepathname))
        files=[]
        for file in os.listdir():
            files.append(file)
        # for n_resumes in range(len(files)):
        #     rankingResumes=entity_extraction(files[n_resumes],skillset)
        # resumes = pd.DataFrame(list(rankingResumes.items()))
        # resumes.columns = ['Candidates', 'Skill Score']
        # final_resumes = resumes.sort_values(by=['Skill Score'], ascending=False)
        return render_template('resumeparse.html',files=files,skillset=skillset,cutoffscore=cutoffscore)
        # rankingResumes=final_resumes)
if __name__=='__main__':
    app.run(debug=False)
