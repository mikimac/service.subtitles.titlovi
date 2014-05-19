# -*- coding: utf-8 -*-

import sys
import urllib
import base64
import xbmc
import xbmcvfs
import unicodedata
from xml.dom import minidom


__addon__ = sys.modules["__main__"].__addon__
__scriptname__ = sys.modules["__main__"].__scriptname__
__version__ = sys.modules["__main__"].__version__

USER_AGENT = "%s_v%s" % (__scriptname__.replace(" ", "_"), __version__)

LANGUAGES = (

    # Full Language name[0]     podnapisi[1]  ISO 639-1[2]   ISO 639-1 Code[3]   Script Setting Language[4]   localized name id number[5]

    ("Albanian"                   , "29",       "sq",            "alb",                 "0",                     30201  ),
    ("Arabic"                     , "12",       "ar",            "ara",                 "1",                     30202  ),
    ("Belarusian"                 , "0" ,       "hy",            "arm",                 "2",                     30203  ),
    ("Bosnian"                    , "10",       "bs",            "bos",                 "3",                     30204  ),
    ("Bulgarian"                  , "33",       "bg",            "bul",                 "4",                     30205  ),
    ("Catalan"                    , "53",       "ca",            "cat",                 "5",                     30206  ),
    ("Chinese"                    , "17",       "zh",            "chi",                 "6",                     30207  ),
    ("Croatian"                   , "38",       "hr",            "hrv",                 "7",                     30208  ),
    ("Czech"                      , "7",        "cs",            "cze",                 "8",                     30209  ),
    ("Danish"                     , "24",       "da",            "dan",                 "9",                     30210  ),
    ("Dutch"                      , "23",       "nl",            "dut",                 "10",                    30211  ),
    ("English"                    , "2",        "en",            "eng",                 "11",                    30212  ),
    ("Estonian"                   , "20",       "et",            "est",                 "12",                    30213  ),
    ("Persian"                    , "52",       "fa",            "per",                 "13",                    30247  ),
    ("Finnish"                    , "31",       "fi",            "fin",                 "14",                    30214  ),
    ("French"                     , "8",        "fr",            "fre",                 "15",                    30215  ),
    ("German"                     , "5",        "de",            "ger",                 "16",                    30216  ),
    ("Greek"                      , "16",       "el",            "ell",                 "17",                    30217  ),
    ("Hebrew"                     , "22",       "he",            "heb",                 "18",                    30218  ),
    ("Hindi"                      , "42",       "hi",            "hin",                 "19",                    30219  ),
    ("Hungarian"                  , "15",       "hu",            "hun",                 "20",                    30220  ),
    ("Icelandic"                  , "6",        "is",            "ice",                 "21",                    30221  ),
    ("Indonesian"                 , "0",        "id",            "ind",                 "22",                    30222  ),
    ("Italian"                    , "9",        "it",            "ita",                 "23",                    30224  ),
    ("Japanese"                   , "11",       "ja",            "jpn",                 "24",                    30225  ),
    ("Korean"                     , "4",        "ko",            "kor",                 "25",                    30226  ),
    ("Latvian"                    , "21",       "lv",            "lav",                 "26",                    30227  ),
    ("Lithuanian"                 , "0",        "lt",            "lit",                 "27",                    30228  ),
    ("Macedonian"                 , "35",       "mk",            "mac",                 "28",                    30229  ),
    ("Malay"                      , "0",        "ms",            "may",                 "29",                    30248  ),
    ("Norwegian"                  , "3",        "no",            "nor",                 "30",                    30230  ),
    ("Polish"                     , "26",       "pl",            "pol",                 "31",                    30232  ),
    ("Portuguese"                 , "32",       "pt",            "por",                 "32",                    30233  ),
    ("PortugueseBrazil"           , "48",       "pb",            "pob",                 "33",                    30234  ),
    ("Romanian"                   , "13",       "ro",            "rum",                 "34",                    30235  ),
    ("Russian"                    , "27",       "ru",            "rus",                 "35",                    30236  ),
    ("Serbian"                    , "36",       "sr",            "scc",                 "36",                    30237  ),
    ("Slovak"                     , "37",       "sk",            "slo",                 "37",                    30238  ),
    ("Slovenian"                  , "1",        "sl",            "slv",                 "38",                    30239  ),
    ("Spanish"                    , "28",       "es",            "spa",                 "39",                    30240  ),
    ("Swedish"                    , "25",       "sv",            "swe",                 "40",                    30242  ),
    ("Thai"                       , "0",        "th",            "tha",                 "41",                    30243  ),
    ("Turkish"                    , "30",       "tr",            "tur",                 "42",                    30244  ),
    ("Ukrainian"                  , "46",       "uk",            "ukr",                 "43",                    30245  ),
    ("Vietnamese"                 , "51",       "vi",            "vie",                 "44",                    30246  ),
    ("BosnianLatin"               , "10",       "bs",            "bos",                 "100",                   30204  ),
    ("Farsi"                      , "52",       "fa",            "per",                 "13",                    30247  ),
    ("English (US)"               , "2",        "en",            "eng",                 "100",                   30212  ),
    ("English (UK)"               , "2",        "en",            "eng",                 "100",                   30212  ),
    ("Portuguese (Brazilian)"     , "48",       "pt-br",         "pob",                 "100",                   30234  ),
    ("Portuguese (Brazil)"        , "48",       "pb",            "pob",                 "33",                    30234  ),
    ("Portuguese-BR"              , "48",       "pb",            "pob",                 "33",                    30234  ),
    ("Brazilian"                  , "48",       "pb",            "pob",                 "33",                    30234  ),
    ("Español (Latinoamérica)"    , "28",       "es",            "spa",                 "100",                   30240  ),
    ("Español (España)"           , "28",       "es",            "spa",                 "100",                   30240  ),
    ("Spanish (Latin America)"    , "28",       "es",            "spa",                 "100",                   30240  ),
    ("Español"                    , "28",       "es",            "spa",                 "100",                   30240  ),
    ("SerbianLatin"               , "36",       "sr",            "scc",                 "100",                   30237  ),
    ("Spanish (Spain)"            , "28",       "es",            "spa",                 "100",                   30240  ),
    ("Chinese (Traditional)"      , "17",       "zh",            "chi",                 "100",                   30207  ),
    ("Chinese (Simplified)"       , "17",       "zh",            "chi",                 "100",                   30207  ) )


