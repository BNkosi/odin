import os
import re
import json
from transformers import AutoModelWithLMHead, AutoTokenizer



class QuestionGenerator:
<<<<<<< HEAD
    def __init__(self, doc_dir: str = '/home/bulelani/Desktop/odin/odin/src_new/data/documents', question_dir: str = '/home/bulelani/Desktop/odin/odin/src_new/data/raw_questions', max_length: int=64):
=======
    def __init__(self, doc_dir: str = 'data/documents', question_dir: str = 'data/training/questions.json', max_length: int=64):
>>>>>>> 4b87155863e49e1fcb420b8cd89224a3e69df555
        self.doc_dir = doc_dir
        self.qu_dir = question_dir

    def list_docs(self):
        for filename in os.listdir(self.doc_dir):
            print(filename)

    def load_models(self):
        self.tokenizer = AutoTokenizer.from_pretrained("mrm8488/t5-base-finetuned-question-generation-ap")
        self.model = AutoModelWithLMHead.from_pretrained("mrm8488/t5-base-finetuned-question-generation-ap")

    def generate_qs(self):
        # Fetch documents
        self.docs=list()
        self.questions={
            "question": list(),
            "title": list(),
            "url": list(),
            "context": list(),
        }
        for filename in os.listdir(self.doc_dir):
            if filename.endswith(".txt"): 
                with open(str(self.doc_dir+"/"+filename), mode = 'r', encoding='utf-8') as doc:
                    text = doc.read()
                    text = self.clean_website_text(text)
                    self.docs.append({"title": filename, "text": text})
                    doc.close()
            else:
                continue
        
        # Generate list of training questions
        # for each document
        for doc in range(len(self.docs)):
            # get data
            title = self.docs[doc]["title"]
            text = self.docs[doc]["text"]
            # text = self.sequence_limiter(text)
            link = [line for line in text.split("\n") if line.startswith("https")]
            long_line = " ".join([line for line in text.split("\n")])
            sentences = [line for line in long_line.split(".") if line.startswith("https")==False or line != "" or line!= " "]
    
            for i in range(len(sentences)):
                for word in sentences[i].split():
                    question = self.get_question(word, sentences[i])
                    question = re.sub('question: ', '', question)
                    print(f"{question}")
                    self.questions["question"].append(question)
                    self.questions["title"].append(title)
                    self.questions["url"].append(link)
                    self.questions["context"].append(text)
        # Save questions to json
<<<<<<< HEAD
            with open(f"{self.qu_dir}/{filename}_questions.json" , 'w') as fp:
                json.dump(self.questions, fp)
                fp.close()
        # Download all files
        # for filename in os.listdir(self.doc_dir):
        #     files.download(f"{self.qu_dir}/{filename}_questions.json")
=======
        with open(self.qu_dir, 'w') as fp:
            json.dump(self.questions, fp)
            fp.close()
            
