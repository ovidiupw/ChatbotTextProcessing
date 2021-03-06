import json
from xml.etree.ElementTree import tostring

from nltk.data import load

from api.models import JsonApiDescription, JsonAcronymToPartOfSpeech, JsonError, JsonAnnotatedSentence, JsonResponseErrorMessage, \
    JsonDetectLanguage

# noinspection PyBroadException
from api.nltk.languagedetector import GenerateReply, DetectLanguage
from api.nltk.probabilitykeyword import probability_keyword
from api.nltk.sentencetreebuilder import SentenceTreeBuilder


class JsonGenerator:
    @staticmethod
    def buildErrorResponse(error):
        return json.dumps({
            JsonError.errorField: True,
            JsonError.errorCodeField: error.code,
            JsonError.errorMessageField: error.message
        })

    @staticmethod
    def buildApiV1VersionResponse():
        return json.dumps({
            JsonApiDescription.jsonVersionField: JsonApiDescription.version,
            JsonApiDescription.jsonLastUpdateDateField: JsonApiDescription.lastUpdateDate,
            JsonApiDescription.jsonDescriptionField: JsonApiDescription.description,
            JsonError.errorField: False
        })

    @staticmethod
    def buildNltkAcronymToPartOfSpeechResponse(requestAcronym):
        acronymDictionary = Utils.readUpennDictionary()
        if requestAcronym is None or requestAcronym.upper() not in acronymDictionary:
            raise Exception("Request acronym could not be identified. Maybe the acronym does not exist in nltk?")

        requestAcronym = requestAcronym.upper()

        return json.dumps({
            JsonAcronymToPartOfSpeech.acronym: requestAcronym,
            JsonAcronymToPartOfSpeech.partOfSpeech: acronymDictionary[requestAcronym][0],
            JsonAcronymToPartOfSpeech.examples: list(filter(
                lambda ex: len(ex) > 0,
                acronymDictionary[requestAcronym][1].replace('...', '').split(' ')
            )),
            JsonError.errorField: False
        })

    @staticmethod
    def buildNltkAnnotatedSentenceResponse(requestSentence):
        return json.dumps({
            JsonAnnotatedSentence.annotatedSentence: tostring(
                element=SentenceTreeBuilder.build_text_xml(requestSentence), encoding="unicode"),
            JsonAnnotatedSentence.sentenceKeywords: probability_keyword(requestSentence),
            JsonError.errorField: False
        })

    @staticmethod
    def buildGenerateErrorMessageResponse(requestLanguage):
        return json.dumps({
            JsonResponseErrorMessage.responseErrorMessage: GenerateReply(requestLanguage),
            JsonError.errorField: False
        })

    @staticmethod
    def buildDetectLanguageResponse(message):
        return json.dumps({
            JsonDetectLanguage.language: DetectLanguage(message),
            JsonError.errorField: False
        })


class Utils:
    @staticmethod
    def readUpennDictionary():
        upennTagsetName = "upenn_tagset"
        tagDictionary = load("help/tagsets/" + upennTagsetName + ".pickle")
        return tagDictionary