def languageTranslate(lang, lang_from, lang_to):
    for x in LANGUAGES:
        if lang == x[lang_from]:
            return x[lang_to]


def normalizeString(str):
    return unicodedata.normalize(
        'NFKD', unicode(unicode(str, 'utf-8'))
    ).encode('ascii', 'ignore')


def log(module, msg):
    xbmc.log((u"### [%s] - %s" % (module, msg,)).encode('utf-8'),
             level=xbmc.LOGDEBUG)


def compare_columns(b, a):
    return cmp(b["language_name"], a["language_name"]) or \
        cmp(a["sync"], b["sync"])


class OSDBServer:

    KEY = "UGE4Qk0tYXNSMWEtYTJlaWZfUE9US1NFRC1WRUQtWA=="

    def create(self):
        self.subtitles_list = []

    def search_subtitles(self, name, tvshow, season, episode, lang, year):
        if len(tvshow) > 1:
            name = tvshow
        search_url = []
        api_key = base64.b64decode(self.KEY)[::-1]
        if len(tvshow) > 0:
            search_string = ("%s S%.2dE%.2d" % (name,
                                                int(season),
                                                int(episode),))
            search_string = search_string.replace(" ", "+")
        else:
            search_string = name.replace(" ", "+")

        # search_url_base = "http://api.titlovi.com/xml_get_api.ashx?" + \
        #                   "x-dev_api_id=%s&keyword=%s&language=%s&" + \
        #                   "uiculture=en" % (api_key, search_string, "%s")
        search_url_base = "http://api.titlovi.com/xml_get_api.ashx?x-dev_api_id=%s&keyword=%s&language=%s&uiculture=en" % (api_key, search_string, "%s")
        subtitles = None

        for i in range(len(lang)):
            if str(lang[i]) == "sr":
                lang1 = "rs"
            elif str(lang[i]) == "bs":
                lang1 = "ba"
            elif str(lang[i]) == "sl":
                lang1 = "si"
            else:
                lang1 = str(lang[i])
            url = search_url_base % lang1
            log(__name__, "%s - Language %i" % (url, i))
            temp_subs = self.fetch(url)
            if temp_subs:
                if subtitles:
                    subtitles = subtitles + temp_subs
                else:
                    subtitles = temp_subs
        try:
            if subtitles:
                url_base = "http://en.titlovi.com/downloads/default.ashx?type=1&mediaid=%s"
                for subtitle in subtitles:
                    subtitle_id = 0
                    rating = 0
                    filename = ""
                    movie = ""
                    lang_name = ""
                    lang_id = ""
                    flag_image = ""
                    link = ""
                    format = "srt"
                    if subtitle.getElementsByTagName("safeTitle")[0].firstChild:
                        movie = subtitle.getElementsByTagName("safeTitle")[0] \
                            .firstChild.data
                    if subtitle.getElementsByTagName("year")[0].firstChild:
                        movie_year = subtitle.getElementsByTagName("year")[0] \
                            .firstChild.data
                    if subtitle.getElementsByTagName("release")[0].firstChild:
                        filename = subtitle.getElementsByTagName("release")[0] \
                            .firstChild.data
                        filename = "%s (%s) %s.srt" % (movie, movie_year, filename,)
                        if len(filename) < 2:
                            filename = "%s (%s).srt" % (movie, movie_year,)
                    else:
                        filename = "%s (%s).srt" % (movie, movie_year,)
                    if subtitle.getElementsByTagName("score")[0].firstChild:
                        rating = int(subtitle.getElementsByTagName("score")[0]
                                     .firstChild.data)*2
                    if subtitle.getElementsByTagName("language")[0].firstChild:
                        lang = subtitle.getElementsByTagName("language")[0] \
                            .firstChild.data
                        if lang == "rs":
                            lang = "sr"
                        if lang == "ba":
                            lang = "bs"
                        if lang == "si":
                            lang = "sl"
                        lang_name = lang
                    subtitle_id = subtitle.getElementsByTagName("url")[0] \
                        .firstChild.data
                    subtitle_id = subtitle_id.split("-")[-1].replace("/", "")
                    flag_image = lang_name
                    link = url_base % subtitle_id
                    self.subtitles_list.append({'filename': filename,
                                                'link': link,
                                                'language_name': languageTranslate((lang_name),2,0),
                                                'language_id': lang_id,
                                                'language_flag': flag_image,
                                                'movie': movie,
                                                'ID': subtitle_id,
                                                'rating': str(rating),
                                                'format': format,
                                                'sync': False,
                                                'hearing_imp': False
                                                })
                return self.subtitles_list
        except:
            return self.subtitles_list

    def fetch(self, url):
        socket = urllib.urlopen(url)
        result = socket.read()
        socket.close()
        xmldoc = minidom.parseString(result)
        return xmldoc.getElementsByTagName("subtitle")
