from math import log

# import csv
#
# with open("data/SMSSpamCollection", encoding="utf-8") as f:
#     data = list(csv.reader(f, delimiter="\t"))


class NaiveBayesClassifier:

    def __init__(self, alpha=0.05):
        self.alpha = alpha
        self.word_qty_in_classes = {}
        self.words_in_classes = {}
        self.word_probabilities = {}
        self.prior_prob_of_classes = {}

    def fit(self, X, y):
        """ Fit Naive Bayes classifier according to X, y. """
        self.word_qty_in_classes = {c: 0 for c in y}
        for msg, class_ in zip(X, y):
            for word in msg.split():
                if word not in self.words_in_classes:
                    self.words_in_classes[word] = {c: 0 for c in y}
                self.words_in_classes[word][class_] += 1
                self.word_qty_in_classes[class_] += 1

        d = len(self.words_in_classes.keys())
        self.word_probabilities = self.words_in_classes.copy()
        for word, classes_count in self.words_in_classes.items():
            for class_, count in classes_count.items():
                self.word_probabilities[word][class_] = (count + self.alpha) / (
                        self.word_qty_in_classes[class_] + self.alpha * d)

        self.prior_prob_of_classes = {class_: (y.count(class_) / len(y)) for class_ in y}

    def predict(self, X):
        """ Perform classification on an array of test vectors X. """
        prediction = {}
        for msg in X:
            prob_class = {}
            for class_ in self.prior_prob_of_classes.keys():
                prob = log(self.prior_prob_of_classes[class_]) + sum(
                    log(self.word_probabilities[word][class_]) for word in msg.split() if
                        word in self.word_probabilities)
                prob_class[class_] = prob
            prediction[msg] = max(prob_class, key=prob_class.get)
        return prediction

    def score(self, X_test, y_test):
        """ Returns the mean accuracy on the given test data and labels. """
        predictions = self.predict(X_test)
        score = 0
        for i, class_ in enumerate(predictions.values()):
            if class_ == y_test[i]:
                score += 1
        return score / len(X_test)


# nbc = NaiveBayesClassifier()
# print(len(data))
#
# import string
#
#
# def clean(s):
#     translator = str.maketrans("", "", string.punctuation)
#     return s.translate(translator)
#
#
# X, y = [], []
# for target, msg in data:
#     X.append(msg)
#     y.append(target)
# X = [clean(x).lower() for x in X]
#
# X_train, y_train, X_test, y_test = X[:3900], y[:3900], X[3900:], y[3900:]
# model = NaiveBayesClassifier()
# model.fit(X_train, y_train)
# print(model.score(X_test, y_test))
#
# from sklearn.naive_bayes import MultinomialNB
# from sklearn.pipeline import Pipeline
# from sklearn.feature_extraction.text import TfidfVectorizer
#
# model = Pipeline([
#     ('vectorizer', TfidfVectorizer()),
#     ('classifier', MultinomialNB(alpha=0.05)),
# ])
#
# model.fit(X_train, y_train)
# print(model.score(X_test, y_test))