>>>>>>> 4b87155863e49e1fcb420b8cd89224a3e69df555


    def get_question(self, answer, context, max_length=64):
        input_text = "answer: %s  context: %s </s>" % (answer, context)
        features = self.tokenizer([input_text], return_tensors='pt')

        output = self.model.generate(
            input_ids=features['input_ids'],
            attention_mask=features['attention_mask'],
            max_length=max_length
        )
        return self.tokenizer.decode(output[0])

    @staticmethod
    def clean_website_text(text: str()):
        # removing lines starting with "<", ">", "="
        exclude = []
        for i in range(len(text.split("\n"))):
            if text.split("\n")[i].startswith("<"):
                exclude.append(text.split("\n")[i])
            elif text.split("\n")[i].startswith("="):
                exclude.append(text.split("\n")[i])
            elif text.split("\n")[i].startswith(">"):
                exclude.append(text.split("\n")[i])
            elif text.split("\n")[i] == "":
                exclude.append(text.split("\n")[i])
            elif text.split("\n")[i] == " ":
                exclude.append(text.split("\n")[i])
        text_clean = []
        for i in text.split("\n"):
            if i not in exclude:
                text_clean.append(i)
        
        text = "\n".join(text_clean)
        
        # Text cleaning
        text = re.sub("Jan ", "January ", text)
        text = re.sub("Feb ", "February ", text)
        text = re.sub("Mar ", "March ", text)
        text = re.sub("Apr ", "April ", text)
        text = re.sub("May ", "May ", text)
        text = re.sub("Jun ", "June ", text)
        text = re.sub("Jul ", "July ", text)
        text = re.sub("Aug ", "August ", text)
        text = re.sub("Sep ", "September ", text)
        text = re.sub("Oct ", "October ", text)
        text = re.sub("Nov ", "November ", text)
        text = re.sub("Dec ", "December ", text)
        text = re.sub("&", "and", text)
        text = re.sub("T�s", "terms", text)
        text = re.sub("C�s", "conditions", text)
        text = re.sub("sure�", "sure?", text)
        text = re.sub("�Find your tribe�", "Find your tribe", text)
        text = re.sub("NQF", "National Qualifications Framework (NQF)", text)
        text = re.sub("team�s", "team's", text)
        text = re.sub("We're", "We are", text)
        text = re.sub("we're", "we are", text)
        text = re.sub("AWS", "Amazon Web Services", text)
        text = re.sub("Amazon's", "Amazon", text)
        text = re.sub("EC2", "Elastic Cloud Compute", text)
        text = re.sub("EBS", "Elastic Block Store", text)
        text = re.sub("EFS", "Elastic File Store", text)
        text = re.sub("S3", "Simple Storage, Service", text)
        text = re.sub("RDS", "Relational Database Service", text)
        text = re.sub("VPC", "Virtual Private Cloud", text)
        text = re.sub("Services", "", text)
        text = re.sub("IAM", "Identity and Access Management", text)
        text = re.sub("CSIR", "Council for Scientific and Industrial Research", text)
        text = re.sub("2/3", "2 to 3", text)
        text = re.sub("NLP", "Natural Language Processing", text)
        text = re.sub("JanuarydeWet", "January de Wet", text)
        text = re.sub("UK", "United Kingdom", text)
        text = re.sub("fin-tech", "financial services technology", text)
        text = re.sub("�ll", " will", text)
        text = re.sub("n�t", " not", text)
        text = re.sub("1:1", "one-on-one", text)
        text = re.sub("we�ve", "we have", text)
        text = re.sub("We�ve", "we have", text)
        text = re.sub("We�re", "We are", text)
        text = re.sub("we�re", "we are", text)
        text = re.sub("/", " or ", text)
        text = re.sub("API�s", "application programming interfaces", text)
        text = re.sub("ANN�s", "Artificial Neural Networks", text)
        text = re.sub("CNN�s", "Convolutional Neural Networks", text)
        text = re.sub("RNN�s", "Recurrent Neural Networks", text)
        text = re.sub("it�s", "it is", text)
        text = re.sub("\t", " ", text)
        text = re.sub("CAs", "Chartered Accountants", text)
        text = re.sub("CA's", "Chartered Accountant's", text)
        text = re.sub("An innovate", "An innovative", text)
        text = re.sub("it's", "it is", text)
        text = re.sub("It's", "It is", text)
        text = re.sub("don't", "do not", text)
        text = re.sub("There's", "There is", text)
        text = re.sub("you'll", "you will", text)
        text = re.sub("you're", "you are", text)
        text = re.sub("We've", "We have", text)
        text = re.sub("we've", "we have", text)
        text = re.sub("you�re", "you are", text)
        text = re.sub("�CTC�", "(CTC)", text)
        text = re.sub("�Qualifying Position�", '"Qualifying Position"', text)
        text = re.sub(".Explore", "Explore", text)
        text = re.sub("Explore�s", "Explore's", text)
        text = re.sub("you�ve", "you have", text)
        text = re.sub("�TWOE�", "(TWOE)", text)
        text = re.sub("coaches�", "coaches'", text)
        text = re.sub("IRP5�s", "IRP5's", text)
        text = re.sub("sill", "will", text)
        text = re.sub("we'll", "we will", text)
        text = re.sub("�ve", " have", text)
        text = re.sub("It�s been", "It has been", text)
        text = re.sub("It�s a", "It is a", text)
        text = re.sub("It�s open", "It is open", text)
        text = re.sub("It�s used", "It is used", text)
        text = re.sub("It�s free", "It is free", text)
        text = re.sub("It�s very", "It is very", text)
        text = re.sub("SVM�s", "Support Vector Machines", text)
        text = re.sub("I�m", " I am", text)
        text = re.sub("country�s", "country's", text)
        text = re.sub("projects�helping", "projects - helping", text)
        text = re.sub("EXPLORE�s", "EXPLORE's", text)
        text = re.sub("That�s", "That is", text)
        text = re.sub("month�s", "month's", text)
        text = re.sub("South African�s", "South Africans", text)
        text = re.sub("Data Scientist�s", "Data Scientist's", text)
        text = re.sub("�Data Scientist�", '"Data Scientist"', text)
        text = re.sub("�sexiest profession of the 21st Century�", '"sexiest profession of the 21st Century"', text)
        text = re.sub("email�protected", "email protected", text)
        text = re.sub("python�s", "Python's", text)
        text = re.sub("he�s", "he is", text)
        text = re.sub("�Reading�s", "Reading's", text)
        text = re.sub("1,000�s", "thousands", text)
        text = re.sub("They�re", "They are", text)
        text = re.sub("they�re", "they are", text)
        text = re.sub("customer�s", "customer's", text)
        text = re.sub('\\"', "", text)
        text = re.sub(" � ", " - ", text)
<<<<<<< HEAD
        text = re.sub("�", "", text)
        text = re.sub(r"^[0-9]{2}$", "", text)   
=======
        text = re.sub("�", "", text)    
>>>>>>> 4b87155863e49e1fcb420b8cd89224a3e69df555
        # Join text into one line
        text = " ".join(text.split('\n'))
        return text

<<<<<<< HEAD
=======
    # @staticmethod
    # def sequence_limiter(text):
    #     text = text.split(". ")
    #     text = ". ".join([sent if len(sent) <=512 else sent[:-512] for sent in text])
    #     return text


>>>>>>> 4b87155863e49e1fcb420b8cd89224a3e69df555
if __name__ == "__main__":
    generator = QuestionGenerator()
    generator.list_docs()
    generator.load_models()
    generator.generate_qs()