#importing libraries
import math
import re
from nltk.corpus import stopwords
import nltk
import os

#nltk.download('stopwords')

text = "यसवर्षको हालसम्म देशभर २० जना बिरामीमा हैजा पुष्टि भएको छ । स्वास्थ्य तथा जनसङ्ख्या मन्त्रालयका प्रवक्ता डा प्रकाश बुढाथोकीले काठमाडौँ, ललितपुर र कैलालीमा गरी २० जनामा हैजा पुष्टि भएको जानकारी दिए । उनले सहरी क्षेत्रमा बढ्दो जनधनत्वसँगै सुरक्षित खानेपानी र पर्यावरणीय स्वच्छतामा कमी तथा बाढीपहिरोका घटनाले पानी तथा सरसफाइका पूर्वाधारमा पार्ने नकारात्मक असरका कारण नेपालमा हैजाको सङ्क्रमण देखिने गरेको बताए । अति सङ्क्रामक र शीघ्र फैलिने झाडापखाला भएकाले हैजाको मुख्य लक्षण चौलानी पानी जस्तो दिशा आउने, वाकवाकी लाग्ने, वान्ता हुने र कडा जलवियोजन हुने गर्दछ । सङ्क्रमणले गम्भीर अवस्थामा पु¥याउँदा आँखा गाडिने, मुख, जिब्रो र घाँटी सुक्खा हुने, पिसाबको रङ्ग पँहेलो हुने, रक्तचाप कम हुने, मुटुको धड्कन अनियन्त्रित हुने र बेहोस हुनसक्ने मन्त्रालयका प्रवक्ता डा बुढाथोकीले बताए । ‘हैजाका बिरामीलाई तुरुन्तै अस्पताल नपु¥याए ५० प्रतिशतको मृत्यु हुने सम्भावना हुन्छ । हैजा सङ्क्रमितमध्ये ८० प्रतिशतमा कुनै लक्षण विकसित हुँदैन तर उनीहरूको दिशामा पहिलादेखि १० दिनसम्म भिब्रियो कोलेरा ब्याक्टेरिया रहन सक्छ र लक्षण देखिएकामा पनि ८० प्रतिशतलाई मन्ददेखि मध्यमस्तरको लक्षण देखिन्छ । २० प्रतिशतलाई चौलानी जस्तै दिशा हुने र पानीको अभावजस्ता तीव्र लक्षण देखिन्छन्’, उनले भने । झिगा लागेको, बासी, सडेगलेको, नपाकेको, चिसिएको खुलास्थानका खाद्यपदार्थ नखान, पानीलाई उमालेर वा क्लेरिन प्रयोग गरेर मात्र प्रयोग गर्न र गराउन, व्यक्तिगत सरसफाइमा विशेष ध्यान दिनुका साथै दिशापिसाब गरिसकेपछि साबुन पानीले मिचिमिची हात हुन मन्त्रालयले सबैमा अनुरोध गरेको छ । "

sents=re.split('।',text)

documents_size = len(sents)

words=text.split()

def create_frequency_matrix(sentences):
    frequency_matrix = {}
    stopWords = set(stopwords.words("nepali"))

    for sent in sentences:
        freq_table = {}
        words=sent.split()
        for word in words:
            if word in stopWords:
                continue

            if word in freq_table:
                freq_table[word] += 1
            else:
                freq_table[word] = 1

        frequency_matrix[sent[:10]] = freq_table

    return frequency_matrix

freq_matrix = create_frequency_matrix(sents)

freq_matrix

def create_tf_matrix(freq_matrix):
    tf_matrix = {}

    for sent, f_table in freq_matrix.items():
        tf_table = {}

        count_words_in_sentence = len(f_table)
        for word, count in f_table.items():
            tf_table[word] = count / count_words_in_sentence

        tf_matrix[sent] = tf_table

    return tf_matrix

tf_matrix = create_tf_matrix(freq_matrix)

tf_matrix

def create_idf_matrix(freq_matrix, count_doc_per_words, documents_size):
    idf_matrix = {}

    for sent, f_table in freq_matrix.items():
        idf_table = {}

        for word in f_table.keys():
            idf_table[word] = math.log10(documents_size / float(count_doc_per_words[word]))

        idf_matrix[sent] = idf_table

    return idf_matrix

def create_documents_per_words(freq_matrix):
    word_per_doc_table = {}

    for sent, f_table in freq_matrix.items():
        for word, count in f_table.items():
            if word in word_per_doc_table:
                word_per_doc_table[word] += 1
            else:
                word_per_doc_table[word] = 1

    return word_per_doc_table


count_doc_per_words = create_documents_per_words(freq_matrix)


idf_matrix = create_idf_matrix(freq_matrix,count_doc_per_words, documents_size)

idf_matrix

def create_tf_idf_matrix(tf_matrix, idf_matrix):
    tf_idf_matrix = {}

    for (sent1, f_table1), (sent2, f_table2) in zip(tf_matrix.items(), idf_matrix.items()):

        tf_idf_table = {}

        for (word1, value1), (word2, value2) in zip(f_table1.items(),
                                                    f_table2.items()):
            tf_idf_table[word1] = float(value1 * value2)

        tf_idf_matrix[sent1] = tf_idf_table

    return tf_idf_matrix


tf_idf_matrix = create_tf_idf_matrix(tf_matrix, idf_matrix)

tf_idf_matrix

def sentence_scores(tf_idf_matrix) -> dict:


    sentenceValue = {}

    for sent, f_table in tf_idf_matrix.items():
        total_score_per_sentence = 0

        count_words_in_sentence = len(f_table)
        for word, score in f_table.items():
            total_score_per_sentence += score
        if count_words_in_sentence !=0:
            sentenceValue[sent] = total_score_per_sentence / count_words_in_sentence
        else:
            sentenceValue[sent]=0
    return sentenceValue

sentence_scores = sentence_scores(tf_idf_matrix)

def find_average_score(sentenceValue) -> int:
    sumValues = 0
    for entry in sentenceValue:
        sumValues += sentenceValue[entry]

    # Average value of a sentence from original summary_text
    average = (sumValues / len(sentenceValue))

    return average

threshold = find_average_score(sentence_scores)

threshold

def generate_summary(sentences, sentenceValue, threshold):
    sentence_count = 0
    summary = []

    for sentence in sentences:
        if sentence[:10] in sentenceValue and sentenceValue[sentence[:10]] >= (threshold):
            summary.append(sentence)
            sentence_count += 1

    return summary

summary = '।'.join(generate_summary(sents, sentence_scores,0.8*threshold ))

print(summary)

