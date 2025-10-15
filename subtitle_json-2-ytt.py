import os
import json
import argparse

def loadSubtitlefile(jsonconfig: str):
    if os.path.isfile(jsonconfig):
        with open(jsonconfig, 'r') as file:
            data = json.load(file)
            if data:
                print("\n")                    
            else:
                print("Abort!")
                exit(2)
    else:
        print("Could not find any config file, Abort!")
        exit(2)

    return data

def findSpeakers(jsondata):
    myspeakers = [""]

    # Find all the speakers
    for key in jsondata['segments']:
        if "speaker" in key:
            match = True
            for x in myspeakers:
                if key['speaker'] != x:
                    match = False
                else:
                    match = True
                    break
            if not match:
                myspeakers.append(key['speaker'])

    myspeakers.pop(0)
    return myspeakers

def createHeader(speakersList):
    print(speakersList)
    headstring = (
        "<?xml version=\"1.0\" encoding=\"utf-8\"?>\n" +
        "<timedtext format=\"3\">\n" +
        "<head>\n"
    )

    i = 0
    k = 0
    # 11 Colors. If we run out of color repeat from 0
    colors = ["#ffffff","#f9f06b","#8ff0a4","#99c1f1","#dc8add","#f66151","#cdab8f","#f8e45c","#c0bfbc","#ffbe6f","#26a269"]
    for x in speakersList:
        headstring += "<pen id=\"" + str(i) + "\" fc=\"" + str(colors[k]) + "\" />\n"
        i = i + 1
        k = k + 1
        if k > 10:
            k = 0

    headstring += (
        "\n" +
        "</head><body>\n\n\n"
    )
    return headstring

def formatSubtitles(jsondata,speakerarr):
    subtitlestring = ""
    speakerfield = 0 # Fallback if we don't have any speaker declaration

    for key in jsondata['segments']:
        if "start" in key:
            starttime = int(key['start'] * 1000)
        if "end" in key:
            # end means duration
            duration = int(key['end'] * 1000) - starttime
        if "speaker" in key:
            i = 0
            for x in speakerarr:
                if key['speaker'] == x:
                    speakerfield = i
                    break
                i = i + 1

        if "text" in key:
            subtitlestring += "<p t=\"" + str(starttime) + "\" d=\"" + str(duration) + "\"><s p=\"" + str(speakerfield) + "\">" + str(key['text']) + "</p>\n"

    # Footer of the file
    subtitlestring += "</body></timedtext>"

    return subtitlestring

def formatSubtitlesWords(jsondata,speakerarr):
    subtitlestring = ""
    speakerfield = 0 # Fallback if we don't have any speaker declaration

    for key in jsondata['segments']:
        if "speaker" in key:
            i = 0
            for x in speakerarr:
                if key['speaker'] == x:
                    speakerfield = i
                    break
                i = i + 1

        if "words" in key:
            for words in key['words']:
                if "start" in words:
                    starttimeword = int(words['start'] * 1000)
                if "end" in words:
                    # end means duration
                    durationword = int(words['end'] * 1000) - starttimeword
                    subtitlestring += "<p t=\"" + str(starttimeword) + "\" d=\"" + str(durationword) + "\"><s p=\"" + str(speakerfield) + "\">" + str(words['word']) + "</p>\n"
                
    # Footer of the file
    subtitlestring += "</body></timedtext>"

    return subtitlestring

parser = argparse.ArgumentParser(description='Convert WhisperX JSON data to colored YTT subtitles')
parser.add_argument(
    "--subtitledir",
    type=str,
    dest="subtitledir",
    metavar="folder with json subtitles",
    default="None",
    help="Folder where the JSON subtitle files are located",
)
parser.add_argument(
    "--words",
    #type=bool,
    dest="words",
    #metavar="",
    action="store_true",
    default=False,
    help="Subtitle each word separately",
)

args = parser.parse_args()

subtitledir = args.subtitledir + "/"
if not os.path.isdir(args.subtitledir):
    print(args.subtitledir + " is not a valid subtitle input folder")
    exit(2)
else:
    print("Subtitle input from folder: " + subtitledir)

for subtitlefile in sorted(os.listdir(subtitledir)):
    if subtitlefile.endswith(".json"):
        yttfile = subtitlefile.replace(".json",".ytt")
        yttwordsfile = subtitlefile.replace(".json","_words.ytt")

        print("Proessing " + subtitlefile + " to ytt format")
        data = loadSubtitlefile(subtitledir + "/" + subtitlefile)
        speakers = findSpeakers(data)
        yttcontent = createHeader(speakers)
        if args.words:
            yttcontent += formatSubtitlesWords(data,speakers)
            subtitleout = open(subtitledir + "/" + yttwordsfile,'w')
        else:
            yttcontent += formatSubtitles(data,speakers)
            subtitleout = open(subtitledir + "/" + yttfile,'w')
        subtitleout.write(yttcontent)
        subtitleout.close()
# ytt example formating
# <p t="14654" d="1101"><s p="0">Wer ist da?</s></p>
