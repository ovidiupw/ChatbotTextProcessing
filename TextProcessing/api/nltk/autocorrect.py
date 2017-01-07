import enchant


class AutoCorrect:
    wordDict = None

    @staticmethod
    def initDict():
        if AutoCorrect.wordDict is None:
            AutoCorrect.wordDict = enchant.Dict('en_US')

    @staticmethod
    def suggest(sentence):
        AutoCorrect.initDict()
        words = sentence.split()
        suggestions = []
        foundError = False
        for word in words:
            if AutoCorrect.wordDict.check(word) == False:
                foundError = True
                try:
                    suggestions.append(AutoCorrect.wordDict.suggest(word)[0])
                except IndexError:
                    raise SuggestionNotFoundException
            else:
                suggestions.append(word)
        if foundError == False:
            return None
        else:
            return ' '.join(suggestions)


class SuggestionNotFoundException(Exception):
    pass